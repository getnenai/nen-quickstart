# Agent

> VLM-powered controller for executing actions, verifying state, and extracting data

```python
from nen import Agent, Computer
```

## Constructor

```python
Agent(model: str | None = None)
```

| Parameter | Type          | Default | Description                                                                            |
| --------- | ------------- | ------- | -------------------------------------------------------------------------------------- |
| `model`   | `str \| None` | `None`  | Default VLM for all calls on this agent. If not set, defaults to `claude-sonnet-4-6`. |

Create an `Agent` instance inside your `run()` function:

```python
def run(params: Params) -> Result:
    agent = Agent()
    # ... use agent.execute(), agent.verify(), agent.extract()
```

---

## agent.execute()

> Perform an action on the screen using a natural language instruction

```python
agent.execute(description: str, max_iterations: int = 10) -> None
```

The VLM takes a screenshot, interprets the instruction, and performs the required interactions (clicks, typing, scrolling, navigation, etc.). It may take multiple steps to complete complex instructions.

### Parameters

| Parameter        | Type  | Default | Description                                                  |
| ---------------- | ----- | ------- | ------------------------------------------------------------ |
| `description`    | `str` | —       | Natural language description of what to do                   |
| `max_iterations` | `int` | `10`    | Maximum number of VLM steps to attempt before giving up      |

### Examples

```python
# Open Chromium browser (always use this exact pattern)
agent.execute("Click the Chromium browser icon in the taskbar (the blue circular icon, second from left)")

# Navigate to a URL
agent.execute(f"Navigate to {params.website}")

# Click a specific element
agent.execute("Click the blue 'Submit' button in the bottom right of the form")

# Fill a field (clear first, then type with Computer)
agent.execute("Click the email field")
computer.hotkey("ctrl", "a")
computer.press("BackSpace")
computer.type(params.email)

# Dismiss popups
agent.execute("Close any welcome messages, popups, or dialogs if they appear", max_iterations=5)

# Complex multi-step action
agent.execute("Fill in the entire registration form with test data", max_iterations=20)
```

> **Tip:** Write instructions as if you're telling a human what to do. Be specific about which element to interact with — "Click the blue 'Submit' button in the form footer" is better than "Click submit".

---

## agent.verify()

> Check whether a visual condition is true on the current screen

```python
agent.verify(condition: str, timeout: int = 10, model: str | None = None) -> bool
```

Polls until the condition is met or the timeout expires. Returns `True` if the condition is met, `False` otherwise.

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
# Check browser opened
if not agent.verify("Is the Chromium browser open?", timeout=10):
    raise RuntimeError("Failed to open Chromium browser")

# Check page loaded
if not agent.verify("Is the website loaded in the browser?", timeout=20):
    raise RuntimeError("Failed to load website")

# Check failure FIRST, then success (more reliable pattern)
if agent.verify("Are we still on the login page?", timeout=10):
    raise RuntimeError("Login failed — still on login page after submitting credentials")
if agent.verify("Is there an error message visible?"):
    raise RuntimeError("Login failed — error message displayed")
if not agent.verify("Is the dashboard visible?", timeout=20):
    raise RuntimeError("Unable to confirm login — dashboard not visible")

# Longer timeout for slow operations
if not agent.verify("Has the file finished downloading?", timeout=30):
    raise RuntimeError("Download timed out")
```

> **Tip:** Be specific in verification questions. "Is there an 'Invalid email' error message visible?" is better than "Did it work?". Always check failure indicators before success indicators.

---

## agent.extract()

> Read structured data from the current screen

```python
agent.extract(query: str, schema: dict) -> dict | list
```

Returns data matching a JSON Schema. The VLM takes a screenshot and extracts the requested information.

### Parameters

| Parameter | Type   | Default | Description                              |
| --------- | ------ | ------- | ---------------------------------------- |
| `query`   | `str`  | —       | What data to extract from the screen     |
| `schema`  | `dict` | —       | JSON Schema defining the output format   |

### Returns

`dict | list` — Structured data matching the schema.

### Examples

```python
# Extract using Result model's schema
data = agent.extract("What is the page title?", Result.model_json_schema())
return Result.model_construct(**data)

# Extract a single value with inline schema
result = agent.extract(
    "What is the page title?",
    schema={
        "type": "object",
        "properties": {"title": {"type": "string"}},
        "required": ["title"]
    }
)
title = result.get("title")

# Extract a list of items
items = agent.extract(
    "List all post titles on this page",
    schema={
        "type": "array",
        "items": {"type": "string"}
    }
)

# Extract a structured object
patient = agent.extract(
    "Extract the patient's demographic information",
    schema={
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "date_of_birth": {"type": "string"},
            "phone": {"type": "string"},
            "email": {"type": "string"}
        }
    }
)

# Extract a table / array of objects
appointments = agent.extract(
    "Extract all appointments visible in the calendar",
    schema={
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "time": {"type": "string"},
                "patient": {"type": "string"},
                "reason": {"type": "string"}
            },
            "required": ["time", "patient"]
        }
    }
)
```

> **Tip:** Always call `agent.verify()` to confirm the data is visible on screen before calling `agent.extract()`. This prevents extraction failures on the wrong page.
