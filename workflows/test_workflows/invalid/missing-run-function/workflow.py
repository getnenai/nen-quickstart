"""
Workflow: Missing Run Function

This workflow is INVALID - missing run() function.
"""
from nen.workflow import agent
from pydantic import BaseModel


class Input(BaseModel):
    """Input model."""
    
    url: str


class Output(BaseModel):
    """Output model."""
    
    success: bool


# run() function is missing!


def execute(input: Input) -> Output:
    """Wrong function name - should be 'run'."""
    agent("Do something")
    return Output(success=True)
