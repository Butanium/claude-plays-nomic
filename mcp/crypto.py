"""Shared encryption primitives for Nomic MCP servers.

Uses AES-256-CBC with PKCS7 padding. Each line is encrypted independently
with its own random IV and salt. Key derivation via PBKDF2-HMAC-SHA256.
"""

from __future__ import annotations

import base64
import hashlib
import os
from pathlib import Path

from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

PBKDF2_ITERATIONS = 100_000


def derive_aes_key(password: str, salt: bytes) -> bytes:
    """Derive a 256-bit AES key from a password and salt using PBKDF2."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=PBKDF2_ITERATIONS,
    )
    return kdf.derive(password.encode())


def encrypt_line(plaintext: str, password: str) -> str:
    """Encrypt a single line, returning 'ENC:base64(ct):base64(iv):base64(salt)'."""
    salt = os.urandom(16)
    iv = os.urandom(16)
    aes_key = derive_aes_key(password, salt)

    padder = padding.PKCS7(128).padder()
    padded = padder.update(plaintext.encode()) + padder.finalize()

    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded) + encryptor.finalize()

    ct_b64 = base64.b64encode(ciphertext).decode()
    iv_b64 = base64.b64encode(iv).decode()
    salt_b64 = base64.b64encode(salt).decode()
    return f"ENC:{ct_b64}:{iv_b64}:{salt_b64}"


def decrypt_line(encrypted: str, password: str) -> str:
    """Decrypt a single 'ENC:ct:iv:salt' line back to plaintext.

    Raises on wrong key (PKCS7 unpadding fails) or malformed input.
    """
    parts = encrypted.split(":")
    assert len(parts) == 4 and parts[0] == "ENC", f"Malformed encrypted line: {encrypted[:50]}"

    ciphertext = base64.b64decode(parts[1])
    iv = base64.b64decode(parts[2])
    salt = base64.b64decode(parts[3])

    aes_key = derive_aes_key(password, salt)

    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded) + unpadder.finalize()
    return plaintext.decode()


def compute_delete_key(path: Path) -> str:
    """Compute a delete_key from file content: sha256(file_bytes)[:16] hex."""
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def format_cat_n(lines: list[str]) -> str:
    """Format lines as cat -n output (1-indexed, right-aligned line numbers, tab separator)."""
    width = max(len(str(len(lines))), 6)
    return "\n".join(f"{i + 1:>{width}}\t{line}" for i, line in enumerate(lines))


def validate_filename(filename: str) -> None:
    """Assert that a filename is safe (no path traversal, no hidden files)."""
    assert filename, "Filename must not be empty"
    assert "/" not in filename and "\\" not in filename, "Filename must not contain path separators"
    assert not filename.startswith("."), "Filename must not start with '.'"


def resolve_storage_dir(key: str, base: Path) -> Path:
    """Derive a storage directory from a key: base / sha256(key)[:16]."""
    h = hashlib.sha256(key.encode()).hexdigest()[:16]
    d = base / h
    d.mkdir(parents=True, exist_ok=True)
    return d


def resolve_note_path(key: str, filename: str, base: Path) -> Path:
    """Resolve an encrypted note file path: base/<hash>/encrypted/<filename>."""
    validate_filename(filename)
    d = resolve_storage_dir(key, base) / "encrypted"
    d.mkdir(exist_ok=True)
    return d / filename


def resolve_file_path(key: str, filename: str, base: Path) -> Path:
    """Resolve a plaintext file path: base/<hash>/files/<filename>."""
    validate_filename(filename)
    d = resolve_storage_dir(key, base) / "files"
    d.mkdir(exist_ok=True)
    return d / filename


def read_encrypted_lines(path: Path) -> list[str]:
    """Read an encrypted file and return its lines."""
    return path.read_text().strip().split("\n")


def write_encrypted_lines(path: Path, lines: list[str]) -> None:
    """Write encrypted lines to a file."""
    path.write_text("\n".join(lines) + "\n")
