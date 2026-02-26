# Introduction

> Build desktop automation workflows with AI-powered vision models

## What is Nen?

Nen is a Python SDK for building desktop automation workflows that run in secure, isolated sandbox containers. Write natural-language instructions to control a virtual desktop — Nen uses vision-language models (VLMs) to see the screen, click buttons, fill forms, and extract structured data from any desktop application.

```python
from nen import Agent, Computer, Secure
```

## Core Concepts

Every Nen workflow is a Python file with a `run()` function. The SDK provides four building blocks:

| Concept       | Purpose                                                                       |
| ------------- | ----------------------------------------------------------------------------- |
| `run()`       | Entry point. Receives validated Pydantic params, returns validated results.   |
| `Agent`       | AI controller that sees the screen and performs actions via natural language.  |
| `Computer`    | Direct keyboard, mouse, and file system access.                               |
| `Secure[str]` | Type-safe secret handling — real values never touch the sandbox.              |

## How It Works

1. **Write a workflow** — Define a `run()` function with Pydantic input/output models. Use `Agent` for AI-driven actions and `Computer` for precise control.
2. **Deploy to sandbox** — Your workflow runs inside an isolated container with a virtual desktop. Nen orchestrates VLM calls to interpret the screen.
3. **Get structured results** — Results are validated against your Pydantic schema and returned via API. Files are packaged as `assets.zip`.

## Quick Example

```python
from nen import Agent
from pydantic import BaseModel, AnyUrl

class Params(BaseModel):
    website: AnyUrl

class Result(BaseModel):
    title: str

def run(params: Params) -> Result:
    agent = Agent()
    agent.execute(f"Open the browser at {params.website}")
    data = agent.extract("What is the page title?", Result.model_json_schema())
    return Result.model_construct(**data)
```
