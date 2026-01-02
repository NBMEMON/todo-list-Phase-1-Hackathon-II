#!/usr/bin/env python3
"""
Main entry point for the Todo Console Application.

This module implements the CLI interface for the todo application,
providing subcommands and flags for all task operations.
"""

import argparse
import sys

# Handle both relative imports (when run as module) and absolute imports (when run directly)
try:
    # Try relative imports first (for when run as module)
    from .services import TaskService
    from .utils import format_task_list_display, format_task_list_display_enhanced
    from .models.task import Task
    from .services_pkg.date_utils import parse_natural_date
    from .lib.display import print_task_list
except ImportError:
    try:
        # Try absolute imports (for when run directly)
        from services import TaskService
        from utils import format_task_list_display, format_task_list_display_enhanced
        from models.task import Task
        from services_pkg.date_utils import parse_natural_date
        from lib.display import print_task_list
    except ImportError:
        # If both fail, try with src prefix (for when run from project root)
        import sys
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
        from src.services import TaskService
        from src.utils import format_task_list_display, format_task_list_display_enhanced
        from src.models.task import Task
        from src.services_pkg.date_utils import parse_natural_date
        from src.lib.display import print_task_list


def create_parser():
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        description="Todo Console Application - Manage your tasks with priorities and tags"
    )

    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new task')
    add_parser.add_argument('title', help='Task title')
    add_parser.add_argument('description', nargs='?', default='', help='Task description (optional)')
    add_parser.add_argument('--priority', '-p', choices=['high', 'medium', 'low'],
                           default='medium', help='Task priority (default: medium)')
    add_parser.add_argument('--tag', '-t', action='append', dest='tags',
                           help='Add a tag to the task (can be used multiple times)')
    add_parser.add_argument('--due', '-d', help='Due date in natural language (e.g., "tomorrow 3pm", "next monday")')
    add_parser.add_argument('--recurring', choices=['daily', 'weekly', 'monthly', 'yearly'],
                           help='Recurrence pattern for the task')
    add_parser.add_argument('--recurring-days', help='Days for weekly recurrence (e.g., "mon,tue,wed")')
    add_parser.add_argument('--show-after-add', action='store_true',
                           help='Show the task list after adding the task')

    # View command (same as list but with simpler interface)
    view_parser = subparsers.add_parser('view', help='View all tasks')
    view_parser.add_argument('--status', choices=['done', 'pending', 'all'],
                            default='all', help='Filter by status (default: all)')
    view_parser.add_argument('--priority', choices=['high', 'medium', 'low', 'all'],
                            help='Filter by priority')
    view_parser.add_argument('--tag', help='Filter by tag')
    view_parser.add_argument('--sort', choices=['id', 'priority', 'title', 'created'],
                            default='id', help='Sort by (default: id)')
    view_parser.add_argument('--order', choices=['asc', 'desc'],
                            default='asc', help='Sort order (default: asc)')
    view_parser.add_argument('--overdue', action='store_true', help='Show only overdue tasks')
    view_parser.add_argument('--due-today', action='store_true', help='Show only tasks due today')

    # List command
    list_parser = subparsers.add_parser('list', help='List all tasks')
    list_parser.add_argument('--status', choices=['done', 'pending', 'all'],
                            default='all', help='Filter by status (default: all)')
    list_parser.add_argument('--priority', choices=['high', 'medium', 'low', 'all'],
                            help='Filter by priority')
    list_parser.add_argument('--tag', help='Filter by tag')
    list_parser.add_argument('--sort', choices=['id', 'priority', 'title', 'created'],
                            default='id', help='Sort by (default: id)')
    list_parser.add_argument('--order', choices=['asc', 'desc'],
                            default='asc', help='Sort order (default: asc)')
    list_parser.add_argument('--overdue', action='store_true', help='Show only overdue tasks')
    list_parser.add_argument('--due-today', action='store_true', help='Show only tasks due today')

    # Search command
    search_parser = subparsers.add_parser('search', help='Search tasks by keyword')
    search_parser.add_argument('keyword', help='Keyword to search for')

    # Update command
    update_parser = subparsers.add_parser('update', help='Update an existing task')
    update_parser.add_argument('id', type=int, help='Task ID to update')
    update_parser.add_argument('title', nargs='?', help='New task title (optional)')
    update_parser.add_argument('description', nargs='?', help='New task description (optional)')
    update_parser.add_argument('--priority', '-p', choices=['high', 'medium', 'low'],
                              help='New priority level')
    update_parser.add_argument('--add-tag', action='append', dest='add_tags',
                              help='Add a tag to the task (can be used multiple times)')
    update_parser.add_argument('--remove-tag', action='append', dest='remove_tags',
                              help='Remove a tag from the task (can be used multiple times)')
    update_parser.add_argument('--due', '-d', help='Update due date in natural language (e.g., "tomorrow 3pm", "next monday")')
    update_parser.add_argument('--recurring', choices=['daily', 'weekly', 'monthly', 'yearly'],
                              help='Update recurrence pattern for the task')
    update_parser.add_argument('--recurring-days', help='Update days for weekly recurrence (e.g., "mon,tue,wed")')

    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete a task')
    delete_parser.add_argument('id', type=int, help='Task ID to delete')

    # Done command
    done_parser = subparsers.add_parser('done', help='Mark a task as complete')
    done_parser.add_argument('id', type=int, help='Task ID to mark complete')

    # Undone command
    undone_parser = subparsers.add_parser('undone', help='Mark a task as incomplete')
    undone_parser.add_argument('id', type=int, help='Task ID to mark incomplete')

    return parser


def main():
    """Main entry point of the application."""
    parser = create_parser()
    args = parser.parse_args()

    # Initialize the task service
    task_service = TaskService()

    try:
        if args.command == 'add':
            # Process tags from command line
            tags = set(args.tags) if args.tags else set()

            # Process due date if provided
            due_date = None
            if args.due:
                due_date = parse_natural_date(args.due)
                if due_date is None:
                    print(f"Error: Could not parse due date '{args.due}'. Please use formats like 'tomorrow', 'next monday', '2026-01-15', etc.")
                    return

            # Process recurrence if provided
            recurrence = args.recurring
            recurrence_config = {}
            if args.recurring_days and recurrence == 'weekly':
                # Parse recurring days (e.g., "mon,tue,wed")
                day_map = {
                    'mon': 0, 'tue': 1, 'wed': 2, 'thu': 3,
                    'fri': 4, 'sat': 5, 'sun': 6,
                    'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
                    'friday': 4, 'saturday': 5, 'sunday': 6
                }
                days = []
                for day in args.recurring_days.split(','):
                    day = day.strip().lower()
                    if day in day_map:
                        days.append(day_map[day])
                    else:
                        print(f"Error: Invalid day '{day}' in recurring days. Use mon, tue, wed, thu, fri, sat, sun")
                        return
                recurrence_config = {'days': days}

            # Create the task with new fields
            task = task_service.add_task(
                title=args.title,
                description=args.description,
                priority=args.priority,
                tags=tags,
                due=due_date,
                recurrence=recurrence,
                recurrence_config=recurrence_config
            )
            print(f"Task '{task.title}' added successfully with ID {task.id}")

            # Always show the task list after adding (as requested by user)
            print("\nCurrent task list:")
            print_task_list(task_service.get_all_tasks())

        elif args.command == 'view' or args.command == 'list':
            # Get all tasks first
            all_tasks = task_service.get_all_tasks()

            # Handle special filters for overdue and due-today
            if args.overdue:
                print_task_list(all_tasks, show_overdue=True)
                return
            elif args.due_today:
                print_task_list(all_tasks, show_due_today=True)
                return

            # Apply filters if specified
            if args.status != 'all' or args.priority or args.tag:
                filtered_tasks = task_service.task_list.filter_tasks(
                    status=args.status if args.status != 'all' else None,
                    priority=args.priority if args.priority != 'all' else None,
                    tag=args.tag
                )
            else:
                filtered_tasks = all_tasks

            # Apply sorting to the filtered results
            if args.sort == 'id':
                sorted_tasks = sorted(filtered_tasks, key=lambda t: t.id, reverse=(args.order == 'desc'))
            elif args.sort == 'priority':
                priority_order = {"high": 0, "medium": 1, "low": 2}
                sorted_tasks = sorted(filtered_tasks, key=lambda t: priority_order[t.priority], reverse=(args.order == 'desc'))
            elif args.sort == 'title':
                sorted_tasks = sorted(filtered_tasks, key=lambda t: t.title.lower(), reverse=(args.order == 'desc'))
            elif args.sort == 'created':
                sorted_tasks = sorted(filtered_tasks, key=lambda t: t.created_at, reverse=(args.order == 'desc'))
            else:  # Default to sorting by ID
                sorted_tasks = sorted(filtered_tasks, key=lambda t: t.id, reverse=(args.order == 'desc'))

            if not sorted_tasks:
                print("No tasks match your criteria.")
            else:
                print_task_list(sorted_tasks)

        elif args.command == 'search':
            if not args.keyword:
                print("Error: Search keyword cannot be empty")
                return

            # Use the search functionality from TaskList
            matching_tasks = task_service.task_list.search_tasks(args.keyword)

            if not matching_tasks:
                print("No tasks match your search.")
            else:
                print_task_list(matching_tasks)

        elif args.command == 'update':
            # Process due date if provided
            due_date = None
            if args.due:
                due_date = parse_natural_date(args.due)
                if due_date is None:
                    print(f"Error: Could not parse due date '{args.due}'. Please use formats like 'tomorrow', 'next monday', '2026-01-15', etc.")
                    return

            # Process recurrence if provided
            recurrence = args.recurring
            recurrence_config = None
            if args.recurring_days and recurrence == 'weekly':
                # Parse recurring days (e.g., "mon,tue,wed")
                day_map = {
                    'mon': 0, 'tue': 1, 'wed': 2, 'thu': 3,
                    'fri': 4, 'sat': 5, 'sun': 6,
                    'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
                    'friday': 4, 'saturday': 5, 'sunday': 6
                }
                days = []
                for day in args.recurring_days.split(','):
                    day = day.strip().lower()
                    if day in day_map:
                        days.append(day_map[day])
                    else:
                        print(f"Error: Invalid day '{day}' in recurring days. Use mon, tue, wed, thu, fri, sat, sun")
                        return
                recurrence_config = {'days': days}

            # Prepare update parameters
            title = args.title if hasattr(args, 'title') and args.title is not None else None
            description = args.description if hasattr(args, 'description') and args.description is not None else None

            # Update the task
            success = task_service.update_task(
                args.id,
                title=title,
                description=description,
                priority=args.priority,
                add_tags=set(args.add_tags) if args.add_tags else None,
                remove_tags=set(args.remove_tags) if args.remove_tags else None,
                due=due_date,
                recurrence=recurrence,
                recurrence_config=recurrence_config
            )

            if success:
                task = task_service.get_task_by_id(args.id)
                if task:
                    print(f"Task with ID {args.id} updated successfully.")
                    print(f"Updated task: {task}")
                else:
                    print(f"Task with ID {args.id} updated successfully.")
            else:
                print(f"Task with ID {args.id} not found.")

        elif args.command == 'delete':
            success = task_service.delete_task(args.id)
            if success:
                print(f"Task with ID {args.id} deleted successfully.")
            else:
                print(f"Task with ID {args.id} not found.")

        elif args.command == 'done':
            success = task_service.mark_task_complete(args.id)
            if success:
                print(f"Task with ID {args.id} marked as complete.")
            else:
                print(f"Task with ID {args.id} not found.")

        elif args.command == 'undone':
            success = task_service.mark_task_incomplete(args.id)
            if success:
                print(f"Task with ID {args.id} marked as incomplete.")
            else:
                print(f"Task with ID {args.id} not found.")

        elif args.command is None:
            # No command provided, show help
            parser.print_help()

        else:
            print(f"Unknown command: {args.command}")
            parser.print_help()

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


def main_entry():
    """Entry point for uv and other package managers."""
    import sys
    import os

    # Add the project root to the Python path to ensure imports work
    # This is needed when the script is run as an installed command
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    main()


def add_cmd():
    """Entry point for the 'add' command."""
    import sys
    # Set sys.argv to simulate the 'add' command
    if len(sys.argv) > 1 and sys.argv[1] != 'add':
        # Insert 'add' as the command if not already present
        sys.argv.insert(1, 'add')
    else:
        # Ensure the command is 'add'
        if len(sys.argv) == 1:
            sys.argv.append('add')
    main()


def delete_cmd():
    """Entry point for the 'delete' command."""
    import sys
    if len(sys.argv) > 1 and sys.argv[1] != 'delete':
        sys.argv.insert(1, 'delete')
    else:
        if len(sys.argv) == 1:
            sys.argv.append('delete')
    main()


def view_cmd():
    """Entry point for the 'view' command."""
    import sys
    if len(sys.argv) > 1 and sys.argv[1] != 'view':
        sys.argv.insert(1, 'view')
    else:
        if len(sys.argv) == 1:
            sys.argv.append('view')
    main()


def list_cmd():
    """Entry point for the 'list' command."""
    import sys
    if len(sys.argv) > 1 and sys.argv[1] != 'list':
        sys.argv.insert(1, 'list')
    else:
        if len(sys.argv) == 1:
            sys.argv.append('list')
    main()


def search_cmd():
    """Entry point for the 'search' command."""
    import sys
    if len(sys.argv) > 1 and sys.argv[1] != 'search':
        sys.argv.insert(1, 'search')
    else:
        if len(sys.argv) == 1:
            sys.argv.append('search')
    main()


def update_cmd():
    """Entry point for the 'update' command."""
    import sys
    if len(sys.argv) > 1 and sys.argv[1] != 'update':
        sys.argv.insert(1, 'update')
    else:
        if len(sys.argv) == 1:
            sys.argv.append('update')
    main()


def done_cmd():
    """Entry point for the 'done' command."""
    import sys
    if len(sys.argv) > 1 and sys.argv[1] != 'done':
        sys.argv.insert(1, 'done')
    else:
        if len(sys.argv) == 1:
            sys.argv.append('done')
    main()


def undone_cmd():
    """Entry point for the 'undone' command."""
    import sys
    if len(sys.argv) > 1 and sys.argv[1] != 'undone':
        sys.argv.insert(1, 'undone')
    else:
        if len(sys.argv) == 1:
            sys.argv.append('undone')
    main()


if __name__ == "__main__":
    main()