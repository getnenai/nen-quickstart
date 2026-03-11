"""Process Multiple Items — loop through a list of items passed as a workflow parameter.

Demonstrates:
- list[str] input params
- Looping with error handling (continue on failure)
- Array schema extraction
- Collecting results into list[dict]
"""

from nen import Agent
from pydantic import BaseModel, Field


class Params(BaseModel):
    provider_names: list[str]


class Result(BaseModel):
    data: list[dict] = Field(min_length=1, description="Appointments per provider")


def run(params: Params) -> Result:
    agent = Agent()
    results = []

    for provider in params.provider_names:
        print(f"Processing: {provider}")

        # Navigate to provider's schedule
        agent.execute(f"Click the Provider dropdown and select '{provider}'")

        if not agent.verify(f"Is the schedule visible for {provider}?", timeout=15):
            results.append({"provider": provider, "error": "Schedule not found"})
            continue

        # Extract appointments
        appointments = agent.extract(
            f"Extract all appointments for {provider}",
            schema={
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "patient_name": {"type": "string"},
                        "time": {"type": "string"},
                        "procedure": {"type": "string"}
                    }
                }
            }
        )

        results.append({"provider": provider, "appointments": appointments})

    any_succeeded = any(
        isinstance(r.get("appointments"), list) and len(r["appointments"]) > 0
        for r in results
    )
    if not any_succeeded:
        raise RuntimeError("No appointments were retrieved for any provider")

    return Result(data=results)
