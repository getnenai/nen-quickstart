"""
Workflow: Minimal Valid Workflow

This is the absolute minimum valid workflow structure.
"""
from nen.workflow import agent
from pydantic import BaseModel


class Input(BaseModel):
    """Minimal input model."""
    
    url: str


class Output(BaseModel):
    """Minimal output model."""
    
    success: bool


def run(input: Input) -> Output:
    """
    Minimal workflow entry point.
    
    Args:
        input: Input parameters
    
    Returns:
        Output with success status
    """
    agent("Navigate to the website")
    return Output(success=True)
