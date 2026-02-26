# Files & Assets

> Sandbox filesystem, assets.zip, and drive access

## Sandbox Filesystem

Your workflow runs inside a sandbox container. Any files you write there are archived into `assets.zip` when the run completes.

```python
from pathlib import Path

# Create output directories
Path("./reports").mkdir(parents=True, exist_ok=True)

# Write files — these end up in assets.zip
Path("./reports/summary.txt").write_text("Report content")
```

---

## Drive Access

Use `Computer.drive()` to access files from the parent container (outside the sandbox).

```python
computer.drive(path: str) -> Drive
```

> **Warning:** Drive access reads files from the parent container outside the sandbox. The sandbox filesystem at `/assets` is a tmpfs — files written there are archived to `assets.zip` when the run completes.

### Mount a directory

```python
from nen import Computer

computer = Computer()
downloads = computer.drive("~/Downloads")
mount = computer.drive("/mnt/tmp")
```

### List files

```python
drive.files(pattern: str = "*") -> list[File]
```

```python
downloads = computer.drive("~/Downloads")

# List all files
for f in downloads.files():
    print(f.name, f.size)

# Filter by glob pattern
for f in downloads.files("*.pdf"):
    print(f.name)
```

### Copy files to sandbox

```python
from pathlib import Path

downloads = computer.drive("~/Downloads")
Path("./output").mkdir(parents=True, exist_ok=True)

for f in downloads.files("*.pdf"):
    (Path("./output") / f.name).write_bytes(f.read_bytes())
```

### Stream large files

```python
downloads = computer.drive("~/Downloads")
for f in downloads.files("*.csv"):
    with open(f.name, 'w') as target:
        target.write(f.read_text())
```

---

## File Object

| Property   | Type       | Description             |
| ---------- | ---------- | ----------------------- |
| `name`     | `str`      | Filename                |
| `size`     | `int`      | Size in bytes           |
| `modified` | `datetime` | Last modified timestamp |

### read_bytes()

```python
file.read_bytes() -> bytes
```

Read file content as bytes. Use for binary files (PDFs, images, etc.).

### read_text()

```python
file.read_text(encoding: str = "utf-8") -> str
```

Read file content as decoded string. Use for text files (CSVs, logs, configs). Accepts any Python codec name (`"utf-16"`, etc.).

---

## Assets in Webhook Response

When the run completes, files in the working directory are archived and delivered with the webhook:

```json
{
  "success": true,
  "result": { "customer_id": "ABC123" },
  "assets": "https://s3.../assets.zip"
}
```

> **Tip:** Organize output files into subdirectories for clarity. The full directory structure is preserved in the zip archive.

---

## Common Pattern: Download and Save

```python
from pathlib import Path
from nen import Agent, Computer

def run(params: Params) -> Result:
    agent = Agent()
    computer = Computer()

    # Trigger a download in the application
    agent.execute("Click the Export CSV button")
    agent.verify("Has the file finished downloading?", timeout=30)

    # Copy from Downloads to sandbox
    downloads = computer.drive("~/Downloads")
    Path("./exports").mkdir(parents=True, exist_ok=True)
    for f in downloads.files("*.csv"):
        (Path("./exports") / f.name).write_text(f.read_text())
```
