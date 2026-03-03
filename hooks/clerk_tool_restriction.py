#!/usr/bin/env python3
"""PreToolUse hook: restrict Clerk agent from Bash and player MCP tools.

Scoped to the Clerk agent via their agent definition (.claude/agents/clerk.md).
"""

import json
import sys

DENIED_TOOLS = {
    "Bash",
    "AskUserQuestion",
}

DENIED_MCP_PREFIX = "mcp__nomic-crypto__"


def main():
    input_data = json.load(sys.stdin)
    tool_name = input_data.get("tool_name", "")

    reason = None

    if tool_name in DENIED_TOOLS:
        reason = f"The Clerk cannot use {tool_name}."

    if tool_name.startswith(DENIED_MCP_PREFIX):
        reason = f"The Clerk cannot use player MCP tools ({tool_name})."

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
