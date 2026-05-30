# Expected Hook Behavior

This document describes what each hook in the demo does when triggered.

## 1. Lint on Save (`lint-on-save.json`)

**Event:** `fileEdited`  
**Action:** `runCommand`  
**Trigger:** Any `.ts` file is saved (pattern: `**/*.ts`)

### What happens:

When you save a TypeScript file (e.g., `examples/sample-file.ts`), Kiro automatically runs:

```bash
npx eslint --fix {file}
```

### Expected output:

- ESLint auto-fixes formatting issues (quotes, semicolons, spacing)
- The file is updated in-place with fixes applied
- If there are unfixable errors, they are reported in the terminal

---

## 2. Validate Write Operations (`validate-write.json`)

**Event:** `preToolUse`  
**Action:** `askAgent`  
**Trigger:** Before any `write` tool operation executes

### What happens:

Before Kiro writes code to a file, the agent reviews the proposed changes against project standards:

- Consistent naming conventions
- Proper error handling
- No hardcoded secrets
- Appropriate documentation

### Expected output:

- The agent flags any concerns before the write proceeds
- If issues are found, the agent suggests corrections
- If no issues, the write operation continues normally

---

## 3. Review Tool Output (`review-output.json`)

**Event:** `postToolUse`  
**Action:** `askAgent`  
**Trigger:** After any `write` tool operation completes

### What happens:

After Kiro writes code to a file, the agent reviews the result for quality:

- Checks for introduced bugs
- Verifies error handling is present
- Scans for security concerns
- Validates alignment with project architecture

### Expected output:

- The agent provides a brief quality assessment
- Suggests improvements if potential issues are detected
- Confirms the change is safe if no issues are found

---

## 4. Generate Documentation (`generate-docs.json`)

**Event:** `userTriggered`  
**Action:** `runCommand`  
**Trigger:** Manually triggered by the user from the Kiro hooks panel

### What happens:

When the user manually triggers this hook, Kiro runs:

```bash
python scripts/generate-docs.py
```

### Expected output:

- Project documentation is regenerated from source code
- Updated docs are written to the project's documentation directory
- A summary of generated/updated files is printed to the terminal
