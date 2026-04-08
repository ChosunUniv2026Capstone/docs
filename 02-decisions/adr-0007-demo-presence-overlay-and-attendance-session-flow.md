---
title: ADR-0007 더미 재실 제어는 Front 관리자 패널과 PresenceService overlay 로 구성하고 출석은 projected slot session 으로 운영
type: decision
status: accepted
updated: 2026-04-08
date: 2026-04-07
deciders:
  - team
supersedes: []
superseded_by:
  - [[/02-decisions/adr-0009-attendance-bundle-session-parent.md]]
related:
  - [[/01-requirements/req-attendance-presence.md]]
  - [[/03-conventions/conv-service-boundary.md]]
  - [[/03-conventions/conv-auth-and-session.md]]
  - [[/04-architecture/presence-eligibility-api.md]]
  - [[/02-decisions/adr-0009-attendance-bundle-session-parent.md]]
  - [[/04-architecture/attendance-workflow-architecture.md]]
  - [[/04-architecture/data-model-overview.md]]
source:
  - [[/06-meetings/raw/2026-04-07-capstone-demo-planning.md]]
---

# Context

캡스톤 시연에서는 관리자 화면에서 재실 입력값을 조작해 학생 eligibility 결과가 자연스럽게 바뀌는 장면과,
그 결과가 교수의 출석 세션 운영과 학생 self check-in 에 연결되는 흐름을 보여줘야 한다.

현재 워크스페이스는 다음 특징을 가진다.

- `Front` 는 학생 eligibility UI 와 관리자 대시보드 / classroom-network surface 를 이미 가지고 있다.
- `Backend` 는 generic attendance eligibility endpoint 를 가지고 있으나 현재 wall-clock schedule gate 에 묶여 있다.
- `PresenceService` 는 baseline dummy snapshot + Redis cache 구조이며 별도 웹 UI 는 없다.
- DB 에 attendance session / audit model 은 아직 없다.

# Decision

- 별도 PresenceService 웹 UI 는 만들지 않는다.
- 더미 재실 제어는 `Front` 관리자 대시보드 안의 demo-mode 전용 패널로 제공한다.
- 더미 제어의 실제 상태 소유는 `PresenceService` 가 가진다.
  - baseline fixture 는 immutable JSON 으로 둔다.
  - mutable state 는 classroom-scoped Redis overlay 로 둔다.
  - effective snapshot merge 와 read-after-write 보장은 PresenceService 가 소유한다.
- generic student eligibility path 는 Branch 1 에서 기존 공식을 유지한다.
- 출석은 generic eligibility endpoint 자체를 그대로 재사용하지 않고,
  `projected slot -> open session -> live presence` 규칙을 가진 attendance-specific Backend path 로 처리한다.
- projected slot 은 기존 시간표 window 를 30분 단위 full segment 로 분해한 결과만 허용한다.
- 학생 self check-in 은 idempotent 하며, 같은 열린 세션의 성공 재시도는 중복 audit row 를 만들지 않는다.
- attendance final state authority 는 Backend 가 가진다.
- professor / student / report realtime 동기화는 Backend attendance event stream 이 소유한다.
- professor override 는 최신 final state 를 덮어쓰되, 이전 self check-in / manual update 이력은 삭제하지 않는다.

# Consequences

- Branch 1 은 관리자 overlay 제어와 학생 eligibility 재확인 흐름을 빠르게 시연할 수 있다.
- Branch 2 는 교수 출석 세션과 학생 self check-in 을 canonical projected-slot identity(`projection_key`) 를 유지한 채 관리할 수 있다.
- 출석 session lifecycle / route / membership 모델의 세부 구조는 후속 ADR-0009 가 refine 한다.
- 이 ADR 은 PresenceService overlay 경계, attendance final-state authority, Backend realtime ownership 결정을 계속 소유한다.
- 기존 legacy endpoint 는 payload/path 를 급격히 깨지 않고도 auth helper hardening 을 적용할 수 있다.
- demo tuple seed/reset 절차가 반드시 필요하다.
- attendance report/dashboard 는 Backend final state 기준 집계를 실시간으로 표시해야 한다.
