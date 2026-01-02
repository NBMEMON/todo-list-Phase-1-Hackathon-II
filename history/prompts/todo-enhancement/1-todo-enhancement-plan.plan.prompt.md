---
id: 1
title: "todo-enhancement-plan"
stage: "plan"
date_iso: "2025-12-30"
surface: "agent"
model: "default"
feature: "todo-enhancement"
branch: "001-todo-enhancement"
user: "user"
command: "/sp.plan"
labels: ["planning", "architecture", "design", "todo-app", "enhancement"]
links:
  spec: "../spec.md"
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "specs/001-todo-enhancement/plan.md"
  - "specs/001-todo-enhancement/research.md"
  - "specs/001-todo-enhancement/data-model.md"
  - "specs/001-todo-enhancement/quickstart.md"
  - "specs/001-todo-enhancement/contracts/cli-api-contract.md"
tests_yaml: []
prompt_text: "Todo In-Memory CLI Application - Implementation Plan v2.0 (Intermediate Level)\nProject Phase: II - Organization & Usability\nDate: December 30, 2025\nGoal: Add priorities, tags, search, filter, sort — while keeping Phase I stable\n\nImplementation Order (recommended sequence - easiest → hardest, best feedback loop)\n\n1. Priority Feature (≈ 1-2 hours)\n   - Update Task model: add priority: str = \"medium\"\n   - Valid values: \"high\", \"medium\", \"low\" (case insensitive, store lowercase)\n   - Modify add command: accept --priority / -p\n   - Modify update command: accept --priority\n   - Update list output: show (H)/(M)/(L) before title\n   - Add validation + error message for invalid priority\n\n2. Tags Feature (≈ 2-3 hours)\n   - Update Task model: add tags: set[str] = set()\n   - Commands:\n     add: --tag work --tag urgent (multiple allowed)\n     update: --add-tag report --remove-tag urgent\n   - List output: show #tag1 #tag2 after title (if any)\n   - Deduplicate tags automatically\n   - Case insensitive tags? → recommend store lowercase, compare lowercase\n\n3. Basic List Enhancements (filter + sort basics) (≈ 2 hours)\n   - Add arguments to list command:\n     --status / --done / --pending\n     --priority high/medium/low/all\n     --sort id (default) / priority / title / created (or date)\n   - Implement simple filtering in todo_service.get_tasks() or new method\n   - Implement sorting with key functions\n     priority order: high > medium > low\n     date: newest first for --sort date-desc (optional)\n\n4. Search Feature (≈ 1 hour)\n   - New command: search <keyword>\n   - Search in: title, description, tags (case insensitive, contains)\n   - Return filtered list using same pretty print as list\n   - If no keyword → show usage/help\n\n5. Advanced Filtering & Sorting Combinations (≈ 1-2 hours)\n   - Allow multiple filters together:\n     list --status pending --priority high --tag work --sort priority\n   - Use argparse with optional arguments\n   - Chain filters in service layer (filter then sort)\n\n6. Polish & Error Handling (≈ 1 hour)\n   - Better help/usage message (python main.py --help)\n   - Consistent error messages (red color if possible with ANSI)\n   - Show \"No tasks match your criteria\" when filter/search returns empty\n   - Keep Phase I commands working without new flags\n\nTechnical Decisions / Reminders\n\n- Argument parsing: Use argparse (stdlib) — best choice for subcommands + flags\n  Alternative: simple if-elif on sys.argv (faster to code but less nice)\n\n- Service layer changes:\n  - todo_service.py → add methods like:\n    get_filtered_tasks(status=None, priority=None, tag=None, search_term=None, sort_by=\"id\")\n  - Keep storage as list[Task], don't change to dict yet\n\n- Output improvements:\n  - Use rich or just basic ANSI colors for [x], (H), #tags\n  - Align columns if possible (id, status, priority, title, tags)\n\nEstimated Total Time (good coder + Qwen help): 8-12 hours\n\nRisks / Watch-outs\n- Don't break Phase I basic commands\n- Argument parsing bugs are common → test each flag combination\n- Tags with spaces? → disallow or replace with underscore\n- Keep code readable — separate concerns (model, service, cli)\n\nNext Steps After This Plan\n1. Update models.py with new fields\n2. Extend argparse in main.py\n3. Implement one feature → test → commit → repeat\n4. After each feature: run manual tests + update README examples\n\nStatus: Ready to start coding Intermediate Level\nUse this plan + previous specs to prompt Qwen for each piece of code"
response_text: "Successfully created the implementation plan for the Todo In-Memory CLI Application enhancement. The plan includes:\n\n1. Updated technical context based on existing codebase analysis\n2. Research document with technical decisions\n3. Data model documentation for the enhanced Task entity\n4. Quickstart guide for developers\n5. CLI API contracts\n6. Agent context updated with new technology stack information\n\nThe plan maintains backward compatibility with Phase I while adding the requested features: priorities, tags, search, filtering, and sorting."
outcome: "Created comprehensive implementation plan with all required documentation for the todo app enhancement project. The plan is ready for the next phase of task breakdown."
evaluation: "The implementation plan successfully addresses all requirements from the feature specification. It maintains backward compatibility with Phase I, uses only standard library dependencies as required, and provides clear documentation for developers. All necessary artifacts (research, data model, quickstart, contracts) have been created."
---

# Implementation Plan: Todo In-Memory CLI Application - Specification v2.0 (Intermediate Level)

**Branch**: `001-todo-enhancement` | **Date**: December 30, 2025 | **Spec**: [link](spec.md)
**Input**: Feature specification from `/specs/001-todo-enhancement/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This plan implements the intermediate-level enhancements to the existing todo CLI application, adding priorities, tags, search, filter, and sort capabilities while maintaining backward compatibility with Phase I functionality. The implementation will extend the existing Task model with priority and tags fields, enhance the CLI argument parsing to support new commands and options, and update the service layer to handle filtering, sorting, and searching operations.

## Technical Context

**Language/Version**: Python 3.8+ (existing codebase uses standard library features)
**Primary Dependencies**: Standard library only (argparse, datetime, etc.) - no external dependencies to maintain simplicity
**Storage**: In-memory only using existing list-based storage (no persistence changes)
**Testing**: pytest (based on existing test files in root directory)
**Target Platform**: Cross-platform console application (Windows, macOS, Linux)
**Project Type**: Single console application with CLI interface
**Performance Goals**: Sub-second response for all operations (given in-memory storage)
**Constraints**: Maintain backward compatibility with Phase I commands, no external dependencies, in-memory storage only
**Scale/Scope**: Single-user console application, up to 1000 tasks in memory

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Test-First (NON-NEGOTIABLE)**: All new features will have tests written before implementation
- **CLI Interface**: All functionality accessible via CLI commands as specified
- **Library-First**: Functionality will be implemented in service layer first, then exposed via CLI
- **Integration Testing**: New features will be tested with existing functionality to ensure no regressions

## Phase 1 Completion

- [x] research.md created with technical decisions
- [x] data-model.md created with updated entity definitions
- [x] quickstart.md created for developer onboarding
- [x] contracts/ directory created with API contracts
- [x] agent context updated with new technology stack information

## Project Structure

### Documentation (this feature)

```text
specs/001-todo-enhancement/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
├── models.py            # Task model with priority and tags fields
├── services.py          # TaskService with filtering, sorting, and search methods
├── main.py              # CLI interface with argparse for new commands/flags
└── utils.py             # Utility functions for formatting and validation

tests/
├── test_basic_functionality.py    # Phase I functionality tests
├── test_complete_functionality.py # Complete functionality tests
├── test_user_story_2.py          # User story specific tests
└── test_user_story_3.py          # User story specific tests

main.py              # Entry point script
```

**Structure Decision**: Single project structure will be maintained with enhancements to existing files rather than creating new directories. The existing src/ structure will be extended with new functionality in the appropriate modules.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [N/A] | [N/A] | [N/A] |