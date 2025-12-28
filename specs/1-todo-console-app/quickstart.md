# Quickstart Guide: Todo Console Application

## Prerequisites
- Python 3.13+ installed on your system
- UV package manager (if using dependencies beyond standard library)

## Setup
1. Clone or download the repository
2. Navigate to the project directory
3. Ensure Python 3.13+ is available in your environment

## Running the Application
```bash
cd src
python main.py
```

## Basic Usage
1. Launch the application with `python main.py`
2. You'll see a menu with options:
   - 1. Add Task
   - 2. View Tasks
   - 3. Update Task
   - 4. Delete Task
   - 5. Mark Task Complete/Incomplete
   - 6. Exit
3. Follow the prompts for each operation
4. Use task IDs (displayed in the task list) to identify tasks for update/delete/mark operations

## Example Workflow
1. Add a task: Select option 1, enter a title and optional description
2. View tasks: Select option 2 to see all tasks with their status
3. Mark a task complete: Select option 5, enter the task ID
4. Update a task: Select option 3, enter the task ID and new details
5. Delete a task: Select option 4, enter the task ID

## Expected Performance
- Adding a task: Should complete in under 3 seconds
- Viewing task list: Should complete in under 2 seconds (for up to 100 tasks)
- Updating a task: Should complete in under 3 seconds
- Deleting a task: Should complete in under 2 seconds
- Marking task complete/incomplete: Should complete in under 2 seconds

## Error Handling
- Invalid task IDs will show clear error messages
- Empty titles will be rejected with an error message
- The application will never crash, even with invalid input