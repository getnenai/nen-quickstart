# Troubleshooting Guide

## Common Issues

### 1. MCP Server Not Found in Cursor

**Symptom:** AI agent doesn't have access to `nen_*` tools.

**Solutions:**
1. Check `mcp.json` exists:
   ```bash
   cat ~/.cursor/mcp.json
   ```

2. Verify the Nen Platform server entry is present with the correct URL:
   ```json
   {
     "mcpServers": {
       "Nen Platform": {
         "url": "https://mcp.getnen.ai/v1"
       }
     }
   }
   ```

3. Check Cursor logs for MCP errors:
   - Open Cursor Developer Tools (Help → Toggle Developer Tools)
   - Look for errors mentioning "MCP" or "nen"

---

### 2. `mcp.json` syntax errors

**Symptom:** The MCP server doesn't load and Cursor shows JSON/config errors.

**Solutions:**
1. Validate JSON:
   ```bash
   python3 -m json.tool ~/.cursor/mcp.json >/dev/null && echo "OK"
   ```
2. Try reinstalling using the deeplink: [Install Nen Platform MCP Server](cursor://anysphere.cursor-deeplink/mcp/install?name=Nen%20Platform&config=eyJ1cmwiOiJodHRwczovL21jcC5nZXRuZW4uYWkvdjEifQ==)

---

### 3. Network errors

**Symptom:** Requests fail with network/proxy errors.

**Solutions:**
1. Check internet connection / firewall / proxy settings.
2. Verify you can reach the MCP endpoint:
   ```bash
   curl -I https://mcp.getnen.ai/v1
   ```
---

## Verify MCP JSON Validity

```bash
# Check mcp.json is valid JSON
cat ~/.cursor/mcp.json | python3 -m json.tool

# Should print formatted JSON with no errors
```

---

## Rollback to Previous Configuration

If you need to revert:

```bash
# Find backups
ls -lt ~/.cursor/mcp.json.backup.*

# Restore most recent backup
cp ~/.cursor/mcp.json.backup.YYYYMMDD_HHMMSS ~/.cursor/mcp.json

# Restart Cursor
```

---

## Still Having Issues?

1. Collect debug info:
   ```bash
   echo "=== System Info ==="
   uname -a
   echo "=== MCP Config ==="
   cat ~/.cursor/mcp.json
   ```

2. Contact support with the output above
