---
title: ADR-0005 PresenceService 는 Redis 에 60초 snapshot 캐시를 둔다
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
  - network-topology
  - presence-eligibility-api
source:
  - 06-meetings/raw/2026-03-30-presence-logic-clarification.md
---

# Context

학생이 출석 버튼이나 시험 시작 버튼을 누를 때마다 OpenWrt 장비에서 전체 station list 를 직접 가져오면 지연과 장비 부하가 커질 수 있다.

# Decision

- PresenceService 는 강의실 단위 또는 AP 단위 snapshot 을 Redis 에 캐시한다.
- snapshot 유효 시간은 60초다.
- Backend 요청 시 PresenceService 는 캐시를 먼저 조회하고, 없거나 만료되었을 때만 OpenWrt 에서 새로 수집한다.
- 수집 실패 시 기본 허용이 아니라 보수적 거부를 기본값으로 둔다.

# Consequences

- 같은 강의실에 대한 짧은 시간 내 반복 요청을 효율적으로 처리할 수 있다.
- 캐시 만료 시 동시 요청 폭주를 막기 위한 refresh lock 이 필요하다.
- Redis 는 성능 최적화 계층이며, 판정 근거 로그는 별도 저장 전략이 필요하다.
