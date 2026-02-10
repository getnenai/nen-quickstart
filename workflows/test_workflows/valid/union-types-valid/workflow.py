"""
Workflow: Union Types Valid

Tests workflows with Union type annotations.
"""
from nen.workflow import agent
from pydantic import BaseModel


class Input(BaseModel):
    """Input with union types."""
    
    value: str | int
    optional_data: dict | list | None = None


class Output(BaseModel):
    """Output with union types."""
    
    success: bool
    result: str | int | float | None = None
    data: dict | list = []


def run(input: Input) -> Output:
    """
    Workflow with union types.
    
    Args:
        input: Input with union types
    
    Returns:
        Output with union type results
    """
    agent("Process the value")
    
    if isinstance(input.value, str):
        result = input.value.upper()
    else:
        result = input.value * 2
    
    return Output(
        success=True,
        result=result,
        data=input.optional_data or {}
    )
