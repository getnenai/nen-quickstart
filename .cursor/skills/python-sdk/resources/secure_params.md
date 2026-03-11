# SecureParams

> Type-safe secret handling — real values are never exposed inside the sandbox

## Overview

`Secure[str]` is a type annotation for secrets (passwords, API keys, tokens). The actual secret value is injected at runtime by the Nen platform — it is **never passed into the sandbox as plaintext**.

Sensitive fields go in a separate `SecureParams` model, which is accepted as the second argument to `run()`:

```python
from nen import Secure
from pydantic import BaseModel, Field


class SecureParams(BaseModel):
    password: Secure[str] = Field(min_length=1)
```

## Usage in `run()`

When a workflow uses secrets, define a `SecureParams` model and accept it as the second argument:

```python
from nen import Agent, Computer, Secure
from pydantic import BaseModel, Field


class Params(BaseModel):
    login_url: str
    username: str


class SecureParams(BaseModel):
    password: Secure[str] = Field(min_length=1, description="Account password")


class Result(BaseModel):
    account_name: str = Field(min_length=1, description="Account name shown after login")


def run(params: Params, secure_params: SecureParams) -> Result:
    agent = Agent()
    computer = Computer()

    agent.execute("Click the Chromium browser icon in the taskbar")
    if not agent.verify("Is the Chromium browser open?", timeout=10):
        raise RuntimeError("Failed to open Chromium browser")

    agent.execute(f"Navigate to {params.login_url}")
    if not agent.verify("Is the login form visible?", timeout=20):
        raise RuntimeError("Login page not found or failed to load")

    agent.execute("Click the username or email field")
    computer.type(params.username)

    # Enter password — value is never exposed in the sandbox
    agent.execute("Click the password field")
    computer.type(secure_params.password, interval=0.01)

    computer.press("Return")

    if not agent.verify("Is the dashboard or main page visible?", timeout=20):
        raise RuntimeError("Login failed — dashboard not visible after submitting credentials")

    data = agent.extract("What is the account name shown on the page?", Result.model_json_schema())
    return Result.model_construct(**data)
```

## Key Rules

- `Secure[str]` fields go in `SecureParams`, **not** in `Params`
- `run()` signature becomes `run(params: Params, secure_params: SecureParams) -> Result`
- Use `computer.type(secure_params.field)` to type secrets — the value never enters the sandbox as plaintext
- **Never convert a `Secure[str]` to a regular string or log it**
- Pydantic `Field` validators (e.g., `min_length`) work as expected
- If a workflow has no secrets, omit `SecureParams` entirely and use `def run(params: Params) -> Result:`
- **`Secure[str]` fields must NOT have a `default=` value.** The platform injects secrets at runtime. Use `Field(min_length=1, description="...")` — never `Field(default="mypassword", ...)`

## Import

```python
from nen import Secure
```

## Example: Multiple Secrets

```python
from nen import Secure
from pydantic import BaseModel, Field


class SecureParams(BaseModel):
    password: Secure[str] = Field(min_length=1, description="Login password")
    api_key: Secure[str] = Field(min_length=1, description="API key for external service")
```
