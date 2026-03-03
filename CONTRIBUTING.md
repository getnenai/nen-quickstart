# Contributing to NenAI MCP Quickstart

Thank you for your interest in contributing! This guide will help you create high-quality workflows and improve the quickstart repository.

---

## Table of Contents

- [Getting Started](#getting-started)
- [Workflow Development](#workflow-development)
- [Code Standards](#code-standards)
- [Testing Workflows](#testing-workflows)
- [Submitting Changes](#submitting-changes)
- [Getting Help](#getting-help)

---

## Getting Started

### Prerequisites

1. Complete the [installation guide](README.md#installation)
2. Verify MCP server is working
3. Review the [FSM authoring guide](.cursorrules)
4. Study example workflows in `workflows/samples/`

### Development Setup

```bash
# Clone the repository
git clone https://github.com/getnenai/mcp-quickstart.git
cd mcp-quickstart
```

---

## Workflow Development

### Creating a New Workflow

1. **Use the AI agent to generate initial structure:**
   ```
   "Create a workflow that [describe your automation]"
   ```

2. **Review generated files:**
   - `orchestrator.json` - High-level flow
   - Individual state FSM files
   - Variable definitions

3. **Follow the FSM authoring guide:**
   - Reference [.cursorrules](.cursorrules) for patterns
   - Use appropriate state types (LLM, Tool, Verification)
   - Add proper error handling

4. **Organize your workflow:**
   ```
   workflows/
   └── your-workflow-name/
           ├── orchestrator.json
           ├── 01_launch_browser.json
           ├── 02_login.json
           └── 03_main_task.json
   ```

### Workflow Best Practices

#### State Design

**✅ Good:**
```json
{
  "id": "search_for_patient",
  "description": "Search for patient and wait for results",
  "message_template": "Click the search field. Type '${PATIENT_NAME}'. Press Enter. Wait for search results to appear.",
  "max_iterations": 10
}
```

**❌ Bad:**
```json
{
  "id": "do_stuff",
  "description": "Do things",
  "message_template": "Search for the patient",
  "max_iterations": 100
}
```

**Why:**
- Specific, actionable instructions
- Descriptive IDs and messages
- Reasonable iteration limits
- Clear success criteria

#### Variable Naming

**✅ Good:**
```json
{
  "name": "PATIENT_DATE_OF_BIRTH",
  "description": "Patient's date of birth in YYYY-MM-DD format"
}
```

**❌ Bad:**
```json
{
  "name": "dob",
  "description": "Date"
}
```

**Why:**
- Use UPPER_SNAKE_CASE for variables
- Descriptive names
- Include format requirements
- Avoid abbreviations

#### Verification States

Always add verification states after critical actions:

```json
{
  "id": "verify_dashboard_loaded",
  "type": "verification",
  "comparison_config": {
    "strategy": "vlm_similarity",
    "prompt": "Is the dashboard visible with patient search field?"
  },
  "verification_config": {
    "strategy": "verify_until",
    "wait_timeout": 30,
    "check_interval": 5
  }
}
```

---

## Code Standards

### JSON Formatting

- Use 2-space indentation
- Sort keys alphabetically (within reason)
- Include trailing commas where allowed
- Use double quotes

**Example:**
```json
{
  "description": "Login to application",
  "id": "login_state",
  "max_attempts": 2,
  "max_iterations": 5,
  "message_template": "Click username field. Type '${USERNAME}'. Press Tab. Type '${PASSWORD}'. Click Login."
}
```

### Documentation

Each workflow should include:

1. **README.md** in the workflow directory:
   ```markdown
   # Workflow Name
   
   ## Description
   Brief description of what this workflow does.
   
   ## Inputs
   - `VARIABLE_NAME`: Description and format
   
   ## Outputs
   - `output_name`: Description and location
   
   ## Prerequisites
   - Required access/credentials
   - System requirements
   
   ## Example Usage
   Steps to run the workflow
   ```

2. **Comments in complex FSM files:**
   ```json
   {
     "id": "extract_data",
     "description": "Extract appointment data from table (handles pagination up to 5 pages)",
     "message_template": "..."
   }
   ```

---

## Testing Workflows

### Local Testing

Before submitting, test your workflow thoroughly:

1. **Upload to platform:**
   ```typescript
   nen_upload({
     localPath: "./workflows/your-workflow",
     orgName: "test-org",
     orgId: "your-org-id",
     deploymentName: "dev",
     workflowId: "your-workflow-id"
   })
   ```

2. **Run with test data:**
   ```typescript
   nen_run({
     workflowId: "your-workflow-id",
     input: {
       TEST_INPUT: "known-good-value"
     }
   })
   ```

3. **Monitor execution:**
   ```typescript
   get_run_status({ messageId: "run-message-id" })
   nen_logs({ messageId: "run-message-id" })
   ```

4. **Review logs:**
   ```typescript
   nen_logs({ messageId: "run-message-id" })
   ```

### Test Cases

Create test cases for:

- **Happy path:** Normal execution with valid inputs
- **Edge cases:** Empty results, maximum pagination, etc.
- **Error handling:** Invalid inputs, timeouts, missing UI elements
- **Recovery:** What happens when popups appear, network issues, etc.

### Checklist Before Submission

- [ ] Workflow completes successfully with test data
- [ ] All required inputs are documented
- [ ] Outputs are clearly defined
- [ ] Error handling is implemented
- [ ] Verification states are added at critical points
- [ ] `max_iterations` values are reasonable (5-15 typical)
- [ ] Variable names use UPPER_SNAKE_CASE
- [ ] README.md is included
- [ ] JSON files are properly formatted
- [ ] No sensitive data (passwords, API keys) in files

---

## Submitting Changes

### Workflow Contributions

To contribute a new workflow to the samples:

1. **Create a feature branch:**
   ```bash
   git checkout -b workflow/your-workflow-name
   ```

2. **Add your workflow:**
   ```bash
   mkdir -p workflows/samples/your-workflow-name
   # Add your FSM files and README
   ```

3. **Test thoroughly** (see Testing section above)

4. **Commit your changes:**
   ```bash
   git add workflows/samples/your-workflow-name
   git commit -m "Add workflow: Brief description"
   ```

5. **Push and create PR:**
   ```bash
   git push origin workflow/your-workflow-name
   # Create pull request on GitHub
   ```

### PR Guidelines

**Title format:**
- `feat: Add [workflow name] workflow`
- `docs: Update installation guide for [IDE]`
- `fix: Correct verification state in [workflow]`

**Description should include:**
- What the workflow does
- Why it's useful
- What was tested
- Any dependencies or prerequisites
- Screenshots/videos of successful runs (if applicable)

**Example PR description:**
```markdown
## Description
Adds a workflow for downloading patient vaccination records from the hospital system.

## What was tested
- Happy path with 5 test patients
- Edge case: Patient with no vaccinations
- Edge case: Patient with >50 vaccination records (pagination)
- Error handling: Invalid patient ID

## Prerequisites
- Access to hospital system
- Valid credentials for vaccination module

## Demo
[Attach video or screenshot of successful run]
```

---

## Documentation Contributions

We welcome improvements to documentation:

- **Installation guides** - Add support for new IDEs
- **Troubleshooting** - Add solutions to common problems
- **Tool reference** - Improve examples or add tips
- **FSM authoring guide** - Add patterns or best practices

---

## Getting Help

### Questions About Contributing

- Review existing workflows in `workflows/samples/`
- Check [.cursorrules](.cursorrules) for FSM patterns
- Ask in pull request comments

### Reporting Issues

When reporting issues:

1. **Search existing issues** first
2. **Include:**
   - Detailed description
   - Steps to reproduce
   - Expected vs actual behavior
   - Workflow files (if relevant)
   - Error messages and logs
   - Your environment (OS, IDE, MCP server version)

### Feature Requests

For new features or enhancements:

1. **Open an issue** describing:
   - What you want to achieve
   - Why it would be useful
   - How you envision it working
2. **Discuss before implementing** large changes

---

## Code of Conduct

- Be respectful and constructive
- Focus on the technical merits
- Help others learn
- Assume good intentions

---

## Recognition

Contributors will be recognized in:
- GitHub contributors list
- Release notes for significant contributions
- Special thanks in documentation for major improvements

Thank you for helping make NenAI workflows better! 🚀
