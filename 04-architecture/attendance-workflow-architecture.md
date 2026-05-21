---
title: 출석 세션 및 projected slot 아키텍처
type: architecture
status: active
updated: 2026-05-21
owners:
  - backend-team
  - frontend-team
  - db-owner
related:
  - [[/01-requirements/req-attendance-presence.md]]
  - [[/02-decisions/adr-0004-attendance-authorization-flow.md]]
  - [[/02-decisions/adr-0007-demo-presence-overlay-and-attendance-session-flow.md]]
  - [[/02-decisions/adr-0009-attendance-bundle-session-parent.md]]
  - [[/03-conventions/conv-auth-and-session.md]]
  - [[/04-architecture/presence-eligibility-api.md]]
  - [[/04-architecture/data-model-overview.md]]
source:
  - [[/06-meetings/raw/2026-04-07-capstone-demo-planning.md]]
  - [[/02-decisions/adr-0007-demo-presence-overlay-and-attendance-session-flow.md]]
  - [[/02-decisions/adr-0009-attendance-bundle-session-parent.md]]
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

- 교수는 하나 이상의 projected slot 을 선택해 **bundle parent session** 1개를 연다.
- session 은 projected slot 집합에서만 생성될 수 있다.
- parent session 은 `attendance_sessions` row 1개로 표현하고 `projection_key` 는 anchor slot identity 로 유지한다.
- 선택된 모든 slot 은 ordered membership row(`attendance_session_slots`) 로 parent session 아래에 저장한다.
- 한 projected slot 은 동시에 하나의 active bundle session 에만 속할 수 있다.
- session mode 는 `manual`, `smart`, `canceled` 로 구분한다.
- lifecycle 은 `active -> closed|expired|canceled -> reopen(optional)` 흐름을 가져야 한다.
- `manual`, `smart`, `canceled` 모두 같은 bundle parent 모델을 사용한다.
- `canceled` mode 는 휴강 처리처럼 즉시 닫힌/취소된 bundle parent 를 남기는 운영 명령으로 취급한다.
- `smart` mode 는 서버 기준 10분 만료 시각(`expires_at`)을 가지는 shared timer 1개만 사용한다.

## 3. attendance record

- 학생별 현재 상태를 저장한다.
- status set 은 `present`, `absent`, `late`, `official`, `sick` 이다.
- `canceled` 는 attendance record status 가 아니라 session/slot lifecycle 상태다.
- record identity 는 `(attendance_session_id, projection_key, student_user_id)` 여야 한다.

## 4. attendance audit

- self check-in 과 professor manual update 둘 다 immutable history 로 남긴다.
- repeated successful self check-in 은 idempotent 하므로 추가 audit row 를 만들지 않는다.
- professor manual update 는 항상 reason 을 포함해야 한다.
- bundle overwrite / bundle check-in 은 slot fan-out write 로 저장하되 실제 값이 바뀐 slot 에만 changed-only audit row 를 남긴다.
- bundle roster 기본값은 anchor slot record 를 따르며 anchor slot 에 기록이 없으면 `absent` 를 사용한다.
- manual session 은 open 직후 미수정 학생을 `absent` 로 해석해야 한다.
- smart session 은 active 동안 미체크 학생을 `pending` 으로 유지하고, close / expire 시점에만 `absent` 로 확정해야 한다.

## 5. realtime projection

- Backend 는 committed attendance state 를 기준으로 professor / student / report surface 에 실시간 이벤트를 발행한다.
- 모든 subscriber 는 bootstrap snapshot 을 먼저 받고 그 뒤 incremental event 를 적용해야 한다.
- incremental event 는 `version` 과 `occurred_at` 을 가져야 하며 stale update 를 버릴 수 있어야 한다.
- 학생 subscriber 는 자기 자신의 active smart-attendance 와 최근 final-state update 만 구독할 수 있어야 한다.

# 서비스 책임

## Front

- 관리자 대시보드에서 demo-mode presence control panel 표시
- 교수 projected slot 조회 / bundle session open / timer / roster / history / report UI 표시
- 학생 bundle smart-attendance card / timer / one-click self check-in / final-state UI 표시
- 학생 attendance tab semester matrix 표시
- 교수 attendance dashboard student-stats 표 표시

## Backend

- auth helper 와 ownership guard 적용
- shared slot-projection service 제공
- professor bundle session open/close/cancel/reopen 와 student bundle self check-in policy 결정
- live presence evidence 와 session open 상태를 결합한 최종 출석 판단
- bundle -> slot membership traversal 과 changed-only record / audit / report aggregate write
- websocket bootstrap / incremental event publish

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
3. 교수는 그 중 여러 개를 선택해 bundle parent session 1개를 연다.
4. 학생 `20201239` 는 open bundle 목록을 보고 self check-in 을 1회 시도한다.
5. Backend 는 아래를 순서대로 검사한다.
   - self ownership
   - open bundle session 존재
   - bundle session 이 valid projected slot 집합에서 생성되었는지
   - live presence eligibility 가 true 인지
6. 성공 시 Backend 는 bundle 대상 slot 별 attendance record 를 `present` 로 만들거나 유지한다.
7. 첫 성공이면 changed slot 별 audit row 를 기록하고, repeated success / unchanged slot 은 no-op 로 처리한다.
8. 교수는 bundle roster 에서 상태를 수정할 수 있고, 그 변경은 slot fan-out + changed-only audit 로 저장된다.
9. 예외 차시 수정은 projection-key 기반 per-slot route 에서 별도로 수행한다.
10. close / expire / professor 수정이 발생하면 professor / student / report surface 는 같은 final state 로 실시간 갱신되고 타이머도 즉시 멈춘다.

## Branch 2 report flow

1. Backend 는 attendance record final state 를 기준으로 slot aggregate 와 dashboard summary 를 계산한다.
2. professor update / student self check-in / lifecycle transition 이 발생하면 Backend 는 updated aggregate 를 event 로 발행한다.
3. report surface 는 bootstrap + incremental event 를 통해 동일 aggregate 를 유지한다.
4. 교수 attendance report export 는 같은 최종 상태 / 화면 해석을 사용해 CSV 를 생성한다.
   - `summary` CSV 는 학생별 `학번`, `이름`, `출석 차시`, `결석 차시`, `지각 차시`, `공결 차시` 누계를 출력한다.
   - `full` CSV 는 summary 컬럼 뒤에 projected slot 순서의 차시별 상태 컬럼을 추가한다.
   - `sick` 은 report/dashboard 와 동일하게 공결에 합산하며, 전체본의 `pending`, `upcoming`, `canceled` 성격 상태는 화면 라벨과 같은 의미로 표기한다.
   - CSV 생성은 기존 report export / authenticated download 경로를 사용하며, CSV variant 때문에 attendance final-state authority 나 DB schema 를 바꾸면 안 된다.

# 이유 코드

- `SESSION_SLOT_INVALID`
- `SESSION_ALREADY_OPEN`
- `SESSION_NOT_OPEN`
- `PRESENCE_INELIGIBLE`
- `ATTENDANCE_CHECK_IN_OK`
- `ATTENDANCE_REASON_REQUIRED`
  - 공결(official) 변경 사유가 비어 있을 때만 발생한다. non-official 상태 변경은 reason 없이 허용하고 reason 필드는 `NULL` 로 저장한다.

# 구현 전 필수 산출물

- pinned demo tuple seed/reset 절차
- shared slot projection contract
- bundle parent / slot membership / slot-aware record / audit schema
- admin / professor / student auth helper design
- websocket bootstrap / event payload contract
