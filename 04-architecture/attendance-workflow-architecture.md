---
title: 출석 세션 및 projected slot 아키텍처
type: architecture
status: active
updated: 2026-06-11
owners:
  - backend-team
  - frontend-team
  - db-owner
related:
  - [[/01-requirements/req-attendance-presence.md]]
  - [[/02-decisions/adr-0004-attendance-authorization-flow.md]]
  - [[/02-decisions/adr-0007-demo-presence-overlay-and-attendance-session-flow.md]]
  - [[/02-decisions/adr-0009-attendance-bundle-session-parent.md]]
  - [[/02-decisions/adr-0014-continuous-attendance-monitoring.md]]
  - [[/03-conventions/conv-auth-and-session.md]]
  - [[/04-architecture/presence-eligibility-api.md]]
  - [[/04-architecture/data-model-overview.md]]
source:
  - [[/06-meetings/raw/2026-04-07-capstone-demo-planning.md]]
  - [[/02-decisions/adr-0007-demo-presence-overlay-and-attendance-session-flow.md]]
  - [[/02-decisions/adr-0009-attendance-bundle-session-parent.md]]
  - [[/02-decisions/adr-0014-continuous-attendance-monitoring.md]]
  - 2026-06-10 continuous attendance deep-interview / ralplan
---

# 목표

교수의 출석 오픈 흐름, `smart_window_v1` 학생 self check-in 흐름, `continuous_presence_v1` 자동 재실 모니터링 흐름, 관리자 재실 시연 흐름을 하나의 일관된 아키텍처로 정의한다.

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
- `smart` mode 는 `attendance_policy` 로 세부 정책을 구분한다.
  - `smart_window_v1`: 서버 기준 10분 만료 시각(`expires_at`)을 가지는 shared timer 1개를 사용한다.
  - `continuous_presence_v1`: 선택된 마지막 projected slot 종료 시각까지 active 상태를 유지하고, 각 slot 시작/종료 시각에 맞춰 자동 모니터링한다.

## 3. attendance record

- 학생별 현재 상태를 저장한다.
- status set 은 `present`, `absent`, `late`, `official`, `sick` 이다.
- `canceled` 는 attendance record status 가 아니라 session/slot lifecycle 상태다.
- record identity 는 `(attendance_session_id, projection_key, student_user_id)` 여야 한다.

## 4. attendance audit

- self check-in, continuous monitoring transition, professor manual update 는 immutable history 로 남긴다.
- repeated successful self check-in 은 idempotent 하므로 추가 audit row 를 만들지 않는다.
- professor manual update 의 reason 은 `official` 변경에서만 필수이며 non-official 상태 변경의 reason 은 `NULL` 로 정규화할 수 있다.
- bundle overwrite / bundle check-in 은 slot fan-out write 로 저장하되 실제 값이 바뀐 slot 에만 changed-only audit row 를 남긴다.
- bundle roster 기본값은 anchor slot record 를 따르며 anchor slot 에 기록이 없으면 `absent` 를 사용한다.
- manual session 은 open 직후 미수정 학생을 `absent` 로 해석해야 한다.
- `smart_window_v1` smart session 은 active 동안 미체크 학생을 `pending` 으로 유지하고, close / expire 시점에만 `absent` 로 확정해야 한다.
- `continuous_presence_v1` smart session 은 active 동안 학생별/slot별 monitoring state 를 누적하고 slot 종료/close 시 자동 final state 를 `present|late|absent` 로 확정해야 한다.

## 5. continuous presence monitoring

- Backend 는 `continuous_presence_v1` session 의 최종 attendance authority 와 이탈 누적 accumulator 를 소유한다.
- Backend lifespan worker 는 기본 10초 cadence 로 active `continuous_presence_v1` session 을 tick 한다.
- 여러 Backend instance 가 동시에 실행될 수 있으므로 tick runner 는 DB lease(`attendance_monitoring_leases`)를 획득한 instance 만 해당 session 을 처리해야 한다.
- monitoring worker instance id 는 replica 별로 유일해야 하며, lease TTL 은 최악 tick 처리 시간보다 길게 설정한다.
  배포 설정에서 shared/static owner id 를 강제하면 lease 안전성이 깨진다.
- worker 는 긴 tick 중에도 PresenceService 외부 호출 직전에 lease heartbeat 를 갱신하고, 소유권을 잃으면 해당 tick 처리를 중단한다.
- 각 student/slot pair 는 monitoring state(`attendance_monitoring_states`)를 가진다.
  - `last_accounted_until`: 마지막으로 시간이 반영된 server timestamp
  - `away_seconds`: slot 시작 이후 누적 이탈 시간
  - `unknown_seconds_consumed`: AP/PRESENCE 장애 unknown grace 누적 사용량
  - `current_presence_state`: `outside_time|present|away|unknown`
  - `last_presence_reason`: 마지막 evidence reason 또는 장애 reason
  - `status_candidate`: `present|late|absent`
- slot 시작 후 최초 재실 확인 전 시간도 이탈 시간으로 누적한다.
- AP offline / PresenceService unavailable / registry timeout 은 60초까지 unknown grace 로 보류하고, 이후 fail-closed away 로 누적한다.
- slot 별 판정 기준은 다음과 같다.
  - `away_seconds < 600`: `present`
  - `600 <= away_seconds < 900`: `late`
  - `away_seconds >= 900`: `absent`
- `late` 또는 `absent` 로 자동 하향될 때 audit reason 은 각각 `강의실 이탈로 인한 지각`, `강의실 이탈로 인한 결석` 이다.
- 학생 check-in API 는 `continuous_presence_v1` 에서 attendance record 를 생성/변경하지 않는다. UI 는 WebSocket/bootstrap snapshot 으로 현재 상태만 표시한다.
- WebSocket 연결 여부는 표시 대상과 실시간 전달 채널일 뿐이며 재실/출석 evidence 로 사용하지 않는다.
- session close/expire/reopen 은 monitoring worker 와 동일한 final-state write path 를 사용해 audit/version/realtime ordering 을 보존해야 한다.

## 6. realtime projection

- Backend 는 committed attendance state 를 기준으로 professor / student / report surface 에 실시간 이벤트를 발행한다.
- 모든 subscriber 는 bootstrap snapshot 을 먼저 받고 그 뒤 incremental event 를 적용해야 한다.
- incremental event 는 `version` 과 `occurred_at` 을 가져야 하며 stale update 를 버릴 수 있어야 한다.
- 학생 subscriber 는 자기 자신의 active smart-attendance 와 최근 final-state update 만 구독할 수 있어야 한다.
- `continuous_presence_v1` 학생 event 는 상태 패널 색상(`gray|green|red`), 현재 출석 시간 여부, 이탈/재실 상태, 마지막 판정 시각을 포함해야 한다.
- `continuous_presence_v1` 교수 roster event 는 slot별 학생 상태와 누적 이탈 시간을 분 단위로 표시할 수 있는 값을 포함해야 한다.

# 서비스 책임

## Front

- 관리자 대시보드에서 demo-mode presence control panel 표시
- 교수 projected slot 조회 / bundle session open / timer / roster / history / report UI 표시
- `smart_window_v1` 학생 bundle smart-attendance card / timer / one-click self check-in / final-state UI 표시
- `continuous_presence_v1` 에서는 학생 출석 버튼 대신 회색/초록/빨간 상태 패널 표시
- `continuous_presence_v1` 에서는 교수 slot roster 에 학생별 이탈 시간(분 단위) 표시
- 학생 attendance tab semester matrix 표시
- 교수 attendance dashboard student-stats 표 표시

## Backend

- auth helper 와 ownership guard 적용
- shared slot-projection service 제공
- professor bundle session open/close/cancel/reopen 와 `smart_window_v1` student bundle self check-in policy 결정
- live presence evidence 와 session open 상태를 결합한 최종 출석 판단
- `continuous_presence_v1` monitoring lease, tick cadence, slot별 이탈 누적, 자동 finalization 소유
- bundle -> slot membership traversal 과 changed-only record / audit / report aggregate write
- websocket bootstrap / incremental event publish

## PresenceService

- baseline snapshot + Redis overlay + effective snapshot merge
- classroom-scoped read-after-write visibility 보장
- network/device evidence 제공
- 출석 상태, 이탈 시간, 지각/결석 최종 판정은 소유하지 않음

# 흐름

## Branch 1 demo flow

1. 관리자 `ADM001` 이 dashboard/classroom-network surface 에서 `B101` overlay 를 수정한다.
2. Backend 가 PresenceService admin demo endpoint 를 호출한다.
3. PresenceService 가 overlay write -> cache eviction -> recompute/prewarm 을 수행한다.
4. 학생 `20201239` 가 generic eligibility 를 재확인한다.
5. Backend 는 generic eligibility path 를 통해 PresenceService 를 호출하고 변경된 evidence 를 받는다.
6. 학생 화면에서 결과와 사유가 바뀐다.

## Branch 2 attendance flow — `smart_window_v1`

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

## Branch 3 attendance flow — `continuous_presence_v1`

1. 교수 `PRF002` 가 `CSE116 / B101 / date` 기준으로 projected slot 을 조회한다.
2. 교수는 같은 주차 안의 하나 이상의 projected slot 을 선택해 `smart` mode bundle parent session 을 열고, Backend 는 `attendance_policy='continuous_presence_v1'` 로 저장한다.
3. session 은 선택된 마지막 slot 종료 시각까지 active 이며, 각 slot 의 자동 판정은 slot 시작 시점에 시작된다.
4. Backend monitoring worker 는 DB lease 를 획득한 뒤 기본 10초 cadence 로 선택 slot 의 enrolled students 에 대해 PresenceService evidence 를 조회한다.
5. worker 는 student/slot 별 `last_accounted_until` 이후 시간을 evidence 상태에 따라 `away_seconds` 또는 present time 으로 반영한다.
6. AP offline / PresenceService unavailable 은 60초 unknown grace 이후 fail-closed away 로 반영한다.
7. `away_seconds` 가 10분에 도달하면 candidate 를 `late` 로 낮추고 audit reason `강의실 이탈로 인한 지각` 을 남긴다.
8. `away_seconds` 가 15분에 도달하면 candidate 를 `absent` 로 낮추고 audit reason `강의실 이탈로 인한 결석` 을 남긴다.
9. slot 종료 또는 교수 close 시 worker 는 candidate 를 final attendance record 로 확정하고 report aggregate / realtime event 를 갱신한다.
10. 학생 화면은 WebSocket/bootstrap snapshot 으로 회색(출석 외 시간), 초록(출석 중 재실), 빨간색(출석 중 이탈) 상태 패널을 표시한다.
11. 교수 slot roster 는 학생별 current state 와 누적 이탈 시간을 분 단위로 표시한다.

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
- `AP_OFFLINE`
- `PRESENCE_SERVICE_UNAVAILABLE`
  - `continuous_presence_v1` 에서는 즉시 최종 거부가 아니라 60초 unknown grace 이후 이탈 누적 근거로 사용한다.

# 구현 전 필수 산출물

- pinned demo tuple seed/reset 절차
- shared slot projection contract
- bundle parent / slot membership / slot-aware record / audit schema
- attendance policy, monitoring lease/state, unknown grace, continuous finalization schema
- admin / professor / student auth helper design
- websocket bootstrap / event payload contract
- 24시간 7일 테스트 과목 seed/reset 절차
