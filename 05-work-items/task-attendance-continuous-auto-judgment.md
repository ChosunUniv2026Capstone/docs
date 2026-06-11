---
title: 스마트출석 continuous 자동 판정 구현
type: task
status: doing
updated: 2026-06-11
owners:
  - team
related:
  - [[/01-requirements/req-attendance-presence.md]]
  - [[/02-decisions/adr-0014-continuous-attendance-monitoring.md]]
  - [[/04-architecture/attendance-workflow-architecture.md]]
  - [[/04-architecture/data-model-overview.md]]
  - [[/07-status/implementation-roadmap.md]]
source:
  - 2026-06-10 continuous attendance deep-interview / ralplan
---

# 목표

스마트출석을 버튼형 10분 window 에서 끝내지 않고, 선택된 차시가 모두 끝날 때까지 Backend 가 학생별/slot별 재실 evidence 를 10초 주기로 적산해 자동으로 `출석/지각/결석` 을 확정한다.

# 구현 순서

## 1. DB / seed

- `attendance_sessions.attendance_policy` 추가와 기존 row backfill
- `attendance_monitoring_leases` 추가
- `attendance_monitoring_states` 추가
- 24시간 7일 전체 시간표를 차지하고 전체 학생을 active enrollment 로 포함하는 테스트 과목 seed/reset 추가

## 2. Backend

- `continuous_presence_v1` session open/close/finalization 정책 추가
- FastAPI lifespan background tick runner 추가
- session 단위 DB lease 획득/갱신/만료 처리
- student/slot 별 `last_accounted_until`, `away_seconds`, `unknown_seconds_consumed` 적산
- 60초 unknown grace 이후 AP/Presence 장애를 fail-closed away 로 누적
- 10분 이탈 시 `late`, 15분 이탈 시 `absent` candidate/audit 반영
- `continuous_presence_v1` check-in endpoint inert 처리
- professor/student realtime payload 에 status panel / away minutes 포함

## 3. Front

- API type 에 `attendance_policy`, continuous monitoring state, away minutes 반영
- 학생 active attendance 영역에서 `continuous_presence_v1` 일 때 출석 버튼 제거
- 학생 상태 패널 색상 규칙 적용
  - 출석 외 시간: 회색
  - 출석 중 재실: 초록색
  - 출석 중 이탈: 빨간색
- 교수 slot roster 에 학생별 누적 이탈 시간(분 단위) 표시
- WebSocket 연결 상태는 표시 대상/전달 상태로만 사용하고 출석 판단처럼 표현하지 않음

## 4. QA / e2e

- unit/integration: threshold 10분/15분, unknown grace, lease takeover, idempotent finalization
- API: session open, continuous check-in inert, roster away minutes, student panel state
- e2e: 24시간 7일 테스트 과목에서 임의 시각 session open 후 재실/이탈 전환과 교수/학생 화면 확인
- regression: 기존 `smart_window_v1` 10분 버튼형 흐름 보존

# 완료 기준

- docs / DB / Backend / Front 가 같은 `continuous_presence_v1` 계약을 따른다.
- 10초 tick 적산에서 slot별 이탈 누적 시간이 10분 이상이면 지각, 15분 이상이면 결석으로 자동 확정된다.
- 강의실 이탈 자동 하향 audit reason 이 문서화된 한국어 사유로 저장된다.
- AP / Presence 장애는 60초 grace 이후 fail-closed away 로 반영된다.
- 학생은 버튼 없이 상태 패널을 보고, 교수는 학생별 이탈 시간을 분 단위로 본다.
- 24시간 7일 테스트 과목으로 어떤 학생 계정이든 언제든 e2e 를 재실행할 수 있다.
