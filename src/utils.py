"""
Utility functions for the Todo Console Application.

This module contains helper functions for input validation, output formatting,
and other utility operations.
"""

try:
    from ..lib.display import format_task_line_with_color
except ImportError:
    from src.lib.display import format_task_line_with_color


def validate_task_title(title):
    """
    Validate that a task title is not empty.

    Args:
        title (str): The title to validate

    Returns:
        bool: True if title is valid (not empty), False otherwise
    """
    return bool(title and title.strip())


def format_task_display(task):
    """
    Format a task for display with clear status indicators.

    Args:
        task (Task): The task to format

    Returns:
        str: Formatted string representation of the task
    """
    # Use the legacy format for backward compatibility with existing tests
    return str(task)


def format_task_list_display(tasks):
    """
    Format a list of tasks for display.

    Args:
        tasks (list): List of Task objects to format

    Returns:
        str: Formatted string with all tasks
    """
    if not tasks:
        return "No tasks found."

    formatted_tasks = []
    for task in tasks:
        formatted_tasks.append(format_task_display(task))

    return "\n".join(formatted_tasks)


def format_task_display_enhanced(task):
    """
    Format a task for display with clear status indicators, priority, and tags.

    Args:
        task (Task): The task to format

    Returns:
        str: Formatted string representation of the task with priority and tags
    """
    # Use the new display formatting that includes due dates and recurrence indicators
    return format_task_line_with_color(task)


def format_task_list_display_enhanced(tasks):
    """
    Format a list of tasks for display with priority and tags.

    Args:
        tasks (list): List of Task objects to format

    Returns:
        str: Formatted string with all tasks including priority and tags
    """
    if not tasks:
        return "No tasks found."

    formatted_tasks = []
    for task in tasks:
        formatted_tasks.append(format_task_display_enhanced(task))

    return "\n".join(formatted_tasks)


def get_valid_task_id_input(prompt="Enter task ID: ", task_list=None):
    """
    Get a valid task ID from user input with validation.

    Args:
        prompt (str): The prompt to display to the user
        task_list (list, optional): List of valid tasks to check against

    Returns:
        int or None: The valid task ID, or None if invalid input or not in task list
    """
    try:
        task_id = int(input(prompt))
        if task_list is not None:
            # Check if the task ID exists in the provided task list
            task_exists = any(task.id == task_id for task in task_list)
            if not task_exists:
                print(f"Error: Task with ID {task_id} does not exist.")
                return None
        return task_id
    except ValueError:
        print("Error: Please enter a valid number for the task ID.")
        return None


def get_user_choice(min_val, max_val, prompt):
    """
    Get a valid numeric choice from the user within a specified range.

    Args:
        min_val (int): Minimum valid value
        max_val (int): Maximum valid value
        prompt (str): Prompt to display to the user

    Returns:
        int or None: The valid choice, or None if invalid input
    """
    try:
        choice = int(input(prompt))
        if min_val <= choice <= max_val:
            return choice
        else:
            print(f"Error: Please enter a number between {min_val} and {max_val}.")
            return None
    except ValueError:
        print("Error: Please enter a valid number.")
        return None


def confirm_action(message="Are you sure?"):
    """
    Ask the user to confirm an action.

    Args:
        message (str): The confirmation message to display

    Returns:
        bool: True if user confirms, False otherwise
    """
    response = input(f"{message} (y/n): ").lower().strip()
    return response in ['y', 'yes', '1', 'true', 'ok']


def display_menu():
    """
    Display the main menu options to the user.
    """
    print("\n" + "="*40)
    print("TODO CONSOLE APPLICATION")
    print("="*40)
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Mark Task Complete/Incomplete")
    print("6. Exit")
    print("="*40)


def clear_screen():
    """
    Clear the console screen (cross-platform).
    """
    import os
    os.system('cls' if os.name == 'nt' else 'clear')