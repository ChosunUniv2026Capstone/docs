---
title: Garage-backed object storage through Backend proxy
type: decision
status: accepted
updated: 2026-05-10
owners:
  - architecture-owner
  - backend-team
  - db-owner
  - service-team
related:
  - [[/01-requirements/req-object-storage.md]]
  - [[/03-conventions/conv-object-storage.md]]
  - [[/04-architecture/object-storage-architecture.md]]
source:
  - 2026-05-10 `.omx/plans/ralplan-garage-object-storage.md`
---

# Context

Smart Class currently stores assignment uploads on the Backend local filesystem while other LMS domains still lack durable file storage. Backend container recreation can therefore lose files or make metadata point at unavailable local paths.

# Decision

Use Garage in local/demo as an S3-compatible object store, but keep application code provider-neutral and route all browser file access through Backend APIs.

The first pass uses one bucket with typed prefixes and internal object keys. DB metadata remains the source of truth for which domain row owns each object. Deleting or replacing metadata must enqueue `object_deletion_jobs`; PostgreSQL `AFTER DELETE` triggers on each object metadata table are the required fallback for owner-level cascades.

# Accepted Design

- One bucket, default name `smart-class`, with typed prefixes for assignment, learning, notice, exam, report, and ops artifacts.
- Backend owns authorization and streams uploads/downloads. Front receives only metadata and Backend route URLs.
- DB stores provider, bucket, internal key, filename, MIME type, size, optional checksum, and timestamps.
- `storage_provider` values are provider-neutral (`local`, `s3`) so local fake storage and future AWS-compatible storage can use the same contract.
- `object_deletion_jobs` is the durable outbox for immediate post-commit deletion and retries.
- First-pass report generation is attendance CSV only; grade/assignment/exam/PDF exports require separate source-data contracts.

# Rejected Alternatives

- Multiple first-pass buckets per domain: better isolation, but more bootstrap/secrets complexity than needed while Front never talks to S3 directly.
- Presigned/direct browser uploads: lower Backend bandwidth, but violates the first-pass Backend-proxy constraint and adds CORS/expiry/client-state complexity.
- Best-effort application-only deletes: misses raw SQL deletes and owner cascades; DB triggers are required as a safety net.
- Storing object bytes in Postgres: increases database size and conflicts with the provider-neutral storage objective.

# Consequences

- Backend and Service work must use S3-compatible operations only, not Garage admin behavior in feature code.
- DB schema changes are additive for existing assignment metadata.
- Deletion is immediate in intent but durable/retryable in execution: failures remain visible as pending or failed jobs.
- Garage ops artifacts are demo/local artifacts unless a later production backup design adds off-host copy or separate backup credentials.
