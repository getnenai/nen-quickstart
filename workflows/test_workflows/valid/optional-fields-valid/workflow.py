"""
Workflow: Optional Fields Valid

Tests workflows with optional input and output fields.
"""
from nen.workflow import agent, validate
from pydantic import BaseModel, Field


class Input(BaseModel):
    """Input with optional fields."""
    
    required_url: str
    optional_username: str | None = None
    optional_timeout: int = Field(default=30)
    optional_flag: bool = False


class Output(BaseModel):
    """Output with optional fields."""
    
    success: bool
    optional_message: str | None = None
    optional_data: dict | None = None
    optional_count: int = 0


def run(input: Input) -> Output:
    """
    Workflow with optional parameters.
    
    Args:
        input: Input with optional fields
    
    Returns:
        Output with optional fields
    """
    agent(f"Navigate to {input.required_url}")
    
    if input.optional_username:
        agent(f"Login as {input.optional_username}")
    
    if validate("Is operation complete?"):
        return Output(
            success=True,
            optional_message="Completed",
            optional_count=42
        )
    
    return Output(success=False)
