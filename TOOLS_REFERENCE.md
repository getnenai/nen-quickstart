# Nen MCP Tools Reference

Quick reference for all Nen Platform MCP tools available via the remote MCP server.

---

## Tool Overview

| Tool | Purpose |
|------|---------|
| `nen_update_workflow` | Create or update a workflow (upload files by content) |
| `nen_run` | Execute a workflow |
| `nen_status` | Check run status and get liveViewUrl |
| `nen_list_runs` | List recent runs for a workflow |
| `nen_list_workflows` | List all deployed workflows |
| `nen_get_run_logs` | Retrieve full log content for a run |

> **Note:** `nen_create_workflow`, `nen_upload`, `update_workflow`, and `get_run_video` no longer exist. Use `nen_update_workflow` for all workflow creation and deployment.

---

## nen_update_workflow

Create a new workflow or update an existing one. Uploads files by content (not by local path) — required because MCP tools run in a containerized environment.

### Parameters

```typescript
{
  workflowId?: string;      // Omit to create a new workflow; provide to update existing
  workflowName?: string;    // Display name for the workflow
  deploymentId?: string;    // Required if API key has multiple deployments
  files: Array<{            // Workflow files to upload
    filename: string;       // File path (e.g., "workflow.py")
    content: string;        // Full file contents (UTF-8)
  }>;
}
```

`files` is required. `workflowId` is optional — omit it to create a new workflow.

### Create a new workflow

```typescript
nen_update_workflow({
  workflowName: "ezyvet-login",
  files: [
    {
      filename: "workflow.py",
      content: "..."   // full file content
    }
  ]
})
```

### Update an existing workflow

```typescript
nen_update_workflow({
  workflowId: "123e4567-e89b-12d3-a456-426614174000",
  files: [
    {
      filename: "workflow.py",
      content: "..."   // updated file content
    }
  ]
})
```

### Notes

- Upserts workflow files (creates or replaces)
- Publishes changes automatically
- Files not included in the `files` array are removed from the bundle
- Always read the local file with the `Read` tool first, then pass its content here

---

## nen_run

Trigger workflow execution on the Nen platform.

### Parameters

```typescript
{
  workflowId: string;                 // Workflow UUID
  params?: Record<string, string>;    // Input parameters as key-value pairs
}
```

### Example

```typescript
nen_run({
  workflowId: "123e4567-e89b-12d3-a456-426614174000",
  params: {
    login_url: "https://example.com/login",
    username: "user@example.com"
  }
})
```

### Response

Returns a `messageId` and a `liveViewUrl`:

```json
{
  "messageId": "msg-xyz789",
  "liveViewUrl": "https://app.getnen.ai/runs/msg-xyz789"
}
```

After calling `nen_run`, open the `liveViewUrl` in the browser so the user can watch execution in real-time:

```bash
open "https://app.getnen.ai/runs/msg-xyz789"   # macOS
```

---

## nen_status

Get the current status of a run, including a `liveViewUrl` to watch it in real-time.

### Parameters

```typescript
{
  messageId: string;    // Message ID from nen_run
}
```

### Example

```typescript
nen_status({
  messageId: "msg-xyz789"
})
```

### Possible Statuses

| Status | Meaning |
|--------|---------|
| `queued` | Waiting to start |
| `running` | Currently executing |
| `completed` | Successfully finished |
| `failed` | Encountered an error |
| `timeout` | Exceeded maximum execution time |

---

## nen_list_runs

List recent runs for a workflow.

### Parameters

```typescript
{
  workflowId: string;    // Workflow UUID
  limit?: number;        // Max results (default: 10)
}
```

### Example

```typescript
nen_list_runs({
  workflowId: "123e4567-e89b-12d3-a456-426614174000",
  limit: 20
})
```

### Use Cases

- Finding a `messageId` to pass to `nen_get_run_logs`
- Reviewing execution history
- Identifying patterns in failures

---

## nen_list_workflows

List all workflows deployed to your account.

### Parameters

```typescript
{
  deploymentId?: string;    // Required if API key has multiple deployments
}
```

### Example

```typescript
nen_list_workflows()
```

### Use Cases

- Finding a workflow's `workflowId` before calling `nen_run`
- Confirming a workflow was deployed successfully
- Reviewing all available workflows

---

## nen_get_run_logs

Retrieve the full log content for a workflow run. Returns log text directly for immediate analysis.

### Parameters

```typescript
{
  messageId: string;       // Message ID from nen_run
  deploymentId?: string;   // Required if API key has multiple deployments
}
```

### Example

```typescript
nen_get_run_logs({
  messageId: "msg-xyz789"
})
```

### What Logs Contain

- Timestamps and step-by-step execution trace
- VLM reasoning and decision-making
- `agent.execute()` actions and results
- `agent.verify()` results (true/false) and reasoning
- `agent.extract()` attempts and extracted values
- Error messages and stack traces

### When to Use

Always call `nen_get_run_logs` when:
- User reports the workflow failed
- User describes what "should have happened" but didn't
- Any unexpected behavior occurred
- You need to understand what the workflow actually did

> **Debugging golden rule:** When the user says "it should have..." or "it didn't..." → call `nen_get_run_logs` immediately before making any changes.

---

## Typical Workflow

### 1. Author

Write `workflow.py` using the Python SDK (`Agent`, `Computer`, Pydantic `Params`/`Result`). See `.cursor/rules/workflow-core.mdc`.

### 2. Deploy

```
Read workflow.py content
↓
nen_update_workflow({ workflowName: "...", files: [{ filename: "workflow.py", content: "..." }] })
↓
Note the returned workflowId
```

### 3. Execute

```
nen_run({ workflowId: "...", params: { ... } })
↓
Open liveViewUrl in browser: open "..."
↓
Wait for user to observe and return with feedback
```

### 4. Debug

```
User reports issue
↓
nen_get_run_logs({ messageId: "..." })
↓
Analyze logs → fix workflow.py → re-deploy → re-run
```

### 5. Update

```
Edit workflow.py locally
↓
nen_update_workflow({ workflowId: "...", files: [{ filename: "workflow.py", content: "..." }] })
↓
nen_run({ workflowId: "...", params: { ... } })
```

---

## Tips & Best Practices

### Deploying

- Always use **content-based upload** — read the file with the `Read` tool, pass the content string to `files[].content`
- Never use `localPath` — it doesn't exist in the current API
- Omit `workflowId` to create a new workflow; include it to update an existing one

### Running

- Always open `liveViewUrl` in the browser after `nen_run` so the user can watch execution
- Do not automatically call `nen_get_run_logs` or `nen_status` after running — wait for user feedback first

### Debugging

- `nen_get_run_logs` is the single best debugging tool — use it first, every time
- Look for `verify` results in logs — they show exactly where conditional logic succeeded or failed
- Look for VLM reasoning to understand why the agent made certain decisions

---

## Getting Help

See `.cursor/rules/` for authoring guides:
- `workflow-core.mdc` — Python SDK template and primitives
- `workflow-creation-process.mdc` — Full build → deploy → run → iterate process
- `mcp-platform-tools.mdc` — When and how to use each MCP tool

Contact your Nen customer engineer with the workflow ID, message ID, and full error message.
