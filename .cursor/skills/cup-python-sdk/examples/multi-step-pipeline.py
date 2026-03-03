"""Multi-Step Pipeline — chain multiple steps that interact with different systems.

Demonstrates:
- Cross-system data transfer (extract from System A, enter into System B)
- SecureParams with Secure[str] for passwords across multiple systems
- Using extracted data in subsequent agent.execute() calls
- Comprehensive agent.verify() checks at each stage
"""

from nen import Agent, Computer, Secure
from pydantic import BaseModel, Field


class Params(BaseModel):
    """Input parameters for this workflow."""
    patient_name: str = Field(min_length=1)
    system_a_url: str
    system_b_url: str
    system_a_username: str
    system_b_username: str


class SecureParams(BaseModel):
    """Secure parameters for this workflow."""
    system_a_password: Secure[str] = Field(min_length=1, description="System A login password")
    system_b_password: Secure[str] = Field(min_length=1, description="System B login password")


class Result(BaseModel):
    """Output returned by this workflow."""
    success: bool
    patient: str | None = None
    error: str | None = None


def run(params: Params, secure_params: SecureParams) -> Result:
    """Full patient onboarding: extract from System A, enter into System B."""
    agent = Agent()
    computer = Computer()

    # Open browser (UNRECOVERABLE if fails)
    agent.execute("Click the Chromium browser icon in the taskbar (the blue circular icon, second from left)")
    if not agent.verify("Is the Chromium browser open?", timeout=10):
        raise RuntimeError("Failed to open Chromium browser")

    # Step 1: Login to System A and extract data (UNRECOVERABLE if fails)
    agent.execute(f"Navigate to {params.system_a_url}")
    if not agent.verify("Is System A login page visible?", timeout=20):
        raise RuntimeError(f"Could not reach System A at {params.system_a_url}")

    agent.execute("Click the username field")
    agent.execute("Select all text in the field using keyboard shortcut")
    computer.press("BackSpace")
    computer.type(params.system_a_username)

    agent.execute("Click the password field")
    agent.execute("Select all text in the field using keyboard shortcut")
    computer.press("BackSpace")
    computer.type(secure_params.system_a_password, interval=0.01)

    computer.press("Return")

    if not agent.verify("Is System A dashboard visible?", timeout=20):
        return Result(success=False, error="System A login failed")

    agent.execute(f"Search for patient '{params.patient_name}'")
    if not agent.verify(f"Is patient '{params.patient_name}' profile visible?", timeout=15):
        return Result(success=False, error="Patient not found in System A")

    # Extract patient data
    source_data = agent.extract(
        "Extract all patient information",
        schema={
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "dob": {"type": "string"},
                "insurance": {"type": "string"},
                "allergies": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["name", "dob"]
        }
    )

    # Step 2: Login to System B and enter data
    agent.execute(f"Open a new tab and navigate to {params.system_b_url}")

    if not agent.verify("Is System B login page visible?", timeout=20):
        return Result(success=False, error="Could not reach System B")

    agent.execute("Click the username field")
    agent.execute("Select all text in the field using keyboard shortcut")
    computer.press("BackSpace")
    computer.type(params.system_b_username)

    agent.execute("Click the password field")
    agent.execute("Select all text in the field using keyboard shortcut")
    computer.press("BackSpace")
    computer.type(secure_params.system_b_password, interval=0.01)

    computer.press("Return")

    if not agent.verify("Is System B main window visible?", timeout=20):
        return Result(success=False, error="System B login failed")

    patient_name_val = source_data.get("name")
    patient_dob_val = source_data.get("dob")
    if not patient_name_val or not patient_dob_val:
        return Result(success=False, error="Extracted patient data is missing required name or dob fields")

    agent.execute("Click the Add New Patient button")
    agent.execute(f"Fill in the patient form: Name = {patient_name_val}, DOB = {patient_dob_val}")
    agent.execute("Click Save")

    if not agent.verify(f"Is patient '{params.patient_name}' record saved successfully?", timeout=15):
        return Result(success=False, error="Failed to save patient in System B")

    return Result(success=True, patient=params.patient_name)
