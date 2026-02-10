"""
Workflow: Wrong Return Type

This workflow is INVALID - run() returns wrong type.
"""
from nen.workflow import agent
from pydantic import BaseModel


class Input(BaseModel):
    """Input model."""
    
    url: str


class Output(BaseModel):
    """Output model."""
    
    success: bool


def run(input: Input) -> Output:
    """
    Workflow entry point.
    
    Args:
        input: Input parameters
    
    Returns:
        Should return Output, but returns dict instead
    """
    agent("Do something")
    # Wrong: returning dict instead of Output model
    return {"success": True}
