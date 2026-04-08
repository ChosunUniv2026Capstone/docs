---
title: 출석 데모 seed / reset 절차
type: architecture
status: active
updated: 2026-04-07
owners:
  - db-owner
  - backend-team
related:
  - [[/04-architecture/attendance-workflow-architecture.md]]
  - [[/04-architecture/data-model-overview.md]]
  - [[/01-requirements/req-attendance-presence.md]]
source:
  - [[/.omx/plans/attendance-ui-realtime-consensus-draft-20260407.md]]
---

# 목적

출석 UI + realtime 데모를 반복 가능한 같은 데이터로 검증하기 위한 pinned demo tuple 과 reset 기준을 정의한다.

# pinned demo tuple

- 관리자: `ADM001`
- 교수: `PRF002`
- 학생: `20201239` (`Kim Student 06`)
- 강의: `CSE116`
- 강의실: `B101`
- 대표 단말 MAC: `52:54:00:12:34:56`
- CSE116 weekly fixed pattern: `월 15:00~17:00` + `수 12:00~13:00` = 주 6차시

# reset 기준

- `users`, `courses`, `course_enrollments`, `course_schedules`, `classrooms`, `classroom_networks`, `registered_devices` seed 는 `DB/postgres/init/010_seed.sql` 기준 truth 를 유지한다.
- 출석 sample seed 는 `DB/postgres/init/012_attendance_demo_seed.sql` 이 소유한다.
- hard reset 으로 demo baseline 을 복구할 때는 postgres volume 을 재생성해 init script 전체를 다시 실행해야 한다.
- Presence overlay reset 은 기존 PresenceService admin reset endpoint 를 사용한다.

# 수동 reset 절차

1. `docker compose down -v`
2. `docker compose up -d`
3. Presence overlay reset
4. 프론트 새로고침
5. 교수 `PRF002` 로 `CSE116` attendance tab 진입
6. 학생 `20201239` 로 smart session 진입 확인

# 기대 결과

- 교수 타임라인에는 baseline sample attendance 가 보인다.
  - 2026-03-09 smart session + override history
  - 2026-03-16 canceled slot
  - 2026-03-23 manual attendance sample
- 학생은 기본 seed 상태에서 열린 smart session 이 없으면 버튼이 비활성화된 상태를 본다.
- professor open -> student check-in -> professor override 시나리오를 seeded historical data 와 별개로 동일 tuple 에서 반복 검증할 수 있다.
