"""Login with Popup Handling — handle popups that appear after login.

Demonstrates:
- SecureParams with Secure[str] for passwords
- Clearing fields before typing
- Popup detection and dismissal pattern
- Checking failure indicators before success
"""

from nen import Agent, Computer, Secure
from pydantic import BaseModel, Field


class Params(BaseModel):
    """Input parameters for this workflow."""
    login_url: str
    username: str


class SecureParams(BaseModel):
    """Secure parameters for this workflow."""
    password: Secure[str] = Field(min_length=1, description="Account password")


class Result(BaseModel):
    """Output returned by this workflow."""
    success: bool
    error: str | None = None


def run(params: Params, secure_params: SecureParams) -> Result:
    agent = Agent()
    computer = Computer()

    # Open browser (UNRECOVERABLE if fails)
    agent.execute("Click the Chromium browser icon in the taskbar (the blue circular icon, second from left)")
    if not agent.verify("Is the Chromium browser open?", timeout=10):
        raise RuntimeError("Failed to open Chromium browser")

    # Navigate to login page (UNRECOVERABLE if fails)
    agent.execute(f"Navigate to {params.login_url}")
    if not agent.verify("Is the login form visible?", timeout=20):
        raise RuntimeError(f"Login page not found at {params.login_url}")

    # Enter username — clear field first
    agent.execute("Click the email or username field")
    agent.execute("Select all text in the field using keyboard shortcut")
    computer.press("BackSpace")
    computer.type(params.username)

    # Enter password — value is never exposed in the sandbox
    agent.execute("Click the password field")
    agent.execute("Select all text in the field using keyboard shortcut")
    computer.press("BackSpace")
    computer.type(secure_params.password, interval=0.01)

    computer.press("Return")

    # Dismiss any save-password popup
    if agent.verify("Is there a save password dialog or popup?", timeout=5):
        agent.execute("Click 'Never' or 'No Thanks' on the save password dialog")

    # Check failure first, then success
    if agent.verify("Are we still on the login page?", timeout=10):
        return Result(success=False, error="Login failed - still on login page")
    elif agent.verify("Is there an error message visible?"):
        return Result(success=False, error="Login failed - error message displayed")
    elif agent.verify("Is the dashboard or main page visible?", timeout=20):
        return Result(success=True)
    else:
        return Result(success=False, error="Unable to verify login state")
