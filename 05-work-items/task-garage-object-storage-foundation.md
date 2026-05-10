---
title: Garage object storage foundation work item
type: task
status: active
updated: 2026-05-10
owners:
  - db-owner
  - backend-team
  - service-team
  - frontend-team
related:
  - [[/01-requirements/req-object-storage.md]]
  - [[/02-decisions/adr-0012-garage-backed-object-storage.md]]
  - [[/04-architecture/object-storage-architecture.md]]
---

# Scope

Implement the Garage-backed object storage plan in dependency order:

1. Contract/docs and DB metadata/deletion outbox foundation.
2. Service Garage compose/bootstrap/env/docs/tests.
3. Backend storage abstraction and assignment migration.
4. Backend learning/notice/exam/report APIs.
5. Front file flows through Backend APIs only.
6. Cross-role E2E and deletion/restart evidence.

# DB Done Criteria

- DB init contains object metadata tables and `object_deletion_jobs`.
- Existing assignment attachment API shape remains compatible.
- `AFTER DELETE` trigger coverage exists for every object metadata table.
- Trigger tests prove owner cascades enqueue deletion jobs.

# Non-goals

- Direct Front-to-Garage access.
- Production backup hardening solely through Garage.
- Grade/assignment/exam/PDF report generation in the first pass.
