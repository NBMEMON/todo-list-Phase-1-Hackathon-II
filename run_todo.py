#!/usr/bin/env python3
"""
Entry point script for the Todo Console Application.

This script allows you to run the todo application from the project root directory.
"""
import sys
import os

# Change to the src directory so the relative imports work correctly
src_dir = os.path.join(os.path.dirname(__file__), 'src')
sys.path.insert(0, src_dir)
os.chdir(src_dir)

# Now import and run the main function
try:
    # Import the main function from the main.py file in src
    import main as todo_main
    if hasattr(todo_main, 'main'):
        todo_main.main()
    else:
        print("Error: Could not find main function in src/main.py")
        sys.exit(1)
except ImportError as e:
    print(f"Error importing main module: {e}")
    sys.exit(1)