"""
Workflow: Syntax Error

This workflow is INVALID - contains Python syntax error.
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
    Workflow with syntax error.
    
    Args:
        input: Input parameters
    
    Returns:
        Output with results
    """
    agent("Do something")
    
    # Syntax error - missing closing parenthesis
    return Output(success=True
