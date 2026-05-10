---
title: Assignment Data Model Addendum
type: architecture
status: active
updated: 2026-05-10
owners:
  - db-owner
  - backend-team
related:
  - [[/04-architecture/object-storage-architecture.md]]
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

- The database stores attachment metadata only. Object bytes live behind Backend storage APIs.
- Existing local uploaded binaries remain on the Backend filesystem until migration; new durable objects use Backend object-storage APIs.
- The storage key must be treated as an internal implementation field, not a user-facing path.

# Object Storage Extension

`assignment_submission_attachments` keeps the existing response contract while adding:

- `storage_provider`
- `bucket_name`
- `checksum_sha256`

`storage_key` remains an internal Backend key and must not be a public URL. Deleting attachment rows, including through submission cascade, enqueues `object_deletion_jobs` through the shared object-storage trigger strategy.
