---
name: post-mortem
description: Find and analyze agent transcripts from a completed Nomic game
disable-model-invocation: true
---

# Post-Mortem: Locate & Analyze Game Transcripts

Run a post-mortem analysis of a completed Nomic game. This involves finding the
agent transcripts (clerk + players), identifying who played, and optionally
producing summaries or analyses.

## Step 1: Find transcripts

Agent transcripts are JSONL files stored in the Claude Code project directory:
```
~/.claude/projects/<project-path>/
```

where `<project-path>` is the working directory with `/` replaced by `-` and
leading `-`. For example:
```
/mnt/nw/home/c.dumas/claude-playground/nomic-game-1
→ ~/.claude/projects/-mnt-nw-home-c-dumas-claude-playground-nomic-game-1/
```

List all `.jsonl` files there. These are agent transcripts — each is a separate
agent session (clerk, players, or auxiliary sub-agents).

## Step 2: Identify agents

For each JSONL file, read the first line to determine the agent type:
- `{"type": "agent-setting", "agentSetting": "clerk"}` → **Clerk**
- `{"type": "agent-setting", "agentSetting": "player"}` → **Player** (but subagent_type may also say "player")
- Files starting with `{"type": "user"}` with large line counts are likely the main orchestrator or player sessions
- Files starting with `{"type": "progress"}` are auxiliary sub-agents (check-bash, explore, etc.)

To identify which player is which, use the `read_agent_transcript` MCP tool
(from transcript-reader) with `limit=5` on each candidate — the initial prompt
contains the player name and model.

## Step 3: Copy transcripts

Copy the identified transcripts into a `transcripts/` folder in the project
with descriptive names:
```
transcripts/
├── clerk.jsonl
├── player-<name>-<model>.jsonl
├── player-<name>-<model>.jsonl
└── player-<name>-<model>.jsonl
```

## Step 4: Analyze (if requested)

Use the `read_agent_transcript` MCP tool to explore transcripts. Useful
parameters:
- `limit` / `offset` for pagination (e.g. `offset=-20` for the last 20 events)
- `max_chars_per_tool=1000` to see more of each tool result
- `get_tool_call_output` with a 4-char tool ID to get full output of a specific call
- Write summaries to `output_file` to avoid blowing context

Things to look for:
- Key strategic decisions each player made
- Voting patterns and alliances
- Rule proposals and their outcomes
- How players used (or tried to exploit) the encryption/MCP system
- Communication patterns between players
