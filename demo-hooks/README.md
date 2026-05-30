# Hooks Demo

> **Execution mode:** local-only — no AWS account or network required

This demo showcases **Kiro hooks** — automations that trigger agent actions based on IDE events. Hooks let you enforce coding standards, validate operations, review outputs, and run scripts automatically, without manual intervention.

## What Are Kiro Hooks?

A hook is a JSON configuration that maps an IDE event to an automated action. When the specified event occurs, Kiro executes the configured action — either running a shell command or asking the AI agent to perform a task.

```json
{
  "id": "hook-id",
  "name": "Human-Readable Name",
  "description": "What this hook does",
  "eventType": "fileEdited | preToolUse | postToolUse | userTriggered",
  "hookAction": "runCommand | askAgent"
}
```

## Hook Examples

This demo includes four hooks covering all major event types:

---

### 1. Lint on Save (`lint-on-save`)

| Property | Value |
|----------|-------|
| **Event Type** | `fileEdited` |
| **Action Type** | `runCommand` |
| **File Patterns** | `**/*.ts` |
| **Command** | `npx eslint --fix {file}` |

**Trigger condition:** Any TypeScript file (`.ts`) is saved in the project.

**Expected outcome:** ESLint runs automatically with auto-fix enabled on the saved file, ensuring consistent code style without manual linting.

---

### 2. Validate Write Operations (`validate-write`)

| Property | Value |
|----------|-------|
| **Event Type** | `preToolUse` |
| **Action Type** | `askAgent` |
| **Tool Types** | `write` |
| **Agent Prompt** | Verify coding standards compliance before proceeding |

**Trigger condition:** The AI agent is about to perform a write operation (creating or modifying a file).

**Expected outcome:** The agent reviews the pending write for naming conventions, error handling, hardcoded secrets, and documentation before the operation executes. Issues are flagged before code is written.

---

### 3. Review Tool Output (`review-output`)

| Property | Value |
|----------|-------|
| **Event Type** | `postToolUse` |
| **Action Type** | `askAgent` |
| **Tool Types** | `write` |
| **Agent Prompt** | Review execution result for bugs, security concerns, and architecture deviations |

**Trigger condition:** The AI agent has just completed a write operation.

**Expected outcome:** The agent reviews the result for introduced bugs, missing error handling, security concerns, or deviations from the project architecture. Improvements are suggested if needed.

---

### 4. Generate Documentation (`generate-docs`)

| Property | Value |
|----------|-------|
| **Event Type** | `userTriggered` |
| **Action Type** | `runCommand` |
| **Command** | `python scripts/generate-docs.py` |

**Trigger condition:** The user manually triggers this hook from the Kiro interface.

**Expected outcome:** The documentation generation script runs, updating project docs from source code comments and docstrings.

---

## Project Structure

```
demo-hooks/
├── .kiro/
│   └── hooks/
│       ├── lint-on-save.json       # fileEdited → runCommand
│       ├── validate-write.json     # preToolUse → askAgent
│       ├── review-output.json      # postToolUse → askAgent
│       └── generate-docs.json      # userTriggered → runCommand
├── examples/
│   ├── sample-file.ts              # Trigger file for fileEdited demo
│   └── expected-output.md          # Expected hook behavior documentation
├── .env.example
├── README.md
└── README.it.md
```

## Hook Configuration Reference

### Required Fields (all hooks)

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Kebab-case identifier |
| `name` | string | Human-readable title |
| `description` | string | What the hook does |
| `eventType` | string | Event that triggers the hook |
| `hookAction` | string | `askAgent` or `runCommand` |

### Conditional Fields

| Field | Required When | Description |
|-------|--------------|-------------|
| `filePatterns` | `eventType: "fileEdited"` | Comma-separated glob patterns (e.g., `**/*.ts, **/*.py`) |
| `toolTypes` | `eventType: "preToolUse"` or `"postToolUse"` | Tool category filter (e.g., `write`, `read`, `shell`) |
| `outputPrompt` | `hookAction: "askAgent"` | Instruction for the AI agent |
| `command` | `hookAction: "runCommand"` | Shell command to execute |

## Creating Your Own Hooks

1. Create a JSON file in `.kiro/hooks/` with a descriptive name
2. Define the event type that should trigger the hook
3. Choose the action: `runCommand` for scripts, `askAgent` for AI review
4. Add the required conditional fields based on your event type
5. Kiro will automatically detect and activate the hook
