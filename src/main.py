#!/usr/bin/env python3
"""
Main entry point for the Todo Console Application.

This module implements the CLI interface for the todo application,
providing a menu-driven interface for all task operations.
"""

import sys
from services import TaskService
from utils import (
    display_menu,
    get_user_choice,
    get_valid_task_id_input,
    format_task_list_display,
    confirm_action,
    validate_task_title
)


class TodoApp:
    """
    Main application class that handles the CLI interface and user interactions.
    """

    def __init__(self):
        """
        Initialize the TodoApp with a TaskService instance.
        """
        self.task_service = TaskService()

    def run(self):
        """
        Run the main application loop with menu options.
        """
        print("Welcome to the Todo Console Application!")
        print("Type '6' or 'exit' to quit the application at any time.")

        while True:
            try:
                display_menu()
                choice = get_user_choice(1, 6, "Select an option (1-6): ")

                if choice is None:
                    continue

                if choice == 1:
                    self.add_task()
                elif choice == 2:
                    self.view_tasks()
                elif choice == 3:
                    self.update_task()
                elif choice == 4:
                    self.delete_task()
                elif choice == 5:
                    self.mark_task_status()
                elif choice == 6:
                    self.exit_app()
                    break
                else:
                    print("Invalid option. Please select a number between 1 and 6.")

            except KeyboardInterrupt:
                print("\n\nApplication interrupted by user. Exiting...")
                sys.exit(0)
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                print("Please try again.")

    def add_task(self):
        """
        Add a new task with required title and optional description.
        """
        print("\n--- Add New Task ---")

        title = input("Enter task title: ").strip()

        # Validate title
        if not validate_task_title(title):
            print("Error: Task title cannot be empty.")
            return

        description = input("Enter task description (optional): ").strip()

        try:
            task = self.task_service.add_task(title, description)
            print(f"Task '{task.title}' added successfully with ID {task.id}")
        except ValueError as e:
            print(f"Error adding task: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while adding task: {e}")

    def view_tasks(self):
        """
        Display all tasks with clear status indicators.
        """
        print("\n--- View All Tasks ---")

        tasks = self.task_service.get_all_tasks()

        if not tasks:
            print("No tasks found.")
            return

        print("\nCurrent Tasks:")
        print(format_task_list_display(tasks))
        print(f"\nTotal tasks: {len(tasks)}")

    def update_task(self):
        """
        Update an existing task by its unique ID.
        """
        print("\n--- Update Task ---")

        tasks = self.task_service.get_all_tasks()
        if not tasks:
            print("No tasks available to update.")
            return

        print("Current tasks:")
        print(format_task_list_display(tasks))

        task_id = get_valid_task_id_input("Enter the ID of the task to update: ", tasks)
        if task_id is None:
            return

        task = self.task_service.get_task_by_id(task_id)
        if not task:
            print(f"Task with ID {task_id} not found.")
            return

        print(f"Current task: {task}")

        new_title = input(f"Enter new title (leave blank to keep '{task.title}'): ").strip()
        new_description = input(f"Enter new description (leave blank to keep '{task.description}'): ").strip()

        # Use current values if user input is blank
        update_title = new_title if new_title else None
        update_description = new_description if new_description else None

        try:
            if self.task_service.update_task(task_id, update_title, update_description):
                updated_task = self.task_service.get_task_by_id(task_id)
                print(f"Task with ID {task_id} updated successfully.")
                print(f"Updated task: {updated_task}")
            else:
                print(f"Failed to update task with ID {task_id}.")
        except ValueError as e:
            print(f"Error updating task: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while updating task: {e}")

    def delete_task(self):
        """
        Delete a task by its unique ID.
        """
        print("\n--- Delete Task ---")

        tasks = self.task_service.get_all_tasks()
        if not tasks:
            print("No tasks available to delete.")
            return

        print("Current tasks:")
        print(format_task_list_display(tasks))

        task_id = get_valid_task_id_input("Enter the ID of the task to delete: ", tasks)
        if task_id is None:
            return

        task = self.task_service.get_task_by_id(task_id)
        if not task:
            print(f"Task with ID {task_id} not found.")
            return

        print(f"Task to delete: {task}")

        if not confirm_action("Are you sure you want to delete this task?"):
            print("Task deletion cancelled.")
            return

        if self.task_service.delete_task(task_id):
            print(f"Task with ID {task_id} deleted successfully.")
        else:
            print(f"Failed to delete task with ID {task_id}.")

    def mark_task_status(self):
        """
        Mark a task as complete or incomplete by its unique ID.
        """
        print("\n--- Mark Task Complete/Incomplete ---")

        tasks = self.task_service.get_all_tasks()
        if not tasks:
            print("No tasks available to update.")
            return

        print("Current tasks:")
        print(format_task_list_display(tasks))

        task_id = get_valid_task_id_input("Enter the ID of the task to update status: ", tasks)
        if task_id is None:
            return

        task = self.task_service.get_task_by_id(task_id)
        if not task:
            print(f"Task with ID {task_id} not found.")
            return

        print(f"Current task: {task}")

        # Determine current status and ask for new status
        current_status = "Complete" if task.completed else "Incomplete"
        new_status = input(f"Mark as (c)omplete or (i)nc. Leave blank to keep current status '{current_status}': ").strip().lower()

        if new_status in ['c', 'complete', 'completed']:
            if self.task_service.mark_task_complete(task_id):
                print(f"Task with ID {task_id} marked as complete.")
            else:
                print(f"Failed to mark task with ID {task_id} as complete.")
        elif new_status in ['i', 'incomplete', 'incompleted', 'not complete']:
            if self.task_service.mark_task_incomplete(task_id):
                print(f"Task with ID {task_id} marked as incomplete.")
            else:
                print(f"Failed to mark task with ID {task_id} as incomplete.")
        elif new_status == "":
            print("Status unchanged.")
        else:
            print("Invalid input. Task status unchanged.")

    def exit_app(self):
        """
        Exit the application gracefully.
        """
        print("\nThank you for using the Todo Console Application!")
        print("Goodbye!")


def main():
    """
    Main entry point of the application.
    """
    try:
        app = TodoApp()
        app.run()
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()