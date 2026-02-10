"""
Workflow: Run Wrong Args

This workflow is INVALID - run() has wrong number of arguments.
"""
from nen.workflow import agent
from pydantic import BaseModel


class Input(BaseModel):
    """Input model."""
    
    url: str


class Output(BaseModel):
    """Output model."""
    
    success: bool


def run(input: Input, extra_param: str, another: int) -> Output:
    """
    Wrong signature - should only take 'input' parameter.
    
    Args:
        input: Input parameters
        extra_param: Extra parameter (invalid)
        another: Another parameter (invalid)
    
    Returns:
        Output with results
    """
    agent("Do something")
    return Output(success=True)
