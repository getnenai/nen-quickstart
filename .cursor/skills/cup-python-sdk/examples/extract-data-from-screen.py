"""Extract Data from Screen — pull structured data from the current screen state.

Demonstrates:
- Navigate → Verify → Extract → Return pattern
- Multiple extract() calls with different schemas (object and array)
- Optional fields in Result (dict | None)
"""

from nen import Agent, Computer
from pydantic import BaseModel, Field


class Params(BaseModel):
    patient_name: str = Field(min_length=1)


class Result(BaseModel):
    demographics: dict
    visits: list[dict] = []


def run(params: Params) -> Result:
    agent = Agent()
    computer = Computer()

    # Navigate to patient profile
    agent.execute(f"Search for and open patient '{params.patient_name}'")

    if not agent.verify(f"Is patient profile for '{params.patient_name}' visible?", timeout=20):
        raise RuntimeError(f"Patient '{params.patient_name}' not found")

    # Extract patient demographics
    demographics = agent.extract(
        "Extract the patient's demographic information",
        schema={
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "date_of_birth": {"type": "string"},
                "phone": {"type": "string"},
                "email": {"type": "string"},
                "address": {"type": "string"}
            }
        }
    )

    # Extract list of recent visits
    visits = agent.extract(
        "Extract the list of recent visits or appointments",
        schema={
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "date": {"type": "string"},
                    "reason": {"type": "string"},
                    "provider": {"type": "string"}
                }
            }
        }
    )

    return Result(demographics=demographics, visits=visits)
