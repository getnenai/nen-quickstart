---
name: cup-python-sdk
description: Reference documentation for the Nen Python SDK used to build desktop automation workflows. Use when writing new workflow.py files, or answering questions about Agent, Computer, agent.execute(), agent.verify(), agent.extract(), computer.type(), computer.press(), computer.mouse, computer.drive(), Drive, File, Secure[str], SecureParams, run(), Params, Result, Pydantic models, error handling, WorkflowError, RPCError, TimeoutError, try/except, raising errors, retry patterns, or error webhooks.
---

# Nen Python SDK Reference

Use this skill whenever you need to write or modify Nen Python workflows. Read the relevant resource files below based on the task.

## Resources

| Resource | Contents |
|----------|----------|
| [introduction.md](resources/introduction.md) | SDK overview, core concepts, how it works |
| [workflow-structure.md](resources/workflow-structure.md) | `run()` entry point, `Params`, `Result`, Pydantic models |
| [agent.md](resources/agent.md) | `Agent` — `execute()`, `verify()`, `extract()` |
| [computer.md](resources/computer.md) | `Computer` — `type/press`, `mouse.click_at/move/scroll`, `drive()` |
| [secure_params.md](resources/secure_params.md) | Handling sensitive data (passwords, tokens) in workflows |
| [files.md](resources/files.md) | `computer.drive()`, `Drive`, `File`, reading files, writing to `/artifacts` |
| [error-handling.md](resources/error-handling.md) | `WorkflowError`, `RPCError`, `TimeoutError`, retry patterns, raising errors, error webhooks |

## Quick Reference

```python
from nen import Agent, Computer, Secure
from pydantic import BaseModel, Field


class Params(BaseModel):
    url: str = Field(default="https://example.com", min_length=1)


class Result(BaseModel):
    success: bool
    title: str | None = None
    error: str | None = None


def run(params: Params) -> Result:
    agent = Agent()
    computer = Computer()

    agent.execute("Click the Chromium browser icon in the taskbar (the blue circular icon, second from left)")
    if not agent.verify("Is the Chromium browser open?", timeout=10):
        return Result(success=False, error="Failed to open browser")

    agent.execute(f"Navigate to {params.url}")
    if not agent.verify("Is the page loaded?", timeout=20):
        return Result(success=False, error="Failed to load page")

    data = agent.extract("What is the page title?", schema={
        "type": "object",
        "properties": {"title": {"type": "string"}},
        "required": ["title"]
    })

    return Result(success=True, title=data.get("title"))
```

## Examples

See `examples/` for complete workflow implementations:

| Example | Pattern |
|---------|---------|
| `basic-web-navigation.py` | Navigate, verify, extract |
| `login-with-popup.py` | Login flow, popup handling |
| `process-multiple-items.py` | Loop through list params |
| `extract-data-from-screen.py` | Multiple extract() calls |
| `multi-step-pipeline.py` | Cross-system data transfer |
| `download-files.py` | File download with tracking |
