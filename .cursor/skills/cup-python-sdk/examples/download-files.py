"""Download Files — download multiple files from a desktop application.

Demonstrates:
- Extract list of items, then loop and act on each
- Download tracking with success/failure counting
- Graceful handling of failed downloads (continue)
- Counting downloaded files via loop success tracking
"""

from pathlib import Path
from nen import Agent
from pydantic import BaseModel, Field

ARTIFACTS_DIR = Path("/artifacts")


class Params(BaseModel):
    """Input parameters for this workflow."""
    patient_name: str = Field(min_length=1)


class Result(BaseModel):
    """Output returned by this workflow."""
    downloaded: int = 0
    files: list[str] = []


def run(params: Params) -> Result:
    agent = Agent()

    # Clear previous downloads
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    for f in ARTIFACTS_DIR.glob("*.pdf"):
        f.unlink(missing_ok=True)

    # Navigate to documents section
    agent.execute(f"Navigate to patient '{params.patient_name}' documents")

    if not agent.verify("Is the documents list visible?", timeout=15):
        raise RuntimeError("Documents list not visible")

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
        raise RuntimeError("No documents were downloaded successfully")

    return Result(downloaded=len(downloaded_files), files=downloaded_files)
