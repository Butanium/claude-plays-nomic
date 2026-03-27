#!/usr/bin/env python3
"""CLI for Nomic player tools.

Workaround for MCP servers not loading in Claude Code subagents/teammates.
Players call this via Bash; the player hook restricts Bash to only this script.

Usage:
    uv run python mcp/player_cli.py <command> [args...]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import player_ops


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
    p.set_defaults(func=lambda a: player_ops.load_note(a.key, a.filename))

    p = sub.add_parser("load_all_notes")
    p.add_argument("key")
    p.set_defaults(func=lambda a: player_ops.load_all_notes(a.key))

    p = sub.add_parser("list_note_files")
    p.add_argument("key")
    p.set_defaults(func=lambda a: player_ops.list_note_files(a.key))

    # Notes: create
    p = sub.add_parser("write_note")
    p.add_argument("key")
    p.add_argument("filename")
    p.add_argument("content")
    p.set_defaults(func=lambda a: player_ops.write_note(a.key, a.filename, a.content))

    # Notes: modify
    p = sub.add_parser("append_note")
    p.add_argument("key")
    p.add_argument("filename")
    p.add_argument("content")
    p.set_defaults(func=lambda a: player_ops.append_note(a.key, a.filename, a.content))

    p = sub.add_parser("edit_line")
    p.add_argument("key")
    p.add_argument("filename")
    p.add_argument("line_number", type=int)
    p.add_argument("content")
    p.set_defaults(func=lambda a: player_ops.edit_line(a.key, a.filename, a.line_number, a.content))

    p = sub.add_parser("delete_line")
    p.add_argument("key")
    p.add_argument("filename")
    p.add_argument("line_number", type=int)
    p.set_defaults(func=lambda a: player_ops.delete_line(a.key, a.filename, a.line_number))

    # Notes: destructive
    p = sub.add_parser("overwrite_note")
    p.add_argument("key")
    p.add_argument("filename")
    p.add_argument("content")
    p.add_argument("delete_key")
    p.set_defaults(func=lambda a: player_ops.overwrite_note(a.key, a.filename, a.content, a.delete_key))

    p = sub.add_parser("delete_note")
    p.add_argument("key")
    p.add_argument("filename")
    p.add_argument("delete_key")
    p.set_defaults(func=lambda a: player_ops.delete_note(a.key, a.filename, a.delete_key))

    # Files
    p = sub.add_parser("list_files")
    p.add_argument("key")
    p.set_defaults(func=lambda a: player_ops.list_files(a.key))

    p = sub.add_parser("write_file")
    p.add_argument("key")
    p.add_argument("filename")
    p.add_argument("content")
    p.set_defaults(func=lambda a: player_ops.write_file(a.key, a.filename, a.content))

    p = sub.add_parser("edit_file")
    p.add_argument("key")
    p.add_argument("filename")
    p.add_argument("old_string")
    p.add_argument("new_string")
    p.set_defaults(func=lambda a: player_ops.edit_file(a.key, a.filename, a.old_string, a.new_string))

    p = sub.add_parser("get_delete_key")
    p.add_argument("key")
    p.add_argument("filename")
    p.set_defaults(func=lambda a: player_ops.get_delete_key(a.key, a.filename))

    p = sub.add_parser("overwrite_file")
    p.add_argument("key")
    p.add_argument("filename")
    p.add_argument("content")
    p.add_argument("delete_key")
    p.set_defaults(func=lambda a: player_ops.overwrite_file(a.key, a.filename, a.content, a.delete_key))

    p = sub.add_parser("delete_file")
    p.add_argument("key")
    p.add_argument("filename")
    p.add_argument("delete_key")
    p.set_defaults(func=lambda a: player_ops.delete_file(a.key, a.filename, a.delete_key))

    # Proposal
    p = sub.add_parser("propose")
    p.add_argument("key")
    p.add_argument("proposal")
    p.set_defaults(func=lambda a: player_ops.propose(a.key, a.proposal))

    p = sub.add_parser("verify_proposal")
    p.add_argument("key")
    p.set_defaults(func=lambda a: player_ops.verify_proposal(a.key))

    # Game mechanics
    p = sub.add_parser("roll_dice")
    p.add_argument("key")
    p.add_argument("--dice", default="1d6")
    p.set_defaults(func=lambda a: player_ops.roll_dice(a.key, a.dice))

    p = sub.add_parser("commit")
    p.add_argument("vote")
    p.add_argument("nonce")
    p.set_defaults(func=lambda a: player_ops.commit(a.vote, a.nonce))

    p = sub.add_parser("verify")
    p.add_argument("vote")
    p.add_argument("nonce")
    p.add_argument("commitment")
    p.set_defaults(func=lambda a: player_ops.verify(a.vote, a.nonce, a.commitment))

    p = sub.add_parser("contact_supervisor")
    p.add_argument("message")
    p.set_defaults(func=lambda a: player_ops.contact_supervisor(a.message))

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    print(args.func(args))


if __name__ == "__main__":
    main()
