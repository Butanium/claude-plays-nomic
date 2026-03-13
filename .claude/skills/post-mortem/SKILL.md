---
name: post-mortem
description: Find agent transcripts from a completed Nomic game
disable-model-invocation: true
---

# Post-Mortem: Locate Game Transcripts

Find the clerk and player agent transcripts from a completed Nomic game, copy
them to the project, and verify they look correct.

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

For each JSONL file, read the first line (JSON) to determine the agent type:
- `{"type": "agent-setting", "agentSetting": "clerk"}` → **Clerk**
- `{"type": "agent-setting", "agentSetting": "player"}` → **Player**
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

## Step 4: Verify transcripts

For each copied transcript, check:
1. **Event count** — use `read_agent_transcript` with defaults and note the
   total event count reported in the `[events X-Y of Z]` header.
2. **Last 5 messages** — use `read_agent_transcript` with `offset=-5` to read
   the final events. Confirm they look like a reasonable end of game (e.g.
   game-over announcement, final scores, post-mortem discussion) rather than a
   mid-conversation cutoff.

Report a summary table to the user:

| Role | Name (Model) | Events | Last message summary |
|------|-------------|--------|---------------------|
| Clerk | ... | ... | ... |
| Player | ... | ... | ... |
| ... | ... | ... | ... |
