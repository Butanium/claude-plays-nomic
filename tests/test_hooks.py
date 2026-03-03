"""Tests for the player and clerk tool restriction hooks.

Tests the shell injection prevention (quote-aware metacharacter scanning)
and the tool allowlist/denylist logic.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "hooks"))

from player_tool_restriction import (
    check_shell_metacharacters,
    validate_bash_command,
)
from clerk_tool_restriction import (
    validate_bash_command as clerk_validate_bash_command,
    validate_write_edit as clerk_validate_write_edit,
)

CLI = "uv run python mcp/player_cli.py"


# --- check_shell_metacharacters ---


class TestShellMetacharacterScanner:
    """Tests for the quote-aware metacharacter scanner."""

    def test_clean_args(self):
        assert check_shell_metacharacters(" write_note key file content") is None

    def test_single_quoted_semicolon(self):
        assert check_shell_metacharacters(" write_note key file 'hello; world'") is None

    def test_single_quoted_pipe(self):
        assert check_shell_metacharacters(" write_note key file 'a | b'") is None

    def test_single_quoted_ampersand(self):
        assert check_shell_metacharacters(" write_note key file 'a && b'") is None

    def test_single_quoted_dollar(self):
        assert check_shell_metacharacters(" write_note key file '$HOME'") is None

    def test_single_quoted_backtick(self):
        assert check_shell_metacharacters(" write_note key file '`whoami`'") is None

    def test_single_quoted_parens(self):
        assert check_shell_metacharacters(" write_note key file '(subshell)'") is None

    def test_single_quoted_redirect(self):
        assert check_shell_metacharacters(" write_note key file '> /dev/null'") is None

    def test_double_quoted_semicolon(self):
        """Semicolon is literal inside double quotes — should be allowed."""
        assert check_shell_metacharacters(' write_note key file "hello; world"') is None

    def test_double_quoted_pipe(self):
        assert check_shell_metacharacters(' write_note key file "a | b"') is None

    def test_double_quoted_dollar_blocked(self):
        """$ inside double quotes allows command substitution — must block."""
        result = check_shell_metacharacters(' write_note key file "$HOME"')
        assert result is not None
        assert "$" in result

    def test_double_quoted_backtick_blocked(self):
        result = check_shell_metacharacters(' write_note key file "`whoami`"')
        assert result is not None
        assert "`" in result

    def test_double_quoted_escaped_dollar(self):
        """Backslash-escaped $ inside double quotes should be allowed."""
        assert check_shell_metacharacters(' write_note key file "price is \\$5"') is None

    def test_unquoted_semicolon(self):
        result = check_shell_metacharacters(" write_note key file content ; rm -rf /")
        assert result is not None

    def test_unquoted_pipe(self):
        result = check_shell_metacharacters(" write_note key file content | cat")
        assert result is not None

    def test_unquoted_ampersand(self):
        result = check_shell_metacharacters(" write_note key file content & bg")
        assert result is not None

    def test_unquoted_double_ampersand(self):
        result = check_shell_metacharacters(" commit yes nonce && rm -rf /")
        assert result is not None

    def test_unquoted_or(self):
        result = check_shell_metacharacters(" commit yes nonce || evil")
        assert result is not None

    def test_unquoted_backtick(self):
        result = check_shell_metacharacters(" write_note key file `whoami`")
        assert result is not None

    def test_unquoted_dollar_paren(self):
        result = check_shell_metacharacters(" write_note key file $(id)")
        assert result is not None

    def test_unquoted_redirect_out(self):
        result = check_shell_metacharacters(" roll_dice key > /tmp/leak")
        assert result is not None

    def test_unquoted_redirect_in(self):
        result = check_shell_metacharacters(" roll_dice key < /etc/passwd")
        assert result is not None

    def test_process_substitution(self):
        result = check_shell_metacharacters(" roll_dice key <(cat /etc/passwd)")
        assert result is not None

    def test_newline_injection(self):
        result = check_shell_metacharacters(" roll_dice key\nrm -rf /")
        assert result is not None

    def test_carriage_return(self):
        result = check_shell_metacharacters(" roll_dice key\rrm -rf /")
        assert result is not None

    def test_unquoted_subshell(self):
        result = check_shell_metacharacters(" roll_dice key (echo pwned)")
        assert result is not None

    def test_unmatched_single_quote(self):
        result = check_shell_metacharacters(" write_note key file 'unmatched")
        assert result is not None
        assert "Unmatched" in result

    def test_unmatched_double_quote(self):
        result = check_shell_metacharacters(' write_note key file "unmatched')
        assert result is not None
        assert "Unmatched" in result

    def test_empty_string(self):
        assert check_shell_metacharacters("") is None

    def test_mixed_quoting_styles(self):
        """Single-quoted dangerous chars followed by clean double-quoted text."""
        assert check_shell_metacharacters(""" write_note key file 'a;b' "clean" """) is None


# --- validate_bash_command ---


class TestValidateBashCommand:
    """Tests for the full Bash command validator (prefix + metacharacter check)."""

    def test_simple_cli_call(self):
        assert validate_bash_command(f"{CLI} commit yes nonce") is None

    def test_cli_with_single_quoted_content(self):
        assert validate_bash_command(f"{CLI} write_note key file 'hello; world'") is None

    def test_wrong_prefix(self):
        result = validate_bash_command("rm -rf /")
        assert result is not None

    def test_python_directly(self):
        result = validate_bash_command("python mcp/player_cli.py commit yes nonce")
        assert result is not None

    def test_different_script(self):
        result = validate_bash_command("uv run python mcp/evil.py commit yes nonce")
        assert result is not None

    def test_semicolon_after_cli(self):
        result = validate_bash_command(f"{CLI} roll_dice key ; rm -rf /")
        assert result is not None

    def test_newline_after_cli(self):
        result = validate_bash_command(f"{CLI} roll_dice key\nrm -rf /")
        assert result is not None

    def test_process_substitution_after_cli(self):
        result = validate_bash_command(f"{CLI} roll_dice key <(cat /etc/passwd)")
        assert result is not None

    def test_command_substitution_in_dquotes(self):
        result = validate_bash_command(f'{CLI} write_note key file "$(whoami)"')
        assert result is not None

    def test_backtick_in_dquotes(self):
        result = validate_bash_command(f'{CLI} write_note key file "`id`"')
        assert result is not None

    def test_leading_whitespace_stripped(self):
        assert validate_bash_command(f"  {CLI} commit yes nonce  ") is None

    def test_no_subcommand(self):
        """Just the prefix with no subcommand — allowed (CLI gives argparse error)."""
        assert validate_bash_command(CLI) is None

    def test_empty_command(self):
        result = validate_bash_command("")
        assert result is not None

    def test_pipe_chaining(self):
        result = validate_bash_command(f"{CLI} load_note key file | grep secret")
        assert result is not None

    def test_background_execution(self):
        result = validate_bash_command(f"{CLI} roll_dice key &")
        assert result is not None

    def test_double_ampersand_chaining(self):
        result = validate_bash_command(f"{CLI} roll_dice key && echo pwned")
        assert result is not None

    def test_or_chaining(self):
        result = validate_bash_command(f"{CLI} roll_dice key || echo fallback")
        assert result is not None

    def test_output_redirect(self):
        result = validate_bash_command(f"{CLI} load_all_notes key > /tmp/leak")
        assert result is not None

    def test_dollar_expansion_unquoted(self):
        result = validate_bash_command(f"{CLI} write_note $KEY file content")
        assert result is not None


# --- Clerk hook ---


CLERK_CLI = "uv run python mcp/clerk_cli.py"


class TestClerkValidateBashCommand:
    """Tests for the Clerk's Bash command validator."""

    def test_generate_key(self):
        assert clerk_validate_bash_command(f"{CLERK_CLI} generate_key") is None

    def test_save_state(self):
        assert clerk_validate_bash_command(
            f"{CLERK_CLI} save_state mykey players.md 'name1: key1'"
        ) is None

    def test_load_state(self):
        assert clerk_validate_bash_command(f"{CLERK_CLI} load_state mykey players.md") is None

    def test_list_state_files(self):
        assert clerk_validate_bash_command(f"{CLERK_CLI} list_state_files mykey") is None

    def test_contact_supervisor(self):
        assert clerk_validate_bash_command(
            f"{CLERK_CLI} contact_supervisor 'need help with rule dispute'"
        ) is None

    def test_wrong_prefix_denied(self):
        result = clerk_validate_bash_command("rm -rf /")
        assert result is not None

    def test_player_cli_allowed(self):
        """Clerk can call the player CLI (e.g. for vote verification)."""
        assert clerk_validate_bash_command(
            "uv run python mcp/player_cli.py verify yes nonce abc123"
        ) is None

    def test_semicolon_injection(self):
        result = clerk_validate_bash_command(f"{CLERK_CLI} generate_key ; rm -rf /")
        assert result is not None

    def test_newline_injection(self):
        result = clerk_validate_bash_command(f"{CLERK_CLI} generate_key\nrm -rf /")
        assert result is not None

    def test_process_substitution(self):
        result = clerk_validate_bash_command(f"{CLERK_CLI} load_state key <(evil)")
        assert result is not None

    def test_single_quoted_content_allowed(self):
        assert clerk_validate_bash_command(
            f"{CLERK_CLI} save_state mykey notes.md 'content with ; and | inside'"
        ) is None

    def test_dollar_in_dquotes_denied(self):
        result = clerk_validate_bash_command(
            f'{CLERK_CLI} save_state mykey notes.md "$(whoami)"'
        )
        assert result is not None


# --- Clerk Write/Edit restriction ---


PROJECT_ROOT = Path(__file__).parent.parent.resolve()


class TestClerkWriteEditRestriction:
    """Tests for the Clerk's Write/Edit file path restriction."""

    def test_game_rules_allowed(self):
        assert clerk_validate_write_edit(
            {"file_path": str(PROJECT_ROOT / "game_rules.md")}
        ) is None

    def test_game_log_allowed(self):
        assert clerk_validate_write_edit(
            {"file_path": str(PROJECT_ROOT / "game_log.md")}
        ) is None

    def test_supervisor_inbox_denied(self):
        result = clerk_validate_write_edit(
            {"file_path": str(PROJECT_ROOT / "supervisor_inbox.md")}
        )
        assert result is not None

    def test_player_file_denied(self):
        result = clerk_validate_write_edit(
            {"file_path": str(PROJECT_ROOT / "players" / "abc123" / "files" / "notes.md")}
        )
        assert result is not None

    def test_hook_script_denied(self):
        result = clerk_validate_write_edit(
            {"file_path": str(PROJECT_ROOT / "hooks" / "player_tool_restriction.py")}
        )
        assert result is not None

    def test_agent_definition_denied(self):
        result = clerk_validate_write_edit(
            {"file_path": str(PROJECT_ROOT / ".claude" / "agents" / "clerk.md")}
        )
        assert result is not None

    def test_arbitrary_file_denied(self):
        result = clerk_validate_write_edit(
            {"file_path": "/tmp/evil.txt"}
        )
        assert result is not None

    def test_path_traversal_denied(self):
        """game_rules.md via path traversal should resolve and be allowed."""
        result = clerk_validate_write_edit(
            {"file_path": str(PROJECT_ROOT / "hooks" / ".." / "game_rules.md")}
        )
        assert result is None

    def test_path_traversal_to_outside_denied(self):
        result = clerk_validate_write_edit(
            {"file_path": str(PROJECT_ROOT / ".." / "game_rules.md")}
        )
        assert result is not None

    def test_missing_file_path_denied(self):
        result = clerk_validate_write_edit({})
        assert result is not None
