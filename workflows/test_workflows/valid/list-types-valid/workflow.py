"""
Workflow: List Types Valid

Tests workflows with list type fields.
"""
from nen.workflow import agent
from pydantic import BaseModel


class Input(BaseModel):
    """Input with list fields."""
    
    urls: list[str]
    counts: list[int]
    flags: list[bool] = []


class Output(BaseModel):
    """Output with list fields."""
    
    success: bool
    results: list[str] = []
    processed_count: int = 0


def run(input: Input) -> Output:
    """
    Workflow with list types.
    
    Args:
        input: Input with lists
    
    Returns:
        Output with list results
    """
    results = []
    
    for url in input.urls:
        agent(f"Visit {url}")
        results.append(f"Processed {url}")
    
    return Output(
        success=True,
        results=results,
        processed_count=len(input.urls)
    )
