# Requirements: URL Shortener CLI Tool

## Introduction

A local command-line URL shortener that validates URLs, generates short codes using hash-based algorithms, stores mappings in memory, and retrieves original URLs from short codes.

## Glossary

- **Short_Code**: A 6-character alphanumeric string derived from the URL hash
- **URL_Mapping**: An in-memory dictionary entry associating a Short_Code with its original URL
- **CLI_Interface**: The command-line interface accepting user commands (shorten, resolve, list)

## Requirements

### Requirement 1: URL Validation

**User Story:** As a user, I want the tool to validate URLs before shortening, so that only well-formed URLs are stored.

#### Acceptance Criteria

1. THE tool SHALL accept URLs with http:// or https:// schemes only.
2. THE tool SHALL reject URLs without a valid domain (must contain at least one dot after the scheme).
3. WHEN an invalid URL is provided, THE tool SHALL display an error message indicating the validation failure reason.

### Requirement 2: Short Code Generation

**User Story:** As a user, I want deterministic short codes generated from URLs, so that the same URL always produces the same short code.

#### Acceptance Criteria

1. THE tool SHALL generate a 6-character alphanumeric short code from the input URL.
2. THE tool SHALL use a hash-based algorithm (SHA-256 truncated) to derive the short code.
3. WHEN the same URL is shortened multiple times, THE tool SHALL return the same short code.

### Requirement 3: In-Memory Storage

**User Story:** As a user, I want URL mappings stored in memory during the session, so that I can resolve short codes back to original URLs.

#### Acceptance Criteria

1. THE tool SHALL store all URL-to-short-code mappings in a Python dictionary.
2. THE tool SHALL support storing at least 1000 mappings in a single session.
3. WHEN the tool exits, THE tool SHALL NOT persist mappings (session-only storage).

### Requirement 4: URL Retrieval

**User Story:** As a user, I want to resolve a short code back to its original URL, so that I can verify the mapping.

#### Acceptance Criteria

1. WHEN a valid short code is provided, THE tool SHALL return the corresponding original URL.
2. WHEN an unknown short code is provided, THE tool SHALL display an error message indicating the code was not found.
3. THE tool SHALL support a "list" command that displays all current mappings.
