#!/usr/bin/env python3
"""CLI for Nomic Clerk tools.

Workaround for MCP servers not loading via --mcp-config with --agent.
The Clerk calls this via Bash; the clerk hook restricts Bash to only this script.

Usage:
    uv run python mcp/clerk_cli.py <command> [args...]
"""

from __future__ import annotations

import argparse
import os
import secrets
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from crypto import (
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


def cmd_generate_key(args):
    """Generate a memorable 4-word key for a player."""
    words = [secrets.choice(WORDLIST) for _ in range(4)]
    print("-".join(words))


def cmd_save_state(args):
    """Encrypt and save Clerk state. Overwrites if the file already exists."""
    path = resolve_note_path(args.key, args.filename, CLERK_DIR)
    lines = args.content.split("\n")
    encrypted_lines = [encrypt_line(line, args.key) for line in lines]
    write_encrypted_lines(path, encrypted_lines)
    print(f"Saved '{args.filename}' ({len(lines)} line(s))")


def cmd_load_state(args):
    """Decrypt and return Clerk state."""
    path = resolve_note_path(args.key, args.filename, CLERK_DIR)
    assert path.exists(), f"State file '{args.filename}' does not exist"
    encrypted_lines = read_encrypted_lines(path)
    decrypted = [decrypt_line(line, args.key) for line in encrypted_lines]
    print(format_cat_n(decrypted))


def cmd_list_state_files(args):
    """List all Clerk state files."""
    state_dir = resolve_storage_dir(args.key, CLERK_DIR)
    files = sorted(f.name for f in state_dir.iterdir() if f.is_file())
    if not files:
        print("No state files yet.")
        return
    print("\n".join(files))


def cmd_commit_all(args):
    """Commit all changed files in the game repository."""
    import subprocess

    project_root = Path(__file__).parent.parent

    branch = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        cwd=project_root,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()

    if not branch.startswith("game"):
        print(
            f"ERROR: Current branch is '{branch}', which does not start with 'game'. "
            "Aborting commit. Contact the supervisor about this issue."
        )
        sys.exit(1)

    subprocess.run(["git", "add", "-A"], cwd=project_root, check=True)

    message = args.message if args.message else "end of turn"
    result = subprocess.run(
        ["git", "commit", "-m", message],
        cwd=project_root,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        if "nothing to commit" in result.stdout:
            print("Nothing to commit — working tree clean.")
            return
        print(f"Git commit failed: {result.stdout}\n{result.stderr}")
        sys.exit(1)

    print(f"Committed all changes on branch '{branch}': {message}")


def cmd_contact_supervisor(args):
    """Send a message to the human supervisor."""
    import httpx

    ntfy_topic = os.environ["NOMIC_NTFY_TOPIC"]
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    entry = f"\n## Report at {timestamp}\n\n{args.message}\n"
    with open(SUPERVISOR_INBOX, "a") as f:
        f.write(entry)
    httpx.post(
        f"https://ntfy.sh/{ntfy_topic}",
        content=f"[Nomic Clerk Report]\n{args.message}".encode(),
        headers={"Title": "Nomic: Clerk Report", "Priority": "high"},
    )
    print("Report sent to supervisor (audit trail + notification).")


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    parser = argparse.ArgumentParser(
        description="Nomic Clerk tools CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("generate_key")
    p.set_defaults(func=cmd_generate_key)

    p = sub.add_parser("save_state")
    p.add_argument("key")
    p.add_argument("filename")
    p.add_argument("content")
    p.set_defaults(func=cmd_save_state)

    p = sub.add_parser("load_state")
    p.add_argument("key")
    p.add_argument("filename")
    p.set_defaults(func=cmd_load_state)

    p = sub.add_parser("list_state_files")
    p.add_argument("key")
    p.set_defaults(func=cmd_list_state_files)

    p = sub.add_parser("commit_all")
    p.add_argument("message", nargs="?", default="end of turn")
    p.set_defaults(func=cmd_commit_all)

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
