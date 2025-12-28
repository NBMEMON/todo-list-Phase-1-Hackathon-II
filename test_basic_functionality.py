#!/usr/bin/env python3
"""
Basic functionality test for the Todo Console Application.

This script tests the core functionality without requiring interactive input.
"""

import sys
import os

# Add src directory to path so we can import the modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from models import Task, TaskList
from services import TaskService
from utils import format_task_display, format_task_list_display, validate_task_title


def test_task_creation():
    """Test Task class creation and basic functionality."""
    print("Testing Task creation...")

    # Test creating a task
    task = Task(1, "Test task", "This is a test description")
    assert task.id == 1
    assert task.title == "Test task"
    assert task.description == "This is a test description"
    assert task.completed == False

    # Test string representation
    task_str = str(task)
    assert "[○]" in task_str  # Incomplete task indicator
    assert "1." in task_str
    assert "Test task" in task_str

    # Test completed task
    task.completed = True
    task_str = str(task)
    assert "[✓]" in task_str  # Complete task indicator

    print("PASS: Task creation test passed")


def test_task_validation():
    """Test task title validation."""
    print("Testing task validation...")

    # Test valid title
    assert validate_task_title("Valid title") == True

    # Test invalid titles
    assert validate_task_title("") == False
    assert validate_task_title("   ") == False
    assert validate_task_title(None) == False

    print("PASS: Task validation test passed")


def test_task_list_operations():
    """Test TaskList operations."""
    print("Testing TaskList operations...")

    task_list = TaskList()

    # Test adding a task
    task = task_list.add_task("First task", "Description of first task")
    assert task.id == 1
    assert task.title == "First task"
    assert task.description == "Description of first task"
    assert len(task_list.get_all_tasks()) == 1

    # Test adding another task
    task2 = task_list.add_task("Second task")
    assert task2.id == 2
    assert len(task_list.get_all_tasks()) == 2

    # Test finding a task
    found_task = task_list.find_task(1)
    assert found_task is not None
    assert found_task.title == "First task"

    # Test updating a task
    success = task_list.update_task(1, "Updated task", "Updated description")
    assert success == True
    updated_task = task_list.find_task(1)
    assert updated_task.title == "Updated task"
    assert updated_task.description == "Updated description"

    # Test marking complete/incomplete
    task_list.mark_task_complete(1)
    marked_task = task_list.find_task(1)
    assert marked_task.completed == True

    task_list.mark_task_incomplete(1)
    marked_task = task_list.find_task(1)
    assert marked_task.completed == False

    # Test removing a task
    success = task_list.remove_task(1)
    assert success == True
    assert len(task_list.get_all_tasks()) == 1
    assert task_list.find_task(1) is None

    print("PASS: TaskList operations test passed")


def test_task_service():
    """Test TaskService functionality."""
    print("Testing TaskService...")

    service = TaskService()

    # Test adding a task
    task = service.add_task("Service task", "Task added via service")
    assert task.id == 1
    assert task.title == "Service task"
    assert task.description == "Task added via service"

    # Test getting all tasks
    tasks = service.get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0].id == 1

    # Test updating a task
    success = service.update_task(1, "Updated service task", "Updated description")
    assert success == True
    updated_task = service.get_task_by_id(1)
    assert updated_task.title == "Updated service task"

    # Test marking complete
    success = service.mark_task_complete(1)
    assert success == True
    marked_task = service.get_task_by_id(1)
    assert marked_task.completed == True

    # Test deleting a task
    success = service.delete_task(1)
    assert success == True
    assert service.get_task_by_id(1) is None
    assert len(service.get_all_tasks()) == 0

    print("PASS: TaskService test passed")


def test_formatting():
    """Test formatting functions."""
    print("Testing formatting functions...")

    from utils import format_task_display, format_task_list_display

    task = Task(1, "Format test", "Test description")

    # Test single task formatting
    formatted = format_task_display(task)
    assert "[○]" in formatted  # Incomplete indicator
    assert "1." in formatted
    assert "Format test" in formatted
    assert "Test description" in formatted

    # Test task list formatting
    task.completed = True
    formatted_list = format_task_list_display([task])
    assert "[✓]" in formatted_list  # Complete indicator

    print("PASS: Formatting test passed")


def test_error_handling():
    """Test error handling."""
    print("Testing error handling...")

    task_list = TaskList()

    # Test adding task with empty title (should raise ValueError)
    try:
        task_list.add_task("")
        assert False, "Should have raised ValueError"
    except ValueError:
        pass  # Expected

    # Test updating task with empty title (should raise ValueError)
    task_list.add_task("Valid task")
    try:
        task_list.update_task(1, "")
        assert False, "Should have raised ValueError"
    except ValueError:
        pass  # Expected

    # Test operations on non-existent task
    assert task_list.find_task(999) is None
    assert task_list.remove_task(999) == False
    assert task_list.update_task(999, "New title") == False
    assert task_list.mark_task_complete(999) == False

    print("PASS: Error handling test passed")


def main():
    """Run all tests."""
    print("Running basic functionality tests for Todo Console Application...\n")

    try:
        test_task_creation()
        test_task_validation()
        test_task_list_operations()
        test_task_service()
        test_formatting()
        test_error_handling()

        print("\nPASS: All tests passed! User Story 1 functionality is working correctly.")
        print("PASS: Add and View Tasks functionality verified.")

        # Mark the test task as completed in the tasks file
        import re

        tasks_file = "specs/1-todo-console-app/tasks.md"
        with open(tasks_file, 'r') as f:
            content = f.read()

        # Replace the test task with completed status
        content = content.replace(
            "- [ ] T022 [US1] Test US1 functionality independently to ensure it works as MVP",
            "- [x] T022 [US1] Test US1 functionality independently to ensure it works as MVP"
        )

        with open(tasks_file, 'w') as f:
            f.write(content)

        print("PASS: Marked T022 as completed in tasks.md")

    except Exception as e:
        print(f"\nFAIL: Test failed with error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())