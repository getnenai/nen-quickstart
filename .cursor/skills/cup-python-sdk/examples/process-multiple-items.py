"""Process Multiple Items — loop through a list of items passed as a workflow parameter.

Demonstrates:
- list[str] params
- Looping with error handling (continue on failure)
- Array schema extraction
- Collecting results into list[dict]
"""

from nen import Agent
from pydantic import BaseModel


class Params(BaseModel):
    provider_names: list[str]


class Result(BaseModel):
    data: list[dict] = []


def run(params: Params) -> Result:
    agent = Agent()
    results = []

    for provider in params.provider_names:
        print(f"Processing: {provider}")

        # Navigate to provider's schedule
        agent.execute(f"Click the Provider dropdown and select '{provider}'")

        if not agent.verify(f"Is the schedule visible for {provider}?"):
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

    return Result(data=results)
