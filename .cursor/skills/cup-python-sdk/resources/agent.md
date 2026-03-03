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
agent.execute(instruction: str, model: str | None = None, max_iterations: int | None = None) -> None
```

The VLM takes a screenshot, interprets the instruction, and performs the required interactions (clicks, typing, scrolling, navigation, etc.). It may take multiple steps to complete complex instructions.

### Parameters

| Parameter        | Type              | Default | Description                                                  |
| ---------------- | ----------------- | ------- | ------------------------------------------------------------ |
| `instruction`    | `str`             | —       | Natural language description of what to do                   |
| `model`          | `str \| None`     | `None`  | Override the default model for this call                     |
| `max_iterations` | `int \| None`     | `None`  | Max screenshot→action loops the agent will attempt (server defaults to **10** when not specified) |

### Understanding `max_iterations`

Each `execute()` call runs in a **screenshot → think → act** loop. One iteration = one cycle of:

1. Take a screenshot of the current screen
2. Send it to the VLM with the instruction
3. VLM decides and performs an action (click, type, scroll, etc.)

`max_iterations` caps how many of these loops can run before the agent stops. This is useful for:

- **Simple actions** (clicking a button): Lower values like `3`–`5` prevent the agent from spinning if it can't find the element.
- **Complex multi-step actions** (filling a form, navigating menus): Higher values like `15`–`20` give the agent enough room to complete all steps.
- **Default behavior**: When omitted, the server defaults to **10** iterations, which works well for most common tasks.

> **When to increase:** If your instruction involves multiple sequential interactions (e.g., filling several fields, navigating through menus), bump it up.
>
> **When to decrease:** If you want fast failure for simple one-click actions, lower it to avoid wasting time on retries.

### Examples

```python
# Open Chromium browser (always use this exact pattern)
agent.execute("Click the Chromium browser icon in the taskbar (the blue circular icon, second from left)")

# Navigate to a URL
agent.execute(f"Navigate to {params.website}")

# Click a specific element
agent.execute("Click the blue 'Submit' button in the bottom right of the form")

# Fill a field (just type directly with Computer)
agent.execute("Click the email field")
computer.type(params.email)

# Simple click — cap at 5 to fail fast if the button isn't visible
agent.execute("Click the Submit button", max_iterations=5)

# Dismiss popups
agent.execute("Close any welcome messages, popups, or dialogs if they appear", max_iterations=5)

# Multi-step form fill — needs more iterations to complete all fields
agent.execute(
    "Fill in the registration form with name 'Jane Doe', email 'jane@example.com', and select 'Premium' plan",
    max_iterations=20,
)

# Default (None) — server uses 10 iterations, good for most tasks
agent.execute("Open Chromium and navigate to https://example.com")
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
