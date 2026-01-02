---
id: 2
title: intelligent-todo-features-plan
stage: plan
date_iso: 2026-01-02
surface: agent
model: Qwen
feature: intelligent-todo-features
branch: 002-intelligent-todo-features
user: user
command: /sp.plan
labels: ["planning", "todo", "features"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "specs/002-intelligent-todo-features/plan.md"
  - "specs/002-intelligent-todo-features/research.md"
  - "specs/002-intelligent-todo-features/data-model.md"
  - "specs/002-intelligent-todo-features/quickstart.md"
  - "specs/002-intelligent-todo-features/contracts/cli-contracts.md"
tests_yaml: []
prompt_text: |
  Todo In-Memory CLI Application - Implementation Plan v3.0 (Advanced Level)
  Project Phase: III - Intelligent Features
  Date: January 02, 2026
  Goal: Add recurring tasks + due dates/reminders without external dependencies
  All features remain in-memory and session-based

  Recommended Implementation Order (safest & fastest feedback loop)

  1. Due Date Feature (Foundation - 2-4 hours)
     - Add field to Task model: due: datetime | None
     - Install dateutil (if not already): pip install python-dateutil
       (it's very common & lightweight - acceptable for advanced phase)
     - Create helper function: parse_natural_date(text: str) -> datetime | None
       Use dateutil.parser.parse() + relativedelta for "tomorrow", "next monday", "in 2 days", etc.
     - Update add command: support --due "tomorrow 3pm" / -d "2026-01-15"
     - Update update command: same --due flag
     - Enhance list output:
       - Show "due: YYYY-MM-DD HH:MM" if set
       - Show "(OVERDUE)" in red if past due
       - Show countdown if due soon (<24h): e.g. "in 3h 45m"
     - Add optional filters: list --overdue, list --due-today

  2. Basic Recurrence Setup (Core logic - 3-5 hours)
     - Add fields to Task:
       recurrence: str | None     ("daily", "weekly", "monthly", "yearly")
       recurrence_config: dict | None   (e.g. {"days": [0,1,3]} for Mon,Tue,Thu)
     - Update add command:
       --recurring daily
       --recurring weekly --recurring-days mon,tue,wed
       --recurring monthly (default day = current day of month)
     - Simple validation: only allow valid patterns
     - When creating task with recurrence → set initial next_due = due or today

  3. Recurring Completion Logic (The intelligent part - 2-4 hours)
     - Modify done/toggle command:
       If task is recurring and being marked complete:
         - Create new Task instance (copy most fields)
         - Generate next due date based on recurrence rule
         - Assign new incremental ID
         - Set completed=False, due=next_due
         - Add new task to storage
         - Mark original as complete
       Else → normal toggle
     - Implement next_due calculation functions (simple rules):
       - daily: current_due + 1 day
       - weekly: find next matching weekday
       - monthly: same day next month (handle 31→28 edge)
       - yearly: same date next year
     - Use dateutil.relativedelta for clean date math

  4. Visual & Usability Polish (1-2 hours)
     - In list output for recurring tasks:
       Show small indicator e.g. ↻ or (recurring)
     - Show next occurrence preview if applicable
     - Better overdue visual: ANSI red + (!) prefix
     - When app starts (in main): optional "Welcome back! X tasks are overdue"

  5. Edge Cases & Final Testing (1-2 hours)
     - Test combinations: recurring + high priority + tags + due date
     - Invalid recurrence → error message
     - Recurrence without due date → set to today + warn
     - Marking non-recurring → no clone
     - Multiple completions in same session → multiple next instances
     - Timezone handling: use datetime.now() local time
     - Preserve all previous features (basic + intermediate)

  Technical Stack Additions
  - Required: python-dateutil (for natural parsing & date math)
  - Optional: colorama or just ANSI codes for colors
  - Still zero heavy dependencies

  Estimated Total Time (with good LLM help): 10-18 hours

  Risks / Common Pitfalls
  - Date parsing failures → fallback to strict YYYY-MM-DD
  - Infinite loop risk if recurrence logic is wrong → add max iterations safeguard
  - ID conflicts when cloning → use existing ID generator
  - Mutable datetimes → always create new datetime objects

  Development Sequence Suggestion
  1. Update models.py with new fields
  2. Create date parsing helper in utils.py or services
  3. Add --due support to add/update
  4. Add visual enhancements to list output
  5. Implement recurrence fields + validation
  6. Finally: implement the clone-on-complete logic in todo_service.mark_complete()
  7. Test heavily with different recurrence patterns

  Status: Ready to start Advanced Level coding
  Use this plan + previous specs to prompt Qwen/Claude step-by-step
  Focus on due dates first — it's the most visible & rewarding part
response_text: |
  Successfully created the implementation plan for intelligent todo features. The plan includes:
  - Updated technical context with project details
  - Constitution check that passes all requirements
  - Project structure with source code organization
  - Research summary with technology decisions
  - Data model with field definitions and validation rules
  - Quickstart guide for using the new features
  - API contracts for the enhanced CLI commands
  - Agent context updated with new technologies
outcome: |
  Implementation plan is complete and ready for the next phase. All required artifacts have been created and the agent context has been updated with the new technologies for the intelligent todo features.
evaluation: |
  The implementation plan is comprehensive and covers all aspects of the intelligent todo features. All required documentation has been created and the project is ready to move to the task breakdown phase.
---
