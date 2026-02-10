# NenAI MCP Tools Reference

**Last Updated:** February 10, 2026  
**Version:** 1.0

This document provides a comprehensive reference for all available tools in the NenAI MCP environment.

---

## Table of Contents

1. [NenAI Platform Tools](#nenai-platform-tools)
2. [GitHub Tools](#github-tools)
3. [File System Tools](#file-system-tools)
4. [Shell Tools](#shell-tools)
5. [Search Tools](#search-tools)
6. [Mode Management](#mode-management)
7. [Tool Testing Status](#tool-testing-status)

---

## NenAI Platform Tools

### Core Workflow Operations

#### `nen_list_workflows()`
Lists all workflows for the current deployment.

**Parameters:**
- `deploymentId` (optional): Deployment ID (auto-detected from API key)

**Returns:**
```json
{
  "success": true,
  "deploymentId": "...",
  "deploymentName": "staging",
  "workflows": [
    {
      "workflowId": "...",
      "workflowName": "...",
      "s3WorkflowPath": "...",
      "createdAt": "...",
      "updatedAt": "...",
      "publishedAt": "..."
    }
  ],
  "count": 10
}
```

**Example:**
```python
result = nen_list_workflows()
print(f"Found {result['count']} workflows")
```

---

#### `nen_validate(content, filename)`
Validates a Python workflow file for syntax and structural correctness.

**Parameters:**
- `content` (required): The Python workflow file content to validate
- `filename` (optional): Filename for better error messages (default: "workflow.py")

**Returns:**
```json
{
  "success": true,
  "valid": true,
  "message": "Workflow file is valid",
  "filename": "workflow.py",
  "warnings": []
}
```

**Checks:**
- Valid Python syntax
- `run()` function signature matches `run(input: Input) -> Output`
- Pydantic `Input` and `Output` models are defined
- `Output` model includes `success: bool` field

**Example:**
```python
# Read the workflow file
workflow_content = Read("workflows/my_workflows/my-workflow/workflow.py")

# Validate it
result = nen_validate(
    content=workflow_content,
    filename="workflow.py"
)

if result['valid']:
    print("✅ Workflow is valid!")
else:
    print(f"❌ Validation failed: {result['message']}")
```

**CRITICAL RULE:** Always call `nen_validate()` after ANY modification to a workflow file.

---

#### `nen_upload(files, workflowName, workflowId, deploymentId, deploymentName)`
Uploads workflow files to S3 and updates DynamoDB.

**Parameters:**
- `files` (required): Array of workflow files with contents
  - `filename`: Relative file path (e.g., "workflow.py")
  - `content`: File contents (UTF-8)
- `workflowName` (optional): Workflow name for new workflows
- `workflowId` (optional): Workflow UUID for updates
- `deploymentId` (optional): Deployment UUID (auto-detected)
- `deploymentName` (optional): Deployment name (auto-detected)

**Returns:**
```json
{
  "success": true,
  "workflowId": "...",
  "workflowName": "...",
  "message": "Workflow uploaded successfully"
}
```

**Example (New Workflow):**
```python
# Read the workflow file
workflow_content = Read("workflows/my_workflows/my-workflow/workflow.py")

# Upload using content-based approach
result = nen_upload(
    files=[{
        "filename": "workflow.py",
        "content": workflow_content
    }],
    workflowName="My Workflow"
)

print(f"✅ Uploaded! Workflow ID: {result['workflowId']}")
```

**Example (Update Existing):**
```python
# Read the updated workflow file
workflow_content = Read("workflows/my_workflows/my-workflow/workflow.py")

# Update existing workflow
result = nen_upload(
    workflowId="existing-workflow-id",
    files=[{
        "filename": "workflow.py",
        "content": workflow_content
    }]
)
```

**⚠️ CRITICAL:** Always use content-based upload (`files` parameter), NOT `localPath`. MCP tools run in a containerized environment and cannot access local filesystem paths.

---

#### `nen_run(workflowId, params)`
Triggers workflow execution via NenAI API.

**Parameters:**
- `workflowId` (required): UUID of the workflow to run
- `params` (optional): Workflow parameters (dict)

**Returns:**
```json
{
  "success": true,
  "messageId": "...",
  "liveViewUrl": "https://app.nen.ai/live/...",
  "status": "started"
}
```

**Example:**
```python
result = nen_run(
    workflowId="workflow-uuid",
    params={
        "email": "test@example.com",
        "password": "secure123"
    }
)

print(f"🚀 Workflow running! Message ID: {result['messageId']}")
print(f"📺 Live view: {result['liveViewUrl']}")

# Open browser automatically (macOS)
Shell(f'open "{result["liveViewUrl"]}"')
```

**⚠️ CRITICAL RULE:** After calling `nen_run()` and opening the browser, IMMEDIATELY STOP and wait for user feedback. Do NOT automatically call `get_run_logs()`, `nen_status()`, or any other debugging tools.

---

#### `get_run_logs(messageId, deploymentId)`
Retrieves the full log content for a workflow run.

**Parameters:**
- `messageId` (required): Run message ID
- `deploymentId` (optional): Deployment ID (auto-detected)

**Returns:**
```
Full log text content showing:
- Agent actions and descriptions
- VLM reasoning and decision-making
- Validation results
- Extraction attempts
- Error messages
- Timing information
```

**Example:**
```python
# ONLY call this when user reports issues
logs = get_run_logs(messageId="run-message-id")
print(logs)
```

**🔍 CRITICAL: When to Use**

**ALWAYS call `get_run_logs()` when the user:**
- Reports the workflow failed or didn't work
- Describes what "should have happened" but didn't
- Says something like "it should have clicked..." or "it was supposed to..."
- Asks why something happened or didn't happen
- Mentions any unexpected behavior
- Wants to debug or troubleshoot

**Why this is critical:**
- Logs show exactly what the workflow did
- Logs reveal where the workflow failed
- Logs contain VLM reasoning and decision-making
- Without logs, you're guessing. With logs, you know.

---

#### `nen_status(messageId, apiKey)`
Gets run status from DynamoDB.

**Parameters:**
- `messageId` (required): Run message ID
- `apiKey` (optional): API Key (auto-injected)

**Returns:**
```json
{
  "status": "completed",
  "success": true,
  "startTime": "...",
  "endTime": "...",
  "duration": 45.2
}
```

---

#### `nen_list_runs(workflowId, limit, deploymentId)`
Lists recent runs for a workflow from DynamoDB.

**Parameters:**
- `workflowId` (required): Workflow UUID
- `limit` (optional): Max runs to return (default: 10)
- `deploymentId` (optional): Deployment ID (auto-detected)

**Returns:**
```json
{
  "runs": [
    {
      "messageId": "...",
      "status": "completed",
      "success": true,
      "startTime": "...",
      "endTime": "..."
    }
  ]
}
```

---

## GitHub Tools

### User Information

#### `user-GitHub-get_me()`
Gets details of the authenticated GitHub user.

**Returns:**
```json
{
  "login": "username",
  "id": 12345,
  "profile_url": "https://github.com/username",
  "details": {
    "name": "User Name",
    "public_repos": 18,
    "followers": 2,
    "following": 3
  }
}
```

---

### Repository Operations

#### `user-GitHub-search_repositories(query, sort, order, page, perPage)`
Find GitHub repositories by name, description, readme, topics, or metadata.

**Parameters:**
- `query` (required): Search query (e.g., "machine learning stars:>1000")
- `sort` (optional): Sort by "stars", "forks", "help-wanted-issues", "updated"
- `order` (optional): "asc" or "desc"
- `page` (optional): Page number
- `perPage` (optional): Results per page (max 100)

---

### Issues and Pull Requests

#### `user-GitHub-list_issues(owner, repo, state, labels, orderBy, direction)`
Lists issues in a repository.

#### `user-GitHub-issue_read(owner, repo, issue_number, method)`
Gets information about a specific issue.

#### `user-GitHub-list_pull_requests(owner, repo, state, head, base)`
Lists pull requests in a repository.

#### `user-GitHub-pull_request_read(owner, repo, pullNumber, method)`
Gets information on a specific pull request.

---

### Code Search

#### `user-GitHub-search_code(query, sort, order, page, perPage)`
Fast and precise code search across ALL GitHub repositories.

**Example:**
```python
# Search for Python code containing "Skill"
result = user-GitHub-search_code(
    query="content:Skill language:Python org:github"
)
```

---

## File System Tools

### Reading Files

#### `Read(path, offset, limit)`
Reads a file from the local filesystem.

**Parameters:**
- `path` (required): Absolute path to file
- `offset` (optional): Line number to start reading from
- `limit` (optional): Number of lines to read

**Returns:**
Line-numbered file contents:
```
1|line 1 content
2|line 2 content
3|line 3 content
```

**Example:**
```python
# Read entire file
content = Read("/path/to/file.py")

# Read specific lines (lines 10-20)
content = Read("/path/to/file.py", offset=10, limit=10)
```

---

#### `LS(target_directory, ignore_globs)`
Lists files and directories in a given path.

**Parameters:**
- `target_directory` (required): Absolute path to directory
- `ignore_globs` (optional): Array of glob patterns to ignore

**Example:**
```python
# List all files
files = LS("/Users/username/project")

# List files, ignoring node_modules
files = LS("/Users/username/project", ignore_globs=["**/node_modules/**"])
```

---

### Writing Files

#### `Write(path, contents)`
Writes a file to the local filesystem (overwrites existing).

**Parameters:**
- `path` (required): Absolute path to file
- `contents` (required): File contents to write

**⚠️ IMPORTANT:** ALWAYS prefer editing existing files. NEVER write new files unless explicitly required.

**Example:**
```python
Write("/path/to/file.py", """
def hello():
    print("Hello, world!")
""")
```

---

#### `StrReplace(path, old_string, new_string, replace_all)`
Performs exact string replacements in files.

**Parameters:**
- `path` (required): Absolute path to file
- `old_string` (required): Text to replace (must be unique unless `replace_all=True`)
- `new_string` (required): Replacement text
- `replace_all` (optional): Replace all occurrences (default: false)

**Example:**
```python
# Replace a specific string
StrReplace(
    path="/path/to/file.py",
    old_string="old_function_name",
    new_string="new_function_name",
    replace_all=True
)
```

---

#### `Delete(path)`
Deletes a file at the specified path.

**Parameters:**
- `path` (required): Absolute path to file to delete

---

### Searching Files

#### `Glob(glob_pattern, target_directory)`
Searches for files matching a glob pattern.

**Parameters:**
- `glob_pattern` (required): Pattern to match (e.g., "*.py", "**/*.tsx")
- `target_directory` (optional): Directory to search in

**Example:**
```python
# Find all Python files
python_files = Glob("*.py", "/path/to/project")

# Find all TypeScript React files
tsx_files = Glob("**/*.tsx", "/path/to/project")
```

---

#### `Grep(pattern, path, output_mode, type, glob, multiline, -A, -B, -C, -i)`
Powerful search tool built on ripgrep.

**Parameters:**
- `pattern` (required): Regular expression pattern
- `path` (optional): File or directory to search in
- `output_mode` (optional): "content" (default), "files_with_matches", "count"
- `type` (optional): File type (e.g., "py", "js", "rust")
- `glob` (optional): Glob pattern to filter files
- `multiline` (optional): Enable multiline mode (default: false)
- `-A` (optional): Lines to show after match
- `-B` (optional): Lines to show before match
- `-C` (optional): Lines to show before and after match
- `-i` (optional): Case insensitive search

**Example:**
```python
# Find all files containing "class Input"
Grep(
    pattern="class Input",
    path="/path/to/project",
    output_mode="files_with_matches"
)

# Search with context
Grep(
    pattern="def run",
    path="/path/to/project",
    type="py",
    -C=3  # 3 lines before and after
)
```

---

#### `SemanticSearch(query, target_directories, num_results)`
Semantic search that finds code by meaning, not exact text.

**Parameters:**
- `query` (required): Complete question (e.g., "How does user authentication work?")
- `target_directories` (required): Array with one directory or empty array for all
- `num_results` (optional): Number of results (max 15, default 15)

**Example:**
```python
# Search entire codebase
SemanticSearch(
    query="How does user authentication work?",
    target_directories=[]
)

# Search specific directory
SemanticSearch(
    query="Where are user roles checked?",
    target_directories=["backend/auth/"]
)
```

---

### Linting

#### `ReadLints(paths)`
Reads linter errors from the current workspace.

**Parameters:**
- `paths` (optional): Array of file or directory paths

**Example:**
```python
# Check specific files
ReadLints([
    "workflows/my_workflows/my-workflow/workflow.py"
])

# Check entire directory
ReadLints(["workflows/my_workflows"])
```

**⚠️ IMPORTANT:** Only call this on files you've edited. After substantive edits, use ReadLints to check for introduced errors.

---

## Shell Tools

#### `Shell(command, working_directory, block_until_ms, description)`
Executes a command in a shell session.

**Parameters:**
- `command` (required): The command to execute
- `working_directory` (optional): Working directory (absolute path)
- `block_until_ms` (optional): How long to wait before backgrounding (default: 30000ms)
- `description` (optional): Clear description of what the command does

**Example:**
```python
# Open browser (macOS)
Shell('open "https://app.nen.ai/live/12345"')

# Git operations
Shell("git status")
Shell("git add . && git commit -m 'Update workflow' && git push")

# Run with custom working directory
Shell("npm install", working_directory="/path/to/project")
```

**⚠️ IMPORTANT:** 
- Use specialized tools instead of terminal commands when possible
- NEVER use shell commands for file operations (use Read, Write, StrReplace instead)
- NEVER use echo or cat to communicate with the user

---

## Mode Management

#### `SwitchMode(target_mode_id, explanation)`
Switches the interaction mode to better match the current task.

**Parameters:**
- `target_mode_id` (required): Mode to switch to ("plan")
- `explanation` (optional): Why the mode switch is requested

**Available Modes:**
- **Agent Mode** (current): Full access to all tools for making changes
- **Plan Mode**: Read-only collaborative mode for designing approaches
- **Debug Mode**: Systematic troubleshooting with runtime evidence
- **Ask Mode**: Read-only exploration and answering questions

**Example:**
```python
# Switch to Plan mode for architectural decisions
SwitchMode(
    target_mode_id="plan",
    explanation="Need to discuss multiple approaches for implementing caching"
)
```

---

## Tool Testing Status

**Last Tested:** February 10, 2026

| Tool Category | Status | Notes |
|--------------|--------|-------|
| NenAI Platform | ✅ Working | All tools tested and functional |
| GitHub | ✅ Working | User info and search tested |
| File System | ✅ Working | Read, Write, LS, Glob, Grep tested |
| Shell | ✅ Working | Command execution tested |
| Search | ✅ Working | Glob and Grep tested |
| Mode Management | ✅ Available | Mode switching functional |

### Test Results

```bash
# NenAI Tools
✅ nen_list_workflows() - Retrieved 10 workflows
✅ nen_validate() - Validated workflow successfully

# GitHub Tools
✅ user-GitHub-get_me() - Retrieved user profile

# File System Tools
✅ Read() - Read workflow files
✅ Glob() - Found Python files
✅ Grep() - Searched for patterns

# All tools verified and operational
```

---

## Best Practices

### 1. Always Validate Before Deploying
```python
# Read workflow
content = Read("workflow.py")

# Validate BEFORE uploading
nen_validate(content=content)

# Then upload
nen_upload(files=[{"filename": "workflow.py", "content": content}])
```

### 2. Use Content-Based Uploads
```python
# ❌ WRONG - localPath doesn't work in containers
nen_upload(localPath="/path/to/workflow")

# ✅ CORRECT - content-based upload
content = Read("/path/to/workflow.py")
nen_upload(files=[{"filename": "workflow.py", "content": content}])
```

### 3. Stop After Running Workflows
```python
# Run the workflow
result = nen_run(workflowId="...", params={...})

# Open browser
Shell(f'open "{result["liveViewUrl"]}"')

# 🛑 STOP HERE - Wait for user feedback
# ❌ DO NOT call get_run_logs() automatically
# ❌ DO NOT call nen_status() automatically
```

### 4. Get Logs When User Reports Issues
```python
# User: "It failed at the password field"

# ✅ IMMEDIATELY get logs
logs = get_run_logs(messageId="...")

# Analyze logs to understand what happened
# Then fix the workflow based on log insights
```

### 5. Use Specialized Tools First
```python
# ❌ WRONG - using shell for file operations
Shell("cat file.py")
Shell("sed 's/old/new/' file.py")

# ✅ CORRECT - using specialized tools
Read("file.py")
StrReplace("file.py", old_string="old", new_string="new")
```

---

## Quick Reference

### Workflow Creation Flow
```
1. Build → Write workflow.py
2. Validate → nen_validate()
3. Deploy → nen_upload()
4. Run → nen_run()
5. Open Browser → Shell('open "url"')
6. 🛑 STOP → Wait for user
7. Debug (if needed) → get_run_logs()
8. Iterate → Back to Step 1
```

### Common Tool Combinations

**Creating a Workflow:**
```python
Write("workflow.py", content)
nen_validate(content=content)
nen_upload(files=[...])
nen_run(workflowId="...")
```

**Debugging a Workflow:**
```python
get_run_logs(messageId="...")
Read("workflow.py")
StrReplace("workflow.py", old=..., new=...)
nen_validate(content=...)
nen_upload(workflowId="...", files=[...])
```

**Searching Codebase:**
```python
Glob("*.py")
Grep(pattern="class Input")
SemanticSearch(query="How does X work?")
```

---

## Support

For more information:
- **Workflow Creation Process**: `.cursor/rules/workflow-creation-process.mdc`
- **Workflow Core Principles**: `.cursor/rules/workflow-core.mdc`
- **MCP Platform Tools**: `.cursor/rules/mcp-platform-tools.mdc`
- **Test Prompts**: `.agents/workflow-test-prompts.md`

---

**Version History:**
- v1.0 (2026-02-10): Initial comprehensive tools reference