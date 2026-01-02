# Data Model: Intelligent Todo Features

## Task Entity

### Fields
- **id**: int - Unique identifier for the task
- **title**: str - Title of the task
- **description**: str - Optional description of the task
- **completed**: bool - Whether the task is completed
- **created_at**: datetime - Timestamp when the task was created
- **priority**: str - Priority level ("high", "medium", "low")
- **tags**: set[str] - Set of tags associated with the task
- **due**: datetime | None - Due date/time for the task (new field)
- **recurrence**: str | None - Recurrence pattern ("daily", "weekly", "monthly", "yearly") (new field)
- **recurrence_config**: dict | None - Configuration for recurrence (e.g., {"days": [0,2,4]} for Mon/Wed/Fri) (new field)
- **next_due**: datetime | None - Next due date for recurring tasks (new field)

### Validation Rules
- **due**: Must be a valid datetime if provided
- **recurrence**: Must be one of "daily", "weekly", "monthly", "yearly" if provided
- **recurrence_config**: Must be a valid configuration for the recurrence type
  - For weekly: days must be integers 0-6 (0=Monday, 6=Sunday)
  - For monthly: day must be 1-31
  - For yearly: date must be in MM-DD format
- **next_due**: Must be a valid datetime if provided

### State Transitions
- **Normal task**: created → completed (via toggle/done command)
- **Recurring task**: created → completed → new instance created with updated due date
  - When a recurring task is marked complete, a new instance is automatically created with:
    - New ID
    - completed=False
    - Updated due date based on recurrence pattern
    - Same title, description, priority, tags, and recurrence settings

## Date/Time Utilities

### Natural Date Parser
- **Function**: parse_natural_date(text: str) -> datetime | None
- **Purpose**: Parse natural language date expressions like "tomorrow 3pm", "next friday", "in 2 days"
- **Implementation**: Uses dateutil.parser with relativedelta for relative dates

### Recurrence Calculator
- **Function**: calculate_next_occurrence(task: Task, current_date: datetime) -> datetime
- **Purpose**: Calculate the next occurrence date based on the recurrence pattern
- **Implementation**: Different logic for each recurrence type (daily, weekly, monthly, yearly)