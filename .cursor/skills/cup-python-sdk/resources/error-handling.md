# Error Handling

> Exception types, raising errors, and error webhooks

Source: https://docs.getnen.ai (Error Handling page)

## Exception Types

Nen defines three exception types:

| Exception       | Description                                 |
| --------------- | ------------------------------------------- |
| `WorkflowError` | Base exception for all workflow failures    |
| `RPCError`      | Communication failure with the orchestrator |
| `TimeoutError`  | Operation exceeded its timeout              |

```python
from nen import WorkflowError
```

## Catching Errors

Wrap calls in `try/except` when your workflow can meaningfully recover (e.g. retry or fallback).

### Retry pattern

```python
def run(params: Params) -> Result:
    agent = Agent()
    for attempt in range(3):
        try:
            agent.execute("Click Submit")
            break
        except WorkflowError:
            if attempt == 2:
                raise
            agent.execute("Scroll down to find the Submit button")
```

### Conditional recovery (alternative path)

```python
def run(params: Params) -> Result:
    agent = Agent()
    try:
        agent.execute("Click the Export button")
    except WorkflowError:
        agent.execute("Open the File menu and click Export")
```

## Raising Errors

Raise any exception to signal a workflow failure. The exception message is forwarded to the error webhook.

```python
# Hard failure — dashboard never loaded
if not agent.verify("Is the dashboard loaded?", timeout=30):
    raise RuntimeError("Dashboard did not load within 30 seconds")

# Missing extracted value
data = agent.extract("Extract the order ID", OrderSchema.model_json_schema())
if not data.get("order_id"):
    raise ValueError("No order ID found on the page")
```

### Uncaught errors (intentional propagation)

If an exception propagates out of `run()` without being caught, the orchestrator marks the run as a **hard failure**. Use this intentionally for unrecoverable conditions — missing required files, unreachable services, failed preconditions, etc.

```python
def run(params: Params) -> Result:
    if not some_precondition:
        raise RuntimeError("Precondition not met — aborting run")
    ...
```

> **Rule of thumb:** Catch and handle errors only when you can recover. For everything else, let the exception propagate so the failure is visible rather than silently returning a partial result.

## Error Webhooks

When a workflow fails, the error webhook payload contains the exception message:

```json
{
  "success": false,
  "error": "No images found for user 0123456789abcdef"
}
```

Any unhandled exception in `run()` automatically becomes an error webhook — no need to catch and re-raise.
