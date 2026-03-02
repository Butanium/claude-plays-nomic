"""MCP server for the Nomic Clerk: encrypted state storage and supervisor contact.

The Clerk uses Write/Edit directly for public game files (game_rules.md, game_log.md).
This server handles only encrypted Clerk state and supervisor escalation.
"""

from __future__ import annotations

import os
import secrets
from datetime import datetime, timezone
from pathlib import Path

import httpx
from mcp.server.fastmcp import FastMCP

from crypto import (
    compute_delete_key,
    decrypt_line,
    encrypt_line,
    format_cat_n,
    read_encrypted_lines,
    resolve_note_path,
    resolve_storage_dir,
    write_encrypted_lines,
)

mcp = FastMCP("nomic-clerk")

CLERK_DIR = Path(__file__).parent.parent / "clerk"
SUPERVISOR_INBOX = Path(__file__).parent.parent / "supervisor_inbox.md"
NTFY_TOPIC = os.environ["NOMIC_NTFY_TOPIC"]


WORDLIST = [
    "amber", "arrow", "atlas", "azure", "basin", "blade", "blaze", "bloom",
    "bonus", "brave", "brisk", "brook", "cairn", "cargo", "cedar", "chain",
    "charm", "chess", "cider", "clasp", "cliff", "cloud", "cobra", "coral",
    "crane", "crest", "crown", "cubic", "delta", "denim", "depot", "diver",
    "dodge", "draft", "drift", "dusk", "eagle", "ember", "epoch", "equal",
    "fable", "faith", "fault", "feast", "fence", "ferry", "finch", "flame",
    "flask", "flint", "forge", "frost", "gavel", "ghost", "glaze", "gleam",
    "globe", "glyph", "goose", "gorge", "grain", "grape", "grove", "guard",
    "haven", "hatch", "hazel", "hedge", "hoist", "honor", "horse", "hover",
    "index", "ivory", "jabot", "jewel", "joker", "juice", "kayak", "knack",
    "knoll", "latch", "ledge", "lever", "linen", "llama", "lodge", "lotus",
    "lunar", "maple", "marsh", "mason", "medal", "merit", "mirth", "moose",
    "mural", "nerve", "nexus", "noble", "north", "oasis", "ocean", "olive",
    "onion", "orbit", "otter", "oxide", "pansy", "patch", "pearl", "pedal",
    "penny", "perch", "pilot", "pixel", "plank", "plaza", "plume", "polar",
    "prism", "prowl", "pulse", "quail", "quark", "quest", "radar", "rapid",
    "raven", "realm", "ridge", "rivet", "robin", "roost", "ruby", "salve",
    "satin", "scout", "shaft", "shark", "shelf", "sigma", "siren", "slate",
    "sleet", "solar", "spark", "spear", "spike", "spire", "spoke", "squid",
    "staff", "steep", "stoic", "stone", "stork", "surge", "swamp", "sworn",
    "talon", "tango", "thorn", "tiger", "token", "topaz", "torch", "tower",
    "trout", "tulip", "ultra", "umbra", "unity", "valor", "vault", "vigor",
    "viola", "viper", "vivid", "vocal", "waltz", "watch", "whale", "wheat",
    "whelk", "width", "winch", "wrath", "yacht", "youth", "zebra", "zippy",
]


@mcp.tool()
def generate_key() -> str:
    """Generate a memorable key for a player.

    Returns a 4-word slug (e.g. 'amber-cliff-polar-trout') drawn from a
    192-word list, giving ~30 bits of entropy. The Clerk should distribute
    this to the player via their system prompt and never store it in plaintext.
    """
    words = [secrets.choice(WORDLIST) for _ in range(4)]
    return "-".join(words)


@mcp.tool()
def save_state(key: str, filename: str, content: str) -> str:
    """Encrypt and save Clerk state. Overwrites if the file already exists.

    Content is split on newlines; each line is encrypted independently.
    """
    path = resolve_note_path(key, filename, CLERK_DIR)
    lines = content.split("\n")
    encrypted_lines = [encrypt_line(line, key) for line in lines]
    write_encrypted_lines(path, encrypted_lines)
    return f"Saved '{filename}' ({len(lines)} line(s))"


@mcp.tool()
def load_state(key: str, filename: str) -> str:
    """Decrypt and return Clerk state in cat -n format."""
    path = resolve_note_path(key, filename, CLERK_DIR)
    assert path.exists(), f"State file '{filename}' does not exist"

    encrypted_lines = read_encrypted_lines(path)
    decrypted = [decrypt_line(line, key) for line in encrypted_lines]
    return format_cat_n(decrypted)


@mcp.tool()
def list_state_files(key: str) -> str:
    """List all Clerk state files."""
    state_dir = resolve_storage_dir(key, CLERK_DIR)
    files = sorted(f.name for f in state_dir.iterdir() if f.is_file())
    if not files:
        return "No state files yet."
    return "\n".join(files)


@mcp.tool()
def contact_supervisor(message: str) -> str:
    """Send a message directly to the human supervisor.

    Use for rule disputes, ambiguous interpretations, or game-critical
    decisions that need human input. The message is sent as a push
    notification and appended to the audit trail.
    """
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    entry = f"\n## Report at {timestamp}\n\n{message}\n"

    with open(SUPERVISOR_INBOX, "a") as f:
        f.write(entry)

    httpx.post(
        f"https://ntfy.sh/{NTFY_TOPIC}",
        content=f"[Nomic Clerk Report]\n{message}".encode(),
        headers={"Title": "Nomic: Clerk Report", "Priority": "high"},
    )

    return "Report sent to supervisor (audit trail + notification)."


if __name__ == "__main__":
    mcp.run()
