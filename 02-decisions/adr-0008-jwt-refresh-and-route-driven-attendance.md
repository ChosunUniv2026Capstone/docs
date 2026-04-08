---
title: ADR-0008 표준 JWT refresh 구조와 route-driven attendance page flow 를 채택한다
type: decision
status: accepted
updated: 2026-04-08
date: 2026-04-07
deciders:
  - team
supersedes: []
superseded_by: null
related:
  - [[/03-conventions/conv-auth-and-session.md]]
  - [[/03-conventions/conv-api-response.md]]
  - [[/04-architecture/service-map.md]]
  - [[/01-requirements/req-student-features.md]]
  - [[/01-requirements/req-professor-features.md]]
source:
  - [[/06-meetings/raw/2026-04-07-capstone-demo-planning.md]]
  - [[/07-status/2026-04-02-workspace-analysis-report.md]]
---

# Context

현재 Front 는 path/router 와 세션 복구 구조가 없고, Backend 는 `dev-token:<login_id>` 기반 임시 인증을 사용한다.
사용자는 정석적인 JWT 구조와 새로고침/뒤로가기/앞으로가기까지 되는 route-driven attendance flow 를 요구했다.

# Decision

- 인증은 `short-lived access token + HttpOnly refresh cookie` 구조로 전환한다.
- refresh token 은 Front JavaScript 에 노출하지 않는다.
- Front 는 route 기반으로 attendance flow 를 구성한다.
  - 일반출석 → roster page
  - 스마트출석 → timer/control page → roster page
- 학생은 자신의 수강 강의 route 만 접근 가능해야 한다.
- 교수는 자신의 담당 강의 route 만 접근 가능해야 한다.
- route 복구는 로그인 복구와 별개이며, attendance/exam 접근 권한은 항상 별도 도메인 검증을 거친다.
- rollout 은 compatibility-gated 로 진행하고 demo-critical legacy route 는 증거가 확보될 때까지 유지한다.

# Consequences

- Backend 에 refresh / logout / bootstrap 계약과 refresh-token durability 가 필요하다.
- Front 에 router, guarded route, restore flow 가 필요하다.
- CORS / credentials / cookie behavior 를 로컬/운영 모두 명시해야 한다.
- auth / routing / attendance regression 테스트가 대폭 늘어난다.
