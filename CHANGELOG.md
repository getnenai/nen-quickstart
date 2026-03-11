# Changelog

All notable changes to the Nen MCP Quickstart repository.

## [1.0.0] - 2026-01-14

### Added
- **Complete installation guide** (in `README.md`)
  - Step-by-step setup for Cursor
  - Detailed troubleshooting section
  - Advanced configuration options

- **MCP tools reference** (`TOOLS_REFERENCE.md`)
  - Comprehensive documentation for all 6 MCP tools
  - Example usage for each tool
  - Parameters and response formats
  - Typical workflow patterns
  - Best practices and tips

- **Enhanced README.md**
  - Improved quick start guide
  - Multi-IDE support instructions
  - Expanded troubleshooting section
  - "What's Next" section for new users
  - Advanced usage patterns
  - Quick links reference table

### Changed
- Updated documentation and examples for MCP tool usage

### Documentation Structure
```
mcp-quickstart/
├── README.md              # Overview, installation, and quick start
├── TOOLS_REFERENCE.md     # MCP tools documentation
├── CHANGELOG.md           # This file
├── .cursorrules           # FSM authoring guide
└── workflows/
    └── samples/           # Example workflows
```

## Future Enhancements

### Planned
- Video tutorials for common workflows
- Interactive workflow builder UI
- Template library for common use cases
- Integration testing examples
- Performance optimization guide

### Under Consideration
- VS Code extension support
- Local development container setup
- Workflow debugging tools
- Community workflow marketplace

## [Unreleased]

### Changed
- Switched to **remote MCP server only** (no local MCP server support).

### Removed
- Local MCP server wrapper/config scripts
- Local MCP server publishing automation under `scripts/`
- Node dependency wiring (`package.json`)
