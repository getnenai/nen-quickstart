"""
Workflow: Missing Input Model

This workflow is INVALID - missing Input class.
"""
from nen.workflow import agent
from pydantic import BaseModel


# Input class is missing!


class Output(BaseModel):
    """Output model."""
    
    success: bool


def run(input: Input) -> Output:
    """
    Workflow entry point.
    
    Args:
        input: Input parameters
    
    Returns:
        Output with results
    """
    agent("Do something")
    return Output(success=True)
