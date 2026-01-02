"""
Module for handling data persistence for the Todo Console Application.

This module provides functions to save and load tasks to/from a JSON file.
"""
import json
import os
from datetime import datetime
from typing import List, Dict, Any

try:
    # Try relative imports first
    from .models.task import Task
    from .task_models import TaskList as OriginalTaskList
except ImportError:
    try:
        # Try absolute imports
        from models.task import Task
        from task_models import TaskList as OriginalTaskList
    except ImportError:
        # If both fail, try with src prefix
        import sys
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
        from src.models.task import Task
        from src.task_models import TaskList as OriginalTaskList


class TaskPersistence:
    """
    Handles saving and loading tasks to/from a JSON file.
    """
    def __init__(self, file_path: str = "tasks.json"):
        """
        Initialize the TaskPersistence with a file path.
        
        Args:
            file_path (str): Path to the JSON file for storing tasks. Defaults to "tasks.json".
        """
        self.file_path = file_path
        self.ensure_file_exists()

    def ensure_file_exists(self):
        """
        Ensure that the tasks file exists, creating it with an empty list if it doesn't.
        """
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump([], f)

    def save_tasks(self, tasks: List[Task]) -> None:
        """
        Save a list of tasks to the JSON file.
        
        Args:
            tasks (List[Task]): List of Task objects to save
        """
        tasks_data = [task.to_dict() for task in tasks]
        with open(self.file_path, 'w') as f:
            json.dump(tasks_data, f, indent=2)

    def load_tasks(self) -> List[Task]:
        """
        Load tasks from the JSON file.
        
        Returns:
            List[Task]: List of Task objects loaded from the file
        """
        if not os.path.exists(self.file_path):
            return []

        with open(self.file_path, 'r') as f:
            try:
                tasks_data = json.load(f)
            except json.JSONDecodeError:
                # If the file is empty or corrupted, return an empty list
                return []

        tasks = []
        for task_data in tasks_data:
            # Convert datetime strings back to datetime objects
            created_at = datetime.fromisoformat(task_data["created_at"]) if task_data["created_at"] else None
            due = datetime.fromisoformat(task_data["due"]) if task_data["due"] else None
            next_due = datetime.fromisoformat(task_data["next_due"]) if task_data["next_due"] else None

            task = Task(
                task_id=task_data["id"],
                title=task_data["title"],
                description=task_data["description"],
                completed=task_data["completed"],
                created_at=created_at,
                priority=task_data["priority"],
                tags=set(task_data["tags"]),
                due=due,
                recurrence=task_data["recurrence"],
                recurrence_config=task_data["recurrence_config"],
                next_due=next_due
            )
            tasks.append(task)

        # Update the next_id based on the highest ID in the loaded tasks
        if tasks:
            max_id = max(task.id for task in tasks)
            TaskList.next_id = max_id + 1
        else:
            TaskList.next_id = 1

        return tasks


# Global instance of TaskPersistence
persistence = TaskPersistence()


class TaskList:
    """
    Represents a collection of Task entities with persistence.
    
    This is a modified version of the original TaskList class that includes
    persistence functionality.
    """
    next_id = 1  # Class variable to keep track of the next ID to assign

    def __init__(self):
        """
        Initialize a new TaskList instance, loading existing tasks from file.
        """
        self.tasks = persistence.load_tasks()

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
        # Increment the class variable for the next task
        TaskList.next_id += 1
        # Save the updated task list to file
        persistence.save_tasks(self.tasks)
        return task

    def remove_task(self, task_id):
        """
        Remove a task by ID and save to file.
        
        Args:
            task_id (int): The ID of the task to remove
            
        Returns:
            bool: True if task was removed, False if task was not found
        """
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                del self.tasks[i]
                # Save the updated task list to file
                persistence.save_tasks(self.tasks)
                return True
        return False

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
                # Save the updated task list to file
                persistence.save_tasks(self.tasks)
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
        Mark a task as complete and save to file.
        
        Args:
            task_id (int): The ID of the task to mark complete
            
        Returns:
            bool: True if task was marked complete, False if task was not found
        """
        task = self.find_task(task_id)
        if task:
            task.completed = True
            # Save the updated task list to file
            persistence.save_tasks(self.tasks)
            return True
        return False

    def mark_task_incomplete(self, task_id):
        """
        Mark a task as incomplete and save to file.
        
        Args:
            task_id (int): The ID of the task to mark incomplete
            
        Returns:
            bool: True if task was marked incomplete, False if task was not found
        """
        task = self.find_task(task_id)
        if task:
            task.completed = False
            # Save the updated task list to file
            persistence.save_tasks(self.tasks)
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