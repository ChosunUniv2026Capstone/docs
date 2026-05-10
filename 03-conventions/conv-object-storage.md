---
title: Object storage conventions
type: convention
status: active
updated: 2026-05-10
owners:
  - backend-team
  - db-owner
  - service-team
applies_to:
  - backend
  - db
  - service
  - frontend
related:
  - [[/01-requirements/req-object-storage.md]]
  - [[/02-decisions/adr-0012-garage-backed-object-storage.md]]
  - [[/04-architecture/object-storage-architecture.md]]
---

# Access Boundary

- Front must not receive Garage/S3 credentials, bucket names as authority, presigned URLs, or public object URLs.
- Backend routes are the only user-facing upload/download surface.
- Backend authorization must be checked before object metadata is returned and before object bytes are streamed.

# Metadata Fields

Object metadata tables use these common fields where applicable:

- `original_filename`
- `stored_filename`
- `mime_type`
- `file_size_bytes`
- `storage_provider`
- `bucket_name`
- `storage_key`
- `checksum_sha256`
- `created_at`

`storage_key` is always an internal object key. It must not be an HTTP URL.

# Key Prefixes

- Assignment submissions: `assignments/{assignment_id}/submissions/{submission_id}/students/{student_user_id}/{uuid}_{filename}`
- Learning materials/videos: `learning/{course_code}/{item_id}/{uuid}_{filename}`
- Notice attachments: `notices/{notice_id}/{uuid}_{filename}`
- Exam question media: `exams/{exam_id}/questions/{question_id}/{uuid}_{filename}`
- Exam answer media: `exams/{exam_id}/submissions/{submission_id}/answers/{answer_id}/{uuid}_{filename}`
- Reports: `reports/{domain}/{course_code}/{yyyy}/{mm}/{uuid}_{filename}`
- Ops artifacts: `ops/{yyyy}/{mm}/{dd}/{artifact_type}/{uuid}_{filename}`

# Deletion Lifecycle

- Replacement flow: write the new object, update metadata in a transaction, enqueue deletion for the old object, then process deletion after commit.
- Delete flow: delete metadata in a transaction; `AFTER DELETE` triggers enqueue `object_deletion_jobs` as a durable safety net.
- Rollback flow: if object write succeeds but DB write fails before commit, Backend must delete the newly written object as compensation or create a tombstone when DB context exists.
- Deletion workers must be idempotent. Missing object should be treated as successful cleanup.

# Report Export Scope

First-pass report export means attendance CSV only. Grade, assignment, exam, and PDF export object metadata fields may exist for compatibility, but generating those files is not implied until their data contracts are documented.
