---
title: Assignment Data Model Addendum
type: architecture
status: active
updated: 2026-05-09
owners:
  - db-owner
  - backend-team
related:
  - [[/04-architecture/data-model-overview.md]]
  - [[/04-architecture/assignment-workflow-api.md]]
source:
  - 2026-05-09 local implementation alignment for assignment workflow
---

# New Tables

- `assignments`
  - course assignment master rows
- `assignment_submissions`
  - one latest submission per assignment and student
- `assignment_submission_attachments`
  - file metadata for one submission

# Relationships

- One `course` has many `assignments`.
- One `assignment` has many `assignment_submissions`.
- One `assignment_submission` has many `assignment_submission_attachments`.
- One `assignment_submission` belongs to one `user` in student role.

# Constraints

- `assignments`
  - `due_at > opens_at`
- `assignment_submissions`
  - unique `(assignment_id, student_user_id)`
- `assignment_submission_attachments`
  - belongs to one submission
  - stores original filename and backend storage key separately

# Storage Notes

- The database stores attachment metadata only.
- The uploaded binary file is stored on the backend local filesystem.
- The storage key must be treated as an internal implementation field, not a user-facing path.
