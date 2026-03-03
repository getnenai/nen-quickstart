# Agent

> VLM-driven controller for executing actions, verifying screen state, and extracting structured data.

```python
from nen import Agent, Computer
```

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
computer.keyboard.hotkey("ctrl", "a")
computer.keyboard.press("BackSpace")
computer.keyboard.type(params.email)

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
agent.verify(question: str, timeout: int = 10) -> bool
```

Polls until the condition is met or the timeout expires. Returns `True` if the condition is met, `False` otherwise.

### Parameters

| Parameter  | Type  | Default | Description                                           |
| ---------- | ----- | ------- | ----------------------------------------------------- |
| `question` | `str` | —       | Natural language yes/no question about the screen     |
| `timeout`  | `int` | `10`    | Seconds to wait before returning `False`              |

### Returns

`bool` — `True` if the condition is met within the timeout, `False` otherwise.

### Examples

```python
# Check browser opened
if not agent.verify("Is the Chromium browser open?", timeout=10):
    return Result(success=False, error="Failed to open browser")

# Check page loaded
if not agent.verify("Is the website loaded in the browser?", timeout=20):
    return Result(success=False, error="Failed to load website")

# Check failure FIRST, then success (more reliable pattern)
if agent.verify("Are we still on the login page?", timeout=10):
    return Result(success=False, error="Login failed - still on login page")
elif agent.verify("Is there an error message visible?"):
    return Result(success=False, error="Login failed - error message displayed")
elif agent.verify("Is the dashboard visible?", timeout=20):
    return Result(success=True)
else:
    return Result(success=False, error="Unable to verify login state")

# Longer timeout for slow operations
if not agent.verify("Has the file finished downloading?", timeout=30):
    return Result(success=False, error="Download timed out")
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
