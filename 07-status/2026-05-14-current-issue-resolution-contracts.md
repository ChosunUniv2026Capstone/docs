---
title: Current issue resolution contract checkpoint
type: status
status: active
updated: 2026-05-14
owners:
  - team
related:
  - [[/01-requirements/req-attendance-presence.md]]
  - [[/01-requirements/req-exam-workflow.md]]
  - [[/01-requirements/req-object-storage.md]]
  - [[/03-conventions/conv-release-and-deployment.md]]
  - [[/04-architecture/assignment-workflow-api.md]]
  - [[/04-architecture/data-model-overview.md]]
  - [[/04-architecture/exam-workflow-api.md]]
  - [[/04-architecture/local-runtime-topology.md]]
  - [[/04-architecture/object-storage-architecture.md]]
source:
  - Smart Class issue snapshot `.omx/ultragoal/reports/open-issues-20260513T150238Z.json`
  - Team run `resolve-all-current-s-f6646c39`, 2026-05-14 KST
---

# Purpose

This checkpoint records the docs-first contracts that must be preserved before the active issue-fix branches are merged.
It is an evidence snapshot for the May 2026 open-issue resolution run, not a replacement for the linked requirement and architecture documents.
If an implementation branch changes an API/schema/runtime behavior beyond the contract below, update the owning requirement/architecture/convention document before merging code.

# Current lane status

| Lane | Evidence at checkpoint | Merge gate |
| --- | --- | --- |
| Backend issues #14/#15/#16/#17/#20/#21/#22 and #19/#23 close-candidates | Worker-1 mapped existing Backend evidence, then committed the midnight-window QA fix on `Backend/fix/backend-current-issues` commit `6179caf`. Worker-4 independently reran `PYTHONPATH=. python3 -m pytest -q` and got `74 passed`. | Backend task #5 still needs final lifecycle/PR evidence before merge. |
| Front issues #19/#20/#21 | Worker-3 completed `Front/fix/front-attendance-ux-contract` commit `5c126f7`; reported `npm run build`, scoped lint, and Playwright auth/presence e2e `11 passed`. | Front PR/check evidence still required before merge. |
| DB #12 and Service #4/#9/#10 plus nginx/upload integration | Worker-2 reported DB existing-volume migration path and Service deploy-runner guard/tests in progress; final task completion was not available at this checkpoint. | Treat unresolved details as pending; do not close DB/Service issues until worker-2 reports final verification and PR evidence. |
| QA coordinator | Worker-4 verified open issue/PR state, docs guard, local Front/Presence/Service/DB smoke checks, and Backend recheck after `6179caf`. | Final whole-system QA waits for task #3/#5 completion and PR/check/merge evidence. |

# Contract checkpoint by issue area

## Backend attendance, exam, notice, device, assignment, and PresenceService-facing behavior

- Backend #14 — manual attendance changes must reject empty audit reasons with `ATTENDANCE_REASON_REQUIRED`.
  - Source of truth: [[/01-requirements/req-attendance-presence.md]] records the required reason and audit history contract.
- Backend #15 — exam answer save/submit must respect the effective per-attempt `expires_at` deadline.
  - Source of truth: [[/01-requirements/req-exam-workflow.md]] and [[/04-architecture/exam-workflow-api.md]] define `expires_at` as the stored attempt deadline.
- Backend #21 — `requires_presence` is a real exam policy field.
  - New exams default to `requires_presence=true` for compatibility.
  - When an exam has `requires_presence=false`, Backend must not run the registered-device / presence eligibility start guard for that exam.
  - Professor create/update responses and student/professor exam reads must preserve the stored value.
- Backend #16 — common notices must be included in student notice lists when the student is authorized to read notices.
  - Source of truth: [[/04-architecture/notice-api-contract.md]]. If the response shape changes, update that contract first.
- Backend #17 — deleted device MAC addresses must not permanently block the same student's re-registration.
  - Source of truth: [[/03-conventions/conv-device-registration.md]] and [[/04-architecture/data-model-overview.md]]; deleted rows are historical state, not active ownership blockers.
- Backend #22 — admin dummy-control validation errors from PresenceService must remain client errors instead of being collapsed into generic 500 responses.
  - Source of truth: [[/03-conventions/conv-api-response.md]] and Backend/PresenceService service boundary docs.
- Backend #20 — assignment grading/feedback is not part of the current assignment API unless a new docs-first contract adds grade fields, feedback visibility, grading roles, and migration rules.
  - Source of truth: [[/04-architecture/assignment-workflow-api.md]] and [[/04-architecture/assignment-data-model-addendum.md]].
- Backend #19/#23 — durable assignment attachments are handled through Backend-owned object-storage APIs, not direct Front/Garage access.
  - Source of truth: [[/01-requirements/req-object-storage.md]] and [[/04-architecture/object-storage-architecture.md]].

## Front attendance bundle, restart, and admin scope labels

- Front #20 — student smart-attendance UI must accept the Backend bundle summary shape while preserving compatibility with flat eligibility fields where still returned.
  - A bundle with multiple slots must render as one actionable bundle card, not one independent check-in button per slot.
- Front #19 — professor attendance UI must expose a restart path after a previous session exists or ended; stale ended smart-session timer UI must return to the roster/restart decision path.
- Front #21 — admin management UI must clearly label demo/MVP read-only scope instead of implying full production management coverage.
- Source of truth: [[/01-requirements/req-attendance-presence.md]], [[/01-requirements/req-admin-features.md]], and [[/03-conventions/conv-frontend-experience-design.md]].

## DB existing-volume migration and object metadata

- DB #12 — existing Postgres volumes need an idempotent upgrade path for assignment and object-storage schema additions.
- The migration path must not rely solely on first-run `/docker-entrypoint-initdb.d` initialization when an existing volume is already present.
- The DB contract must preserve object metadata/deletion outbox tables and trigger behavior documented in [[/04-architecture/object-storage-architecture.md]].
- Worker-2 reported a migration path in progress, but final verification was pending at this checkpoint; do not close DB #12 until that evidence is attached.

## Service release readiness, demo deploy runner, nginx/upload limit, and Garage runtime

- Service #4 — release readiness tests must validate the current release manifest/version rather than hard-coded seed versions.
- Service #9 — `deploy-demo` must not assume a GitHub-hosted runner can reach a private demo SSH host; the workflow must either require the appropriate reachable runner/environment or fail with an actionable guard before attempting unreachable SSH.
- Service #10 — Service runtime owns Garage compose/config/bootstrap for local/image/demo modes.
- Backend #18-related nginx/upload contract — edge nginx upload/body and proxy timeouts must not block files below Backend's accepted assignment upload limit.
- Source of truth: [[/03-conventions/conv-release-and-deployment.md]], [[/02-decisions/adr-0011-service-repo-runtime-orchestration.md]], [[/04-architecture/local-runtime-topology.md]], and [[/04-architecture/object-storage-architecture.md]].
- Worker-2 reported Service/DB changes in progress, but final verification was pending at this checkpoint; do not close Service #4/#9/#10 or Backend #18-related upload evidence until that lane completes.

# Verification snapshot

Worker-4 local QA evidence collected before this docs update:

- `docs`: `git pull --ff-only origin main` reported already up to date before branching.
- Docs guard: required-doc checks returned `docs_gap: no` for backend, frontend, db, and presence/runtime categories.
- Backend: after worker-1 commit `6179caf`, `PYTHONPATH=. python3 -m pytest -q` returned `74 passed`.
- Front: previous QA run reported build/lint pass and Playwright e2e pass; worker-3 later reported Front scoped Playwright `11 passed` on commit `5c126f7`.
- PresenceService: `python3 -m pytest -q` returned `8 passed` with known Pydantic alias warnings.
- Service: contract tests returned `10 passed`; compose local/image/demo config rendered successfully before worker-2's final task evidence.
- DB: required init SQL files were present/non-empty and `postgres/tests/object_storage_triggers.sql` existed before worker-2's final task evidence.

# Open merge gates

- No code PRs were open across `docs`, `Front`, `Backend`, `PresenceService`, `Service`, or `DB` when worker-4 checked.
- Final PR/review/check/merge evidence must be collected after the active branches are pushed and CI completes.
- Initial GitHub issues must not be closed solely from this checkpoint; each closure needs the relevant branch/PR/test evidence and a comment linking the docs contract where behavior changed.
