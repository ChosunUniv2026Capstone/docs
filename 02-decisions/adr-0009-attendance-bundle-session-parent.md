---
title: ADR-0009 출석은 bundle parent session + slot fan-out persistence 로 운영한다
type: decision
status: accepted
updated: 2026-04-08
date: 2026-04-08
deciders:
  - team
supersedes: []
superseded_by: null
related:
  - [[/01-requirements/req-attendance-presence.md]]
  - [[/01-requirements/req-professor-features.md]]
  - [[/01-requirements/req-student-features.md]]
  - [[/02-decisions/adr-0007-demo-presence-overlay-and-attendance-session-flow.md]]
  - [[/04-architecture/attendance-workflow-architecture.md]]
  - [[/04-architecture/data-model-overview.md]]
source:
  - [[/06-meetings/raw/2026-04-07-capstone-demo-planning.md]]
  - [[/02-decisions/adr-0007-demo-presence-overlay-and-attendance-session-flow.md]]
  - [[/05-work-items/task-capstone-demo-presence-attendance.md]]
---

# Context

현재 multi-slot 출석은 projection-key 별 session fan-out 구조에 가깝다.
이 구조는 교수 화면에서 여러 타이머/close 대상으로 보이기 쉽고, 학생에게도 차시별 카드/버튼을 강요해 조작 실수와 realtime drift 위험을 만든다.

반면 학사 기록과 감사 추적은 여전히 차시별 truth 를 유지해야 한다.
따라서 UX 와 lifecycle 은 bundle 단위로 단순화하되, 저장과 audit 은 slot 단위 무결성을 유지하는 결정을 분리해 문서화해야 한다.
이 ADR 은 ADR-0007 이 고정한 presence overlay / Backend final-state authority 결정은 유지하고,
출석 session lifecycle / route / persistence model 만 bundle parent 기준으로 refine 한다.

# Decision

- 교수/학생이 사용하는 출석 lifecycle authority 는 **bundle parent session 1개**다.
- 기존 `attendance_sessions` 를 재사용해 bundle parent 를 표현한다.
  - `projection_key` 는 bundle anchor slot identity 로 유지한다.
  - 공통 mode/status/timer/close/expire/reopen authority 는 parent session 이 소유한다.
- 선택된 slot 집합은 별도 membership (`attendance_session_slots`) 으로 저장한다.
- 교수/학생 API 와 route 는 parent `session_id` 기준으로 bundle 을 다룬다.
- smart bundle 은 차시 수와 무관하게 shared 10분 타이머 1개만 사용한다.
- 학생은 bundle 카드 1개와 check-in 버튼 1개만 본다.
- 학생 bundle check-in 과 교수 bundle overwrite 는 내부적으로 slot fan-out write 로 저장한다.
- `attendance_records` 와 `attendance_status_audit_logs` 는 slot identity(`projection_key`) 를 포함한 per-slot persistence 를 유지한다.
- bundle overwrite / bundle check-in 은 실제 값이 바뀐 slot 에만 changed-only audit row 를 남긴다.
- bundle roster 기본값은 anchor slot record 를 기준으로 하며, anchor slot 기록이 없으면 `absent` 를 기본값으로 사용한다.
- bundle 화면은 bulk overwrite 도구이고, 개별 차시 예외 수정은 기존 per-slot route 를 유지한다.
- report / aggregate / timeline 은 bundle metadata 가 아니라 per-slot attendance record final state 를 기준으로 계산한다.

# Consequences

- Backend / DB 는 parent session + slot membership + slot-aware record/audit 구조로 재설계되어야 한다.
- Front 는 professor timer/roster 와 student attendance card 를 bundle session 기준 route 로 옮겨야 한다.
- websocket bootstrap / incremental event 는 `session_id + projection_keys[]` 를 포함하는 bundle-aware payload 로 바뀌어야 한다.
- bundle close / expire 는 professor/student timer 와 report surface 에 즉시 전파되어야 한다.
- legacy per-slot route 는 예외 수정 경로로만 유지하고, fan-out 기반 multi-session UX 가 기본 경로로 남아 있으면 안 된다.
