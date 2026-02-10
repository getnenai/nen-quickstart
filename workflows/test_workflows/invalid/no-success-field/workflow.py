"""
Workflow: No Success Field

This workflow is INVALID - Output model missing success field.
"""
from nen.workflow import agent
from pydantic import BaseModel


class Input(BaseModel):
    """Input model."""
    
    url: str


class Output(BaseModel):
    """Output model without success field."""
    
    # Missing: success: bool
    message: str
    data: dict | None = None


def run(input: Input) -> Output:
    """
    Workflow entry point.
    
    Args:
        input: Input parameters
    
    Returns:
        Output without success field
    """
    agent("Do something")
    return Output(message="Done", data={})
