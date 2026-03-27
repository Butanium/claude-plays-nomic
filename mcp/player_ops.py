"""Core player operations shared between MCP server and CLI.

All functions return strings. The MCP server wraps them as @mcp.tool(),
the CLI prints the returned strings.
"""

from __future__ import annotations

import hashlib
import os
import re
import secrets
from datetime import datetime, timezone
from pathlib import Path

from crypto import (
    commitment_hash,
    compute_delete_key,
    decrypt_line,
    encrypt_line,
    format_cat_n,
    hash_to_slug,
    read_encrypted_lines,
    resolve_file_path,
    resolve_note_path,
    resolve_storage_dir,
    write_encrypted_lines,
)

PLAYERS_DIR = Path(__file__).parent.parent / "players"
GAME_LOG = Path(__file__).parent.parent / "game_log.md"
SUPERVISOR_INBOX = Path(__file__).parent.parent / "supervisor_inbox.md"
LATEST_PROPOSAL = Path(__file__).parent.parent / "latest_proposal.txt"
LATEST_PROPOSAL_PROOF = Path(__file__).parent.parent / "latest_proposal_proof.txt"


# --- Note operations ---


def load_note(key: str, filename: str) -> str:
    """Load and decrypt a note file, returning cat -n content and delete_key."""
    path = resolve_note_path(key, filename, PLAYERS_DIR)
    assert path.exists(), f"Note '{filename}' does not exist"
    encrypted_lines = read_encrypted_lines(path)
    decrypted = [decrypt_line(line, key) for line in encrypted_lines]
    delete_key = compute_delete_key(path)
    return f"{format_cat_n(decrypted)}\n\ndelete_key: {delete_key}"


def load_all_notes(key: str) -> str:
    """Load and decrypt all note files."""
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
        dk = compute_delete_key(f)
        sections.append(
            f"=== {f.name} ===\n{format_cat_n(decrypted)}\ndelete_key: {dk}"
        )
    return "\n\n".join(sections)


def list_note_files(key: str) -> str:
    """List all encrypted note filenames for the player."""
    enc_dir = resolve_storage_dir(key, PLAYERS_DIR) / "encrypted"
    if not enc_dir.exists():
        return "No notes yet."
    files = sorted(f.name for f in enc_dir.iterdir() if f.is_file())
    if not files:
        return "No notes yet."
    return "\n".join(files)


def write_note(key: str, filename: str, content: str) -> str:
    """Create a new note file. Fails if it already exists."""
    path = resolve_note_path(key, filename, PLAYERS_DIR)
    assert not path.exists(), (
        f"Note '{filename}' already exists. Use overwrite_note to replace."
    )
    lines = content.split("\n")
    encrypted_lines = [encrypt_line(line, key) for line in lines]
    write_encrypted_lines(path, encrypted_lines)
    return f"Created '{filename}' ({len(lines)} line(s))"


def append_note(key: str, filename: str, content: str) -> str:
    """Append lines to an existing note file."""
    path = resolve_note_path(key, filename, PLAYERS_DIR)
    assert path.exists(), f"Note '{filename}' does not exist"
    new_lines = content.split("\n")
    encrypted_new = [encrypt_line(line, key) for line in new_lines]
    existing = read_encrypted_lines(path)
    write_encrypted_lines(path, existing + encrypted_new)
    return f"Appended {len(new_lines)} line(s) to '{filename}'"


def edit_line(key: str, filename: str, line_number: int, content: str) -> str:
    """Replace a specific line (1-indexed) in a note file."""
    path = resolve_note_path(key, filename, PLAYERS_DIR)
    assert path.exists(), f"Note '{filename}' does not exist"
    encrypted_lines = read_encrypted_lines(path)
    assert 1 <= line_number <= len(encrypted_lines), (
        f"Line {line_number} out of range (1-{len(encrypted_lines)})"
    )
    encrypted_lines[line_number - 1] = encrypt_line(content, key)
    write_encrypted_lines(path, encrypted_lines)
    return f"Edited line {line_number} of '{filename}'"


def delete_line(key: str, filename: str, line_number: int) -> str:
    """Remove a specific line (1-indexed) from a note file."""
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


def overwrite_note(key: str, filename: str, content: str, delete_key: str) -> str:
    """Overwrite an existing note file. Requires delete_key for concurrency control."""
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


def delete_note(key: str, filename: str, delete_key: str) -> str:
    """Delete an entire note file. Requires delete_key for concurrency control."""
    path = resolve_note_path(key, filename, PLAYERS_DIR)
    assert path.exists(), f"Note '{filename}' does not exist"
    current_dk = compute_delete_key(path)
    assert delete_key == current_dk, (
        "delete_key mismatch: file was modified since last read. Re-load and retry."
    )
    path.unlink()
    return f"Deleted '{filename}'"


# --- Plaintext file operations ---


def list_files(key: str) -> str:
    """List plaintext files with their full paths."""
    files_dir = resolve_storage_dir(key, PLAYERS_DIR) / "files"
    if not files_dir.exists():
        return "No files yet."
    files = sorted(f for f in files_dir.iterdir() if f.is_file())
    if not files:
        return "No files yet."
    return "\n".join(str(f) for f in files)


def write_file(key: str, filename: str, content: str) -> str:
    """Create a new plaintext file. Fails if it already exists."""
    path = resolve_file_path(key, filename, PLAYERS_DIR)
    assert not path.exists(), (
        f"File '{filename}' already exists. Use overwrite_file to replace."
    )
    path.write_text(content)
    return f"Created '{filename}' at {path}"


def edit_file(key: str, filename: str, old_string: str, new_string: str) -> str:
    """Edit a plaintext file by replacing old_string with new_string (must be unique)."""
    path = resolve_file_path(key, filename, PLAYERS_DIR)
    assert path.exists(), f"File '{filename}' does not exist"
    content = path.read_text()
    count = content.count(old_string)
    assert count > 0, f"old_string not found in '{filename}'"
    assert count == 1, (
        f"old_string appears {count} times in '{filename}' — must be unique"
    )
    path.write_text(content.replace(old_string, new_string, 1))
    return f"Edited '{filename}'"


def get_delete_key(key: str, filename: str) -> str:
    """Get the delete_key for a plaintext file."""
    path = resolve_file_path(key, filename, PLAYERS_DIR)
    assert path.exists(), f"File '{filename}' does not exist"
    return f"delete_key: {compute_delete_key(path)}"


def overwrite_file(key: str, filename: str, content: str, delete_key: str) -> str:
    """Overwrite a plaintext file. Requires delete_key for concurrency control."""
    path = resolve_file_path(key, filename, PLAYERS_DIR)
    assert path.exists(), f"File '{filename}' does not exist"
    current_dk = compute_delete_key(path)
    assert delete_key == current_dk, (
        "delete_key mismatch: file was modified since last read. Re-read and retry."
    )
    path.write_text(content)
    return f"Overwrote '{filename}'"


def delete_file(key: str, filename: str, delete_key: str) -> str:
    """Delete a plaintext file. Requires delete_key for concurrency control."""
    path = resolve_file_path(key, filename, PLAYERS_DIR)
    assert path.exists(), f"File '{filename}' does not exist"
    current_dk = compute_delete_key(path)
    assert delete_key == current_dk, (
        "delete_key mismatch: file was modified since last read. Re-read and retry."
    )
    path.unlink()
    return f"Deleted '{filename}'"


# --- Proposal submission ---


def propose(key: str, proposal: str) -> str:
    """Submit a rule-change proposal with cryptographic proof of authorship."""
    player_hash = hashlib.sha256(key.encode()).hexdigest()[:16]
    proof = hashlib.sha256(f"{proposal}|{key}".encode()).hexdigest()
    LATEST_PROPOSAL.write_text(proposal)
    LATEST_PROPOSAL_PROOF.write_text(f"player:{player_hash}\nproof:{proof}\n")
    return f"Proposal submitted. Player: {player_hash}"


def verify_proposal(player_key: str) -> str:
    """Verify that latest_proposal.txt was submitted by the given player."""
    assert LATEST_PROPOSAL.exists(), "No proposal submitted yet (latest_proposal.txt missing)"
    assert LATEST_PROPOSAL_PROOF.exists(), "No proof file (latest_proposal_proof.txt missing)"

    proposal = LATEST_PROPOSAL.read_text()
    proof_content = LATEST_PROPOSAL_PROOF.read_text().strip()

    proof_lines = {}
    for line in proof_content.split("\n"):
        k, _, v = line.partition(":")
        proof_lines[k] = v

    assert "player" in proof_lines and "proof" in proof_lines, "Malformed proof file"

    expected_player_hash = hashlib.sha256(player_key.encode()).hexdigest()[:16]
    expected_proof = hashlib.sha256(f"{proposal}|{player_key}".encode()).hexdigest()

    player_match = proof_lines["player"] == expected_player_hash
    proof_match = proof_lines["proof"] == expected_proof

    if player_match and proof_match:
        return f"VERIFIED: Proposal was submitted by player:{expected_player_hash}"
    if not player_match:
        return f"FAILED: Player hash mismatch (expected {expected_player_hash}, got {proof_lines['player']})"
    return "FAILED: Proof mismatch — proposal may have been tampered with"


# --- Game mechanics ---


def roll_dice(key: str, dice: str = "1d6") -> str:
    """Roll dice in xdy format. Results appended to game log."""
    match = re.fullmatch(r"(\d+)d(\d+)", dice)
    assert match, f"Invalid dice format '{dice}', expected xdy (e.g. '2d6', '3d12')"
    count, sides = int(match.group(1)), int(match.group(2))
    assert count >= 1, f"Must roll at least 1 die, got {count}"
    assert sides >= 2, f"Dice must have at least 2 sides, got {sides}"

    results = [secrets.randbelow(sides) + 1 for _ in range(count)]
    player_hash = hashlib.sha256(key.encode()).hexdigest()[:16]
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    results_str = ", ".join(str(r) for r in results)
    entry = (
        f"\n**Dice roll** | {timestamp} | player:{player_hash}"
        f" | {dice} → **{results_str}**\n"
    )
    with open(GAME_LOG, "a") as f:
        f.write(entry)
    return f"{dice} → {results_str}"


def commit(vote: str, nonce: str) -> str:
    """Create a commitment slug for a vote."""
    hex_hash = commitment_hash(vote, nonce)
    return hash_to_slug(hex_hash)


def verify(vote: str, nonce: str, commitment: str) -> str:
    """Verify a vote against a commitment. Returns 'true' or 'false'."""
    expected_hex = commitment_hash(vote, nonce)
    expected_slug = hash_to_slug(expected_hex)
    commitment = commitment.strip()
    return "true" if commitment in (expected_hex, expected_slug) else "false"


# --- Supervisor contact ---


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
        content=f"[Nomic Supervisor Report]\n{message}".encode(),
        headers={"Title": "Nomic: Supervisor Report", "Priority": "high"},
    )
    return "Report sent to supervisor (audit trail + notification)."
