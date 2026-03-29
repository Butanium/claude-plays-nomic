"""Core Clerk operations shared between MCP server and CLI.

All functions return strings. The MCP server wraps them as @mcp.tool(),
the CLI prints the returned strings.
"""

from __future__ import annotations

import os
import secrets
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from crypto import (
    SLUG_WORDS,
    decrypt_line,
    encrypt_line,
    format_cat_n,
    read_encrypted_lines,
    resolve_note_path,
    resolve_storage_dir,
    write_encrypted_lines,
)

CLERK_DIR = Path(__file__).parent.parent / "clerk"
SUPERVISOR_INBOX = Path(__file__).parent.parent / "supervisor_inbox.md"
WORDLIST = list(SLUG_WORDS)


def generate_key() -> str:
    """Generate a memorable 4-word key for a player."""
    words = [secrets.choice(WORDLIST) for _ in range(4)]
    return "-".join(words)


def save_state(key: str, filename: str, content: str) -> str:
    """Encrypt and save Clerk state. Overwrites if the file already exists."""
    path = resolve_note_path(key, filename, CLERK_DIR)
    lines = content.split("\n")
    encrypted_lines = [encrypt_line(line, key) for line in lines]
    write_encrypted_lines(path, encrypted_lines)
    return f"Saved '{filename}' ({len(lines)} line(s))"


def load_state(key: str, filename: str) -> str:
    """Decrypt and return Clerk state in cat -n format."""
    path = resolve_note_path(key, filename, CLERK_DIR)
    assert path.exists(), f"State file '{filename}' does not exist"
    encrypted_lines = read_encrypted_lines(path)
    decrypted = [decrypt_line(line, key) for line in encrypted_lines]
    return format_cat_n(decrypted)


def list_state_files(key: str) -> str:
    """List all Clerk state files."""
    encrypted_dir = resolve_storage_dir(key, CLERK_DIR) / "encrypted"
    if not encrypted_dir.exists():
        return "No state files yet."
    files = sorted(f.name for f in encrypted_dir.iterdir() if f.is_file())
    if not files:
        return "No state files yet."
    return "\n".join(files)


def commit_all(
    message: str = "end of turn",
    scores: dict[str, int] = None,
    result: str = None,
    round_number: int | None = None,
    winner: str | list[str] | None = None,
) -> str:
    """Commit all changed files and log structured round data.

    Args:
        message: Git commit message.
        scores: Current scores for all players, e.g. {"alice": 42, "bob": 17}.
            Required — the viewer uses this to display score progression.
        result: Outcome of this round's proposal vote, e.g. "adopted", "defeated".
            Required — use whatever term fits the current rules.
        round_number: Round number. If None, auto-increments from the last
            entry in game_state.yaml (or starts at 1).
        winner: Player name(s) if someone won this round. None if no winner yet.
    """
    assert scores is not None, "scores is required"
    assert result is not None, "result is required"

    project_root = Path(__file__).parent.parent
    game_state_path = project_root / "game_state.yaml"

    # Determine round number
    if round_number is None:
        round_number = _next_round_number(game_state_path)

    # Append round entry to game_state.yaml
    _append_round(game_state_path, round_number, scores, result, winner)

    branch = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        cwd=project_root,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()

    if not branch.startswith("game"):
        return (
            f"ERROR: Current branch is '{branch}', which does not start with 'game'. "
            "Aborting commit. Contact the supervisor about this issue."
        )

    subprocess.run(["git", "add", "-A"], cwd=project_root, check=True)

    git_result = subprocess.run(
        ["git", "commit", "-m", message],
        cwd=project_root,
        capture_output=True,
        text=True,
    )

    if git_result.returncode != 0:
        if "nothing to commit" in git_result.stdout:
            return "Nothing to commit — working tree clean."
        return f"Git commit failed: {git_result.stdout}\n{git_result.stderr}"

    return f"Committed all changes on branch '{branch}': {message}"


def _next_round_number(game_state_path: Path) -> int:
    """Read game_state.yaml and return the next round number."""
    if not game_state_path.exists():
        return 1
    import yaml
    with open(game_state_path) as f:
        state = yaml.safe_load(f)
    if not state or "rounds" not in state or not state["rounds"]:
        return 1
    return state["rounds"][-1]["round"] + 1


def _append_round(
    game_state_path: Path,
    round_number: int,
    scores: dict[str, int],
    result: str,
    winner: str | list[str] | None,
) -> None:
    """Append a round entry to game_state.yaml."""
    import yaml

    entry = {
        "round": round_number,
        "result": result,
        "scores": scores,
    }
    if winner is not None:
        entry["winner"] = winner

    if game_state_path.exists():
        with open(game_state_path) as f:
            state = yaml.safe_load(f) or {}
    else:
        state = {}

    if "rounds" not in state:
        state["rounds"] = []

    state["rounds"].append(entry)

    with open(game_state_path, "w") as f:
        yaml.dump(state, f, default_flow_style=False, sort_keys=False)


def contact_supervisor(message: str) -> str:
    """Send a message to the human supervisor via ntfy and audit trail."""
    import httpx

    ntfy_topic = os.environ["NOMIC_NTFY_TOPIC"]
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    entry = f"\n## Report at {timestamp}\n\n{message}\n"
    with open(SUPERVISOR_INBOX, "a") as f:
        f.write(entry)
    httpx.post(
        f"https://ntfy.sh/{ntfy_topic}",
        content=f"[Nomic Clerk Report]\n{message}".encode(),
        headers={"Title": "Nomic: Clerk Report", "Priority": "high"},
    )
    return "Report sent to supervisor (audit trail + notification)."
