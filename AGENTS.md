# AGENTS.md

## Cursor Cloud specific instructions

### Project overview

This is a **NenAI MCP Quickstart** repository — a template/documentation workspace for authoring browser-automation workflows using the NenAI Python SDK (`nen.workflow`). There is no traditional application to build or run locally. Workflows are authored as Python files and executed remotely on NenAI's platform via the MCP server.

### Key development facts

- **No local services to run.** All workflow execution happens remotely on NenAI's Linux containers via the MCP API (`https://mcp.getnen.ai/v1`).
- **The `nen.workflow` SDK is remote-only.** It is not installable via pip; it is available only inside NenAI execution containers. To locally validate workflow Python files, stub the `nen` and `nen.workflow` modules (see below).
- **`pydantic`** is the only pip-installable dependency used by workflow files.

### Linting

Run `ruff check workflows/` to lint workflow Python files. Ruff is installed at `~/.local/bin/ruff`.

### Syntax / structure validation

To verify workflow files parse correctly and define the required `Input`, `Output`, and `run()` structures:

```bash
python3 -c "import py_compile; py_compile.compile('workflows/samples/website-login/workflow.py', doraise=True)"
```

To load and validate Pydantic models, stub the `nen.workflow` module first:

```python
import sys, types
nen_pkg = types.ModuleType('nen')
nen_workflow = types.ModuleType('nen.workflow')
nen_workflow.agent = lambda *a, **kw: None
nen_workflow.validate = lambda *a, **kw: True
nen_workflow.extract = lambda *a, **kw: {}
nen_workflow.keyboard = types.SimpleNamespace(type=lambda *a, **kw: None, press=lambda *a, **kw: None, hotkey=lambda *a, **kw: None)
nen_workflow.mouse = types.SimpleNamespace(click_at=lambda *a, **kw: None, move=lambda *a, **kw: None)
nen_pkg.workflow = nen_workflow
sys.modules['nen'] = nen_pkg
sys.modules['nen.workflow'] = nen_workflow
```

### Workflow authoring rules

See `.cursor/rules/` for comprehensive authoring guidance. Key files:
- `workflow-core.mdc` — SDK primitives, best practices, common patterns
- `workflow-creation-process.mdc` — end-to-end create/validate/deploy/run process
- `workflow-guide-comprehensive.mdc` — advanced patterns and architecture

### Testing workflows

Actual workflow testing requires deploying to the NenAI platform via MCP tools (`nen_validate`, `nen_upload`, `nen_run`). This requires a valid `NEN_API_KEY` and Cursor MCP server configuration. Without these, local validation is limited to syntax checking, linting, and Pydantic model validation.

### Known caveats

- `.cursor/skills/cup-python-sdk/examples/download-files.py` has an unused variable (`computer`) flagged by ruff — this is in existing sample code.
- Some sample workflows (`get-appointments`, `download-documents`) have required Input fields with no defaults, so `Input()` without arguments will raise Pydantic validation errors. This is by design.
