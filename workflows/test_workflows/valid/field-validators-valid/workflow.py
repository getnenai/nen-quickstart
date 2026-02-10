"""
Workflow: Field Validators Valid

Tests workflows with comprehensive Field validators.
"""
from nen.workflow import agent
from pydantic import BaseModel, Field


class Input(BaseModel):
    """Input with field validators."""
    
    email: str = Field(pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    age: int = Field(ge=0, le=150)
    score: float = Field(gt=0.0, lt=100.0)
    username: str = Field(min_length=3, max_length=20)
    tags: list[str] = Field(max_length=10)


class Output(BaseModel):
    """Output with field validators."""
    
    success: bool
    validation_passed: bool = True
    errors: list[str] = []


def run(input: Input) -> Output:
    """
    Workflow with field validation.
    
    Args:
        input: Validated input with constraints
    
    Returns:
        Output with validation results
    """
    agent(f"Process user {input.username}")
    agent(f"Email: {input.email}")
    
    return Output(
        success=True,
        validation_passed=True
    )
