---
description: Convert a JSON workflow definition into a Nen Python SDK workflow. Use when the user provides a JSON workflow and wants it converted to Python.
---

# JSON to Python Workflow Conversion

## Prerequisites

Read the `cup-python-sdk` skill first — specifically:
- `resources/workflow-structure.md` for run()/Params/Result patterns
- `resources/agent.md` for Agent API
- `resources/computer.md` for Computer API
- `resources/secure.md` for Secure[str] patterns
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
- Missing secrets (are there credentials that aren't in the JSON?)

Do NOT proceed until all ambiguities are resolved.

### 3. Create Pydantic models

```python
from pydantic import BaseModel, Field

class Params(BaseModel):
    # Map JSON input fields here
    field_name: str = Field(description="...", min_length=1)

class SecureParams(BaseModel):
    # Only if secrets are needed
    password: Secure[str] = Field(min_length=12)

class Result(BaseModel):
    # Map JSON output fields here
    extracted_data: dict | None = None
```

Rules:
- Use `Field()` with defaults and validators where appropriate
- Use `Secure[str]` for secrets in `SecureParams`, never in `Params`
- Use `list[str]`, `list[dict]`, `dict | None` for complex types
- Use `pass` for empty Result

### 4. Map actions to SDK calls

| JSON action type | Python SDK equivalent |
|-----------------|----------------------|
| Navigate / open URL | `agent.execute("Open browser and navigate to ...")` |
| Click element | `agent.execute("Click the [specific element]")` |
| Type text | `computer.type("text")` or `agent.execute("Type ... in the field")` |
| Type secret | `computer.type(secure_params.field)` |
| Press key | `computer.press("Return")` |
| Key combo | `computer.hotkey("ctrl", "c")` |
| Wait/check state | `agent.verify("Is [condition]?", timeout=N)` |
| Extract data | `agent.extract("Extract ...", schema={...})` |
| Download file | See `examples/download-files.py` |
| Loop over items | Python `for` loop with `agent.execute()` inside |

### 5. Write the workflow

Assemble the `run()` function following this structure:

```python
def run(params: Params) -> Result:
    agent = Agent()
    computer = Computer()  # only if needed

    # Phase 1: Navigate
    agent.execute("...")

    # Phase 2: Verify state
    if not agent.verify("..."):
        raise RuntimeError("...")

    # Phase 3: Perform actions
    agent.execute("...")

    # Phase 4: Extract results
    data = agent.extract("...", Schema.model_json_schema())

    # Phase 5: Return
    return Result.model_construct(**data)
```

### 6. Review the output

Verify:
- [ ] Every JSON step has a corresponding Python call
- [ ] All secrets use `Secure[str]` in `SecureParams`
- [ ] `agent.verify()` checks are placed after navigation and critical actions
- [ ] Error handling with `RuntimeError` for failures
- [ ] Pydantic models match the JSON input/output schema
- [ ] Natural language in `execute()` is specific (element name, location)
