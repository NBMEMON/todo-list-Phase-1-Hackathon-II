---
id: 1
title: intelligent-todo-features
stage: spec
date_iso: 2026-01-02
surface: agent
model: Qwen
feature: intelligent-todo-features
branch: 002-intelligent-todo-features
user: user
command: /sp.specify
labels: ["specification", "todo", "features"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "specs/002-intelligent-todo-features/spec.md"
  - "specs/002-intelligent-todo-features/checklists/requirements.md"
tests_yaml: []
prompt_text: |
  Todo In-Memory CLI Application - Specification v3.0 (Advanced Level) Project: Todo In-Memory Python Console App Phase: III - Intelligent Features Date: January 02, 2026 CLI Style: Same command/subcommand style Storage: Still in-memory only (data lost on exit - advanced features are in-memory too) 1. Goal of Advanced Level Add intelligent, time-aware features to make the app truly useful Focus on recurring tasks and due dates/reminders Keep everything lightweight – no external scheduler/daemon in Phase III All features must work within a single console session 2. New Required Features (must implement both) A. Recurring Tasks - Task can be recurring with these patterns: - daily - weekly (optionally on specific days: mon,tue,wed,thu,fri,sat,sun) - monthly (on specific day of month 1-31) - yearly (on specific date mm-dd) - When a recurring task is marked complete → auto-create next occurrence - Next due date calculated based on current date + recurrence rule - Fields added to Task: recurrence: str or None ("daily", "weekly", "monthly", "yearly" or None) recurrence_days: list[int] or None (for weekly: 0=mon ... 6=sun) next_due: date or datetime or None B. Due Dates & Reminders - Each task can have a due date/time - Format: flexible parsing (e.g. "tomorrow 3pm", "2026-01-15", "next friday", "in 2 days") - Show overdue tasks in red/bold in list output - Due date/time shown in list (e.g. due: 2026-01-05 15:00) - Simple in-session reminder: - When listing tasks → show countdown for tasks due soon (<24h) - Optional: if task is overdue → mark with (!) or red - Bonus polish (strongly recommended): - When marking complete a recurring task → auto-generate next instance with updated due date - When app starts → check & show any "due now" or overdue tasks 3. Updated Data Model Task (extends Intermediate): - id: int - title: str - description: str - completed: bool - created_at: datetime - priority: str ("high","medium","low") - tags: set[str] - due: datetime or None ← NEW (aware datetime) - recurrence: str or None ← NEW ("daily","weekly","monthly","yearly") - recurrence_config: dict or None ← NEW (e.g. {"days": [0,2,4]} for mon,wed,fri) - next_due: datetime or None ← NEW (for recurring only) 4. New/Updated Command Syntax Examples add "Weekly team meeting" --due "next monday 11:00" --recurring weekly --recurring-days mon add "Pay rent" --due "2026-02-01" --recurring monthly update 5 --due "tomorrow 18:00" --recurring daily done 3 # if recurring → creates next instance automatically list # shows due dates, overdue in red, countdown if soon list --overdue # only show overdue tasks list --due-today # optional filter Natural language date support (highly recommended): - tomorrow, today, next monday, in 3 days, 2 weeks from now, etc. - Use dateutil.parser for flexible parsing 5. List Output Format Suggestion (enhanced again) [x] 3. (H) Weekly team meeting #work due: 2026-01-06 11:00 (in 2 days) [!] 7. (M) Submit report due: 2026-01-01 23:59 (OVERDUE 1 day) [ ] 12. (L) Grocery shopping #home due: 2026-01-04 6. Edge Cases & Behaviors to Handle - Invalid date format → error + show examples - Recurring task with no due date → error or set to today - Marking non-recurring complete → normal behavior - Marking recurring complete → create next occurrence (copy task, update due/next_due) - Overdue tasks → show warning on list command - Timezone → use local time (datetime.now()) - When next occurrence is created: - new id - completed=False - due/next_due updated - same title/desc/priority/tags/recurrence 7. Technical Decisions / Recommendations - Date parsing: use dateutil.parser + relativedelta (from dateutil) for "in 2 days", "next monday" - Recurrence logic: simple if/elif rules (no full rrule library – keep stdlib) - Overdue check: current_time > due - "Soon" threshold: due within next 24h → show countdown (e.g. "in 4h 30m") - Colors: use ANSI escape codes (no rich dependency) 8. Acceptance Criteria for Advanced Level - Can create recurring tasks (at least daily & weekly) - Can set due dates with natural language - Marking recurring task complete creates next instance automatically - List shows due dates, overdue highlighted, soon tasks with countdown - All previous features (basic + intermediate) still work - No crashes on invalid dates/recurrence - Helpful error messages Status: Ready for implementation after Intermediate Level Next: Update models, add date parsing helper, modify done command logic, enhance list output Use Qwen / Claude to generate code step-by-step from this spec
response_text: |
  Created a comprehensive feature specification for intelligent todo features including recurring tasks and due dates. The specification includes user scenarios, functional requirements, and success criteria. A quality checklist was also created to validate the specification.
outcome: |
  Successfully created and validated the feature specification for intelligent todo features with recurring tasks and due dates. The specification is ready for the planning phase.
evaluation: |
  The specification is complete, well-structured, and ready for implementation planning. All required sections have been filled out with appropriate content based on the feature description.
---
