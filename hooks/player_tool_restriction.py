#!/usr/bin/env python3
"""PreToolUse hook: restrict player agents to their allowed toolset.

Scoped to player agents via their agent definition (.claude/agents/player.md).
"""

import json
import sys

ALLOWED_TOOLS = {
    "Read",
    "Grep",
    "Glob",
    "SendMessage",
    "TaskCreate",
    "TaskGet",
    "TaskUpdate",
    "TaskList",
}

ALLOWED_MCP_PREFIX = "mcp__nomic-crypto__"


def main():
    input_data = json.load(sys.stdin)
    tool_name = input_data.get("tool_name", "")

    if tool_name in ALLOWED_TOOLS:
        sys.exit(0)

    if tool_name.startswith(ALLOWED_MCP_PREFIX):
        sys.exit(0)

    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": f"Players cannot use {tool_name}. Your available tools are: {', '.join(sorted(ALLOWED_TOOLS))} and nomic-crypto MCP tools.",
        }
    }
    print(json.dumps(output))
    sys.exit(0)


if __name__ == "__main__":
    main()
