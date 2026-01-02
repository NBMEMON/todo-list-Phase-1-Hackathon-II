---

description: "Task list for intelligent todo features implementation"
---

# Tasks: Intelligent Todo Features

**Input**: Design documents from `/specs/002-intelligent-todo-features/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Install python-dateutil dependency for date parsing
- [X] T002 Create src/models/task.py if it doesn't exist
- [X] T003 Create src/services/date_utils.py for date parsing and recurrence logic
- [X] T004 Create src/lib/display.py for output formatting with due date indicators

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Examples of foundational tasks (adjust based on your project):

- [X] T005 [P] Extend Task model with due date and recurrence fields in src/models/task.py
- [X] T006 [P] Create date parsing utility function in src/services/date_utils.py
- [X] T007 [P] Create recurrence calculation functions in src/services/date_utils.py
- [X] T008 [P] Create ANSI color formatting functions in src/lib/display.py
- [X] T009 Update existing CLI interface to accept new parameters in src/cli/main.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create Recurring Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable users to create recurring tasks that automatically generate new instances when completed

**Independent Test**: Can be fully tested by creating a recurring task with various patterns (daily, weekly, monthly, yearly) and verifying that a new instance is created when the original is marked complete

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

- [X] T010 [P] [US1] Unit test for Task model with recurrence fields in tests/unit/test_task.py
- [X] T011 [P] [US1] Unit test for recurrence calculation functions in tests/unit/test_date_utils.py

### Implementation for User Story 1

- [X] T012 [P] [US1] Update Task model to support recurrence fields in src/models/task.py
- [X] T013 [US1] Implement recurrence validation logic in src/services/date_utils.py
- [X] T014 [US1] Implement recurrence pattern parsing in CLI command in src/cli/main.py
- [X] T015 [US1] Update add command to accept --recurring and --recurring-days flags in src/cli/main.py
- [X] T016 [US1] Update update command to accept --recurring and --recurring-days flags in src/cli/main.py
- [X] T017 [US1] Implement recurring task completion logic in src/services/todo_service.py
- [X] T018 [US1] Test recurring task creation and completion with various patterns

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Set and View Due Dates (Priority: P1)

**Goal**: Enable users to assign due dates to tasks using natural language and see these dates displayed when viewing their task list

**Independent Test**: Can be fully tested by creating tasks with due dates using natural language and verifying they display correctly in the list command

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [X] T019 [P] [US2] Unit test for natural date parsing in tests/unit/test_date_utils.py
- [X] T020 [P] [US2] Integration test for due date functionality in tests/integration/test_due_dates.py

### Implementation for User Story 2

- [X] T021 [P] [US2] Implement natural language date parsing in src/services/date_utils.py
- [X] T022 [US2] Update Task model to support due date field in src/models/task.py
- [X] T023 [US2] Update add command to accept --due flag in src/cli/main.py
- [X] T024 [US2] Update update command to accept --due flag in src/cli/main.py
- [X] T025 [US2] Update list command to display due dates in src/cli/main.py
- [X] T026 [US2] Test due date creation and display with various natural language inputs

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - View Overdue and Soon-Due Tasks (Priority: P2)

**Goal**: Enable users to quickly identify overdue tasks and tasks that are due soon (within 24 hours) to prioritize their work

**Independent Test**: Can be fully tested by creating tasks with past due dates and tasks due soon, then verifying they are highlighted appropriately in the list output

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [X] T027 [P] [US3] Unit test for overdue detection in tests/unit/test_date_utils.py
- [X] T028 [P] [US3] Unit test for soon-due detection in tests/unit/test_date_utils.py

### Implementation for User Story 3

- [X] T029 [P] [US3] Implement overdue detection logic in src/services/date_utils.py
- [X] T030 [P] [US3] Implement soon-due countdown logic in src/services/date_utils.py
- [X] T031 [US3] Update list output formatting to highlight overdue tasks in src/lib/display.py
- [X] T032 [P] [US3] Update list output to show countdown for soon-due tasks in src/lib/display.py
- [X] T033 [US3] Integrate overdue and soon-due indicators in list command in src/cli/main.py
- [X] T034 [US3] Test overdue and soon-due indicators with various due dates

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - Filter Tasks by Due Status (Priority: P3)

**Goal**: Enable users to filter their task list to see only overdue tasks or tasks due today

**Independent Test**: Can be fully tested by creating various tasks with different due dates and using the filter options to verify only the appropriate tasks are displayed

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [X] T035 [P] [US4] Unit test for due date filtering logic in tests/unit/test_todo_service.py
- [X] T036 [P] [US4] Integration test for filtering functionality in tests/integration/test_filters.py

### Implementation for User Story 4

- [X] T037 [P] [US4] Implement overdue filter logic in src/services/todo_service.py
- [X] T038 [P] [US4] Implement due-today filter logic in src/services/todo_service.py
- [X] T039 [US4] Update list command to support --overdue flag in src/cli/main.py
- [X] T040 [US4] Update list command to support --due-today flag in src/cli/main.py
- [X] T041 [US4] Test filtering functionality with various due date scenarios

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T042 [P] Update README.md with new feature documentation
- [X] T043 [P] Add error handling for invalid date formats with helpful messages
- [X] T044 [P] Add error handling for invalid recurrence patterns with helpful messages
- [X] T045 [P] Create comprehensive test suite covering all features in tests/
- [X] T046 [P] Add input validation for all new CLI parameters
- [X] T047 [P] Add ANSI color support detection for terminals that don't support it
- [X] T048 Run quickstart.md validation scenarios

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - Depends on US2 (due dates)
- **User Story 4 (P3)**: Can start after Foundational (Phase 2) - Depends on US2 (due dates)

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Unit test for Task model with recurrence fields in tests/unit/test_task.py"
Task: "Unit test for recurrence calculation functions in tests/unit/test_date_utils.py"

# Launch all models for User Story 1 together:
Task: "Update Task model to support recurrence fields in src/models/task.py"
Task: "Implement recurrence validation logic in src/services/date_utils.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence