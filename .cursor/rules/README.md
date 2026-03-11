# Cursor Rules for Nen Workflows

This directory contains Cursor rules for authoring Nen workflows using the Python SDK approach.

## Rule Structure Overview

This project uses modern `.mdc` (Markdown with frontmatter) files for intelligent context management:

- **Always-Apply Rules** - Core guidance loaded in every session
- **File-Pattern Rules** - Auto-load when editing specific file types
- **Agent-Decided Rules** - AI loads based on task complexity

## Available Rules

### workflow-core.mdc
**Always applies**

Core Nen workflow authoring principles loaded in every session.

**Contains:**
- Basic workflow structure and handler template
- SDK primitives quick reference (agent, validate, extract, mouse, keyboard)
- Common patterns (browser automation, login, data extraction)
- Best practices checklist
- References to detailed guides

**When it applies:** Automatically in all sessions

---

### workflow-creation-process.mdc
**Always applies**

Systematic 4-step process for creating workflows: build → validate → deploy → run.

**Contains:**
- Step 1: Build workflow with Python SDK
- Step 2: Validate workflow structure with nen_validate
- Step 3: Deploy using Nen platform tools
- Step 4: Run and verify execution
- Complete example flow
- Quick reference table

**When it applies:** Automatically in all sessions, especially when user wants to create a new workflow

---

### workflow-python-sdk.mdc
**Agent-decided**

Python SDK execution environment and best practices guide.

**Contains:**
- **Execution environment** (Linux containers, xdotool, platform compatibility)
- **Platform-specific keyboard commands** (ctrl vs command)
- **Common patterns** (clearing fields, validation strategies, keyboard delays)
- **Common pitfalls** (platform incompatibility, field clearing, false positives)
- **Debugging tips** (reading VLM logs, error patterns)
- **SDK function quick reference**

**When it applies:** AI loads this when:
- Need platform-specific guidance (keyboard commands, execution environment)
- Debugging keyboard/mouse control issues
- Learning validation strategies
- Understanding common pitfalls

**How to reference:** `@workflow-python-sdk`

---

### workflow-guide-comprehensive.mdc
**Agent-decided**

Comprehensive guide for complex workflow authoring tasks.

**Contains:**
- Complete SDK primitives documentation
- Execution environment architecture
- Advanced patterns and examples
- Performance considerations
- Debugging strategies
- AI agent guidance for code generation

**When it applies:** AI loads this when:
- Working on complex workflow logic
- Need understanding of execution environment
- Debugging advanced issues
- Generating workflow code programmatically

**How to reference:** `@workflow-guide-comprehensive`

---

### workflow-reference-detailed.mdc
**Agent-decided**

Detailed SDK reference with function signatures and examples.

**Contains:**
- Complete function signatures with parameters
- JSON schema examples for all patterns
- Decision trees (choosing primitives, timeouts, max_iterations)
- Quick troubleshooting guide
- Code snippets for common scenarios

**When it applies:** AI loads this when:
- Need specific SDK function syntax
- Looking up JSON schema patterns
- Quick reference for parameters
- Troubleshooting specific errors

**How to reference:** `@workflow-reference-detailed`

---

### mcp-platform-tools.mdc
**Agent-decided**

Nen MCP tool usage for platform operations including validation.

**Contains:**
- When to use MCP tools vs direct file editing
- Tool-specific documentation (nen_validate, nen_run, get_run_logs, etc.)
- Workflow validation guidelines
- Decision matrix for tool selection
- Deployment and execution workflows
- Debugging with platform logs

**When it applies:** AI loads this when:
- User mentions validation, deployment, running, or testing workflows
- Debugging failed workflow executions
- Working with Nen platform operations
- Need to list or manage deployed workflows

**How to reference:** `@mcp-platform-tools`

---

## Context Loading Strategy

### Automatic Context (Always Loaded)
- `workflow-core.mdc`
- `workflow-creation-process.mdc`

### On-Demand Context (AI-Decided)
AI intelligently loads additional guides based on task:
- Complex authoring → `workflow-guide-comprehensive.mdc`
- Syntax lookup → `workflow-reference-detailed.mdc`
- Platform operations & validation → `mcp-platform-tools.mdc`
- Execution environment & pitfalls → `workflow-python-sdk.mdc`

## How to Use These Rules

### For Simple Questions
Just ask - the always-apply core rules provide enough context:
```
"How do I validate a page loaded?"
```

### For Workflow Editing
Open any workflow file and the core rules are always available:
```
Open: workflows/my_workflows/login/workflow.py
Auto-loaded: workflow-core.mdc + workflow-creation-process.mdc
```

### For Complex Tasks
Mention specific guides explicitly or let AI decide:
```
"I need to understand the execution environment" → AI loads workflow-python-sdk.mdc
"Show me JSON schema examples" → AI loads workflow-reference-detailed.mdc
"How do I deploy my workflow?" → AI loads mcp-platform-tools.mdc
"Help me with advanced patterns" → AI loads workflow-guide-comprehensive.mdc
```

### Manual References
You can explicitly reference rules using @-mentions:
```
"@workflow-guide-comprehensive explain the agent primitive in detail"
"@workflow-reference-detailed show me table extraction schema"
"@mcp-platform-tools how do I debug a failed run?"
"@workflow-python-sdk what keyboard commands work in Linux containers?"
```

## Workflow Approach

All workflows use the **Python SDK** approach:
- Python with the `nen` SDK (`Agent`, `Computer`, `Secure`)
- VLM-based automation with natural language descriptions
- Direct computer control (mouse, keyboard)
- Structured data extraction with JSON schemas
- File: `workflow.py` with `run(params: Params) -> Result` function

## Rule File Locations

All rules in `.cursor/rules/`:
```
.cursor/rules/
├── README.md (this file)
├── workflow-core.mdc (always-apply)
├── workflow-creation-process.mdc (always-apply)
├── workflow-python-sdk.mdc (agent-decided)
├── workflow-guide-comprehensive.mdc (agent-decided)
├── workflow-reference-detailed.mdc (agent-decided)
└── mcp-platform-tools.mdc (agent-decided)
```

---

## Additional Documentation

For detailed validation guidance, see:
- [WORKFLOW_VALIDATION_GUIDE.md](../../WORKFLOW_VALIDATION_GUIDE.md) - Complete validation guide
