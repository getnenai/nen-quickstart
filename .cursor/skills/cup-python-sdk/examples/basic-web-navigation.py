"""Basic Web Navigation — navigate to a website and extract data."""

from nen import Agent, Computer
from pydantic import BaseModel, Field


class Params(BaseModel):
    website_url: str = Field(default="https://news.ycombinator.com", min_length=1)
    post_index: int = Field(default=0, ge=0)


class Result(BaseModel):
    success: bool
    title: str | None = None
    error: str | None = None


def run(params: Params) -> Result:
    agent = Agent()
    computer = Computer()

    # Open browser
    agent.execute("Click the Chromium browser icon in the taskbar (the blue circular icon, second from left)")
    if not agent.verify("Is the Chromium browser open?", timeout=10):
        return Result(success=False, error="Failed to open browser")

    # Navigate to website
    agent.execute(f"Navigate to {params.website_url}")
    if not agent.verify("Is the website loaded in the browser?", timeout=20):
        return Result(success=False, error="Failed to load website")

    # Extract structured data
    result = agent.extract(
        f"What is the title of post {params.post_index + 1}?",
        schema={
            "type": "object",
            "properties": {
                "title": {"type": "string"}
            },
            "required": ["title"]
        }
    )

    return Result(success=True, title=result.get("title"))
