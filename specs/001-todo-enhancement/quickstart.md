# Quickstart Guide: Enhanced Todo CLI Application

## Getting Started

The enhanced todo application builds upon the original Phase I functionality with new features for priorities, tags, search, filtering, and sorting.

### Prerequisites
- Python 3.8 or higher
- No external dependencies required

### Running the Application
```bash
python main.py
```

## New Features Overview

### 1. Task Priorities
Each task can have a priority level: high, medium, or low (default: medium)

### 2. Task Tags
Tasks can be categorized with multiple tags (e.g., work, personal, urgent)

### 3. Search Functionality
Search through all tasks by keyword in title, description, or tags

### 4. Filtering & Sorting
Filter tasks by status, priority, or tags; sort by various criteria

## Command Examples

### Adding Tasks with Priority and Tags
```bash
# Add a high priority task with tags
python main.py add "Finish report" "Q4 summary" --priority high --tag work --tag urgent

# Add a task with default priority and multiple tags
python main.py add "Buy groceries" --tag home --tag shopping
```

### Listing Tasks with Filters and Sorting
```bash
# List all pending tasks
python main.py list --status pending

# List high priority tasks
python main.py list --priority high

# List tasks with specific tag
python main.py list --tag work

# Sort tasks by priority
python main.py list --sort priority

# Combine filters and sorting
python main.py list --status pending --priority high --sort created
```

### Searching Tasks
```bash
# Search for tasks containing "python"
python main.py search python
```

### Updating Tasks
```bash
# Update task priority and add tags
python main.py update 1 --priority low --add-tag report

# Remove tags from a task
python main.py update 1 --remove-tag urgent
```

## Backward Compatibility

All Phase I functionality remains unchanged:
- Menu-driven interface still available
- Original commands continue to work as before
- No breaking changes to existing functionality

## Development

### Running Tests
```bash
pytest
```

### File Structure
- `src/models.py`: Enhanced Task model with priority and tags
- `src/services.py`: TaskService with filtering, sorting, and search methods
- `src/main.py`: CLI interface with argparse for new commands
- `src/utils.py`: Utility functions for formatting and validation