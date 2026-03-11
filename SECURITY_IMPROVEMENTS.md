# Security Improvements: Environment Variable Handling

## What Changed

Previously, setup instructions often led users to paste secrets directly into `~/.cursor/mcp.json`. Now, this repo configures a **remote MCP server** using environment-variable substitution (`${env:...}`), so credentials don't need to be stored in config files.

## New Architecture

### Before
```json
{
  "mcpServers": {
    "nen": {
      "url": "https://your-remote-mcp-url",
      "headers": {
        "X-Api-Key": "actual_key_here"
      }
    }
  }
}
```

### After
```json
{
  "mcpServers": {
    "nen": {
      "url": "${env:NEN_MCP_URL}",
      "headers": {
        "X-Api-Key": "${env:NEN_API_KEY}"
      }
    }
  }
}
```

## How It Works

1. `~/.cursor/mcp.json` points to the **remote** Nen MCP server via `url`.
2. `mcp.json` references credentials via `${env:NEN_API_KEY}` (Cursor substitutes it at runtime).
3. You can keep secrets out of git, out of docs, and out of config files.

## Benefits

✅ **Security**: Credentials never written to `mcp.json`  
✅ **Flexibility**: Update environment variables without editing JSON  
✅ **Portability**: Share `mcp.json` safely (no secrets)  
✅ **Best Practice**: Follows 12-factor app methodology  

## Setup Process

Simply run:

```bash
bash setup-remote-mcp.sh
```

Then restart Cursor completely (Cmd+Q or Ctrl+Q).

## Security Hardening Applied

### 1. Error Handling
- ✅ Setup fails fast if required environment variables are missing
- ✅ Configuration verification after writing `mcp.json`

### 2. Safe .env Parsing
- ✅ No `.env` parsing required by the repo

### 3. Backup & Recovery
- ✅ Automatic backup of existing `mcp.json` with timestamp
- ✅ Easy rollback capability
- ✅ Non-destructive updates

### 4. Validation & Testing
- ✅ `mcp.json` continues to avoid embedded secrets when using `${env:...}`

### 5. Documentation
- ✅ Comprehensive troubleshooting guide
- ✅ Security validation steps
- ✅ Clear error messages with remediation steps

## Files Involved

- `setup-remote-mcp.sh` - Writes/updates `~/.cursor/mcp.json` for remote MCP
- `TROUBLESHOOTING.md` - Comprehensive troubleshooting guide
- `~/.cursor/mcp.json` - Cursor config (no secrets, verified clean)
