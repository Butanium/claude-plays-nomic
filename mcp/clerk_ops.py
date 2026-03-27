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


def commit_all(message: str = "end of turn") -> str:
    """Commit all changed files in the game repository."""
    project_root = Path(__file__).parent.parent

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

    result = subprocess.run(
        ["git", "commit", "-m", message],
        cwd=project_root,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        if "nothing to commit" in result.stdout:
            return "Nothing to commit — working tree clean."
        return f"Git commit failed: {result.stdout}\n{result.stderr}"

    return f"Committed all changes on branch '{branch}': {message}"


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
