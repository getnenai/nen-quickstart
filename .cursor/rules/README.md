# Cursor Rules for Nen Workflows

This directory contains Cursor rules for authoring Nen workflows using the Python SDK approach.

## Rule Structure Overview

This project uses modern `.mdc` (Markdown with frontmatter) files for intelligent context management:

- **Always-Apply Rules** - Core guidance loaded in every session
- **File-Pattern Rules** - Auto-load when editing specific file types
- **Agent-Decided Rules** - AI loads based on task complexity

## Available Rules

### workflow-core.mdc
**Always applies | ~170 lines**

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
**Always applies | ~200 lines**

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
**Agent-decided | ~500 lines**

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
**Agent-decided | 2,542 lines**

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
**Agent-decided | 872 lines**

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
**Agent-decided | ~400 lines**

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
- `workflow-core.mdc` (~180 lines)
- `workflow-creation-process.mdc` (~200 lines)

**Total: ~380 lines baseline context**

### On-Demand Context (AI-Decided)
AI intelligently loads additional guides based on task:
- Complex authoring → `workflow-guide-comprehensive.mdc` (+2,542 lines)
- Syntax lookup → `workflow-reference-detailed.mdc` (+872 lines)
- Platform operations & validation → `mcp-platform-tools.mdc` (+400 lines)
- Execution environment & pitfalls → `workflow-python-sdk.mdc` (+500 lines)

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

## Workflow Approaches

### Python SDK Approach (Primary)
- Uses Python with `nen.workflow` SDK
- VLM-based automation with natural language descriptions
- Direct computer control (mouse, keyboard)
- Structured data extraction with JSON schemas
- File: `workflow.py` with `handler(payload)` function

**Documentation:** This directory's .mdc rules

### FSM Approach (Alternative)
- Uses JSON-based Finite State Machine definitions
- State-based workflow with transitions
- LLMState, ToolState, VerificationState, etc.
- Files: `orchestrator.json` and `workflow.json`

**Documentation:** See legacy `.cursorrules` file (being deprecated)

## When to Use Which Approach

Use **Python SDK** approach when:
- Complex programmatic logic required
- Need custom error handling and retry logic
- Building reusable helper functions
- Prefer imperative programming style
- Need full Python ecosystem access

Use **FSM** approach when:
- Workflow is primarily sequential state transitions
- Need visual workflow representation
- Want declarative workflow definition
- Building resumable workflows with checkpoints
- Prefer configuration over code

## Benefits of Modern Rule Structure

This project uses modern `.mdc` rules with intelligent context management:
- `workflow-core.mdc` (always-on, ~180 lines)
- `workflow-creation-process.mdc` (always-on, ~200 lines)
- `workflow-python-sdk.mdc` (on-demand, ~500 lines)
- `workflow-guide-comprehensive.mdc` (on-demand, ~2542 lines)
- `workflow-reference-detailed.mdc` (on-demand, ~872 lines)
- `mcp-platform-tools.mdc` (on-demand, ~400 lines)

**Advantages:**
- Focused baseline context (~380 lines) for workflow creation
- Systematic 4-step process (build → validate → deploy → run) always available
- Built-in validation step prevents deployment errors
- Intelligent loading of detailed guides based on task complexity
- File-aware Python SDK guidance for workflow files
- Better organization and maintainability

## Key Features

1. **Systematic Workflow Creation** - 4-step process (build → validate → deploy → run) always available
2. **Mandatory Validation** - **CRITICAL:** `nen_validate()` must be called after EVERY workflow file change
3. **Built-in Validation** - nen_validate tool catches errors before deployment
4. **Minimal Context Pollution** - Only ~380 lines always loaded
5. **Intelligent Scaling** - Detailed guides load only when needed
6. **File-Aware** - Python SDK tips auto-load for .py files
7. **Fast Queries** - Simple questions get simple context
8. **Deep Dives** - Complex tasks get comprehensive documentation
9. **Team-Ready** - Version-controlled, well-organized rules

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

---

**Last Updated:** 2026-02-05  
**Version:** 2.1.0
