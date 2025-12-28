# CLI Operations Contract: Todo Console Application

## Overview
This document defines the CLI interface contract for the Todo Console Application. All operations are accessed through a menu-driven console interface.

## Core Operations

### 1. Add Task
**Operation**: Add a new task to the list
**Input**:
- Title (required string)
- Description (optional string)
**Output**:
- Success message with assigned task ID
- Error message if title is empty
**Validation**:
- Title must not be empty
- Description is optional
- Task ID is auto-generated and unique

### 2. View Tasks
**Operation**: Display all tasks with their status
**Input**: None
**Output**:
- List of all tasks with ID, title, description, and completion status
- Message if task list is empty
**Validation**:
- No validation required

### 3. Update Task
**Operation**: Update an existing task's title and/or description
**Input**:
- Task ID (required integer)
- New title (optional string)
- New description (optional string)
**Output**:
- Success message if task updated
- Error message if task ID doesn't exist
**Validation**:
- Task ID must exist in the task list
- Title must not be empty if provided

### 4. Delete Task
**Operation**: Remove a task from the list
**Input**:
- Task ID (required integer)
**Output**:
- Success message if task deleted
- Error message if task ID doesn't exist
**Validation**:
- Task ID must exist in the task list

### 5. Mark Task Complete/Incomplete
**Operation**: Toggle the completion status of a task
**Input**:
- Task ID (required integer)
- Status (required: "complete" or "incomplete")
**Output**:
- Success message if task status updated
- Error message if task ID doesn't exist
**Validation**:
- Task ID must exist in the task list
- Status must be either "complete" or "incomplete"

## Error Handling Contract
All operations must:
1. Provide clear, human-readable error messages
2. Never crash the application
3. Return to the main menu after any operation (success or failure)
4. Preserve all existing data when an operation fails

## Performance Contract
All operations must complete within the following time limits:
- Add Task: < 3 seconds
- View Tasks: < 2 seconds (for up to 100 tasks)
- Update Task: < 3 seconds
- Delete Task: < 2 seconds
- Mark Task Complete/Incomplete: < 2 seconds