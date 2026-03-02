# Workflow Structure

> `run()` entry point, `Params`, `Result`, and Pydantic models

## File Structure

Every Nen workflow is a single Python file (typically `workflow.py`) with a `run()` function:

```python
from nen import Agent, Computer
from pydantic import BaseModel, Field


class Params(BaseModel):
    """Input parameters — validated before run() is called."""
    ...


class Result(BaseModel):
    """Output schema — validated before returning to caller."""
    title: str = Field(min_length=1, description="Extracted page title")


def run(params: Params) -> Result:
    agent = Agent()
    computer = Computer()
    ...
    data = agent.extract("What is the page title?", Result.model_json_schema())
    return Result.model_construct(**data)
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

`run()` receives the validated `Params` model and must return a `Result` model. When a workflow handles sensitive data (passwords, tokens, API keys), add a `SecureParams` model as the second argument. See `secure_params.md` for details.

## Params Model

Use Pydantic `BaseModel` with `Field` for validation:

```python
class Params(BaseModel):
    website_url: str = Field(default="https://example.com", min_length=1)
    post_index: int = Field(default=0, ge=0)
    provider_names: list[str]
    patient_name: str = Field(min_length=1)
    username: str = Field(min_length=1)
```

Supported types: `str`, `int`, `float`, `bool`, `list[str]`, `list[int]`, etc.

> **Sensitive data:** Passwords, tokens, and API keys belong in a `SecureParams` model — not in `Params`. See `secure_params.md`.

## SecureParams Model

For workflows that handle secrets, define a separate `SecureParams` model using `Secure[str]`:

```python
from nen import Secure

class SecureParams(BaseModel):
    password: Secure[str] = Field(min_length=1, description="Login password")
    api_key: Secure[str] = Field(description="API key")
```

- Import `Secure` from `nen`
- The platform injects the real value at runtime — it is never exposed in the sandbox
- Accept as second argument: `def run(params: Params, secure_params: SecureParams) -> Result:`

## Result Model

`Result` models the **actual data** being returned — not a success/failure envelope. Define fields for what the workflow extracts or produces, with `Field` validators to enforce data quality. All failures are communicated by raising exceptions, not by encoding them in the result.

```python
class Result(BaseModel):
    customer_id: str = Field(min_length=8, max_length=16)
    first_name: str
    last_name: str
    phone: str | None = Field(default=None)
    email: EmailStr | None = Field(default=None)
```

Pass `Result.model_json_schema()` directly to `agent.extract()` so the extraction schema stays in sync with the return type, then construct the result with `Result.model_construct(**data)`:

```python
data = agent.extract("Extract customer info from the page", Result.model_json_schema())
return Result.model_construct(**data)
```

## Error Handling

Raise exceptions for all failures — do **not** encode errors in the `Result`:

```python
# ✅ CORRECT — raise for failures
if not agent.verify("Is the page loaded?", timeout=20):
    raise RuntimeError("Page failed to load")

if not agent.verify("Is the login form visible?"):
    raise RuntimeError("Login page not found")

# ❌ WRONG — do not return success/error envelope
if not agent.verify("Is the page loaded?"):
    return Result(success=False, error="Page failed to load")
```

Use `print()` for logging non-sensitive progress:

```python
print(f"Processing: {provider}")
print(f"Found {len(items)} items")
```

## Full Template (No Secrets)

```python
"""
Workflow: [Name]

[Description of what this workflow does.]
"""
from nen import Agent, Computer
from pydantic import BaseModel, Field


class Params(BaseModel):
    """Input parameters for this workflow."""

    website_url: str = Field(default="https://example.com", min_length=1)


class Result(BaseModel):
    """Output returned by this workflow."""

    title: str = Field(min_length=1, description="Page title extracted from the site")


def run(params: Params) -> Result:
    """
    Main workflow entry point.

    Args:
        params: Pydantic model with workflow input parameters.

    Returns:
        Result model with workflow results.
    """
    agent = Agent()
    computer = Computer()

    agent.execute("Click the Chromium browser icon in the taskbar (the blue circular icon, second from left)")
    if not agent.verify("Is the Chromium browser open?", timeout=10):
        raise RuntimeError("Failed to open Chromium browser")

    agent.execute(f"Navigate to {params.website_url}")
    if not agent.verify("Is the website loaded?", timeout=20):
        raise RuntimeError(f"Failed to load {params.website_url}")

    data = agent.extract("What is the page title?", Result.model_json_schema())
    return Result.model_construct(**data)
```

## Full Template (With Secrets)

```python
"""
Workflow: [Name]

[Description of what this workflow does.]
"""
from nen import Agent, Computer, Secure
from pydantic import BaseModel, Field


class Params(BaseModel):
    """Input parameters for this workflow."""

    login_url: str = Field(min_length=1)
    username: str = Field(min_length=1)


class SecureParams(BaseModel):
    """Sensitive parameters — values are never exposed in the sandbox."""

    password: Secure[str] = Field(min_length=1, description="Login password")


class Result(BaseModel):
    """Output returned by this workflow."""

    account_name: str = Field(min_length=1, description="Account name shown on the dashboard after login")


def run(params: Params, secure_params: SecureParams) -> Result:
    """
    Main workflow entry point.

    Args:
        params: Pydantic model with workflow input parameters.
        secure_params: Pydantic model with sensitive parameters.

    Returns:
        Result model with workflow results.
    """
    agent = Agent()
    computer = Computer()

    agent.execute("Click the Chromium browser icon in the taskbar (the blue circular icon, second from left)")
    if not agent.verify("Is the Chromium browser open?", timeout=10):
        raise RuntimeError("Failed to open Chromium browser")

    agent.execute(f"Navigate to {params.login_url}")
    if not agent.verify("Is the login form visible?", timeout=20):
        raise RuntimeError("Login page not found or failed to load")

    agent.execute("Click the username or email field")
    computer.type(params.username)

    agent.execute("Click the password field")
    computer.type(secure_params.password, interval=0.01)

    computer.press("Return")

    if not agent.verify("Is the dashboard or main page visible?", timeout=20):
        raise RuntimeError("Login failed — dashboard not visible after submitting credentials")

    data = agent.extract("What is the account name shown on the dashboard?", Result.model_json_schema())
    return Result.model_construct(**data)
```

## Output Files

Files written to `/artifacts/` are packaged as `assets.zip` when the run completes:

```python
import os
from pathlib import Path

os.makedirs("/artifacts", exist_ok=True)
Path("/artifacts/report.txt").write_text("Report content")
```

See `files.md` for complete file handling reference.
