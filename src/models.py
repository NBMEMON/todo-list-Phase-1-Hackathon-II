"""
Data models for the Todo Console Application.

This module defines the Task and TaskList entities as specified in the data model.
"""

class Task:
    """
    Represents a single task in the todo application.

    Attributes:
        id (int): Unique identifier for the task (auto-incremented)
        title (str): The task title (required)
        description (str): Optional description for the task
        completed (bool): Status indicator showing if the task is complete (default: False)
    """

    def __init__(self, task_id, title, description="", completed=False):
        """
        Initialize a new Task instance.

        Args:
            task_id (int): Unique identifier for the task
            title (str): The task title (required)
            description (str, optional): Optional description for the task. Defaults to "".
            completed (bool, optional): Completion status. Defaults to False.
        """
        if not title:
            raise ValueError("Title cannot be empty")

        self.id = task_id
        self.title = title
        self.description = description
        self.completed = completed

    def __str__(self):
        """
        String representation of the task.

        Returns:
            str: Formatted string showing task details with status indicator
        """
        status = "✓" if self.completed else "○"
        return f"[{status}] {self.id}. {self.title}"

    def to_dict(self):
        """
        Convert the task to a dictionary representation.

        Returns:
            dict: Dictionary containing task attributes
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed
        }


class TaskList:
    """
    Represents a collection of Task entities.

    Attributes:
        tasks (list): Collection of Task entities
        next_id (int): Counter for generating next unique task ID
    """

    def __init__(self):
        """
        Initialize a new TaskList instance.
        """
        self.tasks = []
        self.next_id = 1

    def add_task(self, title, description=""):
        """
        Add a new task to the list with auto-generated ID.

        Args:
            title (str): The task title (required)
            description (str, optional): Optional description for the task. Defaults to "".

        Returns:
            Task: The newly created Task instance
        """
        if not title:
            raise ValueError("Title cannot be empty")

        task = Task(self.next_id, title, description, False)
        self.tasks.append(task)
        self.next_id += 1
        return task

    def remove_task(self, task_id):
        """
        Remove a task by ID.

        Args:
            task_id (int): The ID of the task to remove

        Returns:
            bool: True if task was removed, False if task was not found
        """
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                del self.tasks[i]
                return True
        return False

    def update_task(self, task_id, title=None, description=None):
        """
        Modify task properties by ID.

        Args:
            task_id (int): The ID of the task to update
            title (str, optional): New title for the task. Defaults to None.
            description (str, optional): New description for the task. Defaults to None.

        Returns:
            bool: True if task was updated, False if task was not found
        """
        for task in self.tasks:
            if task.id == task_id:
                if title is not None:
                    if not title:
                        raise ValueError("Title cannot be empty")
                    task.title = title
                if description is not None:
                    task.description = description
                return True
        return False

    def find_task(self, task_id):
        """
        Retrieve a task by ID.

        Args:
            task_id (int): The ID of the task to find

        Returns:
            Task or None: The found Task instance or None if not found
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def get_all_tasks(self):
        """
        Return all tasks in the collection.

        Returns:
            list: List of all Task instances
        """
        return self.tasks

    def mark_task_complete(self, task_id):
        """
        Mark a task as complete.

        Args:
            task_id (int): The ID of the task to mark complete

        Returns:
            bool: True if task was marked complete, False if task was not found
        """
        task = self.find_task(task_id)
        if task:
            task.completed = True
            return True
        return False

    def mark_task_incomplete(self, task_id):
        """
        Mark a task as incomplete.

        Args:
            task_id (int): The ID of the task to mark incomplete

        Returns:
            bool: True if task was marked incomplete, False if task was not found
        """
        task = self.find_task(task_id)
        if task:
            task.completed = False
            return True
        return False