---
title: 2026-04-07 캡스톤 데모 구현 계획 메모
type: meeting
status: active
updated: 2026-04-07
owners:
  - team
related:
  - [[/05-work-items/task-capstone-demo-presence-attendance.md]]
  - [[/04-architecture/attendance-workflow-architecture.md]]
---

# 배경

캡스톤 시연에서 학생 / 교수 / 관리자 흐름을 한 번에 보여주기 위해,
기존 학사 조회 MVP 위에 재실 시연과 출석 세션 흐름을 연결하는 실행 계획을 정리했다.

# 합의 요점

- 구현 순서는 `재실 브랜치 -> 출석 브랜치` 로 진행한다.
- 더미 재실 제어는 별도 PresenceService UI 가 아니라 Front 관리자 대시보드 안에 넣는다.
- 더미 제어는 결과 override 가 아니라 AP / 연결 상태 / 단말 관측 상태 같은 입력값을 조작하는 방식으로 한다.
- 학생 generic eligibility 화면은 Branch 1 에서 기존 공식을 유지한다.
- 교수는 projected slot 기반으로 출석 세션을 열 수 있어야 한다.
- 학생 출석 성공 조건은 `open session + live eligible` 이다.
- 학생 self check-in 은 idempotent 해야 한다.
- 교수 수동 수정과 학생 최초 self check-in 은 모두 audit history 로 남긴다.
- demo tuple 은 `ADM001 / PRF002 / 20201239 / CSE116 / B101 / 52:54:00:12:34:56` 를 기본으로 한다.
- demo day 에는 `CSE116/B101` 이 active 30분 window 로 보이도록 seed/reset 절차가 필요하다.
