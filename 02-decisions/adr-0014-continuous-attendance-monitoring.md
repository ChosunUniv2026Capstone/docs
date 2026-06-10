---
title: ADR-0014 스마트출석은 continuous presence monitoring 정책을 지원한다
type: decision
status: accepted
updated: 2026-06-11
date: 2026-06-11
deciders:
  - team
supersedes: []
superseded_by: null
related:
  - [[/01-requirements/req-attendance-presence.md]]
  - [[/02-decisions/adr-0004-attendance-authorization-flow.md]]
  - [[/02-decisions/adr-0009-attendance-bundle-session-parent.md]]
  - [[/02-decisions/adr-0013-openwrt-local-collector-push.md]]
  - [[/03-conventions/conv-service-boundary.md]]
  - [[/04-architecture/attendance-workflow-architecture.md]]
  - [[/04-architecture/data-model-overview.md]]
source:
  - 2026-06-10 continuous attendance deep-interview / ralplan
---

# Context

기존 스마트출석은 교수가 session 을 열면 서버 기준 10분 동안 학생이 버튼을 눌러 한 번 check-in 하고, 성공 시 bundle 대상 차시에 fan-out 하는 모델이었다.
새 요구는 버튼 조작이 아니라 선택된 모든 차시가 끝날 때까지 학생의 강의실 재실 상태를 계속 관찰해 slot 별 최종 상태를 자동 산출하는 것이다.

이 요구는 ADR-0009 의 bundle parent / slot membership / slot-aware record 원칙은 유지하지만, shared 10분 timer 와 student check-in 버튼을 신규 정책의 핵심 흐름에서 제거한다.

# Decision

스마트출석은 `attendance_sessions.attendance_policy` 로 세부 정책을 구분한다.

- `smart_window_v1`: 기존 10분 버튼형 스마트출석이다.
- `continuous_presence_v1`: 선택된 slot 이 모두 끝날 때까지 Backend 가 학생별/slot별 재실 evidence 를 적산해 자동 판정한다.

`continuous_presence_v1` 의 최종 판단과 누적 상태는 Backend 가 소유한다.

- Backend lifespan worker 는 기본 10초 cadence 로 active continuous session 을 tick 한다.
- 다중 Backend instance 를 고려해 session 단위 DB lease 를 사용한다.
- worker 는 selected slot 의 전체 수강생을 slot 시작 시점부터 모니터링한다.
- slot 시작 후 최초 출석 전 시간도 이탈 시간에 포함한다.
- WebSocket 은 표시와 전달 채널이며 출석 evidence 가 아니다.
- 학생 check-in endpoint 는 이 정책에서 attendance record / audit 을 만들지 않는 inert 경로다.

# Slot 판정 규칙

각 student/slot pair 는 누적 이탈 시간으로 최종 상태를 산출한다.

- 이탈 10분 미만: `present`
- 이탈 10분 이상 15분 미만: `late`
- 이탈 15분 이상: `absent`

AP offline, PresenceService unavailable, AP registry timeout 같은 의존 경로 장애는 student/slot 별 60초 unknown grace 를 먼저 소비한다.
grace 를 초과한 장애 시간은 fail-closed away 로 누적한다.
따라서 continuous session 의 최종 상태는 `present|late|absent` 중 하나로 수렴한다.

자동 판정이 `late` 또는 `absent` 로 내려갈 때 audit reason 은 각각 아래 값을 사용한다.

- `강의실 이탈로 인한 지각`
- `강의실 이탈로 인한 결석`

# UI / realtime 결정

- 학생 화면은 continuous session 에서 출석 버튼을 보여주지 않는다.
- 학생 화면은 WebSocket/bootstrap snapshot 으로 현재 상태 패널을 표시한다.
  - 출석 외 시간: 회색
  - 출석 중 재실: 초록색
  - 출석 중 이탈: 빨간색
- 교수는 slot 을 눌렀을 때 학생 roster 와 함께 누적 이탈 시간을 분 단위로 본다.
- WebSocket 이 끊긴 학생은 display 대상에서 제외될 수 있지만, 이 사실만으로 이탈/결석 처리하면 안 된다.

# Data / seed 결정

- DB 는 `attendance_policy`, monitoring lease, monitoring state 를 영속화한다.
- monitoring state 는 `last_accounted_until`, `away_seconds`, `unknown_seconds_consumed`, `current_presence_state`, `last_presence_reason`, `status_candidate` 를 포함한다.
- QA 와 상시 시연을 위해 seed/reset 데이터에는 24시간 7일 전체 시간표를 차지하는 테스트 과목을 포함한다.

# Consequences

- Backend 는 long-running session tick, idempotent finalization, lease takeover, outage grace accounting 을 검증해야 한다.
- Front 는 기존 버튼형 smart UI 와 신규 continuous status-panel UI 를 정책별로 분기해야 한다.
- PresenceService 는 evidence provider 로 남고 출석 status/away time 을 소유하지 않는다.
- DB migration 은 기존 row 를 `smart_window_v1` 또는 `manual_v1` 로 안전하게 backfill 해야 한다.

# Rejected alternatives

- WebSocket 연결 상태로 출석/이탈 판단: 브라우저 탭/네트워크 품질을 강의실 재실 evidence 로 오인하므로 거부한다.
- PresenceService 가 지각/결석을 직접 결정: 수강생, 시간표, session lifecycle, audit version ordering 은 Backend 도메인이므로 거부한다.
- slot 종료 시 snapshot 만 보고 상태를 계산: 중간 이탈 누적 시간을 잃어 10분/15분 규칙을 증명할 수 없으므로 거부한다.
- 기존 10분 버튼형 smart session 을 덮어쓰기: 과거 row / 기존 UX / 회귀 위험을 줄이기 위해 policy marker 로 병행한다.
