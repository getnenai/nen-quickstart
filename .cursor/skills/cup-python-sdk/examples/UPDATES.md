# Example Updates - Aligned with Workspace Rules

All examples have been updated to align with the workspace conventions defined in `.cursor/rules/`.

## Changes Applied

### 1. Computer API Updates

**Before:**
```python
computer.keyboard.type(params.username)
computer.keyboard.press("Return")
computer.keyboard.hotkey("ctrl", "a")
```

**After:**
```python
computer.type(params.username)
computer.press("Return")
# Note: Do not clear fields - just type directly
```

**Reason:** 
- `computer.keyboard.*` methods are deprecated - use flat API: `computer.type()`, `computer.press()`
- `computer.hotkey()` is broken and unreliable
- Fields should not be cleared before typing - just type directly into clicked fields

### 2. Error Handling Convention

**Before:**
```python
if not agent.verify("Is the Chromium browser open?", timeout=10):
    return Result(success=False, error="Failed to open browser")

if not agent.verify("Is the page loaded?", timeout=20):
    return Result(success=False, error="Failed to load page")
```

**After:**
```python
if not agent.verify("Is the Chromium browser open?", timeout=10):
    raise RuntimeError("Failed to open Chromium browser")

if not agent.verify("Is the page loaded?", timeout=30):
    raise RuntimeError(f"Failed to load page at {params.url}")
```

**Reason:**
- **ALL failures use `raise`** - browser won't open, site unreachable, login failed, extraction failed
- **Result models actual data, not success/failure envelope**
- No `success: bool` or `error: str | None` fields in Result
- Workflows either succeed (return Result with data) or fail (raise exception)

### 3. Result Models Actual Data (Not Success/Failure Envelope)

**Before:**
```python
class Result(BaseModel):
    success: bool
    data: dict | None = None
    error: str | None = None
```

**After:**
```python
class Result(BaseModel):
    """Output returned by this workflow."""
    title: str  # Actual data being extracted
    url: str    # Actual data being extracted
```

**Reason:** 
- Result models the actual data being extracted/returned
- No `success: bool` or `error: str | None` fields
- Use `raise` for all failures instead of returning Result(success=False)
- Workflows either succeed (return Result with data) or fail (raise exception)

### 4. Model Docstrings

**Before:**
```python
class Params(BaseModel):
    username: str

class SecureParams(BaseModel):
    password: Secure[str]
```

**After:**
```python
class Params(BaseModel):
    """Input parameters for this workflow."""
    username: str

class SecureParams(BaseModel):
    """Secure parameters for this workflow."""
    password: Secure[str]
```

**Reason:** Consistent documentation style across all examples

### 5. Timeout Adjustments

**Before:**
```python
if not agent.verify("Is the website loaded?", timeout=20):
```

**After:**
```python
if not agent.verify("Is the website loaded?", timeout=30):
```

**Reason:** Page loads can be slow - increased timeout from 20s to 30s for more reliability

## Files Updated

1. ✅ `login-with-popup.py` - Computer API, error handling, docstrings
2. ✅ `basic-web-navigation.py` - Error handling, docstrings, timeouts
3. ✅ `extract-data-from-screen.py` - Docstrings
4. ✅ `download-files.py` - Docstrings
5. ✅ `multi-step-pipeline.py` - Computer API, error handling, docstrings
6. ✅ `process-multiple-items.py` - Docstrings

## Key Conventions Followed

### Error Handling Pattern

| Condition | Pattern |
|-----------|---------|
| Browser won't open | `raise RuntimeError("Failed to open Chromium browser")` |
| Site unreachable | `raise RuntimeError(f"Failed to load {url}")` |
| Login failed | `raise RuntimeError("Login failed - still on login page")` |
| Extraction returned nothing | `raise ValueError("Extraction returned no content")` |
| Item not found | `raise RuntimeError("Item not found")` |
| **ALL failures** | **Use `raise` - never return Result(success=False)** |

### Computer API

| Task | Correct Method |
|------|---------------|
| Type text | `computer.type(text)` |
| Press key | `computer.press("Return")` |
| Mouse click | `computer.mouse.click_at(x, y)` |
| Note | Do not clear fields - just type directly |

### Result Models

- **Result models actual data, not success/failure envelope**
- No `success: bool` or `error: str | None` fields
- Define fields for the data being extracted (e.g., `title: str`, `customer_id: str`)
- Workflows either succeed (return Result with data) or fail (raise exception)

### SecureParams

- Always use `Secure[str]` for passwords, API keys, tokens
- Never use `default=` on `SecureParams` fields
- Platform injects secrets at runtime

### Verification

- Check failure indicators FIRST, then success
- Use specific questions: "Is there an 'Invalid email' error?" not "Did it work?"
- Use appropriate timeouts: 10s for browser, 30s for page loads
- Raise exceptions for all failures - never return Result(success=False)

## Testing

All examples have been syntax-checked and align with:
- `.cursor/rules/workflow-creation-process.mdc`
- `.cursor/rules/workflow-error-handling.mdc`
- `.cursor/rules/workflow-secure-params.mdc`
- `.cursor/rules/workflow-core.mdc`
