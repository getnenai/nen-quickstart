"""
Workflow: Full Featured Valid Workflow

This workflow demonstrates all SDK features and proper structure.
"""
from nen.workflow import agent, validate, extract, keyboard, mouse
from pydantic import BaseModel, Field


class Input(BaseModel):
    """Full input model with validation."""
    
    website_url: str = Field(min_length=1, description="Target website URL")
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8)
    timeout: int = Field(default=30, ge=10, le=120)


class Output(BaseModel):
    """Full output model with multiple fields."""
    
    success: bool
    message: str | None = None
    error: str | None = None
    data: dict | None = None


def run(input: Input) -> Output:
    """
    Full workflow with all SDK primitives.
    
    Args:
        input: Validated input parameters
    
    Returns:
        Output with results and status
    """
    # Agent actions
    agent("Click the Chromium browser icon in the taskbar (the blue circular icon, second from left)")
    if not validate("Is the Chromium browser open?", timeout=10):
        return Output(success=False, error="Failed to open browser")
    
    agent(f"Navigate to {input.website_url}")
    if not validate("Is the login page loaded?", timeout=input.timeout):
        return Output(success=False, error="Login page failed to load")
    
    # Keyboard actions
    agent("Click username field")
    keyboard.hotkey("ctrl", "a")
    keyboard.press("BackSpace")
    keyboard.type(input.username)
    
    # Mouse actions
    mouse.click_at(500, 300)
    
    # Extract data
    data = extract(
        "What is the user's account info?",
        schema={
            "type": "object",
            "properties": {
                "account_id": {"type": "string"},
                "balance": {"type": "number"}
            },
            "required": ["account_id"]
        }
    )
    
    # Return success
    return Output(
        success=True,
        message="Workflow completed successfully",
        data=data
    )
