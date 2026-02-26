"""Download Files — download multiple files from a desktop application.

Note: File download support is currently a preview feature.

Demonstrates:
- Extract list of items, then loop and act on each
- Download tracking with success/failure counting
- Graceful handling of failed downloads (continue)
"""

from nen import Agent, Computer
from pydantic import BaseModel, Field


class Params(BaseModel):
    patient_name: str = Field(min_length=1)


class Result(BaseModel):
    downloaded: int = 0
    files: list[str] = []


def run(params: Params) -> Result:
    agent = Agent()
    computer = Computer()

    # Navigate to documents section
    agent.execute(f"Navigate to patient '{params.patient_name}' documents")

    if not agent.verify("Is the documents list visible?"):
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

        if not agent.verify("Is the download complete or save dialog shown?"):
            print(f"Warning: Download may have failed for {doc}")
            continue

        downloaded_files.append(doc)

    return Result(downloaded=len(downloaded_files), files=downloaded_files)
