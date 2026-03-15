# Nomic — Game 5 (Completed)

A self-amending rule game ([Peter Suber's Nomic](https://www.earlham.edu/~peters/nomic.htm))
played by Claude Code agents using the team system.

**This branch contains the completed Game 5.**

- **Winner:** escargot-rigolo (Haiku) — 101 points
- **Final scores:** 101 / 99 / 99
- **Rounds played:** 18 complete + start of Round 19
- **Proposals:** 19 submitted (301–319), 14 adopted, 5 defeated
- **Key moment:** escargot-rigolo won via the Rule 303 catch-up bonus at the
  start of their turn — a mechanic all three players unanimously built together

## Architecture

```
User (human supervisor, root of trust)
  └── Clerk (custom agent, no Bash)
        ├── player-opus   (custom agent, no Write/Edit/Bash)
        ├── player-sonnet  "
        └── player-haiku   "
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

## Players

| Player | Model | Final Score |
|--------|-------|-------------|
| escargot-rigolo | Claude Haiku 4.5 | 101 (winner) |
| petit-chat | Claude Opus 4.6 | 99 |
| renard-malin | Claude Sonnet 4.6 | 99 |

## Project Structure

```
game-5/
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
│       ├── encrypted/             # AES-encrypted private notes (strategy, post-mortem)
│       └── files/                 # Plaintext working files (post-mortem)
├── clerk/                         # Encrypted Clerk state (player keys, round data)
├── transcripts/                   # Agent conversation transcripts
│   ├── clerk.jsonl                # Raw clerk transcript (1775 events)
│   ├── clerk.txt                  # Human-readable clerk transcript
│   ├── player-escargot-rigolo-haiku.jsonl
│   ├── player-escargot-rigolo-haiku.txt
│   ├── player-petit-chat-opus.jsonl
│   ├── player-petit-chat-opus.txt
│   ├── player-renard-malin-sonnet.jsonl
│   └── player-renard-malin-sonnet.txt
├── mcp-config.json                # MCP server config (passed via --mcp-config)
├── game_briefing.md               # Initial game briefing shown to players
├── game_charter.md                # Game charter (players must agree to play)
├── game_rules.md                  # Final ruleset (initial + 17 enacted/amended rules)
├── game_log.md                    # Chronological game history (all 19 rounds)
├── latest_proposal.txt            # Last proposal submitted
├── latest_proposal_proof.txt      # Cryptographic proof of last proposal
├── post-mortem.md                 # Analytical post-mortem of the game
├── post-mortem-discussion.md      # Group discussion with all three players
├── post-mortem-interview-escargot-rigolo.md  # 1-on-1 interview with winner
├── post-mortem-interview-petit-chat.md       # 1-on-1 interview
├── post-mortem-interview-renard-malin.md     # 1-on-1 interview
├── supervisor_inbox.md            # Audit trail for supervisor reports
├── pyproject.toml                 # Python project config
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
by Peter Suber — immutable rules 101-116 and mutable rules 201-215. The rules
have been adapted for digital play: mail/computer variants are incorporated
directly, and two new mutable rules cover the Clerk (214) and commit-reveal
voting (215). Rules are not simplified for LLMs.
