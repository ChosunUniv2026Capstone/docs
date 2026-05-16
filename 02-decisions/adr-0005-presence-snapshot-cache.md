---
title: ADR-0005 PresenceService 는 Redis 에 soft TTL 3초, hard TTL 30초 snapshot 캐시를 둔다
type: decision
status: accepted
updated: 2026-05-16
date: 2026-03-30
deciders:
  - team
supersedes: []
superseded_by: null
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
다만 출석 버튼과 관리자/교수 화면에서 재실성 변화가 너무 늦게 보이면 데모와 실제 운영 모두에서 사용자가 납득하기 어렵다.

# Decision

- PresenceService 는 강의실 단위 또는 AP 단위 snapshot 을 Redis 에 캐시한다.
- snapshot 은 soft TTL `3초`, hard TTL `30초` 를 사용한다.
- snapshot age 가 `3초` 이하이면 fresh 로 보고 즉시 재사용한다.
- snapshot age 가 `3초` 를 초과하고 `30초` 이하이면 stale-while-revalidate 로 재사용할 수 있으며, PresenceService 는 refresh lock 을 획득한 경우에만 OpenWrt 재수집을 시도한다.
- snapshot age 가 `30초` 를 초과하면 hard stale 로 보고 새 수집 없이는 eligibility 근거로 사용하지 않는다.
- Backend 요청 시 PresenceService 는 캐시를 먼저 조회하고, fresh 또는 hard TTL 이내 stale snapshot 이 있으면 OpenWrt 재수집 때문에 요청을 불필요하게 막지 않는다.
- OpenWrt 재수집은 cache key 또는 OpenWrt/AP target 단위 refresh lock 을 반드시 거쳐야 한다.
- refresh lock 이 이미 잡혀 있으면 같은 key 에 대한 중복 SSH / station dump 를 시작하지 않고 기존 snapshot 을 반환하거나 bounded wait 후 결과를 사용한다.
- 수집 실패 시 기본 허용이 아니라 보수적 거부를 기본값으로 둔다. 단, hard TTL 이내 stale snapshot 이 있으면 stale-if-error 정책으로 기존 근거를 반환할 수 있다.

# Consequences

- 같은 강의실에 대한 짧은 시간 내 반복 요청을 효율적으로 처리할 수 있다.
- soft TTL 이후에는 재수집을 빠르게 시도하므로 재실성 변화 반영 지연을 줄일 수 있다.
- refresh lock 이 정상 동작하면 동일 cache key 또는 동일 OpenWrt/AP target 에 대한 OpenWrt 접근은 많아도 약 3초에 1회 수준으로 제한된다.
- 이 제한은 전역 제한이 아니라 key / target 단위 제한이다. 여러 강의실 또는 여러 AP 를 독립적으로 refresh 하면 전체 OpenWrt 접근 수는 AP 수와 매핑 구조에 비례한다.
- 캐시 만료 시 동시 요청 폭주를 막기 위한 refresh lock 이 필수다.
- Redis 는 성능 최적화 계층이며, 판정 근거 로그는 별도 저장 전략이 필요하다.
