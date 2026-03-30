---
title: 네트워크 토폴로지 개요
type: architecture
status: active
updated: 2026-03-30
owners:
  - presence-team
related:
  - [[/02-decisions/adr-0003-openwrt-device-collection.md]]
  - [[/02-decisions/adr-0005-presence-snapshot-cache.md]]
  - [[/01-requirements/req-attendance-presence.md]]
source:
  - [[/06-meetings/raw/2026-03-19-capstone-proposal.md]]
  - [[/06-meetings/raw/2026-03-25-kickoff-work-items.md]]
  - [[/06-meetings/raw/2026-03-30-presence-logic-clarification.md]]
---

# 목표

강의실별 Wi-Fi 환경과 연결 단말 정보를 수집해 재실성 판정에 활용할 수 있는 테스트베드 구조를 정의한다.

# 구성 요소

- 강의실
- 강의실별 AP 또는 공유기
- OpenWrt 기반 게이트웨이 또는 연계 장비
- 학생 단말
- PresenceService
- Redis
- Backend

# 데이터 흐름

1. 학생 단말이 강의실 네트워크에 연결된다.
2. Backend 가 출석 또는 시험 접근 시 PresenceService 에 eligibility 확인을 요청한다.
3. PresenceService 는 강의실 매핑 기준으로 Redis 의 60초 이내 snapshot 을 먼저 조회한다.
4. snapshot 이 없거나 만료되었으면 PresenceService 가 OpenWrt 장비에 SSH 로 접속해 station list 를 수집한다.
5. 수집 결과는 Redis 에 저장된다.
6. PresenceService 는 강의실 / Wi-Fi / 단말 매칭 결과를 만든다.
7. Backend 는 이를 수강 정보와 시간표와 결합해 최종 판단한다.

# 주의점

- 실제로 어떤 단말 식별자가 수집 가능한지는 테스트베드 검증이 필요하다.
- 교내 네트워크 정책과 장비 배치 제약을 별도 확인해야 한다.
- 강의실과 Wi-Fi 매핑 정보는 운영 데이터로 관리해야 한다.
- 강의실은 여러 AP 와 매핑될 수 있다.
- 캐시가 만료된 시점의 동시 요청 폭주를 막기 위한 lock 전략이 필요하다.
