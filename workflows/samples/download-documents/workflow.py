"""
Workflow: Download Documents

Navigate to patient profile and download all documents to /artifacts directory.
"""
import os
from nen.workflow import agent, validate, keyboard
from pydantic import BaseModel, Field


class Input(BaseModel):
    """Input parameters for this workflow."""
    
    patient_name: str = Field(min_length=1, description="Patient name to search for")
    login_email: str = Field(min_length=1, description="Login email address")
    login_password: str = Field(min_length=1, description="Login password")


class Output(BaseModel):
    """Output returned by this workflow."""
    
    success: bool
    documents_downloaded: int | None = None
    message: str | None = None
    error: str | None = None


def run(input: Input) -> Output:
    """
    Download all documents for a specific patient.
    
    Args:
        input: Pydantic model with patient and login information
    
    Returns:
        Output model with download results
    """
    
    # Clear previous downloads
    os.system("rm -f /artifacts/*.pdf 2>/dev/null")
    
    # Environment Setup: Launch browser and navigate
    agent("Click the Chromium browser icon in the taskbar (the blue circular icon, second from left)")
    if not validate("Is the Chromium browser open?", timeout=10):
        return Output(success=False, error="Failed to open Chromium browser")
    
    agent("Click the address bar at the top of the browser")
    keyboard.type("https://app.example.com")
    keyboard.press("Return")
    
    if not validate("Is the webpage loading or loaded?", timeout=30):
        return Output(success=False, error="Failed to load application URL")
    
    # Authentication: Login to the application
    agent(f"If a login page is visible, enter email '{input.login_email}' in the email field, enter the password in the password field, then click the login button. If already logged in, do nothing.", max_iterations=15)
    
    if not validate("Is the user logged in? Look for a main navigation menu or dashboard.", timeout=30):
        return Output(success=False, error="Failed to log in")
    
    # Patient Search: Find the target patient
    agent("Find and click on 'Patients' or 'Clients' in the navigation menu", max_iterations=10)
    
    if not validate("Is the patients page visible with a search field?", timeout=15):
        return Output(success=False, error="Could not navigate to patients section")
    
    agent(f"Find the search field and type '{input.patient_name}'. Wait for search results to appear.", max_iterations=10)
    
    # Verify exactly one patient found
    if not validate(f"Is there exactly one patient result matching '{input.patient_name}'?", timeout=10):
        agent("Clear the search field and try searching again", max_iterations=3)
        if not validate(f"Is there exactly one patient result matching '{input.patient_name}'?", timeout=10):
            return Output(success=False, error=f"Could not find unique patient match for '{input.patient_name}'")
    
    agent(f"Click on the patient '{input.patient_name}' to open their profile", max_iterations=5)
    
    if not validate("Is the patient profile page open?", timeout=15):
        return Output(success=False, error="Failed to open patient profile")
    
    # Download: Download all documents
    agent("Look for a 'Documents', 'Files', or 'Attachments' tab or section. Click on it.", max_iterations=10)
    
    if not validate("Is the documents section visible?", timeout=15):
        return Output(success=False, error="Could not find documents section")
    
    agent("""For each document/PDF visible:
1. Click on the document or download button
2. If a download dialog appears, click Save or Download
3. Wait for download to complete
4. Move to the next document

Repeat until all documents are downloaded.""", max_iterations=30)
    
    # Verify downloads completed
    if not validate("Have all visible documents been downloaded?", timeout=60):
        return Output(success=False, error="Not all documents were downloaded")
    
    # Count downloaded PDFs
    result = os.popen("ls /artifacts/*.pdf 2>/dev/null | wc -l").read().strip()
    num_docs = int(result) if result.isdigit() else 0
    
    if num_docs == 0:
        return Output(success=False, error="No PDF documents were downloaded to /artifacts")
    
    return Output(
        success=True,
        documents_downloaded=num_docs,
        message=f"Successfully downloaded {num_docs} document(s)"
    )
