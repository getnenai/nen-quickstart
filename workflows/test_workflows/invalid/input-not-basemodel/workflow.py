"""
Workflow: Input Not BaseModel

This workflow is INVALID - Input class doesn't inherit from BaseModel.
"""
from nen.workflow import agent
from pydantic import BaseModel


class Input:
    """Input model - but NOT inheriting from BaseModel."""
    
    def __init__(self, url: str):
        self.url = url


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
