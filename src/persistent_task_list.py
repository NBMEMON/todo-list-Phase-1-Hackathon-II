"""
Module for handling persistent TaskList with JSON file storage.
"""
import json
import os
from datetime import datetime
from typing import List, Dict, Any

try:
    from .task_models import TaskList as BaseTaskList
    from .models.task import Task
except ImportError:
    from task_models import TaskList as BaseTaskList
    from models.task import Task


class PersistentTaskList(BaseTaskList):
    """
    Extended TaskList that provides persistence to a JSON file.
    """
    def __init__(self, file_path: str = "tasks.json"):
        """
        Initialize a new PersistentTaskList instance, loading existing tasks from file.
        
        Args:
            file_path (str): Path to the JSON file for storing tasks. Defaults to "tasks.json".
        """
        super().__init__()  # Initialize the base TaskList
        self.file_path = file_path
        self.load_tasks_from_file()

    def ensure_file_exists(self):
        """
        Ensure that the tasks file exists, creating it with an empty list if it doesn't.
        """
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump([], f)

    def save_tasks_to_file(self) -> None:
        """
        Save the current tasks to the JSON file.
        """
        self.ensure_file_exists()
        tasks_data = [task.to_dict() for task in self.tasks]
        with open(self.file_path, 'w') as f:
            json.dump(tasks_data, f, indent=2)

    def load_tasks_from_file(self) -> None:
        """
        Load tasks from the JSON file.
        """
        if not os.path.exists(self.file_path):
            return

        with open(self.file_path, 'r') as f:
            try:
                tasks_data = json.load(f)
            except json.JSONDecodeError:
                # If the file is empty or corrupted, return without loading
                return

        self.tasks = []
        for task_data in tasks_data:
            # Convert datetime strings back to datetime objects
            created_at = datetime.fromisoformat(task_data["created_at"]) if task_data["created_at"] else None
            due = datetime.fromisoformat(task_data["due"]) if task_data["due"] else None
            next_due = datetime.fromisoformat(task_data["next_due"]) if task_data["next_due"] else None

            task = Task(
                id=task_data["id"],
                title=task_data["title"],
                description=task_data["description"],
                completed=task_data["completed"],
                created_at=created_at,
                priority=task_data["priority"],
                tags=set(task_data["tags"]) if task_data["tags"] else set(),
                due=due,
                recurrence=task_data["recurrence"],
                recurrence_config=task_data["recurrence_config"],
                next_due=next_due
            )
            self.tasks.append(task)

        # Update the next_id based on the highest ID in the loaded tasks
        if self.tasks:
            max_id = max(task.id for task in self.tasks)
            self.next_id = max_id + 1

    def add_task(self, title, description="", priority="medium", tags=None, due=None,
                 recurrence=None, recurrence_config=None):
        """
        Add a new task to the list with auto-generated ID and save to file.
        
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
        task = super().add_task(title, description, priority, tags, due, recurrence, recurrence_config)
        # Save the updated task list to file
        self.save_tasks_to_file()
        return task

    def remove_task(self, task_id):
        """
        Remove a task by ID and save to file.
        
        Args:
            task_id (int): The ID of the task to remove
            
        Returns:
            bool: True if task was removed, False if task was not found
        """
        result = super().remove_task(task_id)
        if result:
            # Save the updated task list to file
            self.save_tasks_to_file()
        return result

    def update_task(self, task_id, title=None, description=None, priority=None, tags=None,
                    add_tags=None, remove_tags=None, due=None, recurrence=None,
                    recurrence_config=None):
        """
        Modify task properties by ID and save to file.
        
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
        result = super().update_task(task_id, title, description, priority, tags, 
                                    add_tags, remove_tags, due, recurrence, recurrence_config)
        if result:
            # Save the updated task list to file
            self.save_tasks_to_file()
        return result

    def mark_task_complete(self, task_id):
        """
        Mark a task as complete and save to file.
        
        Args:
            task_id (int): The ID of the task to mark complete
            
        Returns:
            bool: True if task was marked complete, False if task was not found
        """
        result = super().mark_task_complete(task_id)
        if result:
            # Save the updated task list to file
            self.save_tasks_to_file()
        return result

    def mark_task_incomplete(self, task_id):
        """
        Mark a task as incomplete and save to file.
        
        Args:
            task_id (int): The ID of the task to mark incomplete
            
        Returns:
            bool: True if task was marked incomplete, False if task was not found
        """
        result = super().mark_task_incomplete(task_id)
        if result:
            # Save the updated task list to file
            self.save_tasks_to_file()
        return result