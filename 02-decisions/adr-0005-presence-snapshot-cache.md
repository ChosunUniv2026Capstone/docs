---
title: ADR-0005 PresenceService 는 Redis 에 60초 snapshot 캐시를 둔다
type: decision
status: accepted
updated: 2026-05-16
date: 2026-03-30
deciders:
  - team
supersedes: []
superseded_by: [[/02-decisions/adr-0013-openwrt-local-collector-push.md]]
related:
  - [[/01-requirements/req-attendance-presence.md]]
  - [[/01-requirements/req-device-auth.md]]
  - [[/04-architecture/network-topology.md]]
  - [[/04-architecture/presence-eligibility-api.md]]
source:
  - [[/06-meetings/raw/2026-03-30-presence-logic-clarification.md]]
---

# Context

학생이 출석 버튼이나 시험 시작 버튼을 누를 때마다 OpenWrt 장비에서 전체 station list 를 직접 가져오면 지연과 장비 부하가 커질 수 있다.

# Decision

> 2026-05-16 현재 routine OpenWrt data path 는 [[/02-decisions/adr-0013-openwrt-local-collector-push.md]] 가 supersede 한다. 이 ADR 은 Redis snapshot 계층을 둔다는 역사적 결정과 demo/cache 내부 원칙을 설명한다. Backend/user-triggered 요청이 Redis miss 를 이유로 OpenWrt SSH/pull 수집을 시작하는 방식은 더 이상 현재 routine 설계가 아니다.

- PresenceService 는 강의실 단위 또는 AP 단위 snapshot 을 Redis 에 저장한다.
- 실제 OpenWrt snapshot 은 AP local collector push 로 갱신된다.
- demo source 는 demo baseline/overlay snapshot 을 사용할 수 있지만 real collector snapshot 과 구분해야 한다.
- 수집 실패 또는 collector heartbeat 만료 시 기본 허용이 아니라 보수적 거부를 기본값으로 둔다.

# Consequences

- 같은 강의실에 대한 짧은 시간 내 반복 요청을 효율적으로 처리할 수 있다.
- collector-push 구조에서는 Redis miss 가 OpenWrt pull fan-out 으로 이어지지 않으므로 OpenWrt 부하가 사용자 요청 수에 직접 비례하지 않는다.
- Redis 는 최신 snapshot/health 전달 계층이며, 판정 근거 로그는 별도 저장 전략이 필요하다.
