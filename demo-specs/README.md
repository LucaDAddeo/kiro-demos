# Spec-Driven Development Demo

> **Execution mode:** local-only — no AWS account or network required

This demo showcases Kiro's spec-driven development workflow, where you define **requirements**, create a **design**, break it into **tasks**, and let Kiro generate the implementation code. The result is a fully traceable URL shortener CLI tool built entirely from spec artifacts.

## The Spec Workflow

Kiro's spec workflow follows a structured pipeline:

```
requirements.md → design.md → tasks.md → generated source code
```

### 1. Requirements

Define **what** the system should do using user stories and acceptance criteria.

📄 `.kiro/specs/url-shortener/requirements.md`

The URL shortener requirements cover:
- URL validation (http/https schemes, valid domains)
- Short code generation (SHA-256 hash truncation, deterministic)
- In-memory storage (dictionary-based, session-only)
- CLI interface (shorten, resolve, list commands)

### 2. Design

Describe **how** the system will be built — data models, interfaces, algorithms.

📄 `.kiro/specs/url-shortener/design.md`

### 3. Tasks

Break the design into **implementable units** with clear acceptance criteria.

📄 `.kiro/specs/url-shortener/tasks.md`

Each task is numbered (e.g., Task 1.1, Task 1.2) and maps directly to one or more requirements.

### 4. Generated Code

Kiro generates source code that references the originating task in comments:

```python
# Task 1.1: Implement URL validation
def validate_url(url: str) -> tuple[bool, str | None]:
    ...

# Task 1.2: Implement short code generation
def generate_short_code(url: str) -> str:
    ...

# Task 1.3: Implement in-memory storage
class URLStore:
    ...

# Task 1.4: Implement CLI interface
def create_parser() -> argparse.ArgumentParser:
    ...
```

## Traceability: From Spec to Source

Every function in `src/url_shortener.py` carries a comment linking it back to the task that generated it. This creates a clear audit trail:

| Task ID | Function / Class | Requirement |
|---------|-----------------|-------------|
| Task 1.1 | `validate_url()` | URL Validation |
| Task 1.2 | `generate_short_code()` | Short Code Generation |
| Task 1.3 | `URLStore` | In-Memory Storage |
| Task 1.4 | `create_parser()`, `main()` | CLI Interface |

## Project Structure

```
demo-specs/
├── .kiro/
│   └── specs/
│       └── url-shortener/
│           ├── .config.kiro
│           ├── requirements.md
│           ├── design.md
│           └── tasks.md
├── src/
│   └── url_shortener.py
├── tests/
│   └── test_url_shortener.py
├── requirements.txt
├── pyproject.toml
├── README.md
└── README.it.md
```

## How to Run

```bash
# Install dependencies
pip install -r requirements.txt

# View available commands
python src/url_shortener.py --help

# Shorten a URL
python src/url_shortener.py shorten https://example.com/long-path

# Resolve a short code
python src/url_shortener.py resolve abc123

# List all mappings
python src/url_shortener.py list
```

## Key Takeaways

- **Specs are living documents** — they evolve with the project and serve as the source of truth
- **Task IDs in code** create traceability between design decisions and implementation
- **The workflow is repeatable** — apply it to any project for structured, AI-assisted development
