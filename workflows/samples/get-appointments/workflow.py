"""
Workflow: Get Appointments

Navigate to calendar and extract appointment slots for a given day.
Results are saved to /artifacts/appointments.json
"""
import json
import os
from nen.workflow import agent, validate, extract, keyboard
from pydantic import BaseModel, Field


class Appointment(BaseModel):
    """Single appointment information."""
    
    start_time: str
    end_time: str
    description: str


class Input(BaseModel):
    """Input parameters for this workflow."""
    
    appointment_day: str = Field(min_length=1, description="Day to retrieve appointments for (e.g., 'January 15, 2026')")
    practice_email: str = Field(min_length=1, description="Practice login email address")
    practice_password: str = Field(min_length=1, description="Practice login password")


class Output(BaseModel):
    """Output returned by this workflow."""
    
    success: bool
    date: str | None = None
    appointments: list[Appointment] | None = None
    appointments_count: int | None = None
    message: str | None = None
    error: str | None = None


def run(input: Input) -> Output:
    """
    Extract all appointments for a specific day from the calendar.
    
    Args:
        input: Pydantic model with appointment day and login credentials
    
    Returns:
        Output model with extracted appointments
    """
    
    # Environment Setup: Launch browser and navigate
    agent("Click the Chromium browser icon in the taskbar (the blue circular icon, second from left)")
    if not validate("Is the Chromium browser open?", timeout=10):
        return Output(success=False, error="Failed to open browser")
    
    agent("Click the address bar at the top of the browser")
    keyboard.type("https://app.example.com/login")
    keyboard.press("Return")
    
    if not validate("Is the login page visible with email and password fields?", timeout=30):
        return Output(success=False, error="Failed to load login page")
    
    # Authentication: Login to the application
    agent(f"Click the email field and type '{input.practice_email}'", max_iterations=5)
    
    agent("Click the password field", max_iterations=3)
    keyboard.type(input.practice_password, interval=0.01)
    
    agent("Click the Login or Sign In button", max_iterations=5)
    
    if not validate("Is the user logged in? Look for a dashboard or navigation menu.", timeout=30):
        return Output(success=False, error="Failed to log in")
    
    # Data Extraction: Navigate to calendar and extract appointments
    agent("Find and click on 'Calendar', 'Appointments', or 'Schedule' in the navigation menu", max_iterations=10)
    
    if not validate("Is the calendar page visible?", timeout=15):
        return Output(success=False, error="Could not navigate to calendar")
    
    agent(f"Navigate to the date {input.appointment_day}. Use the date picker or navigation arrows.", max_iterations=10)
    
    if not validate(f"Is the calendar showing {input.appointment_day}?", timeout=15):
        return Output(success=False, error=f"Could not navigate to date {input.appointment_day}")
    
    # Extract appointments using structured data extraction
    appointments_data = extract(
        f"Look at the calendar for {input.appointment_day}. Extract ALL booked appointments visible. For each appointment, record the start_time, end_time, and description.",
        schema={
            "type": "object",
            "properties": {
                "date": {"type": "string"},
                "appointments": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "start_time": {"type": "string"},
                            "end_time": {"type": "string"},
                            "description": {"type": "string"}
                        },
                        "required": ["start_time", "end_time", "description"]
                    }
                }
            },
            "required": ["date", "appointments"]
        }
    )
    
    if not appointments_data:
        return Output(success=False, error="Failed to extract appointments data")
    
    # Save results to file
    os.makedirs("/artifacts", exist_ok=True)
    with open("/artifacts/appointments.json", "w") as f:
        json.dump(appointments_data, f, indent=2)
    
    # Verify file was created
    if not os.path.exists("/artifacts/appointments.json"):
        return Output(success=False, error="Failed to save appointments.json")
    
    # Convert appointments to Pydantic models
    appointments_list = [
        Appointment(**apt) for apt in appointments_data.get("appointments", [])
    ]
    
    return Output(
        success=True,
        date=appointments_data.get("date", input.appointment_day),
        appointments=appointments_list,
        appointments_count=len(appointments_list),
        message=f"Successfully extracted {len(appointments_list)} appointment(s)"
    )
