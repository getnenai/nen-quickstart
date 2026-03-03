# Computer

> Direct keyboard, mouse, and filesystem access inside the sandbox

```python
from nen import Agent, Computer
```

> **Prefer `agent.execute()` for interactions that require finding elements visually.** Use `Computer` when you need precise, direct control — for example, typing text after clicking a field, or using keyboard shortcuts.

Create a `Computer` instance inside your `run()` function:

```python
def run(params: Params) -> Result:
    agent = Agent()
    computer = Computer()
    # ... use computer.type/press/hotkey and computer.mouse
```

---

## Keyboard Methods

Keyboard methods are called **directly on `computer`** — there is no `computer.keyboard` sub-object.

### type()

```python
computer.type(text: str | SecureValue, interval: float = 0.02) -> None
```

Type text character by character. Also accepts `SecureValue` references for secrets.

| Parameter  | Type                 | Default | Description                |
| ---------- | -------------------- | ------- | -------------------------- |
| `text`     | `str \| SecureValue` | —       | Text to type               |
| `interval` | `float`              | `0.02`  | Seconds between keystrokes |

```python
computer.type("hello@example.com")
computer.type(params.username)
# For secrets, use Secure[str] in SecureParams — never store passwords in plain Params
computer.type(secure_params.password, interval=0.01)
```

> **Important:** Always clear the field before typing. Use `agent.execute()` to select-all and delete any pre-existing content, then type.

### press()

```python
computer.press(key: str) -> None
```

Press a single key.

**Available keys:** `Return`, `Tab`, `Escape`, `BackSpace`, `Delete`, `Up`, `Down`, `Left`, `Right`, `Home`, `End`, `Page_Up`, `Page_Down`, `F1`–`F12`.

```python
computer.press("Return")    # submit form / confirm
computer.press("Tab")       # move to next field
computer.press("Escape")    # close dialog
computer.press("BackSpace") # delete character
```

### hotkey()

```python
computer.hotkey(*keys: str) -> None
```

Press a key combination simultaneously.

**Modifiers:** `ctrl`, `alt`, `shift`, `super`. Always use Linux/Windows modifiers — `command` is macOS-only and will crash.

```python
computer.hotkey("ctrl", "a")         # select all
computer.hotkey("ctrl", "c")         # copy
computer.hotkey("ctrl", "v")         # paste
computer.hotkey("ctrl", "shift", "s") # save as
computer.hotkey("shift", "Tab")      # reverse tab
```

---

## computer.drive()

`Computer` provides access to files on mounted drives from the parent container. See `files.md` for the full API reference including the `Drive` and `File` objects, file listing, reading, and streaming patterns.

```python
drive = computer.drive("~/Downloads")   # home directory path
mount = computer.drive("/mnt/tmp")      # absolute mount path

for f in drive.files():
    data = f.read_bytes()   # read file contents
    print(f.name)           # filename (basename only)
```

---

## computer.mouse

> Use mouse methods when you have exact screen coordinates. Otherwise, prefer `agent.execute()` to locate and click elements visually.

### click_at()

```python
computer.mouse.click_at(x: int, y: int, button: str = "left") -> None
```

Click at specific screen coordinates.

| Parameter | Type  | Default  | Description           |
| --------- | ----- | -------- | --------------------- |
| `x`       | `int` | —        | X coordinate          |
| `y`       | `int` | —        | Y coordinate          |
| `button`  | `str` | `"left"` | `"left"` or `"right"` |

```python
computer.mouse.click_at(100, 200)                   # left click
computer.mouse.click_at(100, 200, button="right")   # right click
```

### move()

```python
computer.mouse.move(x: int, y: int) -> None
```

Move the cursor to a position without clicking.

```python
computer.mouse.move(500, 300)
```

### scroll()

```python
computer.mouse.scroll(direction: str = "down", amount: int = 3, x: int | None = None, y: int | None = None) -> None
```

| Parameter   | Type          | Default  | Description            |
| ----------- | ------------- | -------- | ---------------------- |
| `direction` | `str`         | `"down"` | `"up"` or `"down"`     |
| `amount`    | `int`         | `3`      | Number of scroll ticks |
| `x`         | `int \| None` | `None`   | Scroll at X coordinate |
| `y`         | `int \| None` | `None`   | Scroll at Y coordinate |

```python
computer.mouse.scroll()                         # scroll down 3 ticks
computer.mouse.scroll("up", 5)                  # scroll up 5 ticks
computer.mouse.scroll("down", 3, x=400, y=300) # scroll at position
```
