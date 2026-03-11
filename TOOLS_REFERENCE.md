# MCP Tools Quick Reference

Quick reference guide for Nen MCP tools (via the **remote MCP server**).

---

## Tool Overview

| Tool | Purpose |
|------|---------|
| `nen_create_workflow` | Generate workflow FSM files from natural language |
| `nen_upload` | Upload workflow files to S3 and update DynamoDB |
| `nen_run` | Execute a workflow |
| `nen_status` | Check workflow run status |
| `nen_artifacts` | Download run artifacts (video, logs) |
| `nen_list_runs` | List recent runs for a workflow |
| `update_workflow` | Update workflow files and publish to S3 |
| `get_run_video` | Get URL to view run dashboard |
| `get_run_logs` | Retrieve full log content for a run |

---

## nen_create_workflow

Generate FSM workflow files from natural language descriptions.

### Parameters

```typescript
{
  description: string;           // What the workflow should achieve
  inputs: Array<{               // Input parameters
    name: string;               // Variable name (UPPER_SNAKE_CASE)
    description: string;        // Human-readable description
    exampleValue?: string;      // Example value
  }>;
  outputs: Array<{              // Expected outputs
    name: string;               // Output identifier
    type: 'json' | 'file' | 'screenshot' | 'text';
    description: string;        // What this output contains
  }>;
  workflowName?: string;        // Optional custom name
  outputPath?: string;          // Where to save files (default: ./workflows/generated)
}
```

### Example Usage

**Simple Example (via AI agent):**
> "Create a workflow that navigates to google.com and takes a screenshot"

**Detailed Example:**
```typescript
nen_create_workflow({
  description: "Search for a patient in the hospital system and export their appointment history",
  inputs: [
    {
      name: "PATIENT_NAME",
      description: "Full name of the patient",
      exampleValue: "John Doe"
    },
    {
      name: "DATE_RANGE_START",
      description: "Start date for appointment history",
      exampleValue: "2024-01-01"
    }
  ],
  outputs: [
    {
      name: "appointments_json",
      type: "json",
      description: "List of appointments with dates and providers"
    },
    {
      name: "confirmation_screenshot",
      type: "screenshot",
      description: "Screenshot showing the export was successful"
    }
  ]
})
```

### Generated Files

- `orchestrator.json` - High-level workflow definition
- `01_step_name.json` - Individual FSM state files
- `02_another_step.json`
- etc.

### Best Practices

1. **Be specific in descriptions** - Include details about the application, expected UI, and success criteria
2. **Use descriptive variable names** - `PATIENT_NAME` not `name`, `LOGIN_URL` not `url`
3. **Define all inputs** - Include URLs, credentials, search terms, dates, etc.
4. **Specify outputs clearly** - What data structure? What file format?
5. **Review and edit** - Generated workflows are starting points; customize for your needs

---

## nen_upload

Upload workflow files to the Nen platform.

### Parameters

```typescript
{
  localPath: string;        // Path to local workflow directory
  deploymentName: string;   // Deployment name (e.g., 'pulse')
  workflowId?: string;      // Workflow UUID (optional for new workflows)
  workflowName?: string;    // Workflow name (optional)
}
```

### Example Usage

```typescript
nen_upload({
  localPath: "./workflows/my_workflows/patient-search",
  deploymentName: "pulse",
  workflowId: "123e4567-e89b-12d3-a456-426614174000"
})
```

### Requirements

- Workflow files in the local directory
- Valid deployment name

### Success Response

```json
{
  "success": true,
  "message": "Workflow uploaded successfully"
}
```

---

## nen_run

Trigger workflow execution on the Nen platform.

### Parameters

```typescript
{
  workflowId: string;              // Workflow UUID
  params?: Record<string, any>;    // Optional input variables as key-value pairs
}
```

### Example Usage

```typescript
nen_run({
  workflowId: "123e4567-e89b-12d3-a456-426614174000",
  params: {
    PATIENT_NAME: "John Doe",
    DATE_OF_BIRTH: "1990-01-15",
    SEARCH_TYPE: "name"
  }
})
```

### Requirements

- Workflow must be uploaded via `nen_upload` or `update_workflow`
- All required input variables must be provided

### Success Response

```json
{
  "success": true,
  "runId": "run-abc123",
  "messageId": "msg-xyz789",
  "status": "queued"
}
```

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| 404 Not Found | Workflow doesn't exist | Use `nen_upload` or `update_workflow` first |
| 400 Bad Request | Missing required inputs | Check workflow variables |

---

## nen_status

Check the status of a running or completed workflow.

### Parameters

```typescript
{
  messageId: string;        // Message identifier from nen_run
}
```

### Example Usage

```typescript
nen_status({
  messageId: "msg-xyz789"
})
```

### Response

```json
{
  "success": true,
  "status": "completed",
  "startTime": "2026-01-14T10:30:00Z",
  "endTime": "2026-01-14T10:35:23Z",
  "progress": {
    "currentState": "final_verification",
    "completedStates": 15,
    "totalStates": 15
  },
  "output": {
    "appointments_json": { ... },
    "confirmation_screenshot": "s3://..."
  }
}
```

### Possible Statuses

- `queued` - Waiting to start
- `running` - Currently executing
- `completed` - Successfully finished
- `failed` - Encountered an error
- `timeout` - Exceeded maximum execution time

---

## nen_list_runs

List recent workflow runs.

### Parameters

```typescript
{
  workflowId: string;       // Workflow UUID
  limit?: number;           // Max results (default: 10)
}
```

### Example Usage

```typescript
nen_list_runs({
  workflowId: "123e4567-e89b-12d3-a456-426614174000",
  limit: 20
})
```

### Response

```json
{
  "success": true,
  "runs": [
    {
      "runId": "run-abc123",
      "messageId": "msg-xyz789",
      "workflowId": "123e4567-...",
      "status": "completed",
      "startTime": "2026-01-14T10:30:00Z",
      "endTime": "2026-01-14T10:35:23Z"
    },
    ...
  ]
}
```

### Use Cases

- Finding a specific run to debug
- Monitoring workflow execution history
- Identifying patterns in failures
- Tracking execution times

---

## update_workflow

Update workflow files and publish changes.

### Parameters

```typescript
{
  workflowId: string;       // Workflow UUID
  files: Array<{           // Workflow files to write
    filename: string;      // File path (e.g., orchestrator.json, workflow.json)
    content: string;       // File contents (UTF-8)
  }>;
  workflowName?: string;   // Optional workflow display name
  deploymentId?: string;   // Optional deployment ID (if API key has multiple deployments)
}
```

### Example Usage

```typescript
update_workflow({
  workflowId: "123e4567-e89b-12d3-a456-426614174000",
  files: [
    {
      filename: "orchestrator.json",
      content: JSON.stringify(orchestratorConfig, null, 2)
    },
    {
      filename: "workflow.json",
      content: JSON.stringify(workflowFSM, null, 2)
    }
  ],
  workflowName: "Patient Search v2"
})
```

### Notes

- Upserts workflow files (creates or updates)
- Publishes changes automatically
- Removes any files not included in the `files` array

---

## get_run_video

Get a URL to open the run dashboard with video playback, logs, and downloads.

### Parameters

```typescript
{
  messageId: string;        // Run message ID from nen_run
  deploymentId?: string;    // Optional deployment ID (if API key has multiple deployments)
}
```

### Example Usage

```typescript
get_run_video({
  messageId: "msg-xyz789"
})
```

### Response

```json
{
  "url": "https://dashboard.getnen.ai/runs/msg-xyz789",
  "linkMarkdown": "[View Run Dashboard](https://dashboard.getnen.ai/runs/msg-xyz789)"
}
```

### Notes

- The returned URL should be opened in a browser
- Dashboard includes video playback, execution logs, and artifact downloads
- Always include the clickable link in your response to the user

---

## get_run_logs

Retrieve the full log content for a workflow run.

### Parameters

```typescript
{
  messageId: string;        // Run message ID from nen_run
  deploymentId?: string;    // Optional deployment ID (if API key has multiple deployments)
}
```

### Example Usage

```typescript
get_run_logs({
  messageId: "msg-xyz789"
})
```

### Response

Returns the raw log content as text, including:
- Timestamps
- State transitions
- Tool calls and results
- VLM verification responses
- Error messages and tracebacks

### Use Cases

- Debugging failed runs
- Understanding workflow execution flow
- Identifying timeout or verification issues
- Analyzing performance bottlenecks

---

## nen_artifacts

Download run artifacts (video, logs) to your local machine.

### Parameters

```typescript
{
  workflowId: string;       // Workflow UUID
  messageId: string;        // Run message ID
  outputDir?: string;       // Local directory to sync to (default: ./artifacts)
  sshHost?: string;         // SSH host name (default: puppilot)
  deploymentId?: string;    // Optional deployment ID (if API key has multiple deployments)
}
```

### Example Usage

```typescript
nen_artifacts({
  workflowId: "123e4567-e89b-12d3-a456-426614174000",
  messageId: "msg-xyz789",
  outputDir: "./my-artifacts"
})
```

### Downloaded Files

- `recording.mp4` - Screen recording of workflow execution
- `run.log` - Complete execution logs
- Any output files generated by the workflow

---

## Typical Workflow

### 1. Create

```
Agent: "Create a workflow that searches for patients and downloads their records"
↓
Uses: nen_create_workflow
↓
Output: FSM files in ./workflows/my_workflows/patient-search/
```

### 2. Review & Edit

```
Developer: Reviews generated FSM files
↓
Edits: Adjusts message templates, adds verification states
↓
Commits: Saves changes
```

### 3. Upload

```
Agent: "Upload the patient-search workflow"
↓
Uses: nen_upload
↓
Result: Workflow available on platform
```

### 4. Execute

```
Agent: "Run the patient-search workflow for John Doe"
↓
Uses: nen_run with params { PATIENT_NAME: "John Doe" }
↓
Response: runId and messageId
```

### 5. Monitor

```
Agent: "Check the status of that run"
↓
Uses: nen_status with messageId
↓
Response: Current state and progress
```

### 6. Iterate

```
Developer: Edits FSM files to fix issue
↓
Agent: "Upload the updated workflow"
↓
Uses: update_workflow or nen_upload
↓
Agent: "Run it again"
↓
Uses: nen_run with same params
```

---

## Tips & Best Practices

### Creating Workflows

- **Start simple:** Get basic navigation working before adding complex logic
- **Add verification states:** Wait for UI to be ready before proceeding
- **Use descriptive IDs:** `login_to_dashboard` not `step1`
- **Set reasonable iterations:** 5-10 for most states, 15-20 for complex searches

### Running Workflows

- **Test with known data:** Use test patients/accounts first
- **Monitor first runs:** Watch logs in real-time
- **Keep inputs consistent:** Use the same test data when iterating

### Debugging

- **Check logs first:** Often faster than re-running a workflow
- **Compare successful runs:** What was different?
- **Iterate quickly:** Small changes, frequent tests

### Organization

- **Use consistent naming:** `{org}-{app}-{action}` pattern
- **Group related workflows:** By application or use case
- **Document inputs:** Add descriptions and examples
- **Version control:** Commit FSM files to git

---

## Getting Help

### Documentation
- `.cursorrules` - Comprehensive FSM authoring guide
- `README.md` - Overview, installation, and quick start

### Support
Contact your Nen customer engineer with:
- Tool name and parameters used
- Full error message
- Expected vs actual behavior
- Workflow ID and run ID (if applicable)
