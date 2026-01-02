# Feature Specification: Intelligent Todo Features

**Feature Branch**: `002-intelligent-todo-features`
**Created**: January 02, 2026
**Status**: Draft
**Input**: User description: "Todo In-Memory CLI Application - Specification v3.0 (Advanced Level) Project: Todo In-Memory Python Console App Phase: III - Intelligent Features Date: January 02, 2026 CLI Style: Same command/subcommand style Storage: Still in-memory only (data lost on exit - advanced features are in-memory too) 1. Goal of Advanced Level Add intelligent, time-aware features to make the app truly useful Focus on recurring tasks and due dates/reminders Keep everything lightweight – no external scheduler/daemon in Phase III All features must work within a single console session 2. New Required Features (must implement both) A. Recurring Tasks - Task can be recurring with these patterns: - daily - weekly (optionally on specific days: mon,tue,wed,thu,fri,sat,sun) - monthly (on specific day of month 1-31) - yearly (on specific date mm-dd) - When a recurring task is marked complete → auto-create next occurrence - Next due date calculated based on current date + recurrence rule - Fields added to Task: recurrence: str or None ("daily", "weekly", "monthly", "yearly" or None) recurrence_days: list[int] or None (for weekly: 0=mon ... 6=sun) next_due: date or datetime or None B. Due Dates & Reminders - Each task can have a due date/time - Format: flexible parsing (e.g. "tomorrow 3pm", "2026-01-15", "next friday", "in 2 days") - Show overdue tasks in red/bold in list output - Due date/time shown in list (e.g. due: 2026-01-05 15:00) - Simple in-session reminder: - When listing tasks → show countdown for tasks due soon (<24h) - Optional: if task is overdue → mark with (!) or red - Bonus polish (strongly recommended): - When marking complete a recurring task → auto-generate next instance with updated due date - When app starts → check & show any "due now" or overdue tasks 3. Updated Data Model Task (extends Intermediate): - id: int - title: str - description: str - completed: bool - created_at: datetime - priority: str ("high","medium","low") - tags: set[str] - due: datetime or None ← NEW (aware datetime) - recurrence: str or None ← NEW ("daily","weekly","monthly","yearly") - recurrence_config: dict or None ← NEW (e.g. {"days": [0,2,4]} for mon,wed,fri) - next_due: datetime or None ← NEW (for recurring only) 4. New/Updated Command Syntax Examples add "Weekly team meeting" --due "next monday 11:00" --recurring weekly --recurring-days mon add "Pay rent" --due "2026-02-01" --recurring monthly update 5 --due "tomorrow 18:00" --recurring daily done 3 # if recurring → creates next instance automatically list # shows due dates, overdue in red, countdown if soon list --overdue # only show overdue tasks list --due-today # optional filter Natural language date support (highly recommended): - tomorrow, today, next monday, in 3 days, 2 weeks from now, etc. - Use dateutil.parser for flexible parsing 5. List Output Format Suggestion (enhanced again) [x] 3. (H) Weekly team meeting #work due: 2026-01-06 11:00 (in 2 days) [!] 7. (M) Submit report due: 2026-01-01 23:59 (OVERDUE 1 day) [ ] 12. (L) Grocery shopping #home due: 2026-01-04 6. Edge Cases & Behaviors to Handle - Invalid date format → error + show examples - Recurring task with no due date → error or set to today - Marking non-recurring complete → normal behavior - Marking recurring complete → create next occurrence (copy task, update due/next_due) - Overdue tasks → show warning on list command - Timezone → use local time (datetime.now()) - When next occurrence is created: - new id - completed=False - due/next_due updated - same title/desc/priority/tags/recurrence 7. Technical Decisions / Recommendations - Date parsing: use dateutil.parser + relativedelta (from dateutil) for "in 2 days", "next monday" - Recurrence logic: simple if/elif rules (no full rrule library – keep stdlib) - Overdue check: current_time > due - "Soon" threshold: due within next 24h → show countdown (e.g. "in 4h 30m") - Colors: use ANSI escape codes (no rich dependency) 8. Acceptance Criteria for Advanced Level - Can create recurring tasks (at least daily & weekly) - Can set due dates with natural language - Marking recurring task complete creates next instance automatically - List shows due dates, overdue highlighted, soon tasks with countdown - All previous features (basic + intermediate) still work - No crashes on invalid dates/recurrence - Helpful error messages Status: Ready for implementation after Intermediate Level Next: Update models, add date parsing helper, modify done command logic, enhance list output Use Qwen / Claude to generate code step-by-step from this spec"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create Recurring Tasks (Priority: P1)

A user wants to create recurring tasks that automatically generate new instances when completed. For example, they want to schedule a weekly team meeting every Monday at 11 AM or a monthly rent payment reminder.

**Why this priority**: This is the core functionality that differentiates the app from basic todo lists. It provides significant value by automating repetitive task creation.

**Independent Test**: Can be fully tested by creating a recurring task with various patterns (daily, weekly, monthly, yearly) and verifying that a new instance is created when the original is marked complete.

**Acceptance Scenarios**:

1. **Given** a user wants to create a recurring task, **When** they use the add command with recurrence options, **Then** the task is created with the specified recurrence pattern and due date
2. **Given** a recurring task exists, **When** the user marks it as complete, **Then** a new instance of the task is automatically created with an updated due date based on the recurrence pattern

---

### User Story 2 - Set and View Due Dates (Priority: P1)

A user wants to assign due dates to tasks using natural language (e.g., "tomorrow 3pm", "next friday") and see these dates displayed when viewing their task list.

**Why this priority**: Due dates are essential for time management and task prioritization. Natural language parsing makes the feature user-friendly.

**Independent Test**: Can be fully tested by creating tasks with due dates using natural language and verifying they display correctly in the list command.

**Acceptance Scenarios**:

1. **Given** a user wants to create a task with a due date, **When** they use the add command with a natural language due date, **Then** the task is created with the correctly parsed due date
2. **Given** tasks with due dates exist, **When** the user runs the list command, **Then** the due dates are displayed in a clear format next to each task

---

### User Story 3 - View Overdue and Soon-Due Tasks (Priority: P2)

A user wants to quickly identify overdue tasks and tasks that are due soon (within 24 hours) to prioritize their work.

**Why this priority**: This provides important visibility into urgent tasks and helps users manage their time effectively.

**Independent Test**: Can be fully tested by creating tasks with past due dates and tasks due soon, then verifying they are highlighted appropriately in the list output.

**Acceptance Scenarios**:

1. **Given** tasks with past due dates exist, **When** the user runs the list command, **Then** overdue tasks are highlighted in red/bold with an indicator
2. **Given** tasks due within 24 hours exist, **When** the user runs the list command, **Then** these tasks show a countdown (e.g. "in 4h 30m")

---

### User Story 4 - Filter Tasks by Due Status (Priority: P3)

A user wants to filter their task list to see only overdue tasks or tasks due today.

**Why this priority**: This provides additional convenience for users who want to focus on specific time-sensitive tasks.

**Independent Test**: Can be fully tested by creating various tasks with different due dates and using the filter options to verify only the appropriate tasks are displayed.

**Acceptance Scenarios**:

1. **Given** tasks with various due dates exist, **When** the user runs the list command with the --overdue flag, **Then** only overdue tasks are displayed
2. **Given** tasks with various due dates exist, **When** the user runs the list command with the --due-today flag, **Then** only tasks due today are displayed

---

### Edge Cases

- What happens when a user enters an invalid date format?
- How does the system handle recurring tasks with no due date?
- What happens when a recurring task is marked complete - does it follow the correct recurrence logic?
- How does the system handle tasks with due dates in the past?
- What happens when the system encounters ambiguous date expressions?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST support creating tasks with due dates using natural language parsing (e.g. "tomorrow 3pm", "next friday", "in 2 days")
- **FR-002**: System MUST support recurring tasks with patterns: daily, weekly, monthly, yearly
- **FR-003**: System MUST automatically create a new instance of a recurring task when the current instance is marked complete
- **FR-004**: System MUST display due dates in the list output in a clear format (e.g. due: 2026-01-05 15:00)
- **FR-005**: System MUST highlight overdue tasks in red/bold in the list output
- **FR-006**: System MUST show countdown for tasks due soon (<24h) in the list output (e.g. "in 4h 30m")
- **FR-007**: System MUST support filtering tasks by due status (--overdue, --due-today)
- **FR-008**: System MUST provide helpful error messages when invalid date formats are entered
- **FR-009**: System MUST handle weekly recurring tasks with specific days (mon,tue,wed,thu,fri,sat,sun)
- **FR-010**: System MUST handle monthly recurring tasks on specific days of the month (1-31)
- **FR-011**: System MUST handle yearly recurring tasks on specific dates (mm-dd)
- **FR-012**: System MUST preserve all existing task functionality (title, description, priority, tags, etc.) when adding due dates and recurrence
- **FR-013**: System MUST use local time for all date/time operations
- **FR-014**: System MUST calculate the next occurrence date based on the current date and recurrence rule when creating new instances of recurring tasks

### Key Entities

- **Task**: Represents a single task with id, title, description, completed status, creation date, priority, tags, due date, recurrence pattern, recurrence configuration, and next due date
- **Due Date**: Represents a specific date and time when a task is due, supporting natural language parsing
- **Recurrence Pattern**: Defines how often a task repeats (daily, weekly, monthly, yearly) with optional configuration for specific days/dates

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can create recurring tasks with at least daily and weekly patterns in under 30 seconds
- **SC-002**: Natural language date parsing correctly interprets at least 90% of common expressions (tomorrow, next monday, in 2 days, etc.)
- **SC-003**: When marking a recurring task complete, the next instance is created automatically within 1 second
- **SC-004**: Overdue tasks are clearly highlighted in the list output, with 95% of users able to identify them on first glance
- **SC-005**: The system handles invalid date formats gracefully with helpful error messages in 100% of cases
- **SC-006**: Tasks due within 24 hours display a countdown timer that updates in real-time
- **SC-007**: All previous functionality of the todo app continues to work without degradation after implementing these features
