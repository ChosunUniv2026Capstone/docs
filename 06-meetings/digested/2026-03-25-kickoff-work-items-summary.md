---
title: 킥오프 작업 분해 요약
type: meeting-summary
status: active
updated: 2026-03-25
owners:
  - team
related:
  - task-openwrt-gateway-prototype
  - task-lms-feature-survey
source:
  - 06-meetings/raw/2026-03-25-kickoff-work-items.md
participants:
  - 심재혁
  - 박준완
---

# 회의 목적

초기 작업 항목과 조사 범위를 빠르게 분해한다.

# 핵심 결정

- OpenWrt 게이트웨이 구조에서 단말 목록 수집 검토를 우선 착수한다.
- LMS 기능 조사는 학생 / 교수 / 관리자 관점으로 나눠 진행한다.
- 깃허브 조직은 Front, Backend, PresenceService, DB, docs 레포 구조로 정리한다.

# 새 요구사항

- 학생 기능 목록을 기준으로 Front 와 Backend 의 MVP 범위를 정리해야 한다.
- 교수와 관리자 기능은 운영 도구 관점에서 별도 요구사항 문서화가 필요하다.

# 새 규약

- 문서화를 별도 레포에서 관리한다.
- 기능 조사는 역할 기반 분류를 유지한다.

# 작업 항목 / 담당자 / 기한

- `task-openwrt-gateway-prototype`: OpenWrt 기반 단말 목록 수집 구조 검토 / 담당 미정
- `task-lms-feature-survey`: LMS 기능 조사 / 심재혁, 박준완 / 금요일

# 리스크

- 역할별 기능 조사 결과가 정리되기 전 구현이 앞서 나갈 수 있다.
- 프론트와 백엔드의 경계가 문서 없이 섞일 수 있다.

# 오픈 질문

- 관리자 기능의 상세 범위를 어디까지 둘 것인가
- 수강신청 기능을 이번 프로토타입 MVP 에 포함할 것인가

# source

- `06-meetings/raw/2026-03-25-kickoff-work-items.md`
