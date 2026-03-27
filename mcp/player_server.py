"""MCP server providing encrypted note storage, voting primitives, and supervisor contact for Nomic players.

Players have no Write/Edit/Bash tools. This server is their ONLY write channel.
Identity is derived from the encryption key: storage directory = sha256(key)[:16].
"""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

import player_ops

mcp = FastMCP("nomic-crypto")


# --- Note tools: read operations ---


@mcp.tool()
def load_note(key: str, filename: str) -> str:
    """Load and decrypt a note file.

    Returns content in cat -n format (line numbers starting at 1) plus a
    delete_key footer. The delete_key is required for overwrite_note and
    delete_note operations.
    """
    return player_ops.load_note(key, filename)


@mcp.tool()
def load_all_notes(key: str) -> str:
    """Load and decrypt all note files.

    Returns each file with a === filename === header, cat -n content,
    and per-file delete_key.
    """
    return player_ops.load_all_notes(key)


@mcp.tool()
def list_note_files(key: str) -> str:
    """List all encrypted note filenames for the player."""
    return player_ops.list_note_files(key)


# --- Note tools: create ---


@mcp.tool()
def write_note(key: str, filename: str, content: str) -> str:
    """Create a new note file with one or more lines.

    Fails if the file already exists — use overwrite_note to replace.
    Content is split on newlines; each line is encrypted independently.
    """
    return player_ops.write_note(key, filename, content)


# --- Note tools: modify existing ---


@mcp.tool()
def append_note(key: str, filename: str, content: str) -> str:
    """Append one or more lines to an existing note file.

    Fails if the file doesn't exist — use write_note to create.
    """
    return player_ops.append_note(key, filename, content)


@mcp.tool()
def edit_line(key: str, filename: str, line_number: int, content: str) -> str:
    """Replace a specific line (1-indexed) in a note file.

    Only the target line is re-encrypted; other lines are untouched.
    """
    return player_ops.edit_line(key, filename, line_number, content)


@mcp.tool()
def delete_line(key: str, filename: str, line_number: int) -> str:
    """Remove a specific line (1-indexed) from a note file.

    If this was the last line, the file is deleted.
    """
    return player_ops.delete_line(key, filename, line_number)


# --- Note tools: destructive (require delete_key) ---


@mcp.tool()
def overwrite_note(key: str, filename: str, content: str, delete_key: str) -> str:
    """Overwrite an existing note file entirely.

    Requires the delete_key from the most recent load_note / load_all_notes
    call. This ensures you have read the current content before overwriting
    (optimistic concurrency control).
    """
    return player_ops.overwrite_note(key, filename, content, delete_key)


@mcp.tool()
def delete_note(key: str, filename: str, delete_key: str) -> str:
    """Delete an entire note file.

    Requires the delete_key from the most recent load_note / load_all_notes
    call. This ensures you have read the current content before deleting.
    """
    return player_ops.delete_note(key, filename, delete_key)


# --- Plaintext file tools ---
# Players can read these with the native Read tool.
# These tools provide write/edit access to plaintext files in the player's directory.


@mcp.tool()
def list_files(key: str) -> str:
    """List plaintext files with their full paths (so you can Read them directly)."""
    return player_ops.list_files(key)


@mcp.tool()
def write_file(key: str, filename: str, content: str) -> str:
    """Create a new plaintext file. Fails if the file already exists.

    The file is stored in your player directory and can be read with the
    native Read tool. Use list_files to get the full path.
    """
    return player_ops.write_file(key, filename, content)


@mcp.tool()
def edit_file(key: str, filename: str, old_string: str, new_string: str) -> str:
    """Edit a plaintext file by replacing old_string with new_string.

    Works like Claude Code's Edit tool: old_string must appear exactly once
    in the file. The replacement is targeted — only the matched text changes.
    """
    return player_ops.edit_file(key, filename, old_string, new_string)


@mcp.tool()
def get_delete_key(key: str, filename: str) -> str:
    """Get the delete_key for a plaintext file.

    Required for overwrite_file and delete_file operations.
    Read the file first with the native Read tool, then call this
    to get the delete_key before overwriting or deleting.
    """
    return player_ops.get_delete_key(key, filename)


@mcp.tool()
def overwrite_file(key: str, filename: str, content: str, delete_key: str) -> str:
    """Overwrite a plaintext file entirely. Requires delete_key from get_delete_key."""
    return player_ops.overwrite_file(key, filename, content, delete_key)


@mcp.tool()
def delete_file(key: str, filename: str, delete_key: str) -> str:
    """Delete a plaintext file. Requires delete_key from get_delete_key."""
    return player_ops.delete_file(key, filename, delete_key)


# --- Game mechanics ---


@mcp.tool()
def roll_dice(key: str, dice: str = "1d6") -> str:
    """Roll dice in xdy format (e.g. '2d6', '3d12'). Results appended to game log.

    Returns individual results for each die. The player's identity hash is
    recorded for auditability. Each player may only roll once per turn — the
    Clerk enforces this.
    """
    return player_ops.roll_dice(key, dice)


# --- Proposal submission ---


@mcp.tool()
def propose(key: str, proposal: str) -> str:
    """Submit a rule-change proposal with cryptographic proof of authorship.

    Writes latest_proposal.txt (publicly readable) and latest_proposal_proof.txt
    (ties the proposal to your identity). The Clerk verifies authorship using
    verify_proposal before accepting.
    """
    return player_ops.propose(key, proposal)


@mcp.tool()
def verify_proposal(player_key: str) -> str:
    """Verify that latest_proposal.txt was submitted by the given player.

    Checks the cryptographic proof in latest_proposal_proof.txt against the
    player's key. Returns verification result.
    """
    return player_ops.verify_proposal(player_key)


# --- Crypto primitives for commit-reveal voting ---


@mcp.tool()
def commit(vote: str, nonce: str) -> str:
    """Create a commitment for a vote: returns a slug (e.g. 'bold-cave-duck').

    Use this during the commit phase of voting. Send the returned slug
    to the Clerk. Keep your vote and nonce secret until the reveal phase.
    """
    return player_ops.commit(vote, nonce)


@mcp.tool()
def verify(vote: str, nonce: str, commitment: str) -> str:
    """Verify a vote against a commitment (accepts slug or hex hash).

    Returns 'true' if sha256(vote|nonce) matches the commitment, 'false' otherwise.
    """
    return player_ops.verify(vote, nonce, commitment)


# --- Supervisor contact ---


@mcp.tool()
def contact_supervisor(message: str) -> str:
    """Send a message directly to the human supervisor, bypassing the Clerk.

    Use this to report suspected cheating, rule violations, or other concerns
    that you don't want to go through the Clerk. The message is:
    1. Sent as a push notification via ntfy (if configured)
    2. Appended to supervisor_inbox.md as a permanent audit trail
    """
    return player_ops.contact_supervisor(message)


if __name__ == "__main__":
    mcp.run()
