# Quickstart Guide: Intelligent Todo Features

## Setup

1. Install the required dependency:
   ```bash
   pip install python-dateutil
   ```

2. The new features are integrated into the existing todo application, so no additional setup is required.

## New Features Overview

### Due Dates
- Add tasks with due dates using natural language:
  ```bash
  python main.py add "Submit report" --due "tomorrow 5pm"
  python main.py add "Team meeting" --due "next monday 10am"
  python main.py add "Dentist appointment" --due "in 3 days"
  ```

### Recurring Tasks
- Create recurring tasks with various patterns:
  ```bash
  python main.py add "Weekly team meeting" --due "next monday 11:00" --recurring weekly --recurring-days mon
  python main.py add "Pay rent" --due "2026-02-01" --recurring monthly
  python main.py add "Daily exercise" --recurring daily
  ```

### Enhanced List View
- View tasks with due dates and visual indicators:
  ```bash
  python main.py list
  ```
  - Tasks with due dates show: `due: YYYY-MM-DD HH:MM`
  - Overdue tasks are highlighted in red with (!) indicator
  - Tasks due soon (<24h) show countdown: `(in 4h 30m)`

### Filtering Options
- Show only overdue tasks:
  ```bash
  python main.py list --overdue
  ```
- Show only tasks due today:
  ```bash
  python main.py list --due-today
  ```

### Updating Tasks
- Add due dates to existing tasks:
  ```bash
  python main.py update 5 --due "tomorrow 18:00"
  ```

## Recurrence Patterns

### Daily
- Recurs every day
  ```bash
  --recurring daily
  ```

### Weekly
- Recurs weekly on specified days
  ```bash
  --recurring weekly --recurring-days mon,wed,fri
  ```

### Monthly
- Recurs monthly on the same day
  ```bash
  --recurring monthly
  ```

### Yearly
- Recurs yearly on the same date
  ```bash
  --recurring yearly
  ```

## Important Notes

- When a recurring task is marked complete, a new instance is automatically created with an updated due date
- All existing functionality remains unchanged
- Date formats supported: "tomorrow", "next monday", "in 2 days", "2026-01-15", "Jan 15", etc.
- Invalid date formats will show helpful error messages