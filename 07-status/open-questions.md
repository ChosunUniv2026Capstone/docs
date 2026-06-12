---
title: 오픈 질문
type: status
status: active
updated: 2026-05-16
owners:
  - team
related:
  - [[/01-requirements/req-attendance-presence.md]]
  - [[/01-requirements/req-device-auth.md]]
  - [[/02-decisions/adr-0004-attendance-authorization-flow.md]]
  - [[/02-decisions/adr-0005-presence-snapshot-cache.md]]
  - [[/04-architecture/exam-workflow-api.md]]
  - [[/04-architecture/exam-mvp-contract.md]]
source:
  - [[/06-meetings/raw/2026-03-19-capstone-proposal.md]]
  - [[/06-meetings/raw/2026-03-25-kickoff-work-items.md]]
  - [[/06-meetings/raw/2026-03-30-presence-logic-clarification.md]]
  - [[/06-meetings/raw/2026-04-08-openwrt-setup-and-station-inspection.md]]
  - [[/06-meetings/raw/2026-04-09-openwrt-ap-mode-dhcp-clarification.md]]
  - current code/test audit, 2026-04-25
---

# 2026-04-25

## 아직 열려 있는 질문

- 실제 교내 Wi-Fi 환경에서 안정적으로 사용할 수 있는 식별자와 수집 범위는 어디까지인가?
  - 데모 AP 3대는 collector push 와 Redis collector snapshot 경로로 연결됐지만, 교내/장기 운영 AP 모델별 station 정보 안정성은 별도 검증이 필요하다.
- OpenWrt collector push 실패 시 재시도와 fail-close 정책을 어느 수준까지 둘 것인가?
  - 현재 로컬 MVP는 PresenceService eligibility 응답과 Backend 최종 판단 경계를 유지한다.
  - 운영 정책 수준의 retry/backoff/fail-close 기준은 아직 확정되지 않았다.
- 수강신청 기능을 프로토타입 MVP 범위에 포함할 것인가?
  - 현재 DB seed/enrollment 기반 조회와 출석/시험 흐름은 구현되어 있으나, 수강신청 자체는 후속 범위다.
- 관리자 기능의 후속 범위와 우선순위는 어떻게 정할 것인가?
  - 현재 구현 범위는 사용자/강의실/AP 매핑 조회, AP threshold patch, demo presence overlay/reset 중심이다.
  - 운영 지표, 권한 관리, 감사 화면 등은 후속 범위로 남아 있다.

## 해결되었거나 재분류된 질문

- 시험 접근 제어에 재실성 조건을 어디까지 적용할 것인가?
  - 해결: `requires_presence=true` 시험 start guard 는 active registered device 와 `purpose=exam` PresenceService eligibility 를 함께 요구한다.
  - 운영/demo 환경 모두 설정된 presence source 를 따르며, `demo` evidence 는 collector evidence 와 같은 eligibility 지위를 가진다.
