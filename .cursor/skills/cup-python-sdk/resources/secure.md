# Secure

> Type-safe secret handling — real values never enter the sandbox

## Overview

`Secure[str]` is a type annotation for secrets (passwords, API keys, tokens). The actual secret value is injected at runtime by the Nen platform — it never enters the sandbox as plaintext.

```python
from nen import Secure
from pydantic import BaseModel, Field

class SecureParams(BaseModel):
    password: Secure[str] = Field(min_length=12)
    api_key: Secure[str]
```

## Usage in `run()`

When a workflow uses secrets, define a `SecureParams` model and accept it as the second argument to `run()`:

```python
from nen import Agent, Computer, Secure
from pydantic import BaseModel, Field

class Params(BaseModel):
    login_url: str
    username: str

class SecureParams(BaseModel):
    password: Secure[str] = Field(min_length=12)

class Result(BaseModel):
    pass

def run(params: Params, secure_params: SecureParams) -> Result:
    computer = Computer()

    # Type the secret — value never enters the sandbox
    computer.type(secure_params.password)
```

## Key Rules

- `Secure[str]` fields go in `SecureParams`, NOT in `Params`
- `run()` signature becomes `run(params: Params, secure_params: SecureParams) -> Result`
- Use `computer.type(secure_params.field)` to type secrets — `Computer.type()` accepts `SecureValue`
- Never convert `Secure[str]` to a regular string or log it
- Pydantic `Field` validators (e.g., `min_length`) work as expected
