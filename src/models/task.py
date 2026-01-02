from datetime import datetime
from typing import Optional, Set, Dict, Any
from dataclasses import dataclass


@dataclass
class Task:
    """
    Represents a single task with due date and recurrence capabilities.
    """
    id: int
    title: str
    description: str = ""
    completed: bool = False
    created_at: datetime = None
    priority: str = "medium"  # "high", "medium", "low"
    tags: Set[str] = None
    due: Optional[datetime] = None
    recurrence: Optional[str] = None  # "daily", "weekly", "monthly", "yearly"
    recurrence_config: Optional[Dict[str, Any]] = None  # Configuration for recurrence
    next_due: Optional[datetime] = None  # Next due date for recurring tasks

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.tags is None:
            self.tags = set()
        if self.recurrence_config is None:
            self.recurrence_config = {}

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