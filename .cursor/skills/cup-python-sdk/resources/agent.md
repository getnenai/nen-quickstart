# Agent

> VLM-driven controller. Execute actions, verify screen state, extract structured data.

```python
from nen import Agent

agent = Agent()
```

## Constructor

```python
Agent(model: str | None = None)
```

| Parameter | Type          | Default | Description                                                                           |
| --------- | ------------- | ------- | ------------------------------------------------------------------------------------- |
| `model`   | `str \| None` | `None`  | Default VLM for all calls on this agent. If not set, defaults to `claude-sonnet-4-6`. |

```python
agent = Agent()                          # Use default model (claude-sonnet-4-6)
agent = Agent(model="claude-haiku-4-5")  # Use a specified model
```

## Methods Overview

| Method      | Description                                      |
| ----------- | ------------------------------------------------ |
| `execute()` | Perform an action on screen via natural language |
| `verify()`  | Check whether a visual condition is true         |
| `extract()` | Read structured data from the current screen     |

---

## execute()

> Perform an action on the screen using a natural language instruction

```python
agent.execute(instruction: str, model: str | None = None) -> dict
```

The agent takes a screenshot, interprets the instruction, and performs the required interactions (clicks, typing, scrolling, etc.).

### Parameters

| Parameter     | Type          | Default | Description                                |
| ------------- | ------------- | ------- | ------------------------------------------ |
| `instruction` | `str`         | —       | Natural language description of what to do |
| `model`       | `str \| None` | `None`  | Override the default model for this call   |

### Returns

`dict` — Execution result metadata.

### Raises

`WorkflowError`

### Examples

```python
# Basic navigation
agent.execute("Open the browser to https://example.com")

# Clicking elements
agent.execute("Click the Submit button")

# Typing into fields
agent.execute("Click the email field and type hello@example.com")

# Override model for simple actions
agent.execute("Quit the calendar app", model="claude-haiku-4-5")
```

> **Tip:** Write instructions as if you're telling a human what to do. Be specific about which element to interact with — "Click the blue Submit button in the form" is better than "Click submit".

---

## verify()

> Check whether a visual condition is true on the current screen

```python
agent.verify(condition: str, timeout: int = 10, model: str | None = None) -> bool
```

Polls until the condition is met or the timeout expires.

### Parameters

| Parameter   | Type          | Default | Description                                           |
| ----------- | ------------- | ------- | ----------------------------------------------------- |
| `condition` | `str`         | —       | Natural language description of expected screen state |
| `timeout`   | `int`         | `10`    | Seconds to wait before returning `False`              |
| `model`     | `str \| None` | `None`  | Override the default model for this call              |

### Returns

`bool` — `True` if the condition is met within the timeout, `False` otherwise.

### Examples

```python
# Check login state
if agent.verify("Is the user logged in?"):
    print("Already logged in")

# Retry pattern
if not agent.verify("Is the search results page loaded?"):
    agent.execute("Click the Search button")

# Longer timeout for slow operations
if agent.verify("Has the file finished downloading?", timeout=30):
    print("Download complete")
```

---

## extract()

> Read structured data from the current screen

```python
agent.extract(query: str, schema: dict, model: str | None = None) -> dict | list
```

Returns data matching a JSON Schema.

### Parameters

| Parameter | Type          | Default | Description                              |
| --------- | ------------- | ------- | ---------------------------------------- |
| `query`   | `str`         | —       | What data to extract from the screen     |
| `schema`  | `dict`        | —       | JSON Schema defining the output format   |
| `model`   | `str \| None` | `None`  | Override the default model for this call |

### Returns

`dict | list` — Structured data matching the schema.

### Raises

- `WorkflowError` — on extraction failure
- `ValueError` — if schema is empty

### Examples

```python
# Inline schema
data = agent.extract(
    "What is the page title?",
    {"type": "object", "properties": {"title": {"type": "string"}}, "required": ["title"]}
)

# Using Pydantic models (recommended)
from pydantic import BaseModel

class ProductInfo(BaseModel):
    name: str
    price: float

data = agent.extract("Extract the product details", ProductInfo.model_json_schema())
product = ProductInfo.model_construct(**data)

# Model override for complex extraction
data = agent.extract(
    "Extract all visible invoice line items",
    InvoiceSchema.model_json_schema(),
    model="claude-sonnet-4-5-20250929"
)
```

> **Tip:** Use `YourModel.model_json_schema()` to generate the schema from your Pydantic models — this keeps your schema in sync with your types.
