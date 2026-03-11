# Nen Quickstart

Build computer use automations using natural language in Cursor. Author, test, and run browser automation workflows directly from your IDE.

---

## Prerequisites

- **Cursor** (with support for remote MCP servers)

---

## Installation

### Step 1: Clone the repository

```bash
git clone https://github.com/getnen/nen-quickstart.git
cursor nen-quickstart
```

### Step 2: Configure Cursor

Click the link below to automatically install the Nen Platform MCP Server:

[![Install MCP Server](https://cursor.com/deeplink/mcp-install-dark.svg)](https://cursor.com/en-US/install-mcp?name=Nen%20Platform&config=eyJ1cmwiOiJodHRwczovL21jcC5nZXRuZW4uYWkvdjEiLCJoZWFkZXJzIjp7IngtYXBpLWtleSI6IllPVVJfTkVOQUlfQVBJX0tFWSJ9fQ%3D%3D)

This will automatically add the server configuration to your `mcp.json` file.

<details>
<summary>Manual installation (alternative)</summary>

If the automatic installation doesn't work:

1. Within Cursor, open "Cursor Settings" (Cmd-Shift-J)
2. Select "Tools & MCP" along the left bar
3. Click on "New MCP Server"
4. In `mcp.json`, add the "Nen Platform" key under `mcpServers`:

```json
{
  "mcpServers": {
    "Nen Platform": {
      "url": "https://mcp.getnen.ai/v1",
      "headers": {
        "x-api-key": "YOUR_API_KEY_HERE"
      }
    }
  }
}
```
</details>

### Step 3: Verify

Ask the AI agent in Cursor:

```
Show me the available Nen Platform MCP tools
```

✅ You should see tools like nen_run, nen_status, nen_update_workflow, nen_list_workflows, nen_list_runs, and nen_get_run_logs!

---

## Usage

### Creating Your First Workflow

Ask your AI agent to create a workflow:

```
Create a workflow that navigates to google.com and takes a screenshot
```

The AI will create a workflow and run it using the available MCP tools.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| MCP tools not showing up | Validate JSON syntax in `~/.cursor/mcp.json` |
| Network errors | Check internet connection / proxy / firewall |

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed solutions.

---

## Advanced

### Updating

Remote MCP tools are updated server-side automatically.

### Uninstallation

1. Remove the `"Nen Platform"` entry from `~/.cursor/mcp.json`
2. Restart Cursor

---

## Documentation

- [WORKFLOW_VALIDATION_GUIDE.md](WORKFLOW_VALIDATION_GUIDE.md) - Workflow validation guide
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Detailed troubleshooting guide
- [TOOLS_REFERENCE.md](TOOLS_REFERENCE.md) - Complete MCP tools reference
- [.cursor/rules/](.cursor/rules/) - Workflow authoring guides and rules
- [workflows/samples/](workflows/samples/) - Example workflows

---

## Security

The MCP server configuration uses a public URL endpoint. No credentials are stored in `mcp.json`.

---

## Getting Help

Contact your Nen customer engineer with:
- Full error message
- Contents of `~/.cursor/mcp.json` (redact any secrets)
