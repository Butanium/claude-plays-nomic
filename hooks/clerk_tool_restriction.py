#!/usr/bin/env python3
"""PreToolUse hook: restrict Clerk agent from player MCP tools.

Scoped to the Clerk agent via their agent definition (.claude/agents/clerk.md).

The Clerk can use Bash, but ONLY to call the clerk CLI
(uv run python mcp/clerk_cli.py ...). Shell injection prevention uses
the same shlex-based quote-aware scanner as the player hook.
"""

import json
import shlex
import sys

DENIED_TOOLS = {
    "AskUserQuestion",
}

DENIED_MCP_PREFIX = "mcp__nomic-crypto__"

CLI_TOKENS_PREFIX = ["uv", "run", "python", "mcp/clerk_cli.py"]

# Shell metacharacters dangerous outside any quoting context.
UNQUOTED_DANGEROUS = set(";|&`$><()\n\r")

# Dangerous even inside double quotes (command substitution still works).
DQUOTE_DANGEROUS = set("`$")


def check_shell_metacharacters(text: str) -> str | None:
    """Scan for shell metacharacters outside single-quote contexts.

    Returns None if safe, or a denial reason string.
    """
    in_single = False
    in_double = False
    i = 0
    while i < len(text):
        c = text[i]
        if in_single:
            if c == "'":
                in_single = False
        elif in_double:
            if c == '"':
                in_double = False
            elif c == "\\":
                i += 1  # skip escaped char
            elif c in DQUOTE_DANGEROUS:
                return (
                    f"'{c}' is not allowed in double quotes "
                    "(use single quotes for content with special characters)"
                )
        else:
            if c == "'":
                in_single = True
            elif c == '"':
                in_double = True
            elif c in UNQUOTED_DANGEROUS:
                return f"Unquoted shell metacharacter '{repr(c)}'"
        i += 1
    if in_single or in_double:
        return "Unmatched quote in command"
    return None


def validate_bash_command(command: str) -> str | None:
    """Return None if the Bash command is allowed, or a denial reason."""
    stripped = command.strip()

    try:
        tokens = shlex.split(stripped, posix=False)
    except ValueError as e:
        return f"Malformed command: {e}"

    if len(tokens) < 4 or tokens[:4] != CLI_TOKENS_PREFIX:
        return (
            "The Clerk can only use Bash to call: "
            "uv run python mcp/clerk_cli.py <command> [args...]"
        )

    prefix_str = "uv run python mcp/clerk_cli.py"
    args_start = stripped.index(prefix_str) + len(prefix_str)
    return check_shell_metacharacters(stripped[args_start:])


def main():
    input_data = json.load(sys.stdin)
    tool_name = input_data.get("tool_name", "")

    reason = None

    if tool_name in DENIED_TOOLS:
        reason = f"The Clerk cannot use {tool_name}."
    elif tool_name.startswith(DENIED_MCP_PREFIX):
        reason = f"The Clerk cannot use player MCP tools ({tool_name})."
    elif tool_name == "Bash":
        tool_input = input_data.get("tool_input", {})
        command = tool_input.get("command", "")
        reason = validate_bash_command(command)
        if reason is None:
            sys.exit(0)
    else:
        sys.exit(0)

    if reason:
        output = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": reason,
            }
        }
        print(json.dumps(output))

    sys.exit(0)


if __name__ == "__main__":
    main()
