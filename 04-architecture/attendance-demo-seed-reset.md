---
title: 출석 데모 seed / reset 절차
type: architecture
status: active
updated: 2026-04-26
owners:
  - db-owner
  - backend-team
related:
  - [[/04-architecture/attendance-workflow-architecture.md]]
  - [[/04-architecture/data-model-overview.md]]
  - [[/01-requirements/req-attendance-presence.md]]
source:
  - [[/06-meetings/raw/2026-04-07-capstone-demo-planning.md]]
  - [[/02-decisions/adr-0007-demo-presence-overlay-and-attendance-session-flow.md]]
  - [[/05-work-items/task-capstone-demo-presence-attendance.md]]
  - [[/02-decisions/adr-0011-service-repo-runtime-orchestration.md]]
  - [[/03-conventions/conv-release-and-deployment.md]]
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
- hard reset 으로 demo baseline 을 복구할 때는 `Service` compose project 의 postgres volume 을 재생성해 init script 전체를 다시 실행해야 한다.
- Service manifest 에서 `components.db.resetRequired: true` 이고 DB image digest 가 바뀐 demo deploy 는 `reset_demo_data=true` 입력 없이는 진행하지 않는다.
- reset script 는 Service project name 으로 생성된 DB volume 만 제거해야 하며, 임의 Docker volume 제거는 금지한다.
- Presence overlay reset 은 기존 PresenceService admin reset endpoint 를 사용한다.

# 수동 reset 절차

1. `cd ../Service`
2. local source mode 에서는 `scripts/up-local.sh` 로 stack 을 실행한다.
3. image/demo mode 에서는 release manifest 를 확인한 뒤 `scripts/deploy-demo.sh --service-version vX.Y.Z --reset-demo-data` 처럼 reset 의도를 명시한다.
4. hard reset 이 필요한 수동 로컬 검증에서는 Service compose project 의 postgres volume 만 제거하고 stack 을 다시 실행한다.
5. Presence overlay reset
6. 프론트 새로고침
7. 교수 `PRF002` 로 `CSE116` attendance tab 진입
8. 학생 `20201239` 로 smart session 진입 확인

# 기대 결과

- 교수 타임라인에는 baseline sample attendance 가 보인다.
  - 2026-03-09 smart session + override history
  - 2026-03-16 canceled slot
  - 2026-03-23 manual attendance sample
- 학생은 기본 seed 상태에서 열린 smart session 이 없으면 버튼이 비활성화된 상태를 본다.
- professor open -> student check-in -> professor override 시나리오를 seeded historical data 와 별개로 동일 tuple 에서 반복 검증할 수 있다.
