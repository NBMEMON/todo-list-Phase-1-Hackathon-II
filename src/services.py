"""
Service layer for the Todo Console Application.

This module contains the business logic for task operations.
"""

try:
    from .persistent_task_list import PersistentTaskList
    from .services_pkg.date_utils import calculate_next_occurrence
except ImportError:
    from persistent_task_list import PersistentTaskList
    from services_pkg.date_utils import calculate_next_occurrence


class TaskService:
    """
    Service class that handles all task-related operations.

    This class provides methods for adding, updating, deleting, and managing tasks
    according to the requirements specified in the feature specification.
    """

    def __init__(self):
        """
        Initialize the TaskService with a PersistentTaskList instance.
        """
        self.task_list = PersistentTaskList()

    def add_task(self, title, description="", priority="medium", tags=None,
                 due=None, recurrence=None, recurrence_config=None):
        """
        Add a new task with required title and optional description, priority, tags, due date, and recurrence.

        Args:
            title (str): The task title (required)
            description (str, optional): Optional description for the task. Defaults to "".
            priority (str, optional): Priority level. Defaults to "medium".
            tags (set, optional): Set of tags. Defaults to empty set.
            due (datetime, optional): Due date/time. Defaults to None.
            recurrence (str, optional): Recurrence pattern. Defaults to None.
            recurrence_config (dict, optional): Recurrence configuration. Defaults to None.

        Returns:
            Task: The newly created Task instance

        Raises:
            ValueError: If title is empty or priority is invalid
        """
        if not title.strip():
            raise ValueError("Task title cannot be empty")

        if priority not in ["high", "medium", "low"]:
            raise ValueError("Priority must be one of 'high', 'medium', or 'low'")

        return self.task_list.add_task(
            title.strip(),
            description.strip() if description else "",
            priority,
            tags,
            due=due,
            recurrence=recurrence,
            recurrence_config=recurrence_config
        )

    def get_all_tasks(self):
        """
        Get all tasks with clear status indicators.

        Returns:
            list: List of all Task instances in the task list
        """
        return self.task_list.get_all_tasks()

    def update_task(self, task_id, title=None, description=None, priority=None, tags=None,
                    add_tags=None, remove_tags=None, due=None, recurrence=None,
                    recurrence_config=None):
        """
        Update an existing task by its unique ID.

        Args:
            task_id (int): The unique ID of the task to update
            title (str, optional): New title for the task. Defaults to None.
            description (str, optional): New description for the task. Defaults to None.
            priority (str, optional): New priority for the task. Defaults to None.
            tags (set, optional): New set of tags for the task. Defaults to None.
            add_tags (set, optional): Set of tags to add to the task. Defaults to None.
            remove_tags (set, optional): Set of tags to remove from the task. Defaults to None.
            due (datetime, optional): New due date/time. Defaults to None.
            recurrence (str, optional): New recurrence pattern. Defaults to None.
            recurrence_config (dict, optional): New recurrence configuration. Defaults to None.

        Returns:
            bool: True if task was updated successfully, False if task not found

        Raises:
            ValueError: If title is provided but is empty, or priority is invalid
        """
        if title is not None and not title.strip():
            raise ValueError("Task title cannot be empty")

        if priority is not None and priority not in ["high", "medium", "low"]:
            raise ValueError("Priority must be one of 'high', 'medium', or 'low'")

        # Prepare the new values, ensuring they are stripped of leading/trailing whitespace
        new_title = title.strip() if title else None
        new_description = description.strip() if description and description.strip() else ("" if description is not None else None)

        return self.task_list.update_task(
            task_id,
            new_title,
            new_description,
            priority,
            tags,
            add_tags,
            remove_tags,
            due=due,
            recurrence=recurrence,
            recurrence_config=recurrence_config
        )

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

        For recurring tasks, this creates a new instance with the next occurrence date.

        Args:
            task_id (int): The unique ID of the task to mark complete

        Returns:
            bool: True if task was marked complete successfully, False if task not found
        """
        task = self.task_list.find_task(task_id)
        if not task:
            return False

        # Check if this is a recurring task
        if task.recurrence:
            # Calculate the next occurrence date
            next_due = calculate_next_occurrence(task)

            # Create a new task instance with updated due date
            new_task = self.add_task(
                title=task.title,
                description=task.description,
                priority=task.priority,
                tags=task.tags,
                due=next_due,
                recurrence=task.recurrence,
                recurrence_config=task.recurrence_config
            )

            print(f"New recurring task created with ID {new_task.id} due: {next_due.strftime('%Y-%m-%d %H:%M')}")

        # Use the task_list's method to mark the task as complete (this will persist the change)
        return self.task_list.mark_task_complete(task_id)

    def mark_task_incomplete(self, task_id):
        """
        Mark a task as incomplete by its unique ID.

        Args:
            task_id (int): The unique ID of the task to mark incomplete

        Returns:
            bool: True if task was marked incomplete successfully, False if task not found
        """
        result = self.task_list.mark_task_incomplete(task_id)
        return result

    def get_task_by_id(self, task_id):
        """
        Get a specific task by its ID.

        Args:
            task_id (int): The unique ID of the task to retrieve

        Returns:
            Task or None: The Task instance if found, None otherwise
        """
        return self.task_list.find_task(task_id)