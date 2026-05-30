# Steering Files Demo

> **Execution mode:** local-only — no AWS account or network required

This demo showcases **Kiro steering files** — Markdown documents that guide the AI agent's behavior with project-specific context, coding standards, and domain knowledge. Steering files shape how Kiro writes code, reviews changes, and makes decisions within your project.

## What Are Steering Files?

A steering file is a Markdown document placed in `.kiro/steering/` that provides contextual guidance to the AI agent. Each file has a YAML frontmatter block that controls **when** the guidance is activated:

```markdown
---
inclusion: auto | conditional | manual
globs: "**/*.py"          # Only for conditional mode
description: "Brief description of when this guidance applies"
---

# Your guidance content here
```

## Inclusion Modes

Kiro supports three inclusion modes, each suited to different use cases:

---

### 1. Auto (Always-On): `code-style.md`

```yaml
---
inclusion: auto
description: "Always-on coding style guidelines applied to all files in the project"
---
```

**When it activates:** Always. This guidance is included in every interaction with the AI agent, regardless of which file you're working on.

**Use case:** Universal project standards — naming conventions, documentation requirements, error handling patterns, and code organization rules.

**Example content in this demo:**
- `snake_case` for Python, `camelCase` for TypeScript
- Google-style docstrings required for all public functions
- Type hints mandatory on all function signatures
- No bare `except:` — always catch specific exceptions

📄 `.kiro/steering/code-style.md`

---

### 2. Conditional: `aws-patterns.md`

```yaml
---
inclusion: conditional
globs: "**/*.py"
description: "AWS best practices applied when working with Python files that interact with AWS services"
---
```

**When it activates:** Only when you're working on files that match the `globs` pattern. In this case, any Python file (`.py`) triggers the AWS patterns guidance.

**Use case:** Domain-specific guidance that's only relevant for certain file types — AWS SDK patterns for Python files, React patterns for `.tsx` files, database patterns for migration files.

**Example content in this demo:**
- Explicit boto3 session management (no default sessions)
- Always use paginators for AWS API calls
- Botocore retry configuration with adaptive mode
- Catch specific AWS exceptions using client exceptions

📄 `.kiro/steering/aws-patterns.md`

---

### 3. Manual: `migration-guide.md`

```yaml
---
inclusion: manual
description: "Migration guide for upgrading from v1 to v2 API — activate manually when performing migration work"
---
```

**When it activates:** Only when you explicitly activate it from the Kiro interface. The agent does not load this guidance automatically.

**Use case:** Temporary or situational guidance — migration guides, one-time refactoring instructions, sprint-specific conventions, or experimental patterns you want to try selectively.

**Example content in this demo:**
- Breaking changes between API v1 and v2
- Step-by-step migration instructions
- Rollback plan if issues arise

📄 `.kiro/steering/migration-guide.md`

---

## Project Structure

```
demo-steering/
├── .kiro/
│   └── steering/
│       ├── code-style.md           # inclusion: auto (always-on)
│       ├── aws-patterns.md         # inclusion: conditional (Python files)
│       └── migration-guide.md      # inclusion: manual (user-activated)
├── examples/
│   └── sample-project/
│       └── lambda_handler.py       # Triggers conditional steering
├── README.md
└── README.it.md
```

## Creating Custom Steering Files

### Step 1: Create the file

Create a new `.md` file in your project's `.kiro/steering/` directory:

```bash
mkdir -p .kiro/steering
touch .kiro/steering/my-guidelines.md
```

### Step 2: Add frontmatter

Choose the appropriate inclusion mode:

```markdown
---
inclusion: auto
description: "My project-wide guidelines"
---
```

Or for conditional activation:

```markdown
---
inclusion: conditional
globs: "src/**/*.ts"
description: "TypeScript patterns for the src directory"
---
```

### Step 3: Write your guidance

Add clear, actionable instructions in Markdown. Use headings, code examples, and bullet points:

```markdown
# My Guidelines

## Naming Conventions
- Use descriptive variable names
- Prefix interfaces with `I`

## Code Examples
\```python
# Good
def calculate_total(items: list[Item]) -> Decimal:
    ...

# Bad
def calc(x):
    ...
\```
```

### Step 4: Kiro activates it automatically

Once saved, Kiro detects the steering file and applies it according to its inclusion mode. No restart or configuration needed.

## Tips

- Keep steering files focused — one concern per file
- Use `auto` sparingly to avoid context overload
- `conditional` with specific globs is the most efficient mode for large projects
- Update steering files as your project evolves — they're living documents
