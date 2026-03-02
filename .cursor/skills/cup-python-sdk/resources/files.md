# Files & Assets

> Reading files from mounted drives and writing output files from workflows

## Drive & Files

`Computer` provides access to files on mounted drives from the parent container via `computer.drive()`.

### computer.drive()

```python
computer.drive(path: str) -> Drive
```

Returns a `Drive` object for the given path. The path can be an absolute path or a `~`-prefixed home directory path.

```python
downloads = computer.drive("~/Downloads")   # home directory
mount = computer.drive("/mnt/tmp")          # absolute mount path
```

`Drive` objects also render as their path string in f-strings, so you can pass them directly to `agent.execute()`:

```python
drive = computer.drive("/mnt/tmp")
agent.execute(f"Save the file to {drive}")  # passes the path as a string
```

### Drive.files()

```python
drive.files() -> list[File]
```

Returns a list of `File` objects for all files currently in the drive directory (non-recursive).

```python
drive = computer.drive("~/Downloads")
for f in drive.files():
    print(f.name)  # filename only, e.g. "invoice_001.pdf"
```

### File

Each `File` object has:

| Attribute / Method | Type | Description |
| --- | --- | --- |
| `f.name` | `str` | Filename (basename only, no path) |
| `f.read_bytes()` | `bytes` | Full file contents as bytes |

---

## Two File Strategies

### Copy to sandbox (files appear in `assets.zip`)

Read files from a drive and write them to a local path inside the sandbox. Files in the sandbox are packaged into `assets.zip` when the run completes.

```python
from pathlib import Path
from nen import Agent, Computer

def run(params: Params) -> Result:
    agent = Agent()
    computer = Computer()

    downloads = computer.drive("~/Downloads")
    paid_path = Path("./paid")
    paid_path.mkdir(parents=True, exist_ok=True)

    agent.execute("Select all paid invoices and download them")
    for f in downloads.files():
        if f.name in params.selected_files:
            (paid_path / f.name).write_bytes(f.read_bytes())
```

### Stream to a mounted drive

Read files from one drive and write them directly to another mounted path. Use this for large files or when you want them delivered via the mount rather than `assets.zip`.

```python
drive_mount = computer.drive("/mnt/tmp")
agent.execute(f"Select all unpaid invoices and save to {drive_mount}")
for f in drive_mount.files():
    with open(f.name, "wb") as target:
        target.write(f.read_bytes())
```

---

## Output Directory

Workflows write output files to the `/artifacts/` directory. When the run completes, all files in `/artifacts/` are packaged into `assets.zip` and included in the API response.

```python
import json
import os
from pathlib import Path

# Create the artifacts directory (workflow output location — not the browser download folder)
os.makedirs("/artifacts", exist_ok=True)

# Write files
data = {"example": "value"}  # replace with your actual extracted data
Path("/artifacts/report.txt").write_text("Report content")
Path("/artifacts/data.json").write_text(json.dumps(data, indent=2))
```

> **Note:** Always call `os.makedirs("/artifacts", exist_ok=True)` before writing files to ensure the directory exists. `/artifacts/` is the workflow's designated output directory — files placed here are packaged into `assets.zip` on run completion.

---

## Common Pattern: Save Extracted Data as JSON

```python
import json
import os
from nen import Agent, Computer


def run(params: Params) -> Result:
    agent = Agent()
    computer = Computer()
    # ... navigate and extract data ...

    data = agent.extract("Extract all appointments", schema={...})

    os.makedirs("/artifacts", exist_ok=True)
    with open("/artifacts/appointments.json", "w") as f:
        json.dump(data, f, indent=2)

    # Verify the file was created
    if not os.path.exists("/artifacts/appointments.json"):
        return Result(success=False, error="Failed to save appointments file")

    return Result(success=True)
```

---

## Common Pattern: Count Downloaded Files

When a workflow triggers browser downloads, ensure the browser is configured to save files directly into `/artifacts/` (or move files there after download). The count below relies on files being present in `/artifacts/` — if your download target differs, move the files there first. Verify with `os.popen`:

```python
import os

# Count PDFs in artifacts
result = os.popen("ls /artifacts/*.pdf 2>/dev/null | wc -l").read().strip()
num_docs = int(result) if result.isdigit() else 0

if num_docs == 0:
    return Result(success=False, error="No PDF documents were downloaded")

return Result(success=True, documents_downloaded=num_docs)
```

---

## Common Pattern: Clear Previous Files

Before running a download workflow, clear any leftover files from previous runs:

```python
import os

os.system("rm -f /artifacts/*.pdf 2>/dev/null")
os.makedirs("/artifacts", exist_ok=True)
```

---

## Assets in API Response

When the run completes, files in `/artifacts/` are delivered with the result:

```json
{
  "success": true,
  "result": { "documents_downloaded": 3 },
  "assets": "https://s3.../assets.zip"
}
```

> **Tip:** Organize output files into subdirectories for clarity. The full directory structure is preserved in the zip archive.
