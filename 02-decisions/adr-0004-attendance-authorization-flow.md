---
title: ADR-0004 출석 최종 판정은 Backend 가 하고 PresenceService 는 판정 근거를 제공
type: decision
status: accepted
updated: 2026-03-30
date: 2026-03-30
deciders:
  - team
supersedes: []
superseded_by: null
related:
  - req-attendance-presence
  - req-device-auth
  - conv-service-boundary
  - service-map
  - adr-0005-presence-snapshot-cache
source:
  - 06-meetings/raw/2026-03-19-capstone-proposal.md
  - 06-meetings/raw/2026-03-30-presence-logic-clarification.md
---

# Context

출석 판정에는 수업 시간표, 수강 정보, 강의실, 네트워크 기반 재실성, 등록 단말 여부가 함께 필요하다.

# Decision

- `PresenceService` 는 네트워크와 단말 정보를 바탕으로 재실성 판정 근거와 상태를 제공한다.
- `Backend` 는 수강 정보와 시간표, 강의실 정보, PresenceService 결과를 결합해 출석 또는 시험 허용 여부를 최종 판단한다.
- `Backend` 는 `purpose=attendance|exam` 값을 포함해 PresenceService 에 eligibility 검사를 요청할 수 있다.
- 출석 또는 시험 거부 시 Backend 는 사용자에게 전달 가능한 사유 코드를 반환한다.

# Consequences

- LMS 도메인 규칙은 Backend 가 소유한다.
- 네트워크 판정 규칙은 PresenceService 가 소유한다.
- 출석과 시험은 같은 eligibility 가드를 공유하되 목적별 추가 정책은 Backend 에서 분기할 수 있다.
