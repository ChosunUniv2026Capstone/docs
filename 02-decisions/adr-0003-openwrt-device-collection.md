---
title: ADR-0003 OpenWrt 게이트웨이 구조를 단말 정보 수집 경로로 채택
type: decision
status: accepted
updated: 2026-03-30
date: 2026-03-30
deciders:
  - team
supersedes: []
superseded_by: null
related:
  - [[/01-requirements/req-attendance-presence.md]]
  - [[/01-requirements/req-device-auth.md]]
  - [[/02-decisions/adr-0005-presence-snapshot-cache.md]]
  - [[/04-architecture/network-topology.md]]
source:
  - [[/06-meetings/raw/2026-03-19-capstone-proposal.md]]
  - [[/06-meetings/raw/2026-03-25-kickoff-work-items.md]]
  - [[/06-meetings/raw/2026-03-30-presence-logic-clarification.md]]
---

# Context

재실성 기반 출석을 위해 강의실 인접 네트워크와 연결된 단말 정보를 수집할 수 있는 경로가 필요하다.

# Decision

강의실별 AP / 게이트웨이 환경에 OpenWrt 기반 장비를 두고, 해당 장비 또는 연계 게이트웨이에서 단말 연결 정보를 수집하는 구조를 우선 채택한다.
수집 방식은 PresenceService 가 요청 시 SSH 기반으로 OpenWrt 장비에 접속해 단말 목록을 조회하는 형태를 우선한다.

# Consequences

- PresenceService 는 OpenWrt 또는 게이트웨이에서 들어오는 단말 연결 정보를 처리할 수 있어야 한다.
- OpenWrt 장비는 상단 공유기 내부 대역의 static IP 와 SSH 접근이 가능해야 한다.
- PresenceService 는 `iw dev`, `iwinfo`, `station dump`, `ubus` 계열 명령 결과를 파싱할 수 있어야 한다.
- 실제 수집 가능한 필드와 정확도는 테스트베드 검증이 필요하다.
- 장비 구성과 네트워크 토폴로지는 architecture 문서로 함께 관리한다.
