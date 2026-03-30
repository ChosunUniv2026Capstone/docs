---
title: 서비스 맵
type: architecture
status: active
updated: 2026-03-30
owners:
  - architecture-owner
related:
  - [[/02-decisions/adr-0002-service-boundary.md]]
  - [[/02-decisions/adr-0004-attendance-authorization-flow.md]]
  - [[/02-decisions/adr-0005-presence-snapshot-cache.md]]
  - [[/01-requirements/req-student-features.md]]
  - [[/04-architecture/local-runtime-topology.md]]
source:
  - [[/06-meetings/raw/2026-03-19-capstone-proposal.md]]
  - [[/06-meetings/raw/2026-03-25-kickoff-work-items.md]]
  - [[/06-meetings/raw/2026-03-30-presence-logic-clarification.md]]
---

# 서비스 구성

- `Front`
  - 학생 / 교수 / 관리자 웹 UI
- `Backend`
  - 사용자, 강의, 과제, 시험, 공지, 출석 API
- `PresenceService`
  - 재실성 판정 보조, 단말 연결 정보 처리, Redis snapshot 캐시 관리
- `DB`
  - 스키마, 마이그레이션, 데이터 계약
- `docs`
  - 요구사항, ADR, 규약, 회의록
- `CodexKit`
  - 로컬 Docker Compose 와 온보딩 스크립트

# 기본 상호작용

1. 사용자는 Front 를 통해 로그인하고 LMS 기능을 사용한다.
2. Front 는 LMS 도메인 요청을 Backend 로 전달한다.
3. 출석 또는 시험 접근 시 Backend 는 PresenceService 에 `purpose` 포함 eligibility 판정을 요청한다.
4. PresenceService 는 Redis 의 최근 snapshot 을 재사용하거나, 없으면 OpenWrt 에 요청해 새로 수집한다.
5. Backend 는 시간표, 강의실, 수강 정보, PresenceService 결과를 결합해 최종 판단한다.
6. Backend 와 PresenceService 는 필요한 데이터를 DB 또는 해당 데이터 소스에 반영한다.

# 경계 요약

- Front 는 판정 결과를 소비한다.
- Backend 는 최종 도메인 판단을 한다.
- PresenceService 는 네트워크 / 단말 판정 근거를 제공한다.
- DB 는 저장 구조와 변경 이력을 관리한다.
