---
title: Garage-backed Object Storage Requirements
type: requirement
status: active
updated: 2026-05-10
owners:
  - backend-team
  - db-owner
  - service-team
  - frontend-team
related:
  - [[/02-decisions/adr-0012-garage-backed-object-storage.md]]
  - [[/03-conventions/conv-object-storage.md]]
  - [[/04-architecture/object-storage-architecture.md]]
source:
  - 2026-05-10 `.omx/plans/ralplan-garage-object-storage.md`
---

# Goal

Provide durable object storage for LMS files while keeping authorization and file access behind Backend APIs.

# In Scope

- Assignment submission attachments.
- Learning materials and lecture videos.
- Notice attachments.
- Exam question/explanation media.
- First-pass attendance CSV report exports.
- Local/demo Service-generated backup artifacts.

# Out of Scope

- Direct browser access to Garage/S3.
- Public object URLs, object ACL policy design, object lock, provider-managed lifecycle policy, or bucket encryption as application dependencies.
- Presence snapshot archival.
- First-pass grade, assignment, exam, and PDF report export generation. The DB metadata contract may remain future-compatible for those domains.
- Treating Garage as the sole protected backup target for production.

# Functional Requirements

- Front must never receive Garage credentials, bucket credentials, or public object URLs.
- Backend must upload, stream, range-stream, replace, and delete files through a provider-neutral storage interface.
- DB must store object metadata only: original filename, stored filename, MIME type, byte size, provider, bucket, internal storage key, optional checksum, and timestamps.
- Storage keys must be internal keys, not URLs.
- User-facing APIs may expose attachment metadata and authenticated download routes, but not bucket credentials.
- Deleting or replacing metadata must enqueue a durable object deletion job in the same DB lifecycle that removes old metadata.
- Owner cascades must not bypass deletion capture; PostgreSQL `AFTER DELETE` triggers are the default safety net for object metadata tables.
- Deletion workers must treat object delete as idempotent and retryable.

# Key Prefix Contract

- `assignments/{assignment_id}/submissions/{submission_id}/students/{student_user_id}/{uuid}_{filename}`
- `learning/{course_code}/{item_id}/{uuid}_{filename}`
- `notices/{notice_id}/{uuid}_{filename}`
- `exams/{exam_id}/questions/{question_id}/{uuid}_{filename}`
- `exams/{exam_id}/submissions/{submission_id}/answers/{answer_id}/{uuid}_{filename}`
- `reports/{domain}/{course_code}/{yyyy}/{mm}/{uuid}_{filename}`
- `ops/{yyyy}/{mm}/{dd}/{artifact_type}/{uuid}_{filename}`

# Acceptance

- Assignment attachment metadata remains backward-compatible for existing assignment APIs.
- New learning, notice, exam, and report metadata tables can capture object keys without storing object bytes in Postgres.
- `object_deletion_jobs` records pending deletion work when metadata rows are deleted directly or by owner cascade.
- DB trigger tests prove deletion jobs are created for assignment, learning, notice, exam question, exam answer, and report export metadata.
- Report export implementation starts with attendance CSV only.
