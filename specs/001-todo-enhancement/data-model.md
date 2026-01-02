# Data Model: Enhanced Todo Application

## Task Entity

The Task entity is extended from Phase I with additional fields for priority and tags.

### Fields
- **id** (int): Unique identifier for the task (auto-incremented)
- **title** (str): The task title (required)
- **description** (str): Optional description for the task (default: "")
- **completed** (bool): Status indicator showing if the task is complete (default: False)
- **created_at** (datetime): Timestamp when the task was created (auto-generated)
- **priority** (str): Priority level of the task (values: "high", "medium", "low"; default: "medium")
- **tags** (set[str]): Set of tags associated with the task (default: empty set)

### Validation Rules
- `id`: Must be a positive integer, auto-incremented
- `title`: Cannot be empty or contain only whitespace
- `priority`: Must be one of "high", "medium", or "low" (case-insensitive, stored as lowercase)
- `tags`: Must be a set of strings, automatically deduplicated

### State Transitions
- `completed`: Can transition from False to True (marking complete) or True to False (marking incomplete)
- `priority`: Can be updated to any valid priority value
- `tags`: Can be added or removed, with automatic deduplication

## TaskList Entity

The TaskList entity remains largely unchanged but now manages tasks with additional fields.

### Fields
- **tasks** (list[Task]): Collection of Task entities
- **next_id** (int): Counter for generating next unique task ID

### Methods
- `add_task(title, description="", priority="medium", tags=None)`: Creates a new task with specified parameters
- `get_all_tasks()`: Returns all tasks in the collection
- `find_task(task_id)`: Retrieves a task by ID
- Additional filtering and sorting methods as needed

## Priority Enum

An implicit priority enumeration with three possible values:
- "high": Highest priority tasks
- "medium": Default priority level
- "low": Lowest priority tasks

Priority comparison order: high > medium > low