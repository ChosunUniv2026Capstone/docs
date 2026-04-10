---
title: Exam Workflow API
type: architecture
status: active
updated: 2026-04-10
owners:
  - backend-team
  - frontend-team
  - db-owner
related:
  - [[/01-requirements/req-exam-workflow.md]]
  - [[/02-decisions/adr-0010-objective-exam-workflow-with-start-guard.md]]
  - [[/04-architecture/exam-mvp-contract.md]]
source:
  - 2026-04-09 local alignment with dd exam workflow
  - 2026-04-10 docs lane contract hardening against docs/backend/front bundle review
---

# Domain Model

- `exam`
  - top-level course exam metadata
- `exam_question`
  - ordered question row per exam
- `exam_question_option`
  - option row for objective questions
- `exam_submission`
  - one student attempt row
- `exam_submission_answer`
  - one answer row per question inside a submission

# Status Rules

- Exam status:
  - `draft`
  - `published`
  - `open`
  - `closed`
  - `archived`
- Submission status:
  - `in_progress`
  - `submitted`
  - `auto_submitted`
  - `graded`
  - `expired`

# Professor Endpoints

- `GET /api/professors/{professor_id}/courses/{course_code}/exams`
- `POST /api/professors/{professor_id}/courses/{course_code}/exams`
- `GET /api/professors/{professor_id}/courses/{course_code}/exams/{exam_id}`
- `PUT /api/professors/{professor_id}/courses/{course_code}/exams/{exam_id}`
- `DELETE /api/professors/{professor_id}/courses/{course_code}/exams/{exam_id}`
- `POST /api/professors/{professor_id}/courses/{course_code}/exams/{exam_id}/publish`
- `POST /api/professors/{professor_id}/courses/{course_code}/exams/{exam_id}/close`

# Student Endpoints

- `GET /api/students/{student_id}/courses/{course_code}/exams`
- `GET /api/students/{student_id}/courses/{course_code}/exams/{exam_id}`
- `POST /api/students/{student_id}/courses/{course_code}/exams/{exam_id}/start`
- `PUT /api/students/{student_id}/courses/{course_code}/exams/{exam_id}/submissions/{submission_id}/answers/{question_id}`
- `POST /api/students/{student_id}/courses/{course_code}/exams/{exam_id}/submit`
  - submit targets the student's active `in_progress` attempt for the exam, so the route stays exam-scoped in the current local MVP.

# Response Shape

- Exam summary:
  - `id`
  - `title`
  - `description`
  - `exam_type`
  - `status`
  - `starts_at`
  - `ends_at`
  - `duration_minutes`
  - `late_entry_allowed`
  - `auto_submit_enabled`
  - `shuffle_questions`
  - `max_attempts`
  - `question_count`
  - `attempt_count`
- The response shape may still include `requires_presence` for schema compatibility, but the current local exam policy treats it as always true.
- Student exam detail also returns:
  - `availability`
  - `attempt`
  - `questions`
- Professor exam detail also returns:
  - `submission_overview`
  - `submissions`
- Student detail returns an empty `questions` list before an attempt starts.
- The start endpoint creates the student attempt and only then reveals the question list.
- The start endpoint verifies that the student has at least one active registered device before creating the first attempt.
- The exam start check does not require current class-window resolution or classroom network observation.
- If `late_entry_allowed` is false, the start endpoint rejects the first attempt after the official start time.
- If `late_entry_allowed` is true, the start endpoint still caps the created attempt deadline at the official exam end time.
- The frontend navigates to a dedicated student exam-taking route after the start call succeeds.
- The frontend blocks submit when unanswered required questions remain and shows the missing question numbers before any submit API call.
- If `auto_submit_enabled` is true, the frontend triggers the submit flow automatically when the stored attempt expiry is reached.
- Student endpoint responses do not expose per-question correctness in the student UI.
- Attempt summary returns:
  - `id`
  - `attempt_no`
  - `status`
  - `started_at`
  - `submitted_at`
  - `expires_at`
  - `total_count`
  - `answered_count`
- `expires_at` is the effective per-attempt deadline and may be earlier than the configured `duration_minutes` when a late-started attempt is capped by the official exam end time.
- Professor submission overview returns:
  - `total_students`
  - `started_students`
  - `submitted_students`
  - `not_started_students`
  - `average_score`
  - `max_score`
- Professor submission rows return the latest attempt per enrolled student with:
  - `student_id`
  - `student_name`
  - `status`
  - `attempt_no`
  - `answered_count`
  - `started_at`
  - `submitted_at`
  - `score`
  - `max_score`
  - `total_count`

# First UI Scope

- The current local professor form creates objective questions.
- The current local student UI renders a dedicated exam-taking page with one question at a time, previous/next navigation, a remaining-time view, and numbered question shortcuts.
- The current local backend applies deterministic per-attempt shuffling for questions when the exam flag is enabled.
- Objective choice order remains fixed in the current local exam flow.

# Error Codes

- `EXAM_NOT_FOUND`
- `EXAM_NOT_OPEN`
- `EXAM_NOT_EDITABLE`
- `EXAM_INVALID_WINDOW`
- `EXAM_INVALID_PAYLOAD`
- `EXAM_ATTEMPT_LIMIT_REACHED`
- `EXAM_LATE_ENTRY_NOT_ALLOWED`
- `EXAM_SUBMISSION_NOT_FOUND`
- `EXAM_SUBMISSION_ALREADY_FINALIZED`
- `PRESENCE_INELIGIBLE`
