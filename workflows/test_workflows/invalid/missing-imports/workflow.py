"""
Workflow: Missing Imports

This workflow is INVALID - missing required imports.
"""
# Missing: from nen.workflow import agent
# Missing: from pydantic import BaseModel


class Input:
    """Input model - but BaseModel not imported."""
    
    url: str


class Output:
    """Output model - but BaseModel not imported."""
    
    success: bool


def run(input: Input) -> Output:
    """
    Workflow entry point.
    
    Args:
        input: Input parameters
    
    Returns:
        Output with results
    """
    agent("Do something")  # agent not imported
    return Output(success=True)
