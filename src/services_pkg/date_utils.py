from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from dateutil import parser, relativedelta
import re


def parse_natural_date(text: str) -> Optional[datetime]:
    """
    Parse natural language date expressions like "tomorrow 3pm", "next friday", "in 2 days".
    
    Args:
        text: Natural language date expression
        
    Returns:
        Parsed datetime object or None if parsing fails
    """
    if not text:
        return None
    
    # Handle relative expressions like "in 2 days", "in 3 weeks"
    relative_match = re.match(r'in (\d+) (day|week|month|year)s?', text.lower().strip())
    if relative_match:
        count = int(relative_match.group(1))
        unit = relative_match.group(2)
        
        now = datetime.now()
        if unit == 'day':
            return now + timedelta(days=count)
        elif unit == 'week':
            return now + timedelta(weeks=count)
        elif unit == 'month':
            return now + relativedelta.relativedelta(months=count)
        elif unit == 'year':
            return now + relativedelta.relativedelta(years=count)
    
    # Handle expressions like "tomorrow", "today"
    text_lower = text.lower().strip()
    if text_lower == 'today' or text_lower == 'now':
        return datetime.now().replace(hour=23, minute=59, second=59, microsecond=0)  # End of today
    elif text_lower == 'tomorrow':
        tomorrow = datetime.now() + timedelta(days=1)
        return tomorrow.replace(hour=23, minute=59, second=59, microsecond=0)  # End of tomorrow
    
    # Use dateutil parser for standard formats
    try:
        return parser.parse(text)
    except (parser.ParserError, ValueError):
        # If standard parsing fails, try to handle "next <day>" format
        next_day_match = re.match(r'next (\w+)', text_lower)
        if next_day_match:
            day_name = next_day_match.group(1)
            return parse_next_weekday(day_name)
        
        return None


def parse_next_weekday(day_name: str) -> Optional[datetime]:
    """
    Parse expressions like "next monday", "next friday".
    
    Args:
        day_name: Name of the day (monday, tuesday, etc.)
        
    Returns:
        Datetime for the next occurrence of the specified day
    """
    days = {
        'monday': 0, 'mon': 0,
        'tuesday': 1, 'tue': 1,
        'wednesday': 2, 'wed': 2,
        'thursday': 3, 'thu': 3,
        'friday': 4, 'fri': 4,
        'saturday': 5, 'sat': 5,
        'sunday': 6, 'sun': 6
    }
    
    if day_name.lower() not in days:
        return None
    
    target_weekday = days[day_name.lower()]
    today = datetime.now()
    days_ahead = target_weekday - today.weekday()
    
    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7
    
    return today + timedelta(days_ahead)


def calculate_next_occurrence(task: 'Task', current_date: datetime = None) -> Optional[datetime]:
    """
    Calculate the next occurrence date based on the recurrence pattern.
    
    Args:
        task: The task with recurrence information
        current_date: The date to calculate from (defaults to now)
        
    Returns:
        Next occurrence datetime or None if recurrence is invalid
    """
    if not task.recurrence:
        return None
    
    if current_date is None:
        current_date = datetime.now()
    
    # If the task has a due date, use that as the reference point
    reference_date = task.due if task.due else current_date
    
    if task.recurrence == 'daily':
        return reference_date + timedelta(days=1)
    
    elif task.recurrence == 'weekly':
        # For weekly recurrence, we need to find the next occurrence of the specified days
        if task.recurrence_config and 'days' in task.recurrence_config:
            days = task.recurrence_config['days']  # List of integers 0-6 (Mon-Sun)
            if isinstance(days, list) and len(days) > 0:
                # Find the next occurrence of any of the specified days
                return calculate_next_weekly_occurrence(reference_date, days)
        # Default to same day of week if no specific days specified
        return reference_date + timedelta(weeks=1)
    
    elif task.recurrence == 'monthly':
        # For monthly recurrence, add one month to the reference date
        # Handle edge cases like Jan 31 -> Feb 28/29
        try:
            return reference_date + relativedelta.relativedelta(months=1)
        except ValueError:
            # If the day doesn't exist in the next month (e.g., Jan 31 -> Feb 31), 
            # go to the last day of the next month
            next_month = reference_date + relativedelta.relativedelta(months=1)
            return next_month.replace(day=1) + relativedelta.relativedelta(months=1) - timedelta(days=1)
    
    elif task.recurrence == 'yearly':
        # For yearly recurrence, add one year to the reference date
        try:
            return reference_date + relativedelta.relativedelta(years=1)
        except ValueError:
            # Handle leap year edge cases (e.g., Feb 29 -> Feb 28 in non-leap years)
            return reference_date.replace(year=reference_date.year + 1)
    
    return None


def calculate_next_weekly_occurrence(current_date: datetime, days: List[int]) -> datetime:
    """
    Calculate the next occurrence for weekly recurring tasks with specific days.
    
    Args:
        current_date: The date to calculate from
        days: List of integers representing days of the week (0=Monday, 6=Sunday)
        
    Returns:
        Next occurrence datetime
    """
    current_weekday = current_date.weekday()  # Monday is 0, Sunday is 6
    
    # Find the next occurrence from the list of specified days
    days_sorted = sorted(days)
    
    # Check if any of the specified days is later in this week
    for day in days_sorted:
        if day > current_weekday:
            days_ahead = day - current_weekday
            return current_date + timedelta(days=days_ahead)
    
    # If not, the next occurrence is next week
    days_ahead = 7 - current_weekday + days_sorted[0]
    return current_date + timedelta(days=days_ahead)


def is_overdue(task: 'Task') -> bool:
    """
    Check if a task is overdue.
    
    Args:
        task: The task to check
        
    Returns:
        True if the task is overdue, False otherwise
    """
    if not task.due or task.completed:
        return False
    
    return datetime.now() > task.due


def is_due_soon(task: 'Task', threshold_hours: int = 24) -> bool:
    """
    Check if a task is due soon.
    
    Args:
        task: The task to check
        threshold_hours: Number of hours to consider as "soon" (default 24)
        
    Returns:
        True if the task is due soon, False otherwise
    """
    if not task.due or task.completed:
        return False
    
    time_until_due = task.due - datetime.now()
    return timedelta(0) < time_until_due <= timedelta(hours=threshold_hours)


def get_countdown_text(task: 'Task') -> str:
    """
    Get a human-readable countdown text for a task due soon.
    
    Args:
        task: The task to get countdown for
        
    Returns:
        Countdown text (e.g. "in 4h 30m")
    """
    if not task.due or task.completed:
        return ""
    
    time_until_due = task.due - datetime.now()
    
    if time_until_due <= timedelta(0):
        return "(OVERDUE)"
    
    # Calculate days, hours, minutes
    days = time_until_due.days
    hours, remainder = divmod(time_until_due.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    
    if days > 0:
        return f"(in {days}d {hours}h)"
    elif hours > 0:
        return f"(in {hours}h {minutes}m)"
    else:
        return f"(in {minutes}m)"