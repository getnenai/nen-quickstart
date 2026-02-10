"""
Workflow: MCP Test Workflow

A simple test workflow to validate MCP tool functionality.
Opens Chromium browser and navigates to a test URL.
"""
from nen.workflow import agent, validate
from pydantic import BaseModel, Field


class Input(BaseModel):
    """Input parameters for test workflow."""
    
    test_url: str = Field(default="https://example.com", min_length=1)


class Output(BaseModel):
    """Output returned by test workflow."""
    
    success: bool
    error: str | None = None


def run(input: Input) -> Output:
    """
    Main workflow entry point for test automation.
    
    Args:
        input: Pydantic model with test URL
    
    Returns:
        Output model indicating success/failure
    """
    # Open Chromium browser
    agent("Click the Chromium browser icon in the taskbar (the blue circular icon, second from left)")
    if not validate("Is the Chromium browser open?", timeout=10):
        return Output(success=False, error="Failed to open Chromium browser")
    
    # Navigate to test URL
    agent(f"Navigate to {input.test_url}")
    if not validate("Is the page loaded?", timeout=20):
        return Output(success=False, error="Failed to load page")
    
    return Output(success=True)
