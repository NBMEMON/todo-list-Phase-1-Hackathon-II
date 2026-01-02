"""
Data models for the Todo Console Application.

This module defines the Task and TaskList entities as specified in the data model.
"""
from datetime import datetime
from typing import Optional, Set, Dict, Any


class Task:
    """
    Represents a single task in the todo application.

    Attributes:
        id (int): Unique identifier for the task (auto-incremented)
        title (str): The task title (required)
        description (str): Optional description for the task
        completed (bool): Status indicator showing if the task is complete (default: False)
        created_at (datetime): Timestamp when the task was created (auto-generated)
        priority (str): Priority level of the task (values: "high", "medium", "low"; default: "medium")
        tags (set): Set of tags associated with the task (default: empty set)
        due (datetime): Due date/time for the task (default: None)
        recurrence (str): Recurrence pattern ("daily", "weekly", "monthly", "yearly"; default: None)
        recurrence_config (dict): Configuration for recurrence (default: {})
        next_due (datetime): Next due date for recurring tasks (default: None)
    """

    def __init__(self, task_id, title, description="", completed=False, priority="medium", 
                 tags=None, created_at=None, due=None, recurrence=None, 
                 recurrence_config=None, next_due=None):
        """
        Initialize a new Task instance.

        Args:
            task_id (int): Unique identifier for the task
            title (str): The task title (required)
            description (str, optional): Optional description for the task. Defaults to "".
            completed (bool, optional): Completion status. Defaults to False.
            priority (str, optional): Priority level. Defaults to "medium".
            tags (set, optional): Set of tags. Defaults to empty set.
            created_at (datetime, optional): Creation timestamp. Defaults to now().
            due (datetime, optional): Due date/time. Defaults to None.
            recurrence (str, optional): Recurrence pattern. Defaults to None.
            recurrence_config (dict, optional): Recurrence configuration. Defaults to {}.
            next_due (datetime, optional): Next due date for recurring tasks. Defaults to None.
        """
        if not title:
            raise ValueError("Title cannot be empty")

        if priority not in ["high", "medium", "low"]:
            raise ValueError("Priority must be one of 'high', 'medium', or 'low'")

        self.id = task_id
        self.title = title
        self.description = description
        self.completed = completed
        self.created_at = created_at or datetime.now()
        self.priority = priority
        self.tags = tags or set()
        self.due = due
        self.recurrence = recurrence
        self.recurrence_config = recurrence_config or {}
        self.next_due = next_due

    def __str__(self):
        """
        String representation of the task (legacy format for backward compatibility).

        Returns:
            str: Formatted string showing task details with status indicator only
        """
        status = "✓" if self.completed else "○"
        return f"[{status}] {self.id}. {self.title} - {self.description if self.description else '(No description)'}"

    def to_enhanced_str(self):
        """
        Enhanced string representation of the task (with priority and tags).

        Returns:
            str: Formatted string showing task details with status indicator, priority, and tags
        """
        status = "✓" if self.completed else "○"
        priority_indicator = {"high": "H", "medium": "M", "low": "L"}[self.priority]
        tags_str = " ".join([f"#{tag}" for tag in sorted(self.tags)]) if self.tags else ""
        return f"[{status}] {self.id}. ({priority_indicator}) {self.title} {tags_str}- {self.description}".strip()

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
            "completed": self.completed,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "priority": self.priority,
            "tags": list(self.tags) if self.tags else [],
            "due": self.due.isoformat() if self.due else None,
            "recurrence": self.recurrence,
            "recurrence_config": self.recurrence_config,
            "next_due": self.next_due.isoformat() if self.next_due else None
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

    def add_task(self, title, description="", priority="medium", tags=None, due=None,
                 recurrence=None, recurrence_config=None):
        """
        Add a new task to the list with auto-generated ID.

        Args:
            title (str): The task title (required)
            description (str, optional): Optional description for the task. Defaults to "".
            priority (str, optional): Priority level. Defaults to "medium".
            tags (set, optional): Set of tags. Defaults to empty set.
            due (datetime, optional): Due date/time. Defaults to None.
            recurrence (str, optional): Recurrence pattern. Defaults to None.
            recurrence_config (dict, optional): Recurrence configuration. Defaults to {}.

        Returns:
            Task: The newly created Task instance
        """
        if not title:
            raise ValueError("Title cannot be empty")

        if priority not in ["high", "medium", "low"]:
            raise ValueError("Priority must be one of 'high', 'medium', or 'low'")

        task = Task(
            self.next_id,
            title,
            description,
            False,
            priority,
            tags,
            due=due,
            recurrence=recurrence,
            recurrence_config=recurrence_config
        )
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

    def update_task(self, task_id, title=None, description=None, priority=None, tags=None,
                    add_tags=None, remove_tags=None, due=None, recurrence=None,
                    recurrence_config=None):
        """
        Modify task properties by ID.

        Args:
            task_id (int): The ID of the task to update
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
                if priority is not None:
                    if priority not in ["high", "medium", "low"]:
                        raise ValueError("Priority must be one of 'high', 'medium', or 'low'")
                    task.priority = priority
                if tags is not None:
                    task.tags = tags
                if add_tags is not None:
                    task.tags.update(add_tags)
                if remove_tags is not None:
                    task.tags.difference_update(remove_tags)
                if due is not None:
                    task.due = due
                if recurrence is not None:
                    task.recurrence = recurrence
                if recurrence_config is not None:
                    task.recurrence_config = recurrence_config
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

    def filter_tasks(self, status=None, priority=None, tag=None):
        """
        Filter tasks based on various criteria.

        Args:
            status (str, optional): Filter by status ('done', 'pending', 'all'). Defaults to None (all).
            priority (str, optional): Filter by priority ('high', 'medium', 'low', 'all'). Defaults to None (all).
            tag (str, optional): Filter by specific tag. Defaults to None (all).

        Returns:
            list: List of tasks matching the filter criteria
        """
        filtered_tasks = self.tasks

        # Filter by status
        if status == "done":
            filtered_tasks = [task for task in filtered_tasks if task.completed]
        elif status == "pending":
            filtered_tasks = [task for task in filtered_tasks if not task.completed]

        # Filter by priority
        if priority and priority != "all":
            if priority in ["high", "medium", "low"]:
                filtered_tasks = [task for task in filtered_tasks if task.priority == priority]

        # Filter by tag
        if tag:
            filtered_tasks = [task for task in filtered_tasks if tag in task.tags]

        return filtered_tasks

    def sort_tasks(self, sort_by="id", order="asc"):
        """
        Sort tasks based on various criteria.

        Args:
            sort_by (str): Sort by 'id', 'priority', 'title', or 'created'. Defaults to 'id'.
            order (str): Sort order 'asc' or 'desc'. Defaults to 'asc'.

        Returns:
            list: List of tasks sorted according to criteria
        """
        tasks_to_sort = self.tasks.copy()

        # Define sort key function
        if sort_by == "priority":
            # Define priority order: high > medium > low
            priority_order = {"high": 0, "medium": 1, "low": 2}
            tasks_to_sort.sort(key=lambda task: priority_order[task.priority])
        elif sort_by == "title":
            tasks_to_sort.sort(key=lambda task: task.title.lower())
        elif sort_by == "created":
            tasks_to_sort.sort(key=lambda task: task.created_at)
        else:  # Default to sorting by ID
            tasks_to_sort.sort(key=lambda task: task.id)

        # Reverse if descending order is requested
        if order == "desc":
            tasks_to_sort.reverse()

        return tasks_to_sort

    def search_tasks(self, keyword):
        """
        Search tasks by keyword in title, description, or tags.

        Args:
            keyword (str): Keyword to search for (case-insensitive, partial match)

        Returns:
            list: List of tasks containing the keyword
        """
        keyword_lower = keyword.lower()
        matching_tasks = []

        for task in self.tasks:
            # Check if keyword is in title, description, or any tag
            if (keyword_lower in task.title.lower() or
                keyword_lower in task.description.lower() or
                any(keyword_lower in tag.lower() for tag in task.tags)):
                matching_tasks.append(task)

        return matching_tasks