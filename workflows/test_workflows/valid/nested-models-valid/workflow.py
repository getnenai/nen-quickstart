"""
Workflow: Nested Models Valid

Tests workflows with nested Pydantic models.
"""
from nen.workflow import agent
from pydantic import BaseModel


class Address(BaseModel):
    """Nested address model."""
    
    street: str
    city: str
    zip_code: str


class UserInfo(BaseModel):
    """Nested user info model."""
    
    name: str
    email: str
    address: Address


class Input(BaseModel):
    """Input with nested model."""
    
    user: UserInfo
    action: str


class Output(BaseModel):
    """Output with nested model."""
    
    success: bool
    user_processed: UserInfo | None = None


def run(input: Input) -> Output:
    """
    Workflow with nested models.
    
    Args:
        input: Input with nested user info
    
    Returns:
        Output with processed user data
    """
    agent(f"Process user {input.user.name}")
    agent(f"Send to {input.user.address.city}")
    
    return Output(
        success=True,
        user_processed=input.user
    )
