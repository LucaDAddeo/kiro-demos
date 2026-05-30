# Implementation Tasks: URL Shortener CLI Tool

## Tasks

- [ ] 1. Core implementation
  - [ ] 1.1 Implement URL validation
    - Create `src/url_shortener.py` with `validate_url(url: str) -> tuple[bool, str | None]`
    - Check scheme is http/https, verify domain has at least one dot
    - _Requirements: 1.1, 1.2, 1.3_

  - [ ] 1.2 Implement short code generation
    - Add `generate_short_code(url: str) -> str` using SHA-256 truncation
    - Take first 6 hex characters of the hash digest
    - _Requirements: 2.1, 2.2, 2.3_

  - [ ] 1.3 Implement in-memory storage
    - Add `URLStore` class with `store(url, code)`, `resolve(code)`, and `list_all()` methods
    - Use dict for code→url mapping and reverse dict for deduplication
    - _Requirements: 3.1, 3.2, 3.3_

  - [ ] 1.4 Implement CLI interface
    - Add argparse-based CLI with subcommands: shorten, resolve, list
    - Wire CLI to validator, generator, and store
    - _Requirements: 4.1, 4.2, 4.3_

- [ ] 2. Testing
  - [ ] 2.1 Write unit tests
    - Test URL validation (valid/invalid cases)
    - Test short code generation (determinism, length)
    - Test storage operations (store, resolve, list, not-found)
    - _Requirements: 1.1, 2.1, 3.1, 4.1_
