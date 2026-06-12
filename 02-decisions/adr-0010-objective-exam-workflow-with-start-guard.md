---
title: ADR-0010 Objective Exam Workflow With Start Guard
type: decision
status: accepted
updated: 2026-04-09
date: 2026-04-09
deciders:
  - team
supersedes: []
superseded_by: null
related:
  - [[/01-requirements/req-exam-workflow.md]]
  - [[/01-requirements/req-attendance-presence.md]]
  - [[/02-decisions/adr-0004-attendance-authorization-flow.md]]
  - [[/04-architecture/presence-eligibility-api.md]]
  - [[/04-architecture/exam-workflow-api.md]]
source:
  - 2026-04-09 local alignment with dd exam workflow
---

# Context

The exam feature now exists in the local workspace, but professor operation flow and student attempt flow need one shared rule set so Front, Backend, and DB do not drift apart.
The exam domain also reuses the same eligibility guard family as attendance.

# Decision

- Exams are implemented as separate LMS entities with `draft`, `published`, `open`, and `closed` operational states.
- The current local authoring UI focuses on objective questions first.
- Students can start an attempt only after pressing the explicit start action.
- Professors can edit exams only while the exam is in `draft`.
- The local exam policy checks both active registered-device ownership and course-classroom PresenceService eligibility at exam start time.
- The system does not require a second presence check during answer save or submit.
- Student submit uses stored answers and computes the attempt score at finalization time for objective questions.
- Professor exam detail can expose latest-attempt status per enrolled student for operational monitoring.

# Consequences

- Front needs a dedicated exam route and student take page.
- Backend needs professor CRUD, publish/close, student list/detail/start/save/submit APIs.
- DB needs exam, question, option, submission, and answer entities with strict integrity.
- The professor and student screens can evolve visually later without changing the exam route and lifecycle contract.
