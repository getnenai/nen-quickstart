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
agent.execute("Select all text in the field using keyboard shortcut")
```

**Reason:** 
- `computer.keyboard.*` methods are deprecated - use flat API: `computer.type()`, `computer.press()`
- `computer.hotkey()` is broken and unreliable - use `agent.execute()` for key combinations

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
- **Unrecoverable failures** (browser won't open, site unreachable) → `raise RuntimeError("...")`
- **Expected failures** (wrong password, item not found) → `return Result(success=False, error="...")`
- Browser and page loading failures are unrecoverable - nothing can proceed without them

### 3. Model Docstrings

**Before:**
```python
class Params(BaseModel):
    username: str

class SecureParams(BaseModel):
    password: Secure[str]

class Result(BaseModel):
    success: bool
```

**After:**
```python
class Params(BaseModel):
    """Input parameters for this workflow."""
    username: str

class SecureParams(BaseModel):
    """Secure parameters for this workflow."""
    password: Secure[str]

class Result(BaseModel):
    """Output returned by this workflow."""
    success: bool
```

**Reason:** Consistent documentation style across all examples

### 4. Timeout Adjustments

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
| Extraction returned nothing | `raise ValueError("Extraction returned no content")` |
| Wrong password | `return Result(success=False, error="Login failed")` |
| Item not found | `return Result(success=False, error="Item not found")` |

### Computer API

| Task | Correct Method |
|------|---------------|
| Type text | `computer.type(text)` |
| Press key | `computer.press("Return")` |
| Key combination | `agent.execute("Select all text using keyboard shortcut")` |
| Mouse click | `computer.mouse.click_at(x, y)` |

### SecureParams

- Always use `Secure[str]` for passwords, API keys, tokens
- Never use `default=` on `SecureParams` fields
- Platform injects secrets at runtime

### Verification

- Check failure indicators FIRST, then success
- Use specific questions: "Is there an 'Invalid email' error?" not "Did it work?"
- Use appropriate timeouts: 10s for browser, 30s for page loads

## Testing

All examples have been syntax-checked and align with:
- `.cursor/rules/workflow-creation-process.mdc`
- `.cursor/rules/workflow-error-handling.mdc`
- `.cursor/rules/workflow-secure-params.mdc`
- `.cursor/rules/workflow-core.mdc`
