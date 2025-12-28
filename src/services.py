"""
Service layer for the Todo Console Application.

This module contains the business logic for task operations.
"""

from models import TaskList


class TaskService:
    """
    Service class that handles all task-related operations.

    This class provides methods for adding, updating, deleting, and managing tasks
    according to the requirements specified in the feature specification.
    """

    def __init__(self):
        """
        Initialize the TaskService with a TaskList instance.
        """
        self.task_list = TaskList()

    def add_task(self, title, description=""):
        """
        Add a new task with required title and optional description.

        Args:
            title (str): The task title (required)
            description (str, optional): Optional description for the task. Defaults to "".

        Returns:
            Task: The newly created Task instance

        Raises:
            ValueError: If title is empty
        """
        if not title.strip():
            raise ValueError("Task title cannot be empty")

        return self.task_list.add_task(title.strip(), description.strip() if description else "")

    def get_all_tasks(self):
        """
        Get all tasks with clear status indicators.

        Returns:
            list: List of all Task instances in the task list
        """
        return self.task_list.get_all_tasks()

    def update_task(self, task_id, title=None, description=None):
        """
        Update an existing task by its unique ID.

        Args:
            task_id (int): The unique ID of the task to update
            title (str, optional): New title for the task. Defaults to None.
            description (str, optional): New description for the task. Defaults to None.

        Returns:
            bool: True if task was updated successfully, False if task not found

        Raises:
            ValueError: If title is provided but is empty
        """
        if title is not None and not title.strip():
            raise ValueError("Task title cannot be empty")

        # Prepare the new values, ensuring they are stripped of leading/trailing whitespace
        new_title = title.strip() if title else None
        new_description = description.strip() if description and description.strip() else ("" if description is not None else None)

        return self.task_list.update_task(task_id, new_title, new_description)

    def delete_task(self, task_id):
        """
        Delete a task by its unique ID.

        Args:
            task_id (int): The unique ID of the task to delete

        Returns:
            bool: True if task was deleted successfully, False if task not found
        """
        return self.task_list.remove_task(task_id)

    def mark_task_complete(self, task_id):
        """
        Mark a task as complete by its unique ID.

        Args:
            task_id (int): The unique ID of the task to mark complete

        Returns:
            bool: True if task was marked complete successfully, False if task not found
        """
        return self.task_list.mark_task_complete(task_id)

    def mark_task_incomplete(self, task_id):
        """
        Mark a task as incomplete by its unique ID.

        Args:
            task_id (int): The unique ID of the task to mark incomplete

        Returns:
            bool: True if task was marked incomplete successfully, False if task not found
        """
        return self.task_list.mark_task_incomplete(task_id)

    def get_task_by_id(self, task_id):
        """
        Get a specific task by its ID.

        Args:
            task_id (int): The unique ID of the task to retrieve

        Returns:
            Task or None: The Task instance if found, None otherwise
        """
        return self.task_list.find_task(task_id)