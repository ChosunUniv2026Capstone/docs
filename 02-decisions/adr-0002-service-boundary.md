---
title: ADR-0002 서비스 경계는 Front / Backend / PresenceService / DB 로 분리
type: decision
status: accepted
updated: 2026-03-30
date: 2026-03-30
deciders:
  - team
supersedes: []
superseded_by: null
related:
  - conv-service-boundary
  - service-map
source:
  - 06-meetings/raw/2026-03-19-capstone-proposal.md
  - 06-meetings/raw/2026-03-25-kickoff-work-items.md
---

# Context

LMS 기능과 재실성 판별 로직은 책임이 다르며, 문서와 저장소도 분리 운영하기로 했다.

# Decision

- `Front` 는 학생 / 교수 / 관리자 UI 를 담당한다.
- `Backend` 는 LMS 도메인, 수업 / 과제 / 시험 / 출석 API 와 최종 도메인 판단을 담당한다.
- `PresenceService` 는 Wi-Fi / OpenWrt / 게이트웨이 기반 재실성 판단 보조를 담당한다.
- `DB` 는 스키마, 마이그레이션, 데이터 계약을 담당한다.
- `docs` 는 요구사항과 규약의 source of truth 를 담당한다.

# Consequences

- Front 에 비즈니스 판정 로직을 두지 않는다.
- PresenceService 책임을 Backend 내부에서 중복 구현하지 않는다.
- 스키마 변경은 DB 와 docs 를 먼저 갱신해야 한다.
