---
name: cup-python-sdk
description: Reference documentation for the Nen Python SDK used to build desktop automation workflows. Use when converting JSON workflows to Python, writing new workflow.py files, or answering questions about Agent, Computer, Secure, run(), Params, Result, or Pydantic models.
---

# Nen Python SDK Reference

Use this skill whenever you need to write, convert, or modify Nen Python workflows. Read the relevant resource files below based on the task.

## Resources

| Resource | Contents |
|----------|----------|
| [introduction.md](resources/introduction.md) | SDK overview, core concepts, how it works |
| [workflow-structure.md](resources/workflow-structure.md) | `run()` entry point, `Params`, `Result`, `SecureParams`, Pydantic models |
| [agent.md](resources/agent.md) | `Agent` class — `execute()`, `verify()`, `extract()` |
| [computer.md](resources/computer.md) | `Computer` class — keyboard (`type`, `press`, `hotkey`), mouse (`click_at`, `move`, `scroll`), drives |
| [secure.md](resources/secure.md) | `Secure[str]` — type-safe secret handling |
| [files.md](resources/files.md) | Sandbox filesystem, `Drive`, `File` objects, `assets.zip` |

## Quick Reference

```python
from nen import Agent, Computer, Secure
from pydantic import BaseModel, Field

class Params(BaseModel):
    url: str
    username: Secure[str]

class Result(BaseModel):
    title: str

def run(params: Params) -> Result:
    agent = Agent()
    computer = Computer()

    agent.execute(f"Open browser to {params.url}")
    computer.hotkey("ctrl", "a")

    if agent.verify("Is the page loaded?"):
        data = agent.extract("What is the title?", Result.model_json_schema())
        return Result.model_construct(**data)
```

## Examples

See `examples/` for complete workflow implementations:

| Example | Pattern |
|---------|---------|
| `basic-web-navigation.py` | Navigate, verify, extract |
| `login-with-popup.py` | SecureParams, popup handling |
| `process-multiple-items.py` | Loop through list params |
| `extract-data-from-screen.py` | Multiple extract() calls |
| `multi-step-pipeline.py` | Cross-system data transfer |
| `download-files.py` | File download with tracking |

## JSON → Python Conversion Workflow

When converting a JSON workflow to Python:

1. **Read the JSON workflow** and identify: actions, conditions, extractions, secrets, and input/output fields
2. **Ask clarifying questions** if the JSON has ambiguous steps, unclear UI targets, or missing context
3. **Create Pydantic models**:
   - `Params` for inputs (use `Field` with defaults/validators)
   - `SecureParams` for any secrets (use `Secure[str]`)
   - `Result` for outputs
4. **Map JSON actions** to SDK calls:
   - UI interactions → `agent.execute()` with descriptive natural language
   - Conditional checks → `agent.verify()` with `if/else`
   - Data extraction → `agent.extract()` with JSON schema or `Model.model_json_schema()`
   - Keyboard input → `computer.type()`, `computer.press()`, `computer.hotkey()`
   - Secret input → `computer.type(secure_params.field)`
5. **Add error handling** — `RuntimeError` for failures, `continue` for non-critical items in loops
6. **Review** — verify every JSON step has a corresponding Python call
