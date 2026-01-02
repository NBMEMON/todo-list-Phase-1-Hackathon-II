# Research Summary: Intelligent Todo Features

## Decision: Date Parsing Library
**Rationale**: Using python-dateutil for natural language date parsing as it's lightweight, well-established, and handles relative dates well ("tomorrow", "next monday", "in 2 days").
**Alternatives considered**: 
- Custom regex-based parser (more complex, less reliable)
- pendulum library (heavier dependency than needed)
- arrow library (also heavier than dateutil for this use case)

## Decision: Recurrence Implementation
**Rationale**: Implementing simple recurrence logic with if/elif statements rather than full rrule library to keep dependencies minimal. Using dateutil.relativedelta for date calculations.
**Alternatives considered**:
- Using the full iCalendar rrule standard (unnecessary complexity for this feature)
- Custom date calculation functions (reinventing the wheel, potential bugs)

## Decision: Task Model Extension
**Rationale**: Extending the existing Task model with new fields (due, recurrence, recurrence_config, next_due) to maintain backward compatibility while adding functionality.
**Alternatives considered**:
- Creating separate models for recurring vs regular tasks (would complicate the codebase)
- Using composition instead of extending the model (would require more complex queries)

## Decision: Visual Indicators
**Rationale**: Using ANSI escape codes for color formatting rather than adding heavy dependencies like rich or colorama.
**Alternatives considered**:
- Using the rich library (too heavy for this simple use case)
- Using colorama (another dependency when ANSI codes work fine)

## Decision: Storage Approach
**Rationale**: Maintaining in-memory storage approach to keep consistency with existing application behavior.
**Alternatives considered**:
- Adding file-based persistence (outside scope of this feature)
- Using a database (overkill for a simple todo CLI app)