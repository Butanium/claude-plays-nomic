"""MCP server for the Nomic Clerk: encrypted state storage and supervisor contact.

The Clerk uses Write/Edit directly for public game files (game_rules.md, game_log.md).
This server handles only encrypted Clerk state and supervisor escalation.
"""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

import clerk_ops

mcp = FastMCP("nomic-clerk")

WORDLIST = clerk_ops.WORDLIST


@mcp.tool()
def generate_key() -> str:
    """Generate a memorable key for a player.

    Returns a 4-word slug (e.g. 'amber-cliff-polar-trout') drawn from a
    256-word list, giving ~32 bits of entropy. The Clerk should distribute
    this to the player via their system prompt and never store it in plaintext.
    """
    return clerk_ops.generate_key()


@mcp.tool()
def save_state(key: str, filename: str, content: str) -> str:
    """Encrypt and save Clerk state. Overwrites if the file already exists.

    Content is split on newlines; each line is encrypted independently.
    """
    return clerk_ops.save_state(key, filename, content)


@mcp.tool()
def load_state(key: str, filename: str) -> str:
    """Decrypt and return Clerk state in cat -n format."""
    return clerk_ops.load_state(key, filename)


@mcp.tool()
def list_state_files(key: str) -> str:
    """List all Clerk state files."""
    return clerk_ops.list_state_files(key)


@mcp.tool()
def commit_all(
    message: str = "end of turn",
    scores: dict[str, int] = None,
    result: str = None,
    round_number: int | None = None,
    winner: str | list[str] | None = None,
) -> str:
    """Commit all changed files and log structured round data.

    Call this at the end of each round. Appends round data to game_state.yaml
    before committing.

    Args:
        message: Git commit message.
        scores: Current cumulative scores for ALL players. Required.
        result: Outcome of this round's proposal vote (e.g. "adopted", "defeated"). Required.
        round_number: Round number. If omitted, auto-increments from last round.
        winner: Player name(s) if someone won this round, or None.
    """
    return clerk_ops.commit_all(message, scores, result, round_number, winner)


@mcp.tool()
def contact_supervisor(message: str) -> str:
    """Send a message directly to the human supervisor.

    Use for rule disputes, ambiguous interpretations, or game-critical
    decisions that need human input. The message is sent as a push
    notification and appended to the audit trail.
    """
    return clerk_ops.contact_supervisor(message)


if __name__ == "__main__":
    mcp.run()
