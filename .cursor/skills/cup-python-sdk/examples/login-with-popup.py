"""Login with Popup Handling — handle popups that appear after login.

Demonstrates:
- SecureParams with Secure[str] for passwords
- Computer.type() with secure values
- Popup detection and dismissal pattern
"""

from nen import Agent, Computer, Secure
from pydantic import BaseModel, Field


class Params(BaseModel):
    login_url: str
    username: str


class SecureParams(BaseModel):
    password: Secure[str] = Field(min_length=12)


class Result(BaseModel):
    pass


def run(params: Params, secure_params: SecureParams) -> Result:
    agent = Agent()
    computer = Computer()

    # Navigate to login page
    agent.execute(f"Open browser and navigate to {params.login_url}")

    if not agent.verify("Is the login form visible?"):
        raise RuntimeError("Login page not found")

    # Enter credentials
    agent.execute("Click the email field")
    computer.type(params.username)

    agent.execute("Click the password field")
    computer.type(secure_params.password)

    computer.press("Return")

    # Check for dashboard, handling potential popup
    if not agent.verify("Is the dashboard with navigation visible?"):
        # Popup might be blocking
        if agent.verify("Is there a save password dialog?"):
            agent.execute("Click 'Never' or 'No Thanks' on the save password dialog")

        if not agent.verify("Is the dashboard visible?"):
            raise RuntimeError("Login failed")

    return Result()
