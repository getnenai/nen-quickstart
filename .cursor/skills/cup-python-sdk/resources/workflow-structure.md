# Workflow Structure

> `run()` entry point, `Params`, `Result`, and Pydantic models

## File Structure

Every Nen workflow is a single Python file (typically `workflow.py`) with a `run()` function:

```python
from nen import Agent, Computer, Secure
from pydantic import BaseModel, Field

class Params(BaseModel):
    """Input parameters — validated before run() is called."""
    ...

class SecureParams(BaseModel):
    """Secret parameters — optional, only if workflow needs secrets."""
    ...

class Result(BaseModel):
    """Output schema — validated before returning to caller."""
    ...

def run(params: Params) -> Result:
    ...
```

## `run()` Signatures

**Without secrets:**
```python
def run(params: Params) -> Result:
```

**With secrets:**
```python
def run(params: Params, secure_params: SecureParams) -> Result:
```

## Params Model

Use Pydantic `BaseModel` with `Field` for validation:

```python
class Params(BaseModel):
    website_url: str = Field(default="https://example.com", min_length=1)
    post_index: int = Field(default=0, ge=0)
    provider_names: list[str]              # list types supported
    patient_name: str = Field(min_length=1)
```

Supported types: `str`, `int`, `float`, `bool`, `list[str]`, `list[int]`, `AnyUrl`, etc.

## Result Model

```python
class Result(BaseModel):
    title: str                         # required field
    demographics: dict | None = None   # optional field
    visits: list[dict] = []            # list with default
    downloaded: int = 0                # numeric with default
    files: list[str] = []              # string list
    data: list[dict] = []              # list of dicts
```

An empty result (no return data):
```python
class Result(BaseModel):
    pass
```

## Error Handling

Raise `RuntimeError` for workflow failures:

```python
if not agent.verify("Is the page loaded?"):
    raise RuntimeError("Page failed to load")
```

Use `print()` for logging:
```python
print(f"Processing: {provider}")
print(f"Warning: Download may have failed for {doc}")
```

## Output Files

Files written to the working directory are archived as `assets.zip`:

```python
from pathlib import Path

Path("./reports").mkdir(parents=True, exist_ok=True)
Path("./reports/summary.txt").write_text("Report content")
```

See `files.md` for complete file handling reference.
