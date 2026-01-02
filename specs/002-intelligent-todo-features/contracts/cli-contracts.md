# API Contracts: Intelligent Todo Features

## Command Line Interface Contracts

### Add Command Enhancements
```
add "task title" [description] [--due DUE_DATE] [--recurring PATTERN] [--recurring-days DAYS]
```

**Parameters:**
- `title`: Required string, the task title
- `description`: Optional string, task description
- `--due`: Optional string, due date in natural language ("tomorrow 3pm", "next monday")
- `--recurring`: Optional string, recurrence pattern ("daily", "weekly", "monthly", "yearly")
- `--recurring-days`: Optional string, days for weekly recurrence ("mon,tue,wed")

**Success Response:**
- Status: 0
- Output: "Task added with ID: {id}"

**Error Responses:**
- Invalid date format: Status 1, Error message with examples
- Invalid recurrence pattern: Status 1, Error message with valid patterns

### Update Command Enhancements
```
update ID [--title TITLE] [--description DESCRIPTION] [--due DUE_DATE] [--recurring PATTERN] [--recurring-days DAYS]
```

**Parameters:**
- `ID`: Required integer, task ID
- `--title`: Optional string, new title
- `--description`: Optional string, new description
- `--due`: Optional string, due date in natural language
- `--recurring`: Optional string, recurrence pattern
- `--recurring-days`: Optional string, days for weekly recurrence

**Success Response:**
- Status: 0
- Output: "Task {id} updated"

**Error Responses:**
- Task not found: Status 1, Error message
- Invalid date format: Status 1, Error message with examples

### List Command Enhancements
```
list [--overdue] [--due-today]
```

**Parameters:**
- `--overdue`: Optional flag, show only overdue tasks
- `--due-today`: Optional flag, show only tasks due today

**Success Response:**
- Status: 0
- Output: Formatted task list with due dates, overdue indicators, and countdowns

### Done Command Behavior
```
done ID
```

**Behavior for Recurring Tasks:**
- When a recurring task is marked complete, a new instance is automatically created
- New task has updated due date based on recurrence pattern
- Original task is marked as completed

## Data Model Contracts

### Task Object
```
{
  "id": int,
  "title": str,
  "description": str,
  "completed": bool,
  "created_at": datetime,
  "priority": str,
  "tags": set[str],
  "due": datetime | None,
  "recurrence": str | None,
  "recurrence_config": dict | None,
  "next_due": datetime | None
}
```

## Date Parsing Contract

### parse_natural_date(text: str) -> datetime | None
- Accepts natural language date expressions
- Returns datetime object or None if parsing fails
- Supports expressions like: "tomorrow", "next monday", "in 2 days", "2026-01-15 3pm"