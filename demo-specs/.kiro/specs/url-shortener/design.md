# Design: URL Shortener CLI Tool

## Overview

A lightweight Python CLI tool that shortens URLs using SHA-256 hash truncation, stores mappings in an in-memory dictionary, and provides commands to shorten, resolve, and list URL mappings.

## Architecture

```
┌─────────────────────────────────────────┐
│              CLI Interface               │
│         (argparse / input loop)          │
├─────────────────────────────────────────┤
│            Core Logic Layer              │
│  ┌───────────┐  ┌──────────────────┐   │
│  │ Validator │  │ Code Generator   │   │
│  │ (urllib)  │  │ (hashlib SHA-256)│   │
│  └───────────┘  └──────────────────┘   │
├─────────────────────────────────────────┤
│           Storage Layer                  │
│     (Python dict: code → url)           │
└─────────────────────────────────────────┘
```

## Components

### 1. URL Validator

Validates input URLs using `urllib.parse`:
- Checks scheme is `http` or `https`
- Verifies netloc contains at least one dot (valid domain)
- Returns tuple of (is_valid: bool, error_message: str | None)

### 2. Short Code Generator

Generates deterministic 6-character codes:
- Computes SHA-256 hash of the full URL string
- Takes first 6 characters of the hex digest
- Maps to alphanumeric charset (0-9, a-z) via modulo

### 3. In-Memory Store

Simple dictionary-based storage:
- `_store: dict[str, str]` — maps short_code → original_url
- `_reverse: dict[str, str]` — maps original_url → short_code (for deduplication)
- No persistence; cleared on process exit

### 4. CLI Interface

Command-line interface using argparse subcommands:
- `shorten <url>` — validate and shorten a URL
- `resolve <code>` — look up original URL from short code
- `list` — display all current mappings

## Data Flow

1. User invokes `python url_shortener.py shorten https://example.com/page`
2. Validator checks URL format → passes
3. Generator computes SHA-256 → truncates to 6 chars → `"a1b2c3"`
4. Store saves mapping: `{"a1b2c3": "https://example.com/page"}`
5. CLI prints: `Short code: a1b2c3`

## Error Handling

| Error | Response |
|-------|----------|
| Invalid scheme | "Error: URL must use http:// or https:// scheme" |
| Missing domain | "Error: URL must contain a valid domain" |
| Unknown short code | "Error: Short code 'xyz123' not found" |
| No mappings | "No URL mappings stored in current session" |

## Dependencies

- Python 3.10+ (standard library only: `hashlib`, `urllib.parse`, `argparse`)
- pytest 8.3.4 (dev dependency for testing)
