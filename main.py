#!/usr/bin/env python3
"""
Entry point script for the Todo Console Application.

This script allows you to run the todo application from the project root directory.
"""
import sys
import os

# Add the src directory to the Python path so imports work correctly
src_dir = os.path.join(os.path.dirname(__file__), 'src')
sys.path.insert(0, src_dir)

# Now import and run the main function
try:
    # Import the main function from the main.py file in src
    from src.main import main
    main()
except ImportError as e:
    print(f"Error importing main module: {e}")
    sys.exit(1)