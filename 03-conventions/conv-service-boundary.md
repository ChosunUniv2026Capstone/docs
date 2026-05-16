---
title: 서비스 경계 규약
type: convention
status: active
updated: 2026-05-16
owners:
  - architecture-owner
applies_to:
  - frontend
  - backend
  - presence
  - db
related:
  - [[/02-decisions/adr-0002-service-boundary.md]]
  - [[/02-decisions/adr-0004-attendance-authorization-flow.md]]
  - [[/04-architecture/service-map.md]]
source:
  - [[/06-meetings/raw/2026-03-19-capstone-proposal.md]]
---

# Front

- 학생 / 교수 / 관리자 웹 UI 소유
- 비즈니스 최종 판정 로직 소유 금지

# Backend

- LMS 도메인, 수업 / 과제 / 시험 / 출석 API 소유
- 출석과 시험의 최종 도메인 판단 소유
- AP registry/token lifecycle API 소유

# PresenceService

- Wi-Fi / OpenWrt / 게이트웨이 기반 재실성 판단 보조 소유
- OpenWrt collector ingestion, AP health, 단말 연결 snapshot 처리와 판정 근거 생성 소유
- Backend/DB canonical AP registry 를 cache/read 하되 collector-supplied classroom mapping 을 신뢰하지 않음

# DB

- 스키마, 마이그레이션, 롤백, 데이터 계약 소유

# 규칙

- Front 는 Backend / PresenceService 의 판정 결과를 소비한다.
- Backend 는 PresenceService 책임을 중복 구현하지 않는다.
- 서비스 경계 변경은 docs 와 ADR 갱신이 선행되어야 한다.

# OpenWrt collector boundary

- OpenWrt collector 는 AP local client state 를 push 하는 data-plane agent 이며 LMS domain rule 을 소유하지 않는다.
- Backend 는 AP token 을 발급/회전/폐기하지만 station matching 을 구현하지 않는다.
- PresenceService 는 AP_OFFLINE 과 network/device eligibility evidence 를 반환하지만 수강/시간표/세션 최종 권한을 갖지 않는다.
- Front 는 Backend 응답의 reason/status 를 표시하며 AP 상태를 직접 추론하지 않는다.
