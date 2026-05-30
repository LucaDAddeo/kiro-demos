"""URL Shortener CLI Tool

A lightweight CLI tool that shortens URLs using SHA-256 hash truncation,
stores mappings in an in-memory dictionary, and provides commands to
shorten, resolve, and list URL mappings.

Generated following the Kiro spec-driven development workflow.
See .kiro/specs/url-shortener/ for the full spec artifacts.
"""

import argparse
import hashlib
import sys
from urllib.parse import urlparse


# Task 1.1: Implement URL validation
def validate_url(url: str) -> tuple[bool, str | None]:
    """Validate that a URL has a valid http/https scheme and domain.

    Args:
        url: The URL string to validate.

    Returns:
        A tuple of (is_valid, error_message). If valid, error_message is None.
    """
    parsed = urlparse(url)

    if parsed.scheme not in ("http", "https"):
        return False, "Error: URL must use http:// or https:// scheme"

    if not parsed.netloc or "." not in parsed.netloc:
        return False, "Error: URL must contain a valid domain"

    return True, None


# Task 1.2: Implement short code generation
def generate_short_code(url: str) -> str:
    """Generate a deterministic 6-character short code from a URL.

    Uses SHA-256 hash of the URL and takes the first 6 hex characters.

    Args:
        url: The URL to generate a short code for.

    Returns:
        A 6-character hexadecimal string.
    """
    hash_digest = hashlib.sha256(url.encode("utf-8")).hexdigest()
    return hash_digest[:6]


# Task 1.3: Implement in-memory storage
class URLStore:
    """In-memory URL storage using dictionaries.

    Stores short_code → original_url mappings and provides
    deduplication via a reverse lookup dictionary.
    """

    def __init__(self) -> None:
        self._store: dict[str, str] = {}
        self._reverse: dict[str, str] = {}

    def store(self, url: str, code: str) -> None:
        """Store a URL with its short code.

        Args:
            url: The original URL.
            code: The generated short code.
        """
        self._store[code] = url
        self._reverse[url] = code

    def resolve(self, code: str) -> str | None:
        """Resolve a short code to its original URL.

        Args:
            code: The short code to look up.

        Returns:
            The original URL, or None if not found.
        """
        return self._store.get(code)

    def list_all(self) -> dict[str, str]:
        """List all stored URL mappings.

        Returns:
            A dictionary of short_code → original_url mappings.
        """
        return dict(self._store)


# Task 1.4: Implement CLI interface
def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser with subcommands."""
    parser = argparse.ArgumentParser(
        prog="url_shortener",
        description="Shorten URLs using SHA-256 hash truncation",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # shorten subcommand
    shorten_parser = subparsers.add_parser("shorten", help="Shorten a URL")
    shorten_parser.add_argument("url", help="The URL to shorten")

    # resolve subcommand
    resolve_parser = subparsers.add_parser(
        "resolve", help="Resolve a short code to its original URL"
    )
    resolve_parser.add_argument("code", help="The short code to resolve")

    # list subcommand
    subparsers.add_parser("list", help="List all stored URL mappings")

    return parser


def main() -> None:
    """Main entry point for the URL shortener CLI."""
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    store = URLStore()

    if args.command == "shorten":
        is_valid, error = validate_url(args.url)
        if not is_valid:
            print(error)
            sys.exit(1)

        code = generate_short_code(args.url)
        store.store(args.url, code)
        print(f"Short code: {code}")

    elif args.command == "resolve":
        result = store.resolve(args.code)
        if result is None:
            print(f"Error: Short code '{args.code}' not found")
            sys.exit(1)
        print(f"Original URL: {result}")

    elif args.command == "list":
        mappings = store.list_all()
        if not mappings:
            print("No URL mappings stored in current session")
        else:
            for code, url in mappings.items():
                print(f"  {code} → {url}")


if __name__ == "__main__":
    main()
