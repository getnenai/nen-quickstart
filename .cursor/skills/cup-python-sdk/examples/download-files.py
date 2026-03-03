"""Download Files — download multiple files from a desktop application.

Demonstrates:
- Extract list of items, then loop and act on each
- Download tracking with success/failure counting
- Graceful handling of failed downloads (continue)
- Counting downloaded files via loop success tracking
"""

from pathlib import Path
from nen import Agent, Computer
from pydantic import BaseModel, Field

ARTIFACTS_DIR = Path("/artifacts")


class Params(BaseModel):
    patient_name: str = Field(min_length=1)


class Result(BaseModel):
    success: bool
    downloaded: int = 0
    files: list[str] = []
    error: str | None = None


def run(params: Params) -> Result:
    agent = Agent()
    computer = Computer()

    # Clear previous downloads
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    for f in ARTIFACTS_DIR.glob("*.pdf"):
        f.unlink(missing_ok=True)

    # Navigate to documents section
    agent.execute(f"Navigate to patient '{params.patient_name}' documents")

    if not agent.verify("Is the documents list visible?", timeout=15):
        return Result(success=False, error="Documents list not visible")

    # Discover available documents
    documents = agent.extract(
        "List all downloadable document names",
        schema={"type": "array", "items": {"type": "string"}}
    )

    print(f"Found {len(documents)} documents to download")

    # Download each document
    downloaded_files = []
    for doc in documents:
        agent.execute(f"Click on document '{doc}'")
        agent.execute("Click the download button")

        if not agent.verify("Is the download complete or save dialog shown?", timeout=30):
            print(f"Warning: Download may have failed for {doc}")
            continue

        downloaded_files.append(doc)

    if not downloaded_files:
        return Result(success=False, error="No documents were downloaded successfully")

    return Result(success=True, downloaded=len(downloaded_files), files=downloaded_files)
