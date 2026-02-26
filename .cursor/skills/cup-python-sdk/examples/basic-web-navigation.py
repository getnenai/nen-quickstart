"""Basic Web Navigation — navigate to a website and extract data."""

from nen import Agent
from pydantic import BaseModel, Field


class Params(BaseModel):
    website_url: str = Field(default="https://news.ycombinator.com", min_length=1)
    post_index: int = Field(default=0, ge=0)


class Result(BaseModel):
    title: str


def run(params: Params) -> Result:
    agent = Agent()

    # Navigate to website
    agent.execute(f"Open the browser and navigate to {params.website_url}")

    # Validate we reached the expected state
    if not agent.verify("Is the website loaded in the browser?"):
        raise RuntimeError("Failed to load website")

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

    return Result(title=result["title"])
