"""
Workflow: Website Login

Navigate to a website and log in with provided credentials.
A simple, reusable login workflow.
"""
from nen.workflow import agent, validate, keyboard
from pydantic import BaseModel, Field


class Input(BaseModel):
    """Input parameters for this workflow."""
    
    web_url: str = Field(default="https://practicetestautomation.com/practice-test-login/", min_length=1, description="URL of the website to log in to")
    username: str = Field(default="student", min_length=1, description="Username or email for login")
    password: str = Field(default="Password123", min_length=1, description="Password for login")


class Output(BaseModel):
    """Output returned by this workflow."""
    
    success: bool
    message: str | None = None
    error: str | None = None


def run(input: Input) -> Output:
    """
    Log into a website with username and password.
    
    Args:
        input: Pydantic model with login credentials
    
    Returns:
        Output model with login results
    """
    
    # Environment Setup: Launch browser and navigate
    agent("Click the Chromium browser icon in the taskbar (the blue circular icon, second from left)")
    if not validate("Is the Chromium browser open?", timeout=10):
        return Output(success=False, error="Failed to open browser")
    
    # Dismiss any startup popups
    agent("Close any welcome messages, popups, or dialogs if they appear", max_iterations=5)
    
    agent("Click the address bar at the top of the browser")
    keyboard.type(input.web_url)
    keyboard.press("Return")
    
    if not validate("Is the webpage loading or loaded?", timeout=30):
        return Output(success=False, error=f"Failed to load {input.web_url}")
    
    # Authentication: Login to the website
    agent(f"Click the username or email field and type '{input.username}'", max_iterations=5)
    
    agent("Click the password field", max_iterations=10)
    keyboard.type(input.password, interval=0.01)
    
    agent("Click the Login or Sign In button", max_iterations=5)
    
    # Verify successful login
    if not validate("Is the user logged in? Look for a dashboard, profile menu, navigation sidebar, or welcome message.", timeout=30):
        return Output(success=False, error="Login verification failed - user does not appear to be logged in")
    
    return Output(
        success=True,
        message=f"Successfully logged into {input.web_url}"
    )
