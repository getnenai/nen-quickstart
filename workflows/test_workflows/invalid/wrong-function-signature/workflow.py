"""
Workflow: Wrong Function Signature

This workflow is INVALID - run() has wrong signature.
"""
from nen.workflow import agent
from pydantic import BaseModel


class Input(BaseModel):
    """Input model."""
    
    url: str


class Output(BaseModel):
    """Output model."""
    
    success: bool


def run(params: dict) -> dict:
    """
    Wrong signature - should be run(input: Input) -> Output.
    
    Args:
        params: Wrong parameter type
    
    Returns:
        Wrong return type
    """
    agent("Do something")
    return {"success": True}
