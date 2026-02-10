# Sample Workflows

This directory contains example workflows demonstrating various NenAI workflow patterns and use cases.

## Working Samples

### ✅ SDK Primitives Test (`sample-workflow.py`)
- **Status:** Fully functional
- **Description:** Demonstrates basic SDK primitives (agent, validate, extract)
- **What it does:** Opens Chromium, navigates to Hacker News, and extracts post titles
- **Test URL:** https://news.ycombinator.com

### ✅ Website Login (`website-login/workflow.py`)
- **Status:** Fully functional
- **Description:** Generic reusable login workflow
- **What it does:** Opens browser, navigates to any URL, logs in with credentials
- **Test URL:** https://practicetestautomation.com/practice-test-login/
- **Test Credentials:** Username: `student`, Password: `Password123`

## Reference-Only Samples

These workflows are provided as **reference examples** and cannot be tested without a real application:

### 📚 Get Appointments (`get-appointments/workflow.py`)
- **Status:** Reference only - No test site available
- **Description:** Calendar automation workflow for extracting appointments
- **What it demonstrates:**
  - Browser navigation and login
  - Calendar date navigation
  - Structured data extraction with JSON schema
  - Saving results to `/artifacts` directory
- **Use case:** Healthcare/scheduling applications

### 📚 Download Documents (`download-documents/workflow.py`)
- **Status:** Reference only - No test site available
- **Description:** Document retrieval workflow for patient records
- **What it demonstrates:**
  - Multi-step navigation (login → search → patient profile)
  - File download automation
  - File system verification
  - Counting downloaded files
- **Use case:** Healthcare document management systems

## Usage

### Running Working Samples

The working samples can be deployed and tested immediately:

```bash
# Deploy SDK Primitives Test
nen_upload(workflowName="SDK Primitives Test", files=[...])

# Deploy Website Login
nen_upload(workflowName="Website Login", files=[...])
```

### Using Reference Samples

The reference samples are provided as templates. To use them:

1. **Copy the workflow file** to your own workflow directory
2. **Update the URLs** to point to your actual application
3. **Modify the field selectors** to match your UI
4. **Adjust validation logic** for your specific use case
5. **Test thoroughly** with your application

## Key Patterns Demonstrated

All samples demonstrate these core patterns:

- ✅ **Browser Management:** Opening Chromium and navigating
- ✅ **Form Interaction:** Clicking fields and typing input
- ✅ **Validation:** Checking UI state before proceeding
- ✅ **Error Handling:** Returning structured error messages
- ✅ **Pydantic Models:** Type-safe input/output definitions

### Advanced Patterns (Reference Samples)

- 📚 **Data Extraction:** Using `extract()` with JSON schemas
- 📚 **File Operations:** Saving to `/artifacts` directory
- 📚 **Multi-step Workflows:** Complex navigation flows
- 📚 **Search and Selection:** Finding specific records
