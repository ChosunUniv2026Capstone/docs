---
title: 출석 세션 및 projected slot 아키텍처
type: architecture
status: active
updated: 2026-04-07
owners:
  - backend-team
  - frontend-team
  - db-owner
related:
  - [[/01-requirements/req-attendance-presence.md]]
  - [[/02-decisions/adr-0004-attendance-authorization-flow.md]]
  - [[/02-decisions/adr-0007-demo-presence-overlay-and-attendance-session-flow.md]]
  - [[/03-conventions/conv-auth-and-session.md]]
  - [[/04-architecture/presence-eligibility-api.md]]
  - [[/04-architecture/data-model-overview.md]]
source:
  - [[/06-meetings/raw/2026-04-07-capstone-demo-planning.md]]
---

# 목표

교수의 출석 오픈 흐름, 학생 self check-in 흐름, 관리자 재실 시연 흐름을 하나의 일관된 아키텍처로 정의한다.

# 핵심 개념

## 1. projected slot

- projected slot 은 기존 `course_schedules` row 를 날짜 기준으로 구체화한 출석 가능 차시다.
- projected slot 은 아래 규칙으로 만든다.
  1. 대상 강의 / 강의실 / 날짜를 선택한다.
  2. 그 날짜에 해당하는 schedule window 를 찾는다.
  3. `starts_at` 기준으로 contiguous 30분 segment 로 분해한다.
  4. full 30분 segment 만 유효 slot 으로 채택한다.
  5. tail 이 30분 미만이면 버린다.
- canonical identity 는 `projection_key = courseCode + classroomCode + sessionDate + slotStartAt + slotEndAt` 이다.

## 2. attendance session

- 교수는 projected slot 중 하나를 선택해 출석 session 을 연다.
- session 은 projected slot 에서만 생성될 수 있다.
- 한 projected slot 에 대해 active session 은 하나만 허용한다.

## 3. attendance record

- 학생별 현재 상태를 저장한다.
- status set 은 `present`, `absent`, `late`, `official`, `sick` 이다.

## 4. attendance audit

- self check-in 과 professor manual update 둘 다 immutable history 로 남긴다.
- repeated successful self check-in 은 idempotent 하므로 추가 audit row 를 만들지 않는다.

# 서비스 책임

## Front

- 관리자 대시보드에서 demo-mode presence control panel 표시
- 교수 projected slot 조회 / session open / roster / history UI 표시
- 학생 eligibility 재확인 및 self check-in UI 표시

## Backend

- auth helper 와 ownership guard 적용
- shared slot-projection service 제공
- professor session open/close 와 student self check-in policy 결정
- live presence evidence 와 session open 상태를 결합한 최종 출석 판단
- attendance record / audit write

## PresenceService

- baseline snapshot + Redis overlay + effective snapshot merge
- classroom-scoped read-after-write visibility 보장
- network/device evidence 제공

# 흐름

## Branch 1 demo flow

1. 관리자 `ADM001` 이 dashboard/classroom-network surface 에서 `B101` overlay 를 수정한다.
2. Backend 가 PresenceService admin demo endpoint 를 호출한다.
3. PresenceService 가 overlay write -> cache eviction -> recompute/prewarm 을 수행한다.
4. 학생 `20201239` 가 generic eligibility 를 재확인한다.
5. Backend 는 generic eligibility path 를 통해 PresenceService 를 호출하고 변경된 evidence 를 받는다.
6. 학생 화면에서 결과와 사유가 바뀐다.

## Branch 2 attendance flow

1. 교수 `PRF002` 가 `CSE116 / B101 / date` 기준으로 projected slot 을 조회한다.
2. Backend shared slot-projection service 가 canonical slots 를 계산한다.
3. 교수는 그 중 하나를 선택해 session 을 연다.
4. 학생 `20201239` 는 open session 목록을 보고 self check-in 을 시도한다.
5. Backend 는 아래를 순서대로 검사한다.
   - self ownership
   - open session 존재
   - session 이 valid projected slot 에서 생성되었는지
   - live presence eligibility 가 true 인지
6. 성공 시 attendance record 를 `present` 로 만들거나 유지한다.
7. 첫 성공이면 audit row 를 기록하고, repeated success 면 no-op 로 처리한다.
8. 교수는 이후 상태를 수정할 수 있고, 그 변경은 새 audit row 로 남는다.

# 이유 코드

- `SESSION_SLOT_INVALID`
- `SESSION_NOT_OPEN`
- `PRESENCE_INELIGIBLE`
- `ATTENDANCE_CHECK_IN_OK`

# 구현 전 필수 산출물

- pinned demo tuple seed/reset 절차
- shared slot projection contract
- attendance session / record / audit schema
- admin / professor / student auth helper design
