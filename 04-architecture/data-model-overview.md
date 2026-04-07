---
title: 데이터 모델 개요
type: architecture
status: active
updated: 2026-04-07
owners:
  - db-owner
related:
  - [[/01-requirements/req-attendance-presence.md]]
  - [[/01-requirements/req-device-auth.md]]
  - [[/03-conventions/conv-db-naming.md]]
  - [[/02-decisions/adr-0005-presence-snapshot-cache.md]]
  - [[/02-decisions/adr-0007-demo-presence-overlay-and-attendance-session-flow.md]]
  - [[/04-architecture/attendance-workflow-architecture.md]]
source:
  - [[/06-meetings/raw/2026-03-19-capstone-proposal.md]]
  - [[/06-meetings/raw/2026-03-30-presence-logic-clarification.md]]
  - [[/06-meetings/raw/2026-04-07-capstone-demo-planning.md]]
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
- `attendance_sessions`
  - 교수가 projected slot 에 대해 연 출석 세션
- `attendance_records`
  - 학생별 현재 출석 상태
- `attendance_status_audit_logs`
  - 상태 전이 audit history

# 관계 요약

- 한 사용자는 여러 강의를 수강할 수 있다.
- 한 강의는 여러 시간표 슬롯을 가질 수 있다.
- 한 시간표 슬롯은 하나의 강의실에 연결된다.
- 한 강의실은 하나 이상의 허용 네트워크를 가질 수 있다.
- 한 사용자는 하나 이상의 등록 단말을 가질 수 있다.
- 한 사용자는 최대 5개의 등록 단말을 가질 수 있다.
- 하나의 등록 단말 MAC 은 하나의 사용자에게만 속해야 한다.
- 하나의 `attendance_session` 은 하나의 `projection_key` 와 1:1 로 대응되는 active session 만 가질 수 있다.
- 하나의 `attendance_record` 는 `(attendance_session_id, student_user_id)` 기준으로 유일해야 한다.
- `attendance_status_audit_logs` 는 self check-in 과 professor manual update 둘 다 기록해야 한다.

# 설계 원칙

- 강의실, 네트워크, 단말 정보를 분리 저장한다.
- 출석 결과뿐 아니라 판정 근거도 추적 가능해야 한다.
- 시험 접근 제어에도 재사용 가능한 모델을 지향한다.
- Redis snapshot 캐시는 영속 저장소가 아니라 성능 최적화 계층으로 취급한다.
- demo mode 의 mutable presence state 는 DB 테이블이 아니라 PresenceService overlay 계층이 소유한다.
- AP threshold 는 overlay 가 아니라 영속 운영 데이터이며 DB 가 소유한다.

# Branch 2 출석 모델 규칙

- projected slot 은 `courseCode + classroomCode + sessionDate + slotStartAt + slotEndAt` 로 canonical identity 를 만든다.
- projected slot 은 schedule window 를 `starts_at` 기준으로 30분 단위 full segment 로 나눈 결과만 허용한다.
- `attendance_sessions` 는 `projection_key` 를 저장해야 한다.
- student self check-in 은 첫 성공 시 audit row 를 남기고, 동일 open session 에 대한 성공 재시도는 no-op / no-extra-audit 이어야 한다.

# Presence refinement 모델 규칙

- `classroom_networks` 는 `signal_threshold_dbm` 같은 AP 별 운영 threshold 값을 가질 수 있어야 한다.
- `signal_threshold_dbm` 이 null 이면 fallback `-65 dBm` 을 사용한다.
- 관리자 UI 의 device dropdown source 는 등록 디바이스와 현재 관측 station 의 union 이다.
