"""MCP server providing encrypted note storage, voting primitives, and supervisor contact for Nomic players.

Players have no Write/Edit/Bash tools. This server is their ONLY write channel.
Identity is derived from the encryption key: storage directory = sha256(key)[:16].
"""

from __future__ import annotations

import hashlib
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
    resolve_file_path,
    resolve_note_path,
    resolve_storage_dir,
    validate_filename,
    write_encrypted_lines,
)

mcp = FastMCP("nomic-crypto")

PLAYERS_DIR = Path(__file__).parent.parent / "players"
SUPERVISOR_INBOX = Path(__file__).parent.parent / "supervisor_inbox.md"
NTFY_TOPIC = os.environ["NOMIC_NTFY_TOPIC"]


# --- Note tools: read operations ---


@mcp.tool()
def load_note(key: str, filename: str) -> str:
    """Load and decrypt a note file.

    Returns content in cat -n format (line numbers starting at 1) plus a
    delete_key footer. The delete_key is required for overwrite_note and
    delete_note operations.
    """
    path = resolve_note_path(key, filename, PLAYERS_DIR)
    assert path.exists(), f"Note '{filename}' does not exist"

    encrypted_lines = read_encrypted_lines(path)
    decrypted = [decrypt_line(line, key) for line in encrypted_lines]
    delete_key = compute_delete_key(path)

    return f"{format_cat_n(decrypted)}\n\ndelete_key: {delete_key}"


@mcp.tool()
def load_all_notes(key: str) -> str:
    """Load and decrypt all note files.

    Returns each file with a === filename === header, cat -n content,
    and per-file delete_key.
    """
    enc_dir = resolve_storage_dir(key, PLAYERS_DIR) / "encrypted"
    if not enc_dir.exists():
        return "No notes yet."
    files = sorted(f for f in enc_dir.iterdir() if f.is_file())
    if not files:
        return "No notes yet."

    sections = []
    for f in files:
        encrypted_lines = read_encrypted_lines(f)
        decrypted = [decrypt_line(line, key) for line in encrypted_lines]
        delete_key = compute_delete_key(f)
        sections.append(f"=== {f.name} ===\n{format_cat_n(decrypted)}\ndelete_key: {delete_key}")

    return "\n\n".join(sections)


@mcp.tool()
def list_note_files(key: str) -> str:
    """List all encrypted note filenames for the player."""
    enc_dir = resolve_storage_dir(key, PLAYERS_DIR) / "encrypted"
    if not enc_dir.exists():
        return "No notes yet."
    files = sorted(f.name for f in enc_dir.iterdir() if f.is_file())
    if not files:
        return "No notes yet."
    return "\n".join(files)


# --- Note tools: create ---


@mcp.tool()
def write_note(key: str, filename: str, content: str) -> str:
    """Create a new note file with one or more lines.

    Fails if the file already exists — use overwrite_note to replace.
    Content is split on newlines; each line is encrypted independently.
    """
    path = resolve_note_path(key, filename, PLAYERS_DIR)
    assert not path.exists(), f"Note '{filename}' already exists. Use overwrite_note to replace."

    lines = content.split("\n")
    encrypted_lines = [encrypt_line(line, key) for line in lines]
    write_encrypted_lines(path, encrypted_lines)

    return f"Created '{filename}' ({len(lines)} line(s))"


# --- Note tools: modify existing ---


@mcp.tool()
def append_note(key: str, filename: str, content: str) -> str:
    """Append one or more lines to an existing note file.

    Fails if the file doesn't exist — use write_note to create.
    """
    path = resolve_note_path(key, filename, PLAYERS_DIR)
    assert path.exists(), f"Note '{filename}' does not exist"

    new_lines = content.split("\n")
    encrypted_new = [encrypt_line(line, key) for line in new_lines]

    existing = read_encrypted_lines(path)
    write_encrypted_lines(path, existing + encrypted_new)

    return f"Appended {len(new_lines)} line(s) to '{filename}'"


@mcp.tool()
def edit_line(key: str, filename: str, line_number: int, content: str) -> str:
    """Replace a specific line (1-indexed) in a note file.

    Only the target line is re-encrypted; other lines are untouched.
    """
    path = resolve_note_path(key, filename, PLAYERS_DIR)
    assert path.exists(), f"Note '{filename}' does not exist"

    encrypted_lines = read_encrypted_lines(path)
    assert 1 <= line_number <= len(encrypted_lines), (
        f"Line {line_number} out of range (1-{len(encrypted_lines)})"
    )

    encrypted_lines[line_number - 1] = encrypt_line(content, key)
    write_encrypted_lines(path, encrypted_lines)

    return f"Edited line {line_number} of '{filename}'"


@mcp.tool()
def delete_line(key: str, filename: str, line_number: int) -> str:
    """Remove a specific line (1-indexed) from a note file.

    If this was the last line, the file is deleted.
    """
    path = resolve_note_path(key, filename, PLAYERS_DIR)
    assert path.exists(), f"Note '{filename}' does not exist"

    encrypted_lines = read_encrypted_lines(path)
    assert 1 <= line_number <= len(encrypted_lines), (
        f"Line {line_number} out of range (1-{len(encrypted_lines)})"
    )

    encrypted_lines.pop(line_number - 1)

    if encrypted_lines:
        write_encrypted_lines(path, encrypted_lines)
    else:
        path.unlink()

    return f"Deleted line {line_number} from '{filename}'"


# --- Note tools: destructive (require delete_key) ---


@mcp.tool()
def overwrite_note(key: str, filename: str, content: str, delete_key: str) -> str:
    """Overwrite an existing note file entirely.

    Requires the delete_key from the most recent load_note / load_all_notes
    call. This ensures you have read the current content before overwriting
    (optimistic concurrency control).
    """
    path = resolve_note_path(key, filename, PLAYERS_DIR)
    assert path.exists(), f"Note '{filename}' does not exist"

    current_dk = compute_delete_key(path)
    assert delete_key == current_dk, (
        "delete_key mismatch: file was modified since last read. Re-load and retry."
    )

    lines = content.split("\n")
    encrypted_lines = [encrypt_line(line, key) for line in lines]
    write_encrypted_lines(path, encrypted_lines)

    return f"Overwrote '{filename}' ({len(lines)} line(s))"


@mcp.tool()
def delete_note(key: str, filename: str, delete_key: str) -> str:
    """Delete an entire note file.

    Requires the delete_key from the most recent load_note / load_all_notes
    call. This ensures you have read the current content before deleting.
    """
    path = resolve_note_path(key, filename, PLAYERS_DIR)
    assert path.exists(), f"Note '{filename}' does not exist"

    current_dk = compute_delete_key(path)
    assert delete_key == current_dk, (
        "delete_key mismatch: file was modified since last read. Re-load and retry."
    )

    path.unlink()
    return f"Deleted '{filename}'"


# --- Plaintext file tools ---
# Players can read these with the native Read tool.
# These tools provide write/edit access to plaintext files in the player's directory.


@mcp.tool()
def list_files(key: str) -> str:
    """List plaintext files with their full paths (so you can Read them directly)."""
    files_dir = resolve_storage_dir(key, PLAYERS_DIR) / "files"
    if not files_dir.exists():
        return "No files yet."
    files = sorted(f for f in files_dir.iterdir() if f.is_file())
    if not files:
        return "No files yet."
    return "\n".join(str(f) for f in files)


@mcp.tool()
def write_file(key: str, filename: str, content: str) -> str:
    """Create a new plaintext file. Fails if the file already exists.

    The file is stored in your player directory and can be read with the
    native Read tool. Use list_files to get the full path.
    """
    path = resolve_file_path(key, filename, PLAYERS_DIR)
    assert not path.exists(), f"File '{filename}' already exists. Use overwrite_file to replace."
    path.write_text(content)
    return f"Created '{filename}' at {path}"


@mcp.tool()
def edit_file(key: str, filename: str, old_string: str, new_string: str) -> str:
    """Edit a plaintext file by replacing old_string with new_string.

    Works like Claude Code's Edit tool: old_string must appear exactly once
    in the file. The replacement is targeted — only the matched text changes.
    """
    path = resolve_file_path(key, filename, PLAYERS_DIR)
    assert path.exists(), f"File '{filename}' does not exist"

    content = path.read_text()
    count = content.count(old_string)
    assert count > 0, f"old_string not found in '{filename}'"
    assert count == 1, f"old_string appears {count} times in '{filename}' — must be unique"

    path.write_text(content.replace(old_string, new_string, 1))
    return f"Edited '{filename}'"


@mcp.tool()
def get_delete_key(key: str, filename: str) -> str:
    """Get the delete_key for a plaintext file.

    Required for overwrite_file and delete_file operations.
    Read the file first with the native Read tool, then call this
    to get the delete_key before overwriting or deleting.
    """
    path = resolve_file_path(key, filename, PLAYERS_DIR)
    assert path.exists(), f"File '{filename}' does not exist"
    return f"delete_key: {compute_delete_key(path)}"


@mcp.tool()
def overwrite_file(key: str, filename: str, content: str, delete_key: str) -> str:
    """Overwrite a plaintext file entirely. Requires delete_key from get_delete_key."""
    path = resolve_file_path(key, filename, PLAYERS_DIR)
    assert path.exists(), f"File '{filename}' does not exist"

    current_dk = compute_delete_key(path)
    assert delete_key == current_dk, (
        "delete_key mismatch: file was modified since last read. Re-read and retry."
    )

    path.write_text(content)
    return f"Overwrote '{filename}'"


@mcp.tool()
def delete_file(key: str, filename: str, delete_key: str) -> str:
    """Delete a plaintext file. Requires delete_key from get_delete_key."""
    path = resolve_file_path(key, filename, PLAYERS_DIR)
    assert path.exists(), f"File '{filename}' does not exist"

    current_dk = compute_delete_key(path)
    assert delete_key == current_dk, (
        "delete_key mismatch: file was modified since last read. Re-read and retry."
    )

    path.unlink()
    return f"Deleted '{filename}'"


# --- Game mechanics ---


GAME_LOG = Path(__file__).parent.parent / "game_log.md"


@mcp.tool()
def roll_dice(key: str, sides: int = 6) -> str:
    """Roll a cryptographically random die. The result is appended to the game log.

    The player's identity hash is recorded for auditability. Each player may
    only roll once per turn — the Clerk enforces this.
    """
    assert sides >= 2, f"Dice must have at least 2 sides, got {sides}"
    result = secrets.randbelow(sides) + 1
    player_hash = hashlib.sha256(key.encode()).hexdigest()[:16]
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    entry = f"\n**Dice roll** | {timestamp} | player:{player_hash} | d{sides} → **{result}**\n"
    with open(GAME_LOG, "a") as f:
        f.write(entry)
    return f"d{sides} → {result}"


# --- Crypto primitives for commit-reveal voting ---


@mcp.tool()
def commit(vote: str, nonce: str) -> str:
    """Create a commitment hash for a vote: sha256(vote|nonce).

    Use this during the commit phase of voting. Send the returned hash
    to the Clerk. Keep your vote and nonce secret until the reveal phase.
    """
    return hashlib.sha256(f"{vote}|{nonce}".encode()).hexdigest()


@mcp.tool()
def verify(vote: str, nonce: str, commitment: str) -> str:
    """Verify a vote against a commitment hash.

    Returns 'true' if sha256(vote|nonce) matches the commitment, 'false' otherwise.
    """
    expected = hashlib.sha256(f"{vote}|{nonce}".encode()).hexdigest()
    return "true" if expected == commitment else "false"


# --- Supervisor contact ---


@mcp.tool()
def contact_supervisor(message: str) -> str:
    """Send a message directly to the human supervisor, bypassing the Clerk.

    Use this to report suspected cheating, rule violations, or other concerns
    that you don't want to go through the Clerk. The message is:
    1. Sent as a push notification via ntfy (if configured)
    2. Appended to supervisor_inbox.md as a permanent audit trail
    """
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    entry = f"\n## Report at {timestamp}\n\n{message}\n"

    with open(SUPERVISOR_INBOX, "a") as f:
        f.write(entry)

    httpx.post(
        f"https://ntfy.sh/{NTFY_TOPIC}",
        content=f"[Nomic Supervisor Report]\n{message}".encode(),
        headers={"Title": "Nomic: Supervisor Report", "Priority": "high"},
    )

    return "Report sent to supervisor (audit trail + notification)."


if __name__ == "__main__":
    mcp.run()
