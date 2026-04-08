---
title: 데이터 모델 개요
type: architecture
status: active
updated: 2026-04-08
owners:
  - db-owner
related:
  - [[/01-requirements/req-attendance-presence.md]]
  - [[/01-requirements/req-device-auth.md]]
  - [[/03-conventions/conv-db-naming.md]]
  - [[/02-decisions/adr-0005-presence-snapshot-cache.md]]
  - [[/02-decisions/adr-0007-demo-presence-overlay-and-attendance-session-flow.md]]
  - [[/02-decisions/adr-0009-attendance-bundle-session-parent.md]]
  - [[/04-architecture/attendance-workflow-architecture.md]]
source:
  - [[/06-meetings/raw/2026-03-19-capstone-proposal.md]]
  - [[/06-meetings/raw/2026-03-30-presence-logic-clarification.md]]
  - [[/06-meetings/raw/2026-04-07-capstone-demo-planning.md]]
  - [[/02-decisions/adr-0007-demo-presence-overlay-and-attendance-session-flow.md]]
  - [[/02-decisions/adr-0009-attendance-bundle-session-parent.md]]
---

# 핵심 엔티티

- `users`
  - 학생 / 교수 / 관리자
- `courses`
  - 강의 기본 정보
- `course_enrollments`
  - 수강 관계
- `classrooms`
  - 강의실 정보
- `course_schedules`
  - 강의 시간표와 강의실 배정
- `classroom_networks`
  - 강의실별 허용 Wi-Fi / AP / 게이트웨이 정보
  - AP 별 signal threshold 운영 데이터 포함
- `registered_devices`
  - 사용자 등록 단말
- `network_snapshots`
  - 네트워크 수집 결과 또는 effective snapshot view
- `presence_eligibility_logs`
  - 출석 / 시험 eligibility 요청 로그
- `refresh_sessions`
  - refresh token rotation / replay detection / logout revocation 을 위한 인증 세션 영속 저장소
- `attendance_sessions`
  - 교수가 선택한 여러 projected slot 을 묶어 여는 bundle parent 출석 세션
- `attendance_session_slots`
  - bundle parent session 이 포함하는 ordered projected slot membership
- `attendance_records`
  - 학생별 / slot별 현재 출석 상태
- `attendance_status_audit_logs`
  - 학생별 / slot별 상태 전이 audit history

# 관계 요약

- 한 사용자는 여러 강의를 수강할 수 있다.
- 한 강의는 여러 시간표 슬롯을 가질 수 있다.
- 한 시간표 슬롯은 하나의 강의실에 연결된다.
- 한 강의실은 하나 이상의 허용 네트워크를 가질 수 있다.
- 한 사용자는 하나 이상의 등록 단말을 가질 수 있다.
- 한 사용자는 최대 5개의 등록 단말을 가질 수 있다.
- 하나의 등록 단말 MAC 은 하나의 사용자에게만 속해야 한다.
- 한 사용자는 하나 이상의 `refresh_sessions` row 를 가질 수 있어야 하며, `session_key` 는 전역 유일해야 한다.
- replay / revoke 상태는 `refresh_sessions` 에 append-only audit 가 아니라 mutable session state 로 남을 수 있다.
- 하나의 `attendance_session` 은 bundle parent 1개를 의미한다.
- 하나의 active projected slot 은 동시에 하나의 bundle parent 에만 속할 수 있다.
- 하나의 `attendance_session` 은 여러 `attendance_session_slots` membership row 를 가질 수 있다.
- 하나의 `attendance_record` 는 `(attendance_session_id, projection_key, student_user_id)` 기준으로 유일해야 한다.
- `attendance_status_audit_logs` 는 self check-in 과 professor manual update 둘 다 기록해야 한다.
- `attendance_status_audit_logs` 는 append-only 여야 하며 삭제 / 덮어쓰기를 허용하면 안 된다.

# 설계 원칙

- 강의실, 네트워크, 단말 정보를 분리 저장한다.
- 출석 결과뿐 아니라 판정 근거도 추적 가능해야 한다.
- 시험 접근 제어에도 재사용 가능한 모델을 지향한다.
- Redis snapshot 캐시는 영속 저장소가 아니라 성능 최적화 계층으로 취급한다.
- demo mode 의 mutable presence state 는 DB 테이블이 아니라 PresenceService overlay 계층이 소유한다.
- AP threshold 는 overlay 가 아니라 영속 운영 데이터이며 DB 가 소유한다.
- refresh token durability / replay detection 을 위한 인증 세션 영속 데이터는 DB 가 소유한다.

# Branch 2 출석 모델 규칙

- projected slot 은 `courseCode + classroomCode + sessionDate + slotStartAt + slotEndAt` 로 canonical identity 를 만든다.
- projected slot 은 schedule window 를 `starts_at` 기준으로 30분 단위 full segment 로 나눈 결과만 허용한다.
- `attendance_sessions.projection_key` 는 bundle anchor slot identity 로 유지해야 한다.
- `attendance_sessions` 는 `mode(manual|smart)` 와 `status(active|closed|expired|canceled)` 를 가져야 한다.
- `attendance_sessions` 는 `opened_by_user_id`, `opened_at`, `closed_at`, `expires_at`, `latest_version` 을 가져야 한다.
- `attendance_session_slots` 는 `(attendance_session_id, projection_key, slot_order)` 를 가지며 membership 순서를 보존해야 한다.
- `attendance_session_slots.projection_key` 는 bundle 이 포함한 실제 slot 집합의 source of truth 여야 한다.
- student self check-in 은 첫 성공 시 audit row 를 남기고, 동일 open session 에 대한 성공 재시도는 no-op / no-extra-audit 이어야 한다.
- bundle overwrite / bundle check-in write 는 slot fan-out 으로 저장해야 한다.
- `attendance_records.final_status` 는 `present|absent|late|official|sick` 만 허용한다.
- `attendance_records` 는 `projection_key` 를 가져야 한다.
- `attendance_records` 는 `attendance_reason`, `finalized_by_user_id`, `finalized_at` 을 가져야 한다.
- `attendance_status_audit_logs` 는 `projection_key` 를 가져야 한다.
- `attendance_status_audit_logs` 는 `actor_user_id`, `actor_role`, `change_source`, `previous_status`, `new_status`, `reason`, `changed_at`, `version` 을 가져야 한다.
- bundle overwrite 는 실제 값이 달라진 slot 에만 changed-only audit row 를 남겨야 한다.
- realtime replay 를 위해 `attendance_sessions.latest_version` 과 audit / event ordering 규칙이 일치해야 한다.
- 리포트와 집계는 bundle metadata 가 아니라 slot별 `attendance_records` 최종 상태를 기준으로 계산해야 한다.

# Presence refinement 모델 규칙

- `classroom_networks` 는 `signal_threshold_dbm` 같은 AP 별 운영 threshold 값을 가질 수 있어야 한다.
- `signal_threshold_dbm` 이 null 이면 fallback `-65 dBm` 을 사용한다.
- 관리자 UI 의 device dropdown source 는 등록 디바이스와 현재 관측 station 의 union 이다.
