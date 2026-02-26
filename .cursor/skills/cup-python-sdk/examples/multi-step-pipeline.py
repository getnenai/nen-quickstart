"""Multi-Step Pipeline — chain multiple steps that interact with different systems.

Demonstrates:
- Cross-system data transfer (extract from System A, enter into System B)
- Multi-step login flows
- Using extracted data in subsequent execute() calls
- Comprehensive verify() checks at each stage
"""

from nen import Agent
from pydantic import BaseModel, Field


class Params(BaseModel):
    patient_name: str = Field(min_length=1)
    system_a_url: str
    system_b_url: str


class Result(BaseModel):
    patient: str


def run(params: Params) -> Result:
    """Full patient onboarding: extract from System A, enter into System B."""
    agent = Agent()

    # Step 1: Login to System A and extract data
    agent.execute(f"Open browser and navigate to {params.system_a_url}")

    if not agent.verify("Is System A login page visible?"):
        raise RuntimeError("Could not reach System A")

    agent.execute("Login with credentials")

    if not agent.verify("Is System A dashboard visible?"):
        raise RuntimeError("System A login failed")

    agent.execute(f"Search for patient '{params.patient_name}'")

    if not agent.verify(f"Is patient '{params.patient_name}' profile visible?"):
        raise RuntimeError("Patient not found in System A")

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
            }
        }
    )

    # Step 2: Login to System B and enter data
    agent.execute(f"Open new tab and navigate to {params.system_b_url}")
    agent.execute("Login to System B")

    if not agent.verify("Is System B main window visible?"):
        raise RuntimeError("System B login failed")

    agent.execute("Click Add New Patient button")
    agent.execute(f"Fill in the patient form with: Name={source_data['name']}, DOB={source_data['dob']}")
    agent.execute("Click Save")

    if not agent.verify(f"Is patient '{params.patient_name}' record saved successfully?"):
        raise RuntimeError("Failed to save patient in System B")

    return Result(patient=params.patient_name)
