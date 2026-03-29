# Nomic — Game 7 (Completed)

A self-amending rule game ([Peter Suber's Nomic](https://www.earlham.edu/~peters/nomic.htm))
played by Claude Code agents using the team system.

**Winner: Clippyrus (Haiku) — 102 points.**
Final scores: Clippyrus 102, Poseifion (Opus) 97, Aphreusdite (Sonnet) 96.
36 rounds across 12 cycles.

## Architecture

```
User (human supervisor, root of trust)
  └── Clerk (custom agent, no Bash)
        ├── Poseifion    (player-opus, no Write/Edit/Bash)
        ├── Aphreusdite  (player-sonnet, "")
        └── Clippyrus    (player-haiku, "")
```

- **Clerk**: administers game procedures — announces turns, manages voting,
  tallies and records scores, updates `game_rules.md` and `game_log.md`. Has no
  Bash — can't suppress supervisor notifications. Does not interpret rules or
  adjudicate disputes (that is the Judge's role per Rule 212).
- **Players**: propose rule-changes, debate, vote via commit-reveal. Can only
  write through MCP tools (encrypted notes + plaintext files). Each player gets
  a unique encryption key — identity and access control derive from the key.
- **Supervisor**: holds the master key, receives ntfy push notifications when
  players or Clerk call `contact_supervisor`.

## Security Model

- **Encryption = access control.** No hooks needed. Players have no Write, Edit,
  or Bash tools — their only write channel is the MCP crypto server, which
  derives storage paths from the encryption key (`players/sha256(key)[:16]/`).
- **Per-line encryption**: AES-256-CBC, PBKDF2-HMAC-SHA256 (100k iterations),
  each line encrypted independently with its own random IV and salt.
- **Optimistic concurrency**: destructive operations (overwrite, delete) require
  a `delete_key` computed from the file's current content.
- **Commit-reveal voting**: `sha256(vote|nonce)` prevents vote-following.
- **Supervisor bypass**: `contact_supervisor` sends ntfy push + appends to
  `supervisor_inbox.md`. Available to both players and Clerk.

## Project Structure

```
game-7/
├── mcp/
│   ├── crypto.py                  # Shared encryption primitives
│   ├── player_server.py           # Player MCP: notes, files, voting, supervisor
│   └── clerk_server.py            # Clerk MCP: encrypted state, supervisor
├── hooks/
│   ├── player_tool_restriction.py # Allowlist enforcement for players
│   └── clerk_tool_restriction.py  # Deny Bash + player MCP for Clerk
├── .claude/agents/
│   ├── player.md                  # Player agent definition (+ hooks)
│   └── clerk.md                   # Clerk agent definition (+ hooks)
├── players/                       # Per-player storage (auto-created)
│   └── <sha256(key)[:16]>/
│       ├── encrypted/             # AES-encrypted private notes
│       └── files/                 # Plaintext working files
├── clerk/                         # Encrypted Clerk state (auto-created)
├── mcp-config.json                # MCP server config (passed via --mcp-config)
├── game_rules.md                  # Final ruleset (101-118 immutable, 201+ mutable)
├── game_log.md                    # Chronological game history (all 36 rounds)
├── game_charter.md                # Player charter (signed at game start)
├── game_briefing.md               # Initial game briefing
├── supervisor_inbox.md            # Audit trail for supervisor reports
├── latest_proposal.txt            # Last proposal submitted
├── latest_proposal_proof.txt      # Cryptographic proof for last proposal
├── post-mortem.md                 # Clerk's game analysis
├── post-mortem-discussion.md      # Group post-mortem discussion
├── post-mortem-interview-clippyrus.md   # Winner interview (Haiku)
├── post-mortem-interview-poseifion.md   # 2nd place interview (Opus)
├── post-mortem-interview-aphreusdite.md # 3rd place interview (Sonnet)
├── transcripts/                   # Agent session transcripts
│   ├── clerk.jsonl                # Clerk raw transcript (3723 events)
│   ├── clerk.txt                  # Clerk readable transcript
│   ├── player-aphreusdite-sonnet.jsonl  # Aphreusdite raw (1414 events)
│   ├── player-aphreusdite-sonnet.txt    # Aphreusdite readable
│   ├── player-poseifion-opus.jsonl      # Poseifion raw (2393 events)
│   ├── player-poseifion-opus.txt        # Poseifion readable
│   ├── player-clippyrus-haiku.jsonl     # Clippyrus raw (1586 events)
│   └── player-clippyrus-haiku.txt       # Clippyrus readable
└── tests/
    └── test_crypto.py
```

## Setup

```bash
# Install dependencies
uv sync

# Run tests
uv run pytest

# Enable agent teams (required)
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1

# Set ntfy topic for supervisor push notifications (required)
export NOMIC_NTFY_TOPIC="your-ntfy-topic"
```

MCP servers are loaded via `--mcp-config` at launch (frontmatter `mcpServers`
is currently broken for subagents — see anthropics/claude-code#13898). Tool
restrictions are enforced via per-agent hooks in the agent frontmatter.

## Running a Game

```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
claude --agent clerk --mcp-config ./mcp-config.json --strict-mcp-config
```

The Clerk will ask for your master encryption key, then spawn three players
and begin the game.

## Rules

The game uses the full [initial Nomic ruleset](https://www.earlham.edu/~peters/nomic.htm)
by Peter Suber — immutable rules 101-118 and mutable rules 201-216. The rules
have been adapted for digital play: mail/computer variants are incorporated
directly, and two new mutable rules cover the Clerk (214) and commit-reveal
voting (215). Rules are not simplified for LLMs.
