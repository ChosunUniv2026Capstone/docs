---
title: Object storage architecture
type: architecture
status: active
updated: 2026-05-21
owners:
  - architecture-owner
  - backend-team
  - db-owner
  - service-team
related:
  - [[/01-requirements/req-object-storage.md]]
  - [[/02-decisions/adr-0012-garage-backed-object-storage.md]]
  - [[/03-conventions/conv-object-storage.md]]
  - [[/04-architecture/data-model-overview.md]]
source:
  - 2026-05-10 DB/postgres/init/015_object_storage_schema.sql
---

# Overview

Object storage is split into three responsibilities:

- Service runs Garage for local/demo and bootstraps the bucket and app credentials.
- Backend owns upload/download authorization, object streaming, range reads, and deletion job processing.
- DB owns metadata, ownership relations, and the durable object deletion outbox.

# DB Foundation

The schema extends assignment attachments and adds metadata tables for the new object-backed domains:

- `assignment_submission_attachments`: existing assignment metadata plus `storage_provider`, `bucket_name`, and `checksum_sha256`.
- `learning_items`: persisted course learning material records.
- `learning_item_attachments`: uploaded learning material/video object metadata.
- `notice_attachments`: notice attachment object metadata.
- `exam_question_attachments`: professor-authored exam prompt/explanation media metadata.
- `exam_answer_attachments`: future-compatible answer file metadata.
- `report_exports`: generated report file metadata; first pass is attendance CSV, including professor summary/full attendance variants.
- `object_deletion_jobs`: durable deletion outbox.

# Trigger Strategy

Every object metadata table has an `AFTER DELETE` trigger that calls `enqueue_object_deletion_job()`.

The trigger captures:

- `storage_provider`
- `bucket_name`
- `storage_key`
- owner domain
- owner id, when available
- reason `metadata_deleted`
- status `pending`

The trigger suppresses duplicate active jobs for the same provider/bucket/key when a pending or processing job already exists. This lets application code enqueue explicit replacement jobs while preserving trigger safety for raw deletes and cascading owner deletes.

# Rollback and Retry

DB triggers capture deletion after metadata disappears. They do not delete object bytes directly. Backend must process pending jobs after commit and retry failed jobs. Backend must also compensate newly uploaded objects when a DB transaction fails before metadata is committed.

# Auth Boundary

Object keys are internal implementation details. APIs must authorize against course ownership, enrollment, role, report ownership, or exam/assignment ownership before returning metadata or streaming bytes.

# Migration Notes

Existing assignment rows default to `storage_provider='local'` and `bucket_name='local'` so current local files remain readable until Backend migration imports them into Garage/S3 and updates metadata.
