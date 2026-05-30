---
inclusion: auto
description: "Always-on coding style guidelines applied to all files in the project"
---

# Code Style Guidelines

## Naming Conventions

- Use `snake_case` for Python functions, variables, and module names
- Use `PascalCase` for Python class names
- Use `camelCase` for TypeScript/JavaScript variables and functions
- Use `UPPER_SNAKE_CASE` for constants in all languages
- Prefix private methods with underscore: `_internal_method()`

## Documentation

- Every public function must have a docstring explaining its purpose, parameters, and return value
- Use Google-style docstrings for Python:
  ```python
  def function_name(param: str) -> bool:
      """Brief description of the function.

      Args:
          param: Description of the parameter.

      Returns:
          Description of the return value.
      """
  ```
- Add inline comments only for non-obvious logic

## Type Hints

- All Python function signatures must include type hints for parameters and return values
- Use `typing` module for complex types: `Optional`, `Union`, `list[str]`
- TypeScript code must use explicit types (no `any` unless absolutely necessary)

## Error Handling

- Never use bare `except:` — always catch specific exceptions
- Raise custom exceptions with descriptive messages
- Log errors before re-raising when appropriate

## Code Organization

- Keep functions under 30 lines; extract helpers for complex logic
- Group imports: stdlib, third-party, local (separated by blank lines)
- One class per file for major classes; utility functions can share a module
