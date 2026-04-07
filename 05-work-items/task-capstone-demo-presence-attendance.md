---
title: 캡스톤 데모 재실 + 출석 구현
type: task
status: doing
updated: 2026-04-07
owners:
  - team
related:
  - [[/05-work-items/epic-full-lms-delivery-plan.md]]
  - [[/01-requirements/req-attendance-presence.md]]
  - [[/04-architecture/attendance-workflow-architecture.md]]
  - [[/07-status/implementation-roadmap.md]]
source:
  - [[/06-meetings/raw/2026-04-07-capstone-demo-planning.md]]
---

# 목표

캡스톤 시연에서 아래 두 장면을 끊김 없이 보여줄 수 있도록 구현한다.

1. 관리자 대시보드에서 더미 재실 입력값을 조작하면 학생 eligibility 결과가 자연스럽게 바뀐다.
2. 교수가 projected slot 기반으로 출석 세션을 열고, 학생이 self check-in 하며, 이후 교수 수정 이력이 남는다.

# 구현 순서

## Branch 1 — Presence demo

- 관리자 대시보드 안의 demo-mode presence control panel
- baseline + overlay + effective snapshot merge
- classroom-scoped read-after-write 보장
- 학생 generic eligibility 재확인 흐름 검증

## Branch 2 — Attendance demo

- shared slot projection service
- projected slot 기반 session open/close
- student self check-in
- attendance record / audit log
- professor roster / history UI

# 완료 기준

- pinned demo tuple 이 seed/reset 가능하다.
- Branch 1 에서 eligibility 결과 변화가 시연 가능하다.
- Branch 2 에서 projected slot -> open session -> live presence -> self check-in 흐름이 동작한다.
- self check-in retry 는 idempotent 하다.
- audit history 에 self / professor transition 이 모두 보인다.
