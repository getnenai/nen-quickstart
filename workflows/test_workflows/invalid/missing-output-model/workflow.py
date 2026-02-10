"""
Workflow: Missing Output Model

This workflow is INVALID - missing Output class.
"""
from nen.workflow import agent
from pydantic import BaseModel


class Input(BaseModel):
    """Input model."""
    
    url: str


# Output class is missing!


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
