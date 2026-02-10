"""
Workflow: Invalid Pydantic Model

This workflow is INVALID - malformed Pydantic model.
"""
from nen.workflow import agent
from pydantic import BaseModel


class Input(BaseModel):
    """Input model with invalid syntax."""
    
    url str  # Missing colon


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
