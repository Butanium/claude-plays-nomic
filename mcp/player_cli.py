#!/usr/bin/env python3
"""CLI for Nomic player tools.

Workaround for MCP servers not loading in Claude Code subagents/teammates.
Players call this via Bash; the player hook restricts Bash to only this script.

Usage:
    uv run python mcp/player_cli.py <command> [args...]
"""

from __future__ import annotations

import argparse
import hashlib
import os
import secrets
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

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


# --- Note commands ---


def cmd_load_note(args):
    path = resolve_note_path(args.key, args.filename, PLAYERS_DIR)
    assert path.exists(), f"Note '{args.filename}' does not exist"
    encrypted_lines = read_encrypted_lines(path)
    decrypted = [decrypt_line(line, args.key) for line in encrypted_lines]
    delete_key = compute_delete_key(path)
    print(f"{format_cat_n(decrypted)}\n\ndelete_key: {delete_key}")


def cmd_load_all_notes(args):
    enc_dir = resolve_storage_dir(args.key, PLAYERS_DIR) / "encrypted"
    if not enc_dir.exists():
        print("No notes yet.")
        return
    files = sorted(f for f in enc_dir.iterdir() if f.is_file())
    if not files:
        print("No notes yet.")
        return
    sections = []
    for f in files:
        encrypted_lines = read_encrypted_lines(f)
        decrypted = [decrypt_line(line, args.key) for line in encrypted_lines]
        dk = compute_delete_key(f)
        sections.append(
            f"=== {f.name} ===\n{format_cat_n(decrypted)}\ndelete_key: {dk}"
        )
    print("\n\n".join(sections))


def cmd_list_note_files(args):
    enc_dir = resolve_storage_dir(args.key, PLAYERS_DIR) / "encrypted"
    if not enc_dir.exists():
        print("No notes yet.")
        return
    files = sorted(f.name for f in enc_dir.iterdir() if f.is_file())
    if not files:
        print("No notes yet.")
        return
    print("\n".join(files))


def cmd_write_note(args):
    path = resolve_note_path(args.key, args.filename, PLAYERS_DIR)
    assert not path.exists(), (
        f"Note '{args.filename}' already exists. Use overwrite_note to replace."
    )
    lines = args.content.split("\n")
    encrypted_lines = [encrypt_line(line, args.key) for line in lines]
    write_encrypted_lines(path, encrypted_lines)
    print(f"Created '{args.filename}' ({len(lines)} line(s))")


def cmd_append_note(args):
    path = resolve_note_path(args.key, args.filename, PLAYERS_DIR)
    assert path.exists(), f"Note '{args.filename}' does not exist"
    new_lines = args.content.split("\n")
    encrypted_new = [encrypt_line(line, args.key) for line in new_lines]
    existing = read_encrypted_lines(path)
    write_encrypted_lines(path, existing + encrypted_new)
    print(f"Appended {len(new_lines)} line(s) to '{args.filename}'")


def cmd_edit_line(args):
    path = resolve_note_path(args.key, args.filename, PLAYERS_DIR)
    assert path.exists(), f"Note '{args.filename}' does not exist"
    encrypted_lines = read_encrypted_lines(path)
    assert 1 <= args.line_number <= len(encrypted_lines), (
        f"Line {args.line_number} out of range (1-{len(encrypted_lines)})"
    )
    encrypted_lines[args.line_number - 1] = encrypt_line(args.content, args.key)
    write_encrypted_lines(path, encrypted_lines)
    print(f"Edited line {args.line_number} of '{args.filename}'")


def cmd_delete_line(args):
    path = resolve_note_path(args.key, args.filename, PLAYERS_DIR)
    assert path.exists(), f"Note '{args.filename}' does not exist"
    encrypted_lines = read_encrypted_lines(path)
    assert 1 <= args.line_number <= len(encrypted_lines), (
        f"Line {args.line_number} out of range (1-{len(encrypted_lines)})"
    )
    encrypted_lines.pop(args.line_number - 1)
    if encrypted_lines:
        write_encrypted_lines(path, encrypted_lines)
    else:
        path.unlink()
    print(f"Deleted line {args.line_number} from '{args.filename}'")


def cmd_overwrite_note(args):
    path = resolve_note_path(args.key, args.filename, PLAYERS_DIR)
    assert path.exists(), f"Note '{args.filename}' does not exist"
    current_dk = compute_delete_key(path)
    assert args.delete_key == current_dk, (
        "delete_key mismatch: file was modified since last read. Re-load and retry."
    )
    lines = args.content.split("\n")
    encrypted_lines = [encrypt_line(line, args.key) for line in lines]
    write_encrypted_lines(path, encrypted_lines)
    print(f"Overwrote '{args.filename}' ({len(lines)} line(s))")


def cmd_delete_note(args):
    path = resolve_note_path(args.key, args.filename, PLAYERS_DIR)
    assert path.exists(), f"Note '{args.filename}' does not exist"
    current_dk = compute_delete_key(path)
    assert args.delete_key == current_dk, (
        "delete_key mismatch: file was modified since last read. Re-load and retry."
    )
    path.unlink()
    print(f"Deleted '{args.filename}'")


# --- File commands ---


def cmd_list_files(args):
    files_dir = resolve_storage_dir(args.key, PLAYERS_DIR) / "files"
    if not files_dir.exists():
        print("No files yet.")
        return
    files = sorted(f for f in files_dir.iterdir() if f.is_file())
    if not files:
        print("No files yet.")
        return
    print("\n".join(str(f) for f in files))


def cmd_write_file(args):
    path = resolve_file_path(args.key, args.filename, PLAYERS_DIR)
    assert not path.exists(), (
        f"File '{args.filename}' already exists. Use overwrite_file to replace."
    )
    path.write_text(args.content)
    print(f"Created '{args.filename}' at {path}")


def cmd_edit_file(args):
    path = resolve_file_path(args.key, args.filename, PLAYERS_DIR)
    assert path.exists(), f"File '{args.filename}' does not exist"
    content = path.read_text()
    count = content.count(args.old_string)
    assert count > 0, f"old_string not found in '{args.filename}'"
    assert count == 1, (
        f"old_string appears {count} times in '{args.filename}' — must be unique"
    )
    path.write_text(content.replace(args.old_string, args.new_string, 1))
    print(f"Edited '{args.filename}'")


def cmd_get_delete_key(args):
    path = resolve_file_path(args.key, args.filename, PLAYERS_DIR)
    assert path.exists(), f"File '{args.filename}' does not exist"
    print(f"delete_key: {compute_delete_key(path)}")


def cmd_overwrite_file(args):
    path = resolve_file_path(args.key, args.filename, PLAYERS_DIR)
    assert path.exists(), f"File '{args.filename}' does not exist"
    current_dk = compute_delete_key(path)
    assert args.delete_key == current_dk, (
        "delete_key mismatch: file was modified since last read. Re-read and retry."
    )
    path.write_text(args.content)
    print(f"Overwrote '{args.filename}'")


def cmd_delete_file(args):
    path = resolve_file_path(args.key, args.filename, PLAYERS_DIR)
    assert path.exists(), f"File '{args.filename}' does not exist"
    current_dk = compute_delete_key(path)
    assert args.delete_key == current_dk, (
        "delete_key mismatch: file was modified since last read. Re-read and retry."
    )
    path.unlink()
    print(f"Deleted '{args.filename}'")


# --- Game mechanics ---


def cmd_roll_dice(args):
    assert args.sides >= 2, f"Dice must have at least 2 sides, got {args.sides}"
    result = secrets.randbelow(args.sides) + 1
    player_hash = hashlib.sha256(args.key.encode()).hexdigest()[:16]
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    entry = (
        f"\n**Dice roll** | {timestamp} | player:{player_hash}"
        f" | d{args.sides} → **{result}**\n"
    )
    with open(GAME_LOG, "a") as f:
        f.write(entry)
    print(f"d{args.sides} → {result}")


def cmd_commit(args):
    hex_hash = commitment_hash(args.vote, args.nonce)
    slug = hash_to_slug(hex_hash)
    print(f"{slug} ({hex_hash})")


def cmd_verify(args):
    expected_hex = commitment_hash(args.vote, args.nonce)
    expected_slug = hash_to_slug(expected_hex)
    commitment = args.commitment.strip()
    print("true" if commitment in (expected_hex, expected_slug) else "false")


def cmd_contact_supervisor(args):
    import httpx

    ntfy_topic = os.environ["NOMIC_NTFY_TOPIC"]
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    entry = f"\n## Report at {timestamp}\n\n{args.message}\n"
    with open(SUPERVISOR_INBOX, "a") as f:
        f.write(entry)
    httpx.post(
        f"https://ntfy.sh/{ntfy_topic}",
        content=f"[Nomic Supervisor Report]\n{args.message}".encode(),
        headers={"Title": "Nomic: Supervisor Report", "Priority": "high"},
    )
    print("Report sent to supervisor (audit trail + notification).")


# --- Argument parser ---


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    parser = argparse.ArgumentParser(
        description="Nomic player tools CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # Notes: read
    p = sub.add_parser("load_note")
    p.add_argument("key")
    p.add_argument("filename")
    p.set_defaults(func=cmd_load_note)

    p = sub.add_parser("load_all_notes")
    p.add_argument("key")
    p.set_defaults(func=cmd_load_all_notes)

    p = sub.add_parser("list_note_files")
    p.add_argument("key")
    p.set_defaults(func=cmd_list_note_files)

    # Notes: create
    p = sub.add_parser("write_note")
    p.add_argument("key")
    p.add_argument("filename")
    p.add_argument("content")
    p.set_defaults(func=cmd_write_note)

    # Notes: modify
    p = sub.add_parser("append_note")
    p.add_argument("key")
    p.add_argument("filename")
    p.add_argument("content")
    p.set_defaults(func=cmd_append_note)

    p = sub.add_parser("edit_line")
    p.add_argument("key")
    p.add_argument("filename")
    p.add_argument("line_number", type=int)
    p.add_argument("content")
    p.set_defaults(func=cmd_edit_line)

    p = sub.add_parser("delete_line")
    p.add_argument("key")
    p.add_argument("filename")
    p.add_argument("line_number", type=int)
    p.set_defaults(func=cmd_delete_line)

    # Notes: destructive
    p = sub.add_parser("overwrite_note")
    p.add_argument("key")
    p.add_argument("filename")
    p.add_argument("content")
    p.add_argument("delete_key")
    p.set_defaults(func=cmd_overwrite_note)

    p = sub.add_parser("delete_note")
    p.add_argument("key")
    p.add_argument("filename")
    p.add_argument("delete_key")
    p.set_defaults(func=cmd_delete_note)

    # Files
    p = sub.add_parser("list_files")
    p.add_argument("key")
    p.set_defaults(func=cmd_list_files)

    p = sub.add_parser("write_file")
    p.add_argument("key")
    p.add_argument("filename")
    p.add_argument("content")
    p.set_defaults(func=cmd_write_file)

    p = sub.add_parser("edit_file")
    p.add_argument("key")
    p.add_argument("filename")
    p.add_argument("old_string")
    p.add_argument("new_string")
    p.set_defaults(func=cmd_edit_file)

    p = sub.add_parser("get_delete_key")
    p.add_argument("key")
    p.add_argument("filename")
    p.set_defaults(func=cmd_get_delete_key)

    p = sub.add_parser("overwrite_file")
    p.add_argument("key")
    p.add_argument("filename")
    p.add_argument("content")
    p.add_argument("delete_key")
    p.set_defaults(func=cmd_overwrite_file)

    p = sub.add_parser("delete_file")
    p.add_argument("key")
    p.add_argument("filename")
    p.add_argument("delete_key")
    p.set_defaults(func=cmd_delete_file)

    # Game mechanics
    p = sub.add_parser("roll_dice")
    p.add_argument("key")
    p.add_argument("--sides", type=int, default=6)
    p.set_defaults(func=cmd_roll_dice)

    p = sub.add_parser("commit")
    p.add_argument("vote")
    p.add_argument("nonce")
    p.set_defaults(func=cmd_commit)

    p = sub.add_parser("verify")
    p.add_argument("vote")
    p.add_argument("nonce")
    p.add_argument("commitment")
    p.set_defaults(func=cmd_verify)

    p = sub.add_parser("contact_supervisor")
    p.add_argument("message")
    p.set_defaults(func=cmd_contact_supervisor)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
