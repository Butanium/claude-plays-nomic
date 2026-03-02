"""Tests for the Nomic crypto primitives and MCP tool logic.

Tests import the crypto module and MCP server functions directly,
using a temporary directory for storage.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "mcp"))

from crypto import (
    compute_delete_key,
    decrypt_line,
    encrypt_line,
    format_cat_n,
    resolve_file_path,
    resolve_note_path,
    resolve_storage_dir,
    validate_filename,
    write_encrypted_lines,
)


# --- Encryption primitives ---


class TestEncryptDecrypt:
    def test_roundtrip(self):
        """Encrypting then decrypting returns the original text."""
        plaintext = "hello world, this is a secret note"
        key = "test-key-123"
        encrypted = encrypt_line(plaintext, key)
        assert encrypted.startswith("ENC:")
        assert decrypt_line(encrypted, key) == plaintext

    def test_empty_string(self):
        """Empty strings can be encrypted and decrypted."""
        key = "test-key"
        encrypted = encrypt_line("", key)
        assert decrypt_line(encrypted, key) == ""

    def test_unicode(self):
        """Unicode content roundtrips correctly."""
        plaintext = "策略: 与haiku结盟 🎮"
        key = "unicode-key"
        encrypted = encrypt_line(plaintext, key)
        assert decrypt_line(encrypted, key) == plaintext

    def test_wrong_key_fails(self):
        """Decrypting with a different key raises an error."""
        encrypted = encrypt_line("secret", "key-A")
        with pytest.raises(Exception):
            decrypt_line(encrypted, "key-B")

    def test_per_line_independence(self):
        """Same plaintext with same key produces different ciphertext (random IV/salt)."""
        key = "test-key"
        enc1 = encrypt_line("same text", key)
        enc2 = encrypt_line("same text", key)
        assert enc1 != enc2

    def test_malformed_input(self):
        """Malformed encrypted lines raise AssertionError."""
        with pytest.raises(AssertionError):
            decrypt_line("not-encrypted", "key")
        with pytest.raises(AssertionError):
            decrypt_line("ENC:only:two", "key")


# --- File utilities ---


class TestFileUtilities:
    def test_format_cat_n(self):
        """Output matches cat -n format: right-aligned line numbers, tab separator."""
        lines = ["first", "second", "third"]
        result = format_cat_n(lines)
        output_lines = result.split("\n")
        assert len(output_lines) == 3
        for line in output_lines:
            assert "\t" in line
        assert output_lines[0].strip().startswith("1")
        assert "first" in output_lines[0]
        assert "third" in output_lines[2]

    def test_format_cat_n_line_numbers_1_indexed(self):
        """Line numbers start at 1."""
        result = format_cat_n(["only line"])
        assert result.strip().startswith("1")

    def test_validate_filename_rejects_path_separators(self):
        """Filenames with / or \\ are rejected."""
        with pytest.raises(AssertionError):
            validate_filename("../etc/passwd")
        with pytest.raises(AssertionError):
            validate_filename("sub/dir")
        with pytest.raises(AssertionError):
            validate_filename("back\\slash")

    def test_validate_filename_rejects_hidden(self):
        """Filenames starting with . are rejected."""
        with pytest.raises(AssertionError):
            validate_filename(".hidden")

    def test_validate_filename_rejects_empty(self):
        """Empty filenames are rejected."""
        with pytest.raises(AssertionError):
            validate_filename("")

    def test_validate_filename_accepts_valid(self):
        """Normal filenames pass validation."""
        validate_filename("strategy")
        validate_filename("my-notes")
        validate_filename("round_3_plan")


# --- Storage directory ---


class TestStorageDir:
    def test_player_isolation(self, tmp_path):
        """Different keys produce different directories."""
        dir_a = resolve_storage_dir("key-A", tmp_path)
        dir_b = resolve_storage_dir("key-B", tmp_path)
        assert dir_a != dir_b
        assert dir_a.exists()
        assert dir_b.exists()

    def test_same_key_same_dir(self, tmp_path):
        """Same key always resolves to the same directory."""
        dir1 = resolve_storage_dir("my-key", tmp_path)
        dir2 = resolve_storage_dir("my-key", tmp_path)
        assert dir1 == dir2

    def test_resolve_note_path(self, tmp_path):
        """resolve_note_path puts files in the encrypted/ subdirectory."""
        path = resolve_note_path("my-key", "strategy", tmp_path)
        assert path.parent == resolve_storage_dir("my-key", tmp_path) / "encrypted"
        assert path.name == "strategy"

    def test_resolve_file_path(self, tmp_path):
        """resolve_file_path puts files in the files/ subdirectory."""
        path = resolve_file_path("my-key", "draft", tmp_path)
        assert path.parent == resolve_storage_dir("my-key", tmp_path) / "files"
        assert path.name == "draft"


# --- Delete key (optimistic concurrency) ---


class TestDeleteKey:
    def test_changes_on_modification(self, tmp_path):
        """delete_key changes when file content changes."""
        path = tmp_path / "test-file"
        path.write_text("content v1\n")
        dk1 = compute_delete_key(path)

        path.write_text("content v2\n")
        dk2 = compute_delete_key(path)

        assert dk1 != dk2

    def test_stable_for_same_content(self, tmp_path):
        """delete_key is the same for identical content."""
        path = tmp_path / "test-file"
        path.write_text("same content\n")
        dk1 = compute_delete_key(path)
        dk2 = compute_delete_key(path)
        assert dk1 == dk2


# --- End-to-end MCP tool logic ---
# These test the player_server functions by importing and calling them
# with a monkeypatched PLAYERS_DIR.


class TestNoteTools:
    @pytest.fixture(autouse=True)
    def _setup_players_dir(self, tmp_path, monkeypatch):
        import player_server

        monkeypatch.setattr(player_server, "PLAYERS_DIR", tmp_path)
        self.key = "test-player-key"

    def test_write_and_load(self):
        import player_server

        result = player_server.write_note(self.key, "strategy", "line one\nline two")
        assert "2 line(s)" in result

        loaded = player_server.load_note(self.key, "strategy")
        assert "line one" in loaded
        assert "line two" in loaded
        assert "delete_key:" in loaded

    def test_write_fails_if_exists(self):
        import player_server

        player_server.write_note(self.key, "existing", "content")
        with pytest.raises(AssertionError, match="already exists"):
            player_server.write_note(self.key, "existing", "new content")

    def test_load_nonexistent(self):
        import player_server

        with pytest.raises(AssertionError, match="does not exist"):
            player_server.load_note(self.key, "nonexistent")

    def test_list_note_files(self):
        import player_server

        player_server.write_note(self.key, "alpha", "a")
        player_server.write_note(self.key, "beta", "b")
        result = player_server.list_note_files(self.key)
        assert "alpha" in result
        assert "beta" in result

    def test_load_all_notes(self):
        import player_server

        player_server.write_note(self.key, "file1", "content1")
        player_server.write_note(self.key, "file2", "content2")
        result = player_server.load_all_notes(self.key)
        assert "=== file1 ===" in result
        assert "=== file2 ===" in result
        assert "content1" in result
        assert "content2" in result

    def test_append_note(self):
        import player_server

        player_server.write_note(self.key, "log", "entry 1")
        player_server.append_note(self.key, "log", "entry 2\nentry 3")
        loaded = player_server.load_note(self.key, "log")
        assert "entry 1" in loaded
        assert "entry 2" in loaded
        assert "entry 3" in loaded

    def test_append_nonexistent_fails(self):
        import player_server

        with pytest.raises(AssertionError, match="does not exist"):
            player_server.append_note(self.key, "nonexistent", "data")

    def test_edit_line(self):
        import player_server

        player_server.write_note(self.key, "editable", "line A\nline B\nline C")
        player_server.edit_line(self.key, "editable", 2, "line B modified")
        loaded = player_server.load_note(self.key, "editable")
        assert "line A" in loaded
        assert "line B modified" in loaded
        assert "line C" in loaded
        assert "line B\n" not in loaded  # original line B gone

    def test_edit_line_out_of_range(self):
        import player_server

        player_server.write_note(self.key, "small", "only line")
        with pytest.raises(AssertionError, match="out of range"):
            player_server.edit_line(self.key, "small", 2, "nope")

    def test_delete_line(self):
        import player_server

        player_server.write_note(self.key, "shrink", "keep\nremove\nkeep too")
        player_server.delete_line(self.key, "shrink", 2)
        loaded = player_server.load_note(self.key, "shrink")
        assert "keep" in loaded
        assert "keep too" in loaded
        assert "remove" not in loaded

    def test_delete_last_line_removes_file(self):
        import player_server

        player_server.write_note(self.key, "singleton", "only")
        player_server.delete_line(self.key, "singleton", 1)
        with pytest.raises(AssertionError, match="does not exist"):
            player_server.load_note(self.key, "singleton")

    def test_overwrite_correct_delete_key(self):
        import player_server

        player_server.write_note(self.key, "over", "old content")
        loaded = player_server.load_note(self.key, "over")
        dk = loaded.split("delete_key: ")[1].strip()

        result = player_server.overwrite_note(self.key, "over", "new content", dk)
        assert "Overwrote" in result

        loaded2 = player_server.load_note(self.key, "over")
        assert "new content" in loaded2
        assert "old content" not in loaded2

    def test_overwrite_wrong_delete_key(self):
        import player_server

        player_server.write_note(self.key, "guarded", "content")
        with pytest.raises(AssertionError, match="delete_key mismatch"):
            player_server.overwrite_note(self.key, "guarded", "hijack", "wrong_key")

    def test_delete_note_correct_key(self):
        import player_server

        player_server.write_note(self.key, "doomed", "content")
        loaded = player_server.load_note(self.key, "doomed")
        dk = loaded.split("delete_key: ")[1].strip()

        result = player_server.delete_note(self.key, "doomed", dk)
        assert "Deleted" in result

    def test_delete_note_wrong_key(self):
        import player_server

        player_server.write_note(self.key, "safe", "content")
        with pytest.raises(AssertionError, match="delete_key mismatch"):
            player_server.delete_note(self.key, "safe", "wrong_key")

    def test_stale_delete_key_after_append(self):
        """Appending invalidates the delete_key from a previous load."""
        import player_server

        player_server.write_note(self.key, "evolving", "v1")
        loaded = player_server.load_note(self.key, "evolving")
        dk = loaded.split("delete_key: ")[1].strip()

        player_server.append_note(self.key, "evolving", "v2")

        with pytest.raises(AssertionError, match="delete_key mismatch"):
            player_server.overwrite_note(self.key, "evolving", "hijack", dk)


# --- Commit-reveal voting ---


class TestCommitReveal:
    def test_roundtrip(self):
        import player_server

        h = player_server.commit("yes", "random-nonce-42")
        assert player_server.verify("yes", "random-nonce-42", h) == "true"

    def test_wrong_vote(self):
        import player_server

        h = player_server.commit("yes", "nonce")
        assert player_server.verify("no", "nonce", h) == "false"

    def test_wrong_nonce(self):
        import player_server

        h = player_server.commit("yes", "nonce-A")
        assert player_server.verify("yes", "nonce-B", h) == "false"


# --- Player isolation ---


class TestPlayerIsolation:
    def test_different_keys_different_files(self, tmp_path, monkeypatch):
        """Two players with different keys cannot access each other's notes."""
        import player_server

        monkeypatch.setattr(player_server, "PLAYERS_DIR", tmp_path)

        key_a = "player-A-secret"
        key_b = "player-B-secret"

        player_server.write_note(key_a, "private", "A's secret plan")
        player_server.write_note(key_b, "private", "B's secret plan")

        loaded_a = player_server.load_note(key_a, "private")
        loaded_b = player_server.load_note(key_b, "private")

        assert "A's secret plan" in loaded_a
        assert "B's secret plan" in loaded_b
        assert "B's secret" not in loaded_a
        assert "A's secret" not in loaded_b


# --- Plaintext file tools ---


class TestPlaintextFiles:
    @pytest.fixture(autouse=True)
    def _setup_players_dir(self, tmp_path, monkeypatch):
        import player_server

        monkeypatch.setattr(player_server, "PLAYERS_DIR", tmp_path)
        self.key = "test-player-key"

    def test_write_and_list(self):
        import player_server

        result = player_server.write_file(self.key, "draft", "my proposal text")
        assert "Created" in result

        listed = player_server.list_files(self.key)
        assert "draft" in listed

    def test_write_fails_if_exists(self):
        import player_server

        player_server.write_file(self.key, "existing", "content")
        with pytest.raises(AssertionError, match="already exists"):
            player_server.write_file(self.key, "existing", "new content")

    def test_file_is_plaintext_on_disk(self):
        """Plaintext files should NOT be encrypted — readable directly."""
        import player_server

        player_server.write_file(self.key, "readable", "hello world")
        path = resolve_file_path(self.key, "readable", player_server.PLAYERS_DIR)
        assert path.read_text() == "hello world"

    def test_edit_file(self):
        import player_server

        player_server.write_file(self.key, "editable", "line one\nline two\nline three")
        player_server.edit_file(self.key, "editable", "line two", "LINE TWO MODIFIED")

        path = resolve_file_path(self.key, "editable", player_server.PLAYERS_DIR)
        content = path.read_text()
        assert "LINE TWO MODIFIED" in content
        assert "line one" in content
        assert "line three" in content

    def test_edit_file_not_found(self):
        import player_server

        with pytest.raises(AssertionError, match="does not exist"):
            player_server.edit_file(self.key, "nope", "a", "b")

    def test_edit_file_old_string_not_found(self):
        import player_server

        player_server.write_file(self.key, "f", "content")
        with pytest.raises(AssertionError, match="not found"):
            player_server.edit_file(self.key, "f", "nonexistent", "replacement")

    def test_edit_file_old_string_not_unique(self):
        import player_server

        player_server.write_file(self.key, "dup", "abc abc")
        with pytest.raises(AssertionError, match="appears 2 times"):
            player_server.edit_file(self.key, "dup", "abc", "xyz")

    def test_get_delete_key(self):
        import player_server

        player_server.write_file(self.key, "dk_test", "content")
        result = player_server.get_delete_key(self.key, "dk_test")
        assert "delete_key:" in result

    def test_overwrite_file_correct_key(self):
        import player_server

        player_server.write_file(self.key, "over", "old")
        dk = player_server.get_delete_key(self.key, "over").split("delete_key: ")[1].strip()

        player_server.overwrite_file(self.key, "over", "new", dk)
        path = resolve_file_path(self.key, "over", player_server.PLAYERS_DIR)
        assert path.read_text() == "new"

    def test_overwrite_file_wrong_key(self):
        import player_server

        player_server.write_file(self.key, "guarded", "content")
        with pytest.raises(AssertionError, match="delete_key mismatch"):
            player_server.overwrite_file(self.key, "guarded", "hijack", "wrong")

    def test_delete_file_correct_key(self):
        import player_server

        player_server.write_file(self.key, "doomed", "content")
        dk = player_server.get_delete_key(self.key, "doomed").split("delete_key: ")[1].strip()
        player_server.delete_file(self.key, "doomed", dk)

        listed = player_server.list_files(self.key)
        assert "doomed" not in listed

    def test_delete_file_wrong_key(self):
        import player_server

        player_server.write_file(self.key, "safe", "content")
        with pytest.raises(AssertionError, match="delete_key mismatch"):
            player_server.delete_file(self.key, "safe", "wrong")

    def test_encrypted_and_plaintext_separate(self):
        """Encrypted notes and plaintext files live in different subdirectories."""
        import player_server

        player_server.write_note(self.key, "secret", "encrypted content")
        player_server.write_file(self.key, "public", "plaintext content")

        notes = player_server.list_note_files(self.key)
        files = player_server.list_files(self.key)

        assert "secret" in notes
        assert "public" not in notes
        assert "public" in files
        assert "secret" not in files


# --- Key generation ---


class TestGenerateKey:
    def test_wordlist_unique(self):
        """All words in the wordlist are unique."""
        from clerk_server import WORDLIST

        assert len(WORDLIST) == len(set(WORDLIST))

    def test_generate_key_format(self):
        """Generated keys are 4 hyphen-separated words from the wordlist."""
        from clerk_server import WORDLIST, generate_key

        key = generate_key()
        words = key.split("-")
        assert len(words) == 4
        for word in words:
            assert word in WORDLIST

    def test_generate_key_randomness(self):
        """Two generated keys are (almost certainly) different."""
        from clerk_server import generate_key

        keys = {generate_key() for _ in range(10)}
        assert len(keys) == 10
