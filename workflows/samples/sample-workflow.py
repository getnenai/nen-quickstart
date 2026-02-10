"""
Workflow: SDK Primitives Test

This workflow demonstrates the nen.workflow SDK primitives.
Modify this file to build your automation workflow.
"""
from nen.workflow import agent, validate, extract
from pydantic import BaseModel, Field


class Input(BaseModel):
    """Input parameters for this workflow.
    
    Define your workflow's input variables here.
    These will be provided when the workflow is executed.
    """
    
    website_url: str = Field(default="https://news.ycombinator.com", min_length=1)
    post_index: int = Field(default=0, ge=0)


class Output(BaseModel):
    """Output returned by this workflow.
    
    Define the structured data your workflow returns.
    """
    
    success: bool
    title: str | None = None
    error: str | None = None


def run(input: Input) -> Output:
    """
    Main workflow entry point.

    Args:
        input: Pydantic model with workflow input parameters.

    Returns:
        Output model with workflow results.
    """
    # Use natural language to control the computer
    agent("Click the Chromium browser icon in the taskbar (the blue circular icon, second from left)")
    agent(f"Navigate to {input.website_url}")

    # Validate that we reached the expected state
    if not validate("Is the website loaded in the browser?"):
        return Output(
            success=False,
            error="Failed to load website"
        )

    # Extract structured data from the screen
    result = extract(
        f"What is the title of post {input.post_index + 1}?",
        schema={
            "type": "object",
            "properties": {
                "title": {"type": "string"}
            },
            "required": ["title"]
        }
    )

    return Output(
        success=True,
        title=result.get("title")
    )
