---
description: "Task list for Todo Console Application implementation"
---

# Tasks: Todo Console Application

**Input**: Design documents from `/specs/1-todo-console-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure per implementation plan in src/
- [x] T002 Initialize Python project with proper directory structure (models.py, services.py, utils.py, main.py)
- [x] T003 [P] Create src/models.py file for Task data structure
- [x] T004 [P] Create src/services.py file for task operations
- [x] T005 [P] Create src/utils.py file for helper functions
- [x] T006 [P] Create src/main.py file for CLI interface

---
## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Examples of foundational tasks (adjust based on your project):

- [x] T007 Implement Task class in src/models.py with id, title, description, completed fields
- [x] T008 Implement TaskList class in src/models.py with tasks list and next_id counter
- [x] T009 [P] Create CLI helper functions in src/utils.py for input validation
- [x] T010 [P] Create CLI helper functions in src/utils.py for output formatting
- [x] T011 Implement core task operations in src/services.py (add_task, get_all_tasks)
- [x] T012 Set up main application loop in src/main.py with menu options
- [x] T013 Configure error handling framework for graceful failure

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---
## Phase 3: User Story 1 - Add and View Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable users to add new tasks with titles and optional descriptions, then view their list of tasks with clear status indicators to track their progress.

**Independent Test**: Can be fully tested by adding multiple tasks and viewing the list to verify they appear correctly with proper status indicators.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

- [ ] T014 [P] [US1] Manual test scenario: Add task with title "Buy groceries" and verify it appears with incomplete status
- [ ] T015 [P] [US1] Manual test scenario: Add multiple tasks and verify all appear with correct status indicators

### Implementation for User Story 1

- [x] T016 [P] [US1] Implement add_task method in src/services.py with title validation
- [x] T017 [P] [US1] Implement get_all_tasks method in src/services.py to return all tasks
- [x] T018 [US1] Add CLI command for adding tasks in src/main.py (option 1)
- [x] T019 [US1] Add CLI command for viewing tasks in src/main.py (option 2)
- [x] T020 [US1] Implement input validation to ensure title is not empty
- [x] T021 [US1] Add clear status indicators (complete/incomplete) in task display
- [x] T022 [US1] Test US1 functionality independently to ensure it works as MVP

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---
## Phase 4: User Story 2 - Update and Delete Tasks (Priority: P2)

**Goal**: Enable users to maintain their task list by updating existing tasks when details change or removing tasks that are no longer needed using unique IDs.

**Independent Test**: Can be fully tested by adding tasks, updating their details, and deleting unwanted tasks by their unique IDs.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T023 [P] [US2] Manual test scenario: Update a task by ID and verify details are updated
- [ ] T024 [P] [US2] Manual test scenario: Delete a task by ID and verify it's removed from list

### Implementation for User Story 2

- [x] T025 [P] [US2] Implement update_task method in src/services.py to modify task details by ID
- [x] T026 [P] [US2] Implement delete_task method in src/services.py to remove task by ID
- [x] T027 [US2] Add CLI command for updating tasks in src/main.py (option 3
- [x] T028 [US2] Add CLI command for deleting tasks in src/main.py (option 4)
- [x] T029 [US2] Add validation to ensure task exists before update/delete operations
- [x] T030 [US2] Add error handling for invalid task IDs
- [x] T031 [US2] Test US2 functionality independently

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---
## Phase 5: User Story 3 - Mark Tasks Complete/Incomplete (Priority: P3)

**Goal**: Enable users to track their progress by marking tasks as complete when finished and potentially marking them as incomplete if they need to be revisited.

**Independent Test**: Can be fully tested by marking tasks as complete and incomplete and verifying the status indicators update appropriately in the task list.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T032 [P] [US3] Manual test scenario: Mark a task as complete and verify status updates
- [ ] T033 [P] [US3] Manual test scenario: Mark a completed task as incomplete and verify status updates

### Implementation for User Story 3

- [x] T034 [P] [US3] Implement mark_task_complete method in src/services.py to toggle completion status
- [x] T035 [P] [US3] Implement mark_task_incomplete method in src/services.py to toggle completion status
- [x] T036 [US3] Add CLI command for marking tasks complete/incomplete in src/main.py (option 5)
- [x] T037 [US3] Add validation to ensure task exists before status change
- [x] T038 [US3] Update display functions to show accurate status indicators
- [x] T039 [US3] Test US3 functionality independently

**Checkpoint**: All user stories should now be independently functional

---
## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T040 [P] Add comprehensive error handling for all edge cases (empty title, invalid ID, etc.)
- [x] T041 [P] Add performance validation to ensure operations meet time requirements
- [x] T042 [P] Improve UI/UX consistency across all menu options
- [x] T043 [P] Add input sanitization for task titles and descriptions
- [x] T044 [P] Add graceful handling of keyboard interrupts (Ctrl+C)
- [x] T045 [P] Add documentation comments to all functions
- [x] T046 [P] Run quickstart.md validation to ensure all features work as expected
- [x] T047 [P] Final integration testing of all features together

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
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Models before services
- Services before CLI implementation
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

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
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---
## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence