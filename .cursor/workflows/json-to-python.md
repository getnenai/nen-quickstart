---
description: Convert a JSON workflow definition into a Nen Python SDK workflow. Use when the user provides a JSON workflow and wants it converted to Python.
---

# JSON to Python Workflow Conversion

## Prerequisites

Read the `cup-python-sdk` skill first — specifically:
- `resources/workflow-structure.md` for run()/Params/Result patterns
- `resources/agent.md` for Agent — execute(), verify(), extract() API
- `resources/computer.md` for Computer — keyboard/mouse API
- `resources/secure_params.md` for handling sensitive data
- `examples/` for reference implementations

## Steps

### 1. Analyze the JSON workflow

Read the full JSON workflow. Identify:
- **Input fields** — what parameters does the workflow accept?
- **Output fields** — what data does the workflow return?
- **Secrets** — are there passwords, API keys, or tokens?
- **Actions** — what UI interactions does it perform (click, type, navigate)?
- **Conditions** — what checks or branches exist?
- **Extractions** — what data is read from the screen?
- **Loops** — does it iterate over a list of items?
- **Files** — does it download or upload files?

### 2. Ask clarifying questions

Before writing code, ask about anything unclear:
- Ambiguous action descriptions ("interact with the form" — which fields?)
- Missing error handling (what should happen if a step fails?)
- Unclear UI targets ("click the button" — which button?)
- Unknown application context (what app is this for? what does the screen look like?)
- Missing credentials (are there passwords that aren't in the JSON?)

Do NOT proceed until all ambiguities are resolved.

### 3. Create Pydantic models

```python
from nen import Secure
from pydantic import BaseModel, Field

class Params(BaseModel):
    # Non-sensitive input fields
    field_name: str = Field(description="...", min_length=1)
    username: str = Field(min_length=1)

class SecureParams(BaseModel):
    # Sensitive fields only — values are never exposed in the sandbox
    password: Secure[str] = Field(min_length=1, description="Account password")
    api_key: Secure[str] = Field(description="API key")  # only if needed

class Result(BaseModel):
    # Result should include success: bool
    success: bool
    extracted_data: dict | None = None
    error: str | None = None
```

Rules:
- Use `Field()` with defaults and validators where appropriate
- **Passwords, tokens, and API keys go in `SecureParams` with `Secure[str]`** — not in `Params`
- If there are no secrets, omit `SecureParams` entirely
- Use `list[str]`, `list[dict]`, `dict | None` for complex types
- `Result` should include `success: bool`
- Set `error: str | None = None` in `Result` for failure messages

### 4. Map actions to SDK calls

| JSON action type | Python SDK equivalent |
|-----------------|----------------------|
| Open browser | `agent.execute("Click the Chromium browser icon in the taskbar (the blue circular icon, second from left)")` |
| Navigate / open URL | `agent.execute(f"Navigate to {params.url}")` |
| Click element | `agent.execute("Click the [specific element name and location]")` |
| Type text | `computer.type(params.field)` (after clearing field with `ctrl+a` + `BackSpace`) |
| Type password/secret | `computer.type(secure_params.password, interval=0.01)` — field must be `Secure[str]` in `SecureParams` |
| Press key | `computer.press("Return")` |
| Key combo | `computer.hotkey("ctrl", "a")` — always use `ctrl`, never `command` |
| Wait/check state | `agent.verify("Is [condition]?", timeout=N)` → returns bool |
| Extract data | `agent.extract("Extract ...", schema={...})` → returns dict/list |
| Download file | See `examples/download-files.py` |
| Loop over items | Python `for` loop with `agent.execute()` inside |
| Save result to file | `os.makedirs("/artifacts", exist_ok=True)` then write to `/artifacts/` |
| Workflow failure | `return Result(success=False, error="descriptive message")` |

### 5. Write the workflow

Assemble the `run()` function following this structure:

```python
from nen import Agent, Computer, Secure
from pydantic import BaseModel, Field


class Params(BaseModel):
    url: str = Field(min_length=1)
    username: str = Field(min_length=1)


class SecureParams(BaseModel):  # omit entirely if no secrets
    password: Secure[str] = Field(min_length=1, description="Login password")


class Result(BaseModel):
    success: bool
    data: dict | None = None
    error: str | None = None


def run(params: Params, secure_params: SecureParams) -> Result:  # drop secure_params if no secrets
    agent = Agent()
    computer = Computer()

    # Phase 1: Open browser
    agent.execute("Click the Chromium browser icon in the taskbar (the blue circular icon, second from left)")
    if not agent.verify("Is the Chromium browser open?", timeout=10):
        return Result(success=False, error="Failed to open browser")

    # Phase 2: Navigate
    agent.execute(f"Navigate to {params.url}")
    if not agent.verify("Is the page loaded?", timeout=20):
        return Result(success=False, error="Failed to load page")

    # Phase 3: Perform actions
    agent.execute("Click the [element]")
    computer.hotkey("ctrl", "a")
    computer.press("BackSpace")
    computer.type(params.url)

    # Phase 4: Verify result — check failure FIRST
    if agent.verify("Is there an error message visible?"):
        return Result(success=False, error="Action failed - error message shown")

    # Phase 5: Extract results
    data = agent.extract("Extract ...", schema={...})

    # Phase 6: Return
    return Result(success=True, data=data)
```

### 6. Review the output

Verify:
- [ ] Every JSON step has a corresponding Python call
- [ ] `Result` includes `success: bool`
- [ ] `agent.execute()` calls use `agent.verify()` checks after critical actions
- [ ] Error handling uses `return Result(success=False, error=...)` — not `raise`
- [ ] Pydantic models match the JSON input/output schema
- [ ] Natural language in `agent.execute()` is specific (element name, location, color)
- [ ] Fields are cleared before typing (`ctrl+a` + `BackSpace`)
- [ ] Keyboard uses Linux modifiers (`ctrl` not `command`)
- [ ] Failure indicators are checked before success indicators in `agent.verify()`
- [ ] All secrets use `Secure[str]` in `SecureParams` — never in `Params`
- [ ] `run()` signature includes `secure_params: SecureParams` if secrets are present
