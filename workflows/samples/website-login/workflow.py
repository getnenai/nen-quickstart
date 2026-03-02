"""
Workflow: NenAI Docs Login

Navigates to the NenAI documentation site, enters the access code,
and extracts the page title to confirm successful access.
"""
from nen import Agent, Computer, Secure
from pydantic import BaseModel, Field


class Params(BaseModel):
    login_url: str = Field(default="https://docs.getnen.ai/login", min_length=1, description="URL of the docs login page")


class SecureParams(BaseModel):
    password: Secure[str] = Field(min_length=1, description="Access code for the NenAI docs")


class Result(BaseModel):
    page_title: str = Field(min_length=1, description="Title of the first page shown after gaining access")


def run(params: Params, secure_params: SecureParams) -> Result:
    agent = Agent()
    computer = Computer()

    agent.execute("Click the Chromium browser icon in the taskbar (the blue circular icon, second from left)")
    if not agent.verify("Is the Chromium browser open?", timeout=10):
        raise RuntimeError("Failed to open Chromium browser")

    agent.execute(f"Navigate to {params.login_url}")
    if not agent.verify("Is the 'Enter access code' input field visible?", timeout=20):
        raise RuntimeError(f"Access code page not found at {params.login_url}")

    agent.execute("Click the access code input field")
    computer.type(secure_params.password, interval=0.01)
    agent.execute("Click the 'Access' button")

    # Dismiss save-password popup before checking page state
    if agent.verify("Is there a save password dialog or popup?", timeout=5):
        agent.execute("Click 'Never' on the save password dialog")

    # Check failure indicators first
    if agent.verify("Is the 'Enter access code' input still visible?", timeout=5):
        raise RuntimeError("Access denied — access code may be incorrect")
    if not agent.verify("Is the documentation content visible?", timeout=20):
        raise RuntimeError("Failed to load documentation after entering access code")

    data = agent.extract(
        "What is the title of the page now shown?",
        Result.model_json_schema(),
    )
    return Result.model_construct(**data)
