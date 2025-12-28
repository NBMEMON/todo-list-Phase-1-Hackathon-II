# Data Model: Todo Console Application

## Task Entity

**Name**: Task
**Fields**:
- `id`: Integer - Unique identifier for the task (auto-incremented)
- `title`: String (required) - The task title as specified in functional requirements
- `description`: String (optional) - Optional description for the task
- `completed`: Boolean - Status indicator showing if the task is complete (default: False)

**Validation rules**:
- `title` must not be empty (as required by FR-007 in spec)
- `id` must be unique within the task list
- `completed` must be a boolean value

**State transitions**:
- `completed` can transition from False to True (mark complete)
- `completed` can transition from True to False (mark incomplete)

## Task List Entity

**Name**: TaskList
**Fields**:
- `tasks`: List[Task] - Collection of Task entities
- `next_id`: Integer - Counter for generating next unique task ID

**Operations**:
- Add task: Appends a new task to the list with auto-generated ID
- Remove task: Removes a task by ID
- Update task: Modifies task properties by ID
- Find task: Retrieves a task by ID
- List all tasks: Returns all tasks in the collection

## Relationships
- TaskList contains multiple Task entities (one-to-many relationship)
- Each Task has a unique ID within its containing TaskList