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
    """Input parameters for this workflow."""
    # Non-sensitive input fields
    field_name: str = Field(description="...", min_length=1)
    username: str = Field(min_length=1)

class SecureParams(BaseModel):
    """Secure parameters for this workflow."""
    # Sensitive fields only — values are never exposed in the sandbox
    # CRITICAL: SecureParams fields NEVER use default= — platform injects at runtime
    password: Secure[str] = Field(min_length=1, description="Account password")
    api_key: Secure[str] = Field(min_length=1, description="API key")  # only if needed

class Result(BaseModel):
    """Output returned by this workflow."""
    # Result should include success: bool
    success: bool
    extracted_data: dict | None = None
    error: str | None = None
```

Rules:
- Use `Field()` with defaults and validators where appropriate
- **Passwords, tokens, and API keys go in `SecureParams` with `Secure[str]`** — not in `Params`
- **`SecureParams` fields NEVER use `default=`** — the platform injects secrets at runtime
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
| Type text | `computer.type(params.field)` — just type directly, no need to clear |
| Type password/secret | `computer.type(secure_params.password, interval=0.01)` — field must be `Secure[str]` in `SecureParams` |
| Press key | `computer.press("Return")` |
| Wait/check state | `agent.verify("Is [condition]?", timeout=N)` → returns bool |
| Extract data | `agent.extract("Extract ...", schema={...})` → returns dict/list |
| Download file | See `examples/download-files.py` |
| Loop over items | Python `for` loop with `agent.execute()` inside |
| Save result to file | `os.makedirs("/artifacts", exist_ok=True)` then write to `/artifacts/` |
| Unrecoverable failure | `raise RuntimeError("descriptive message")` — browser won't open, site unreachable, extraction empty |
| Expected failure | `return Result(success=False, error="descriptive message")` — wrong password, item not found |

### 5. Write the workflow

Assemble the `run()` function following this structure:

```python
"""
Workflow: [Name]

Description of what this workflow does.
"""
from nen import Agent, Computer, Secure
from pydantic import BaseModel, Field


class Params(BaseModel):
    """Input parameters for this workflow."""
    url: str = Field(min_length=1)
    username: str = Field(min_length=1)


class SecureParams(BaseModel):  # omit entirely if no secrets
    """Secure parameters for this workflow."""
    # NEVER use default= on SecureParams fields
    password: Secure[str] = Field(min_length=1, description="Login password")


class Result(BaseModel):
    """Output returned by this workflow."""
    success: bool
    data: dict | None = None
    error: str | None = None


def run(params: Params, secure_params: SecureParams) -> Result:  # drop secure_params if no secrets
    """
    Main workflow entry point.

    Args:
        params: Pydantic model with workflow input parameters
        secure_params: Pydantic model with secure parameters

    Returns:
        Result model with workflow results
    """
    agent = Agent()
    computer = Computer()

    # Phase 1: Open browser (UNRECOVERABLE if fails → raise)
    agent.execute("Click the Chromium browser icon in the taskbar (the blue circular icon, second from left)")
    if not agent.verify("Is the Chromium browser open?", timeout=10):
        raise RuntimeError("Failed to open Chromium browser")

    # Phase 2: Navigate (UNRECOVERABLE if fails → raise)
    agent.execute(f"Navigate to {params.url}")
    if not agent.verify("Is the page loaded?", timeout=30):
        raise RuntimeError(f"Failed to load page at {params.url}")

    # Phase 3: Login
    agent.execute("Click the username field")
    computer.type(params.username)
    
    agent.execute("Click the password field")
    computer.type(secure_params.password, interval=0.01)
    
    agent.execute("Click the login button")

    # Phase 4: Verify result — check FAILURE indicators FIRST
    if agent.verify("Are we still on the login page?", timeout=10):
        return Result(success=False, error="Login failed - still on login page")
    
    if agent.verify("Is there an error message visible?"):
        return Result(success=False, error="Login failed - error message displayed")
    
    if not agent.verify("Is the dashboard visible?", timeout=20):
        return Result(success=False, error="Unable to verify login state")

    # Phase 5: Extract results (optional)
    try:
        data = agent.extract("Extract user info", schema={
            "type": "object",
            "properties": {
                "username": {"type": "string"}
            },
            "required": ["username"]
        })
    except Exception:
        data = None

    # Phase 6: Return success
    return Result(success=True, data=data)
```

### 6. Review the output

Verify:
- [ ] Every JSON step has a corresponding Python call
- [ ] `Result` includes `success: bool`
- [ ] `agent.execute()` calls use `agent.verify()` checks after critical actions
- [ ] **Error handling uses `raise` for unrecoverable failures** (browser won't open, site unreachable)
- [ ] **Error handling uses `return Result(success=False)` for expected failures** (wrong password, item not found)
- [ ] Pydantic models match the JSON input/output schema
- [ ] Natural language in `agent.execute()` is specific (element name, location, color)
- [ ] **Keyboard uses `computer.type()` and `computer.press()`** — NOT `computer.keyboard.type()`
- [ ] **DO NOT clear fields before typing** — just type directly into clicked fields
- [ ] **DO NOT use `computer.hotkey()`** — it is broken and unreliable
- [ ] **Failure indicators are checked FIRST** before success indicators in `agent.verify()`
- [ ] All secrets use `Secure[str]` in `SecureParams` — never in `Params`
- [ ] **`SecureParams` fields do NOT use `default=`** — platform injects at runtime
- [ ] `run()` signature includes `secure_params: SecureParams` if secrets are present
- [ ] Docstrings use standard Python format (no `\n` or `\"""` escaping)
- [ ] Timeouts are appropriate for slow operations (20-30s for page loads)
