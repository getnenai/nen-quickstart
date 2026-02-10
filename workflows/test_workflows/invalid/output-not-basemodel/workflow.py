"""
Workflow: Output Not BaseModel

This workflow is INVALID - Output class doesn't inherit from BaseModel.
"""
from nen.workflow import agent
from pydantic import BaseModel


class Input(BaseModel):
    """Input model."""
    
    url: str


class Output:
    """Output model - but NOT inheriting from BaseModel."""
    
    def __init__(self, success: bool):
        self.success = success


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
