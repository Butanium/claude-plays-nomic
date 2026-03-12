#!/usr/bin/env python3
"""PreToolUse hook: restrict Clerk agent.

Configured in .claude/settings.json, skips non-clerk agents via agent_type check.

- Bash: only for clerk or player CLI (uv run python mcp/{clerk,player}_cli.py ...)
- Write/Edit: only for game_rules.md and game_log.md
- AskUserQuestion: denied
"""

import json
import shlex
import sys
from pathlib import Path

DENIED_TOOLS = {
    "AskUserQuestion",
}

ALLOWED_CLI_PREFIXES = [
    ["uv", "run", "python", "mcp/clerk_cli.py"],
    ["uv", "run", "python", "mcp/player_cli.py"],
]

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
ALLOWED_WRITE_FILES = {
    PROJECT_ROOT / "game_rules.md",
    PROJECT_ROOT / "game_log.md",
    PROJECT_ROOT / "post-mortem.md",
    PROJECT_ROOT / "post-mortem-discussion.md",
}

# Patterns for dynamic post-mortem filenames (e.g. post-mortem-interview-alice.md)
ALLOWED_WRITE_PREFIXES = [
    "post-mortem-interview-",
]

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
                return (
                    f"Unquoted shell metacharacter {repr(c)}. "
                    "Wrap arguments containing special characters in single quotes."
                )
        i += 1
    if in_single or in_double:
        return "Unmatched quote in command"
    return None


def validate_sleep_command(tokens: list[str]) -> str | None:
    """Return None if the command is a valid sleep call, or a denial reason."""
    if len(tokens) != 2:
        return "sleep requires exactly one argument (duration in seconds)"
    try:
        duration = float(tokens[1].strip("'\""))
        if duration <= 0 or duration > 900:
            return "sleep duration must be between 0 and 900 seconds (15 minutes)"
    except ValueError:
        return f"Invalid sleep duration: {tokens[1]}"
    return None


def validate_bash_command(command: str) -> str | None:
    """Return None if the Bash command is allowed, or a denial reason."""
    stripped = command.strip()

    try:
        tokens = shlex.split(stripped, posix=False)
    except ValueError as e:
        return f"Malformed command: {e}"

    # Allow sleep for timing/pacing
    if tokens and tokens[0] == "sleep":
        return validate_sleep_command(tokens)

    matched_prefix = None
    if len(tokens) >= 4:
        for prefix in ALLOWED_CLI_PREFIXES:
            if tokens[:4] == prefix:
                matched_prefix = " ".join(prefix)
                break
    if matched_prefix is None:
        return (
            "The Clerk can only use Bash to call: "
            "uv run python mcp/clerk_cli.py or mcp/player_cli.py <command> [args...] "
            "or sleep <seconds>"
        )

    args_start = stripped.index(matched_prefix) + len(matched_prefix)
    return check_shell_metacharacters(stripped[args_start:])


def validate_write_edit(tool_input: dict) -> str | None:
    """Return None if the Write/Edit target is allowed, or a denial reason."""
    file_path = Path(tool_input.get("file_path", "")).resolve()
    if file_path in ALLOWED_WRITE_FILES:
        return None
    if file_path.parent == PROJECT_ROOT:
        for prefix in ALLOWED_WRITE_PREFIXES:
            if file_path.name.startswith(prefix) and file_path.name.endswith(".md"):
                return None
    return (
        f"The Clerk can only Write/Edit game files and post-mortem files, "
        f"not '{file_path.name}'. Use save_state (MCP or CLI) for private Clerk data."
    )


def auto_allow(reason: str):
    """Print an auto-allow decision and exit."""
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
            "permissionDecisionReason": f"Auto-approved: {reason}",
        }
    }
    print(json.dumps(output))
    sys.exit(0)


def main():
    input_data = json.load(sys.stdin)
    agent_type = input_data.get("agent_type")
    if agent_type != "clerk":
        return

    tool_name = input_data.get("tool_name", "")

    reason = None

    if tool_name in DENIED_TOOLS:
        reason = (
            f"The Clerk cannot use {tool_name}. "
            "The Clerk is an automated game administrator and must not prompt the "
            "human supervisor interactively. Use contact_supervisor (MCP or CLI) "
            "to escalate issues asynchronously."
        )
    elif tool_name == "Bash":
        tool_input = input_data.get("tool_input", {})
        command = tool_input.get("command", "")
        reason = validate_bash_command(command)
    elif tool_name in ("Write", "Edit"):
        tool_input = input_data.get("tool_input", {})
        reason = validate_write_edit(tool_input)
    else:
        auto_allow("allowed tool for Clerk")
        return

    if reason is None:
        auto_allow(f"valid {tool_name} usage")
        return

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
