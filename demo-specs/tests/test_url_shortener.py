"""Tests for the URL shortener CLI tool.

Verifies that the generated code satisfies the spec:
- URL validation (scheme and domain checks)
- Short code generation (deterministic, 6-char hex)
- URLStore (store/resolve round-trip, list_all)
- CLI interface (--help, shorten, resolve)
"""

import subprocess
import sys
import os

# Add src directory to path so we can import the module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from url_shortener import validate_url, generate_short_code, URLStore

# Path to the url_shortener.py script for CLI tests
SCRIPT_PATH = os.path.join(os.path.dirname(__file__), "..", "src", "url_shortener.py")


# --- URL Validation Tests ---


class TestValidateUrl:
    """Test URL validation logic."""

    def test_valid_http_url(self):
        """Valid http URL returns (True, None)."""
        is_valid, error = validate_url("http://example.com")
        assert is_valid is True
        assert error is None

    def test_valid_https_url(self):
        """Valid https URL returns (True, None)."""
        is_valid, error = validate_url("https://example.com/path?q=1")
        assert is_valid is True
        assert error is None

    def test_invalid_scheme_ftp(self):
        """ftp:// scheme returns (False, error message)."""
        is_valid, error = validate_url("ftp://files.example.com/data.zip")
        assert is_valid is False
        assert error is not None
        assert "scheme" in error.lower() or "http" in error.lower()

    def test_missing_domain(self):
        """URL without domain returns (False, error message)."""
        is_valid, error = validate_url("http://")
        assert is_valid is False
        assert error is not None
        assert "domain" in error.lower()

    def test_domain_without_dot(self):
        """URL with domain lacking a dot returns (False, error message)."""
        is_valid, error = validate_url("http://localhost")
        assert is_valid is False
        assert error is not None
        assert "domain" in error.lower()


# --- Short Code Generation Tests ---


class TestGenerateShortCode:
    """Test short code generation logic."""

    def test_returns_six_characters(self):
        """Short code is exactly 6 characters long."""
        code = generate_short_code("https://example.com")
        assert len(code) == 6

    def test_deterministic(self):
        """Same URL always produces the same code."""
        url = "https://example.com/page"
        code1 = generate_short_code(url)
        code2 = generate_short_code(url)
        assert code1 == code2

    def test_different_urls_produce_different_codes(self):
        """Different URLs produce different codes."""
        code1 = generate_short_code("https://example.com/a")
        code2 = generate_short_code("https://example.com/b")
        assert code1 != code2

    def test_alphanumeric_hex(self):
        """Short code contains only hexadecimal characters (0-9, a-f)."""
        code = generate_short_code("https://example.com")
        assert all(c in "0123456789abcdef" for c in code)


# --- URLStore Tests ---


class TestURLStore:
    """Test in-memory URL storage."""

    def test_store_and_resolve_round_trip(self):
        """Storing a URL and resolving its code returns the original URL."""
        store = URLStore()
        store.store("https://example.com", "abc123")
        assert store.resolve("abc123") == "https://example.com"

    def test_resolve_unknown_code_returns_none(self):
        """Resolving an unknown code returns None."""
        store = URLStore()
        assert store.resolve("xxxxxx") is None

    def test_list_all_returns_all_mappings(self):
        """list_all() returns all stored mappings."""
        store = URLStore()
        store.store("https://a.com", "aaaaaa")
        store.store("https://b.com", "bbbbbb")
        mappings = store.list_all()
        assert mappings == {"aaaaaa": "https://a.com", "bbbbbb": "https://b.com"}

    def test_list_all_empty_when_nothing_stored(self):
        """list_all() returns empty dict when nothing stored."""
        store = URLStore()
        assert store.list_all() == {}


# --- CLI Interface Tests ---


class TestCLI:
    """Test CLI interface via subprocess."""

    def test_help_exits_zero(self):
        """--help flag exits with code 0."""
        result = subprocess.run(
            [sys.executable, SCRIPT_PATH, "--help"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "usage" in result.stdout.lower() or "shorten" in result.stdout.lower()

    def test_shorten_command_works(self):
        """shorten command with valid URL exits 0 and prints a short code."""
        result = subprocess.run(
            [sys.executable, SCRIPT_PATH, "shorten", "https://example.com"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "Short code:" in result.stdout

    def test_shorten_invalid_url_fails(self):
        """shorten command with invalid URL exits non-zero."""
        result = subprocess.run(
            [sys.executable, SCRIPT_PATH, "shorten", "ftp://bad.com/file"],
            capture_output=True,
            text=True,
        )
        assert result.returncode != 0

    def test_resolve_unknown_code_fails(self):
        """resolve command with unknown code exits non-zero."""
        result = subprocess.run(
            [sys.executable, SCRIPT_PATH, "resolve", "zzzzzz"],
            capture_output=True,
            text=True,
        )
        assert result.returncode != 0
        assert "not found" in result.stdout.lower()
