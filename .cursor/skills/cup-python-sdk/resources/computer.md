# Computer

> Direct keyboard, mouse, and filesystem access inside the sandbox

```python
from nen import Computer

computer = Computer()
```

## Constructor

```python
Computer()
```

Takes no arguments. Reads configuration from environment variables set by the sandbox runtime.

---

## Drive & Files

`Computer` provides access to files on mounted drives from the parent container. See `files.md` for the full API reference including `Drive` and `File` objects, file listing, reading, and streaming patterns.

---

## Keyboard

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
computer.type("slow input", interval=0.05)

# Type a secret — value never enters the sandbox
computer.type(secure_params.password)
```

### press()

```python
computer.press(key: str) -> None
```

Press a single key.

**Available keys:** `Return`, `Tab`, `Escape`, `BackSpace`, `Delete`, `Up`, `Down`, `Left`, `Right`, `Home`, `End`, `Page_Up`, `Page_Down`, `F1`–`F12`.

```python
computer.press("Return")
computer.press("Tab")
computer.press("Escape")
```

### hotkey()

```python
computer.hotkey(*keys: str) -> None
```

Press a key combination.

**Modifiers:** `ctrl`, `alt`, `shift`, `super`.

```python
computer.hotkey("ctrl", "c")
computer.hotkey("ctrl", "shift", "s")
```

---

## Mouse

> Prefer `Agent.execute()` for interactions that require finding elements visually. Use `Computer` mouse methods when you know exact coordinates.

### click_at()

```python
computer.click_at(x: int, y: int, button: str = "left") -> None
```

Click at specific screen coordinates.

| Parameter | Type  | Default  | Description           |
| --------- | ----- | -------- | --------------------- |
| `x`       | `int` | —        | X coordinate          |
| `y`       | `int` | —        | Y coordinate          |
| `button`  | `str` | `"left"` | `"left"` or `"right"` |

```python
computer.click_at(100, 200)                    # Left click
computer.click_at(100, 200, button="right")    # Right click
```

### move()

```python
computer.move(x: int, y: int) -> None
```

Move the cursor without clicking.

```python
computer.move(500, 300)
```

### scroll()

```python
computer.scroll(direction: str = "down", amount: int = 3, x: int | None = None, y: int | None = None) -> None
```

| Parameter   | Type          | Default  | Description            |
| ----------- | ------------- | -------- | ---------------------- |
| `direction` | `str`         | `"down"` | `"up"` or `"down"`     |
| `amount`    | `int`         | `3`      | Number of scroll ticks |
| `x`         | `int \| None` | `None`   | Scroll at X coordinate |
| `y`         | `int \| None` | `None`   | Scroll at Y coordinate |

```python
computer.scroll()                          # Scroll down 3 ticks
computer.scroll("up", 5)                   # Scroll up 5 ticks
computer.scroll("down", 3, x=400, y=300)  # Scroll at position
```
