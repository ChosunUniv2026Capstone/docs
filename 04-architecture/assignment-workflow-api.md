---
title: Assignment Workflow API
type: architecture
status: active
updated: 2026-05-14
owners:
  - backend-team
  - frontend-team
  - db-owner
related:
  - [[/01-requirements/req-student-features.md]]
  - [[/01-requirements/req-professor-features.md]]
  - [[/04-architecture/assignment-data-model-addendum.md]]
  - [[/04-architecture/object-storage-architecture.md]]
source:
  - 2026-05-09 local implementation alignment for course assignment workflow
  - 2026-05-14 current issue-resolution checkpoint for grading/feedback scope
---

# Domain Model

- `assignment`
  - course-level assignment metadata managed by the professor
- `assignment_submission`
  - one latest submission row per assignment and student
- `assignment_submission_attachment`
  - attachment metadata rows that belong to a submission

# MVP Rules

- Assignments belong to one course.
- Professors can create assignments for their own course.
- Students can only see assignments for courses they are enrolled in.
- Each student keeps one mutable submission per assignment.
- Students may submit or re-submit only while the assignment state is `open`.
- A submission contains:
  - free-form text
  - zero or more attached files
- Attached files are stored behind Backend object-storage APIs. Existing local filesystem rows remain readable during migration, but new durable storage uses the provider-neutral storage metadata contract.
- Professor detail view shows:
  - roster of who submitted
  - submission timestamp
  - submission text
  - attachment metadata
- Grading and feedback are out of scope for the current assignment API. Adding grade fields, feedback visibility, rubric state, or score publication requires a docs-first contract and DB migration plan.
- Assignment state is computed from the configured window:
  - `upcoming`
  - `open`
  - `closed`

# Professor Endpoints

- `GET /api/professors/{professor_id}/courses/{course_code}/assignments`
- `POST /api/professors/{professor_id}/courses/{course_code}/assignments`
- `GET /api/professors/{professor_id}/courses/{course_code}/assignments/{assignment_id}`
- `GET /api/professors/{professor_id}/courses/{course_code}/assignments/{assignment_id}/attachments/{attachment_id}`

# Student Endpoints

- `GET /api/students/{student_id}/courses/{course_code}/assignments`
- `GET /api/students/{student_id}/courses/{course_code}/assignments/{assignment_id}`
- `POST /api/students/{student_id}/courses/{course_code}/assignments/{assignment_id}/submission`
  - multipart form fields:
    - `submission_text`
    - `files`
- `GET /api/students/{student_id}/courses/{course_code}/assignments/{assignment_id}/attachments/{attachment_id}`

# Response Shape

- Assignment summary returns:
  - `id`
  - `title`
  - `description`
  - `opens_at`
  - `due_at`
  - `status`
  - `created_at`
- Student summary also returns:
  - `submitted`
  - `submitted_at`
  - `attachment_count`
- Student detail also returns:
  - `submission`
- Professor summary also returns:
  - `submission_count`
  - `total_students`
- Professor detail also returns:
  - `submissions`
- Submission detail returns:
  - `id`
  - `student_id`
  - `student_name`
  - `submission_text`
  - `submitted_at`
  - `updated_at`
  - `attachments`
- Attachment detail returns:
  - `id`
  - `original_filename`
  - `mime_type`
  - `file_size_bytes`
  - `uploaded_at`
  - no public object URL or Garage credential fields

# Validation Rules

- `due_at` must be later than `opens_at`.
- Submission updates are blocked after the assignment becomes `closed`.
- The current local MVP accepts up to 5 files per submission.
- The current local MVP rejects any single uploaded file larger than 10 MiB.

# Error Codes

- `ASSIGNMENT_NOT_FOUND`
- `ASSIGNMENT_INVALID_WINDOW`
- `ASSIGNMENT_INVALID_PAYLOAD`
- `ASSIGNMENT_NOT_OPEN`
- `ASSIGNMENT_ATTACHMENT_NOT_FOUND`
- `ASSIGNMENT_SUBMISSION_FILE_LIMIT_EXCEEDED`
- `ASSIGNMENT_SUBMISSION_FILE_TOO_LARGE`
