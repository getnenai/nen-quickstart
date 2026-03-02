"""
Workflow: Web Navigation and Data Extraction

Navigates to a website and extracts the title and URL of a post or article
by index from a list page (e.g. Hacker News, a blog, or a news feed).
"""
from nen import Agent
from pydantic import BaseModel, Field


class Params(BaseModel):
    website_url: str = Field(default="https://news.ycombinator.com", min_length=1, description="URL of the list page")
    post_index: int = Field(default=0, ge=0, description="Zero-based index of the post to extract")


class Result(BaseModel):
    title: str = Field(min_length=1, description="Title of the post")
    url: str = Field(min_length=1, description="URL the post links to")


def run(params: Params) -> Result:
    agent = Agent()

    agent.execute("Click the Chromium browser icon in the taskbar (the blue circular icon, second from left)")
    if not agent.verify("Is the Chromium browser open?", timeout=10):
        raise RuntimeError("Failed to open Chromium browser")

    agent.execute(f"Navigate to {params.website_url}")
    if not agent.verify("Is the website loaded in the browser?", timeout=20):
        raise RuntimeError(f"Failed to load {params.website_url}")

    if not agent.verify("Is there a list of posts or articles visible?", timeout=10):
        raise RuntimeError("No list of posts or articles found on the page")

    data = agent.extract(
        f"What is the title and URL of post number {params.post_index + 1} in the list?",
        Result.model_json_schema(),
    )
    return Result.model_construct(**data)
