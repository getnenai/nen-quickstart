# NenAI MCP Quickstart - Documentation Map

```
┌─────────────────────────────────────────────────────────────────┐
│                         📚 START HERE                            │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  DOCUMENTATION_GUIDE.md                                 │    │
│  │  Master guide to navigate all documentation             │    │
│  │  • Quick reference by task                              │    │
│  │  • Learning path roadmap                                │    │
│  │  • Document descriptions                                │    │
│  └────────────────────────────────────────────────────────┘    │
│                             ↓                                    │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      🚀 GETTING STARTED                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────────────────────┐  ┌──────────────┐      │
│  │  README.md                         │  │ workflows/   │      │
│  │  • Prerequisites                   │  │  samples/    │      │
│  │  • Installation (auto & manual)    │  │  • Examples  │      │
│  │  • First workflow                  │  │  • Patterns  │      │
│  │  • Tools overview                  │  │              │      │
│  │  • Troubleshooting                 │  │              │      │
│  │  • Advanced topics                 │  │              │      │
│  └────────────────────────────────────┘  └──────────────┘      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────┐
│                      🛠️  USING THE TOOLS                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  TOOLS_REFERENCE.md                                     │    │
│  │  Complete reference for all 6 MCP tools                 │    │
│  │                                                          │    │
│  │  Tools covered:                                          │    │
│  │  • nen_create_workflow  → Generate workflow files       │    │
│  │  • nen_upload           → Deploy to platform            │    │
│  │  • nen_run              → Execute workflow              │    │
│  │  • get_run_status      → Check run status               │    │
│  │  • list_runs            → List run history              │    │
│  │                                                          │    │
│  │  For each tool:                                          │    │
│  │  • Parameters with types                                │    │
│  │  • Example usage                                        │    │
│  │  • Response formats                                     │    │
│  │  • Common errors                                        │    │
│  │  • Use cases                                            │    │
│  │  • Best practices                                       │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    ✍️  AUTHORING WORKFLOWS                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  .cursorrules                                           │    │
│  │  FSM authoring guide for AI agents                      │    │
│  │  • Workflow structure                                   │    │
│  │  • State types                                          │    │
│  │    - LLMState (agentic actions)                         │    │
│  │    - ToolState (deterministic)                          │    │
│  │    - VerificationState (wait for UI)                    │    │
│  │    - CoordinateToolState (LLM + tool)                   │    │
│  │    - CallbackState (dynamic values)                     │    │
│  │  • Variable system                                      │    │
│  │  • Failure recovery                                     │    │
│  │  • Environment normalization                            │    │
│  │  • FSM templates                                        │    │
│  │  • Common pitfalls                                      │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                     🤝 CONTRIBUTING                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  CONTRIBUTING.md                                        │    │
│  │  Guidelines for contributing workflows                  │    │
│  │  • Development setup                                    │    │
│  │  • Workflow best practices                              │    │
│  │  • Code standards                                       │    │
│  │  • Testing checklist                                    │    │
│  │  • Submission process                                   │    │
│  │  • PR guidelines                                        │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      📋 REFERENCE                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐ │
│  │  CHANGELOG.md    │  │  LICENSE         │  │ DOCS_        │ │
│  │  • Version       │  │  • MIT License   │  │  SUMMARY.md  │ │
│  │    history       │  │  • Copyright     │  │  • Overview  │ │
│  │  • Future plans  │  │  • Terms         │  │  • Stats     │ │
│  └──────────────────┘  └──────────────────┘  └──────────────┘ │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                     🎯 TASK-BASED NAVIGATION                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  I want to...                           → Go to...              │
│  ───────────────────────────────────────────────────────────────│
│  Understand the docs                    → DOCUMENTATION_GUIDE   │
│  Install the MCP server                 → README.md             │
│  Learn what each tool does              → TOOLS_REFERENCE.md    │
│  Create my first workflow               → README.md + samples/  │
│  Master FSM authoring                   → .cursorrules          │
│  See example workflows                  → workflows/samples/    │
│  Troubleshoot installation              → README.md             │
│  Debug a workflow run                   → TOOLS_REFERENCE.md    │
│  Contribute workflows                   → CONTRIBUTING.md       │
│  See what's changed                     → CHANGELOG.md          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    📊 LEARNING PATH                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Week 1: Basics                                                  │
│  ├─ README.md (installation & first workflow)                   │
│  ├─ TOOLS_REFERENCE.md (basics)                                 │
│  └─ workflows/samples/                                          │
│                                                                  │
│  Week 2: Intermediate                                            │
│  ├─ .cursorrules (state types)                                  │
│  ├─ TOOLS_REFERENCE.md (all tools)                              │
│  ├─ workflows/samples/ (study)                                  │
│  └─ Complex workflow                                            │
│                                                                  │
│  Week 3: Advanced                                                │
│  ├─ .cursorrules (advanced patterns)                            │
│  ├─ CONTRIBUTING.md                                             │
│  ├─ Production workflows                                        │
│  └─ Share with community                                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    🆘 TROUBLESHOOTING                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Installation issues          → README.md §Troubleshooting      │
│  API key problems             → README.md §Troubleshooting      │
│  Tool usage questions         → TOOLS_REFERENCE.md              │
│  Workflow not working         → .cursorrules §Common Pitfalls   │
│  Network connectivity         → README.md §Troubleshooting      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                     📦 REPOSITORY STRUCTURE                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  mcp-quickstart/                                                 │
│  ├── 📄 README.md               # Start here (complete guide)   │
│  ├── 📘 DOCUMENTATION_GUIDE.md  # Navigate docs                 │
│  ├── 📕 TOOLS_REFERENCE.md      # Tool reference                │
│  ├── 📙 CONTRIBUTING.md         # How to contribute             │
│  ├── 📋 CHANGELOG.md            # Version history               │
│  ├── 📜 LICENSE                 # MIT license                   │
│  ├── 📊 DOCS_SUMMARY.md         # Documentation summary         │
│  ├── 🗺️  DOCS_MAP.md            # This map                      │
│  ├── 🎯 .cursorrules            # FSM authoring                 │
│  ├── 🔧 setup-remote-mcp.sh     # Configure remote MCP in Cursor │
│  └── 📁 workflows/                                               │
│      └── your-workflow-name/    # Your workflows go here        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      💡 QUICK TIPS                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  • Start with README.md for complete setup guide                │
│  • Follow the learning path for best results                    │
│  • Use DOCUMENTATION_GUIDE.md to navigate docs                  │
│  • Bookmark TOOLS_REFERENCE.md for tool usage                   │
│  • Study .cursorrules before authoring workflows                │
│  • Check samples/ for working examples                          │
│  • Restart IDE after changing env vars or config                │
│  • Contact customer engineer for API key issues                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

                         Happy Automating! 🤖
```
