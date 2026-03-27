#!/usr/bin/env python3
"""CLI for Nomic Clerk tools.

Workaround for MCP servers not loading via --mcp-config with --agent.
The Clerk calls this via Bash; the clerk hook restricts Bash to only this script.

Usage:
    uv run python mcp/clerk_cli.py <command> [args...]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import clerk_ops


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    parser = argparse.ArgumentParser(
        description="Nomic Clerk tools CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("generate_key")
    p.set_defaults(func=lambda args: clerk_ops.generate_key())

    p = sub.add_parser("save_state")
    p.add_argument("key")
    p.add_argument("filename")
    p.add_argument("content")
    p.set_defaults(func=lambda args: clerk_ops.save_state(args.key, args.filename, args.content))

    p = sub.add_parser("load_state")
    p.add_argument("key")
    p.add_argument("filename")
    p.set_defaults(func=lambda args: clerk_ops.load_state(args.key, args.filename))

    p = sub.add_parser("list_state_files")
    p.add_argument("key")
    p.set_defaults(func=lambda args: clerk_ops.list_state_files(args.key))

    p = sub.add_parser("commit_all")
    p.add_argument("message", nargs="?", default="end of turn")
    p.set_defaults(func=lambda args: clerk_ops.commit_all(args.message))

    p = sub.add_parser("contact_supervisor")
    p.add_argument("message")
    p.set_defaults(func=lambda args: clerk_ops.contact_supervisor(args.message))

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    print(args.func(args))


if __name__ == "__main__":
    main()
