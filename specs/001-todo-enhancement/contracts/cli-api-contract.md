# CLI API Contract: Enhanced Todo Application

## Overview
This document specifies the command-line interface contracts for the enhanced todo application, including new functionality for priorities, tags, search, filtering, and sorting.

## Command Structure
```
python main.py [command] [arguments] [options]
```

## Commands

### 1. Add Task
**Command**: `add`
**Description**: Add a new task with optional description, priority, and tags
**Arguments**:
- `title` (required): Task title
- `description` (optional): Task description

**Options**:
- `--priority, -p`: Priority level (high, medium, low; default: medium)
- `--tag, -t`: Add tag to task (can be used multiple times)

**Example**:
```bash
python main.py add "Finish report" "Q4 summary" --priority high --tag work --tag urgent
```

**Success Response**: Task added successfully with ID
**Error Response**: Error message explaining the issue

### 2. List Tasks
**Command**: `list`
**Description**: List all tasks with optional filtering and sorting
**Options**:
- `--status`: Filter by status (done, pending, all; default: all)
- `--priority`: Filter by priority (high, medium, low, all; default: all)
- `--tag`: Filter by tag
- `--sort`: Sort by (id, priority, title, created; default: id)
- `--order`: Sort order (asc, desc; default: asc for id/title, desc for created)

**Example**:
```bash
python main.py list --status pending --priority high --sort priority
```

**Success Response**: Formatted list of tasks matching criteria
**Error Response**: Error message if invalid filter/sort options provided

### 3. Search Tasks
**Command**: `search`
**Description**: Search tasks by keyword in title, description, or tags
**Arguments**:
- `keyword` (required): Search term

**Example**:
```bash
python main.py search python
```

**Success Response**: Formatted list of matching tasks
**Error Response**: Error message if keyword is empty

### 4. Update Task
**Command**: `update`
**Description**: Update an existing task's properties
**Arguments**:
- `id` (required): Task ID to update
- `title` (optional): New title
- `description` (optional): New description

**Options**:
- `--priority, -p`: New priority level
- `--add-tag`: Add tag to task (can be used multiple times)
- `--remove-tag`: Remove tag from task (can be used multiple times)

**Example**:
```bash
python main.py update 1 --priority low --add-tag report --remove-tag urgent
```

**Success Response**: Task updated successfully
**Error Response**: Error message if task not found or invalid inputs

### 5. Delete Task
**Command**: `delete`
**Description**: Delete a task by ID
**Arguments**:
- `id` (required): Task ID to delete

**Example**:
```bash
python main.py delete 1
```

**Success Response**: Task deleted successfully
**Error Response**: Error message if task not found

### 6. Mark Task Complete/Incomplete
**Command**: `done` or `undone`
**Description**: Mark a task as complete or incomplete
**Arguments**:
- `id` (required): Task ID to update

**Example**:
```bash
python main.py done 1
python main.py undone 1
```

**Success Response**: Task status updated successfully
**Error Response**: Error message if task not found

## Common Error Responses

### Invalid Priority
**Error**: "Invalid priority. Valid options: high, medium, low"
**Trigger**: Using an invalid priority value

### Invalid Status
**Error**: "Invalid status. Valid options: done, pending, all"
**Trigger**: Using an invalid status filter

### Task Not Found
**Error**: "Task with ID X not found"
**Trigger**: Referencing a non-existent task ID

### Empty Title
**Error**: "Task title cannot be empty"
**Trigger**: Attempting to create or update a task with an empty title

## Output Format

### Task Display Format
```
[✓/○] ID. (P) TITLE #tag1 #tag2 - DESCRIPTION
```
Where:
- `✓` indicates completed task, `○` indicates pending task
- `P` is the priority indicator: H (high), M (medium), L (low)
- `#tag1 #tag2` are the associated tags
- `DESCRIPTION` is the task description (if any)

### Example Output
```
[x] 3. (H) Finish report #work #urgent - Q4 final
[ ] 7. (M) Buy groceries #home - Milk and bread
```

## Backward Compatibility
All Phase I commands and functionality remain unchanged to ensure backward compatibility.