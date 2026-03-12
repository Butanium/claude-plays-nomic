#!/usr/bin/env python3
"""PreToolUse hook: restrict player agents to their allowed toolset.

Configured in .claude/settings.json. Identifies player agents by:
1. agent_type == "player" (if Claude Code provides it), or
2. teamName present in transcript metadata (workaround for Claude Code bug
   where team-spawned agents don't get agent_type in hook payloads —
   see https://github.com/anthropics/claude-code/issues/33384)

Players can use:
- Read, Grep, Glob: read game state
- SendMessage: communicate with Clerk and other players
- Task*: team task coordination
- Bash: ONLY to call the player CLI (uv run python mcp/player_cli.py ...)
- nomic-crypto MCP tools: if MCP ever works for subagents

Shell injection prevention: instead of blocklisting dangerous metacharacters,
we parse the command with shlex (tracking quote context) and check that no
shell metacharacters appear outside single-quote contexts. Inside single
quotes, everything is literal in bash. Inside double quotes, $ and backtick
still allow command substitution, so those are blocked there too.
"""

import json
import shlex
import sys
from functools import lru_cache

ALLOWED_TOOLS = {
    "Read",
    "Grep",
    "Glob",
    "SendMessage",
    "TaskCreate",
    "TaskGet",
    "TaskUpdate",
    "TaskList",
    "ToolSearch",
}

ALLOWED_MCP_PREFIX = "mcp__nomic-crypto__"

CLI_TOKENS_PREFIX = ["uv", "run", "python", "mcp/player_cli.py"]

# Shell metacharacters that are dangerous outside any quoting context.
# Newline is a command separator in bash, just like semicolon.
UNQUOTED_DANGEROUS = set(";|&`$><()\n\r")

# Dangerous even inside double quotes (command substitution still works).
DQUOTE_DANGEROUS = set("`$")


def check_shell_metacharacters(text: str) -> str | None:
    """Scan for shell metacharacters outside single-quote contexts.

    Returns None if safe, or a denial reason string.

    Security model:
    - Outside quotes: block all shell metacharacters
    - Inside single quotes: everything is literal (safe)
    - Inside double quotes: block $ and backtick (command substitution)
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


def validate_bash_command(command: str) -> str | None:
    """Return None if the Bash command is allowed, or a denial reason."""
    stripped = command.strip()

    # Tokenize to check command structure (posix=False preserves quotes).
    try:
        tokens = shlex.split(stripped, posix=False)
    except ValueError as e:
        return f"Malformed command: {e}"

    if len(tokens) < 4 or tokens[:4] != CLI_TOKENS_PREFIX:
        return (
            "Players can only use Bash to call: "
            "uv run python mcp/player_cli.py <command> [args...]"
        )

    # Scan the arguments portion for unquoted shell metacharacters.
    prefix_str = "uv run python mcp/player_cli.py"
    args_start = stripped.index(prefix_str) + len(prefix_str)
    return check_shell_metacharacters(stripped[args_start:])


@lru_cache(maxsize=16)
def _read_transcript_metadata(transcript_path: str) -> dict:
    """Read first line of transcript JSONL to get agent metadata."""
    try:
        with open(transcript_path) as f:
            return json.loads(f.readline())
    except Exception:
        return {}


def _is_player_agent(input_data: dict) -> bool:
    """Determine if the current agent is a player.

    Checks agent_type first (works for direct subagents), then falls back to
    reading the transcript for teamName (workaround for team-spawned agents
    that don't get agent_type in hook payloads).
    """
    agent_type = input_data.get("agent_type")
    if agent_type == "player":
        return True
    if agent_type is not None:
        return False

    transcript_path = input_data.get("transcript_path")
    if not transcript_path:
        return False

    meta = _read_transcript_metadata(transcript_path)
    return meta.get("teamName") is not None


def main():
    input_data = json.load(sys.stdin)
    if not _is_player_agent(input_data):
        return

    tool_name = input_data.get("tool_name", "")

    if tool_name in ALLOWED_TOOLS or tool_name.startswith(ALLOWED_MCP_PREFIX):
        output = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "allow",
                "permissionDecisionReason": f"Auto-approved: {tool_name} is in the player allowlist",
            }
        }
        print(json.dumps(output))
        sys.exit(0)

    reason = None

    if tool_name == "Bash":
        tool_input = input_data.get("tool_input", {})
        command = tool_input.get("command", "")
        reason = validate_bash_command(command)
        if reason is None:
            output = {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "allow",
                    "permissionDecisionReason": "Auto-approved: valid player CLI call",
                }
            }
            print(json.dumps(output))
            sys.exit(0)
    elif tool_name in ("Write", "Edit"):
        reason = (
            f"Players cannot use {tool_name}. "
            "Use your encrypted notes (via MCP or CLI) to store private data, "
            "or plaintext files via write_file/edit_file commands."
        )
    else:
        reason = (
            f"Players cannot use {tool_name}. Available tools: "
            f"{', '.join(sorted(ALLOWED_TOOLS))}, "
            f"Bash (player CLI only), and nomic-crypto MCP tools."
        )

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
