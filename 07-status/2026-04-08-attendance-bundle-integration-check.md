---
title: 2026-04-08 attendance bundle integration check
type: status
status: active
updated: 2026-04-08
owners:
  - team
related:
  - [[/02-decisions/adr-0009-attendance-bundle-session-parent.md]]
  - [[/04-architecture/attendance-workflow-architecture.md]]
  - [[/04-architecture/data-model-overview.md]]
source:
  - [[/.omx/plans/attendance-bundle-session-consensus-draft-20260408.md]]
---

# 목적

bundle-session semantics 문서 반영 이후, Backend / Front / DB 구현 상태가 어디까지 문서와 맞는지 빠르게 확인하고 lane 간 handoff 포인트를 남긴다.

# 기준 문서

- docs commit: `8267e2e` (`docs/attendance-bundle-session-parent`)
- canonical docs:
  - [[/02-decisions/adr-0009-attendance-bundle-session-parent.md]]
  - [[/04-architecture/attendance-workflow-architecture.md]]
  - [[/04-architecture/data-model-overview.md]]

# 일치하는 부분

- `DB/postgres/init/001_schema.sql`
  - `attendance_session_slots` table 이 존재한다.
  - `attendance_records` unique key 가 `(attendance_session_id, projection_key, student_user_id)` 이다.
  - `attendance_status_audit_logs.projection_key` 가 존재한다.

# 아직 bundle semantics 와 어긋나는 부분

## Backend

- `Backend/app/attendance.py`
  - `build_attendance_timeline()` 이 여전히 `projection_key -> latest session` 관점으로 slot row 를 직결한다.
  - `open_attendance_sessions_batch()` 가 per-slot `results[]` / `changed_projection_keys[]` 중심 응답을 유지한다.
  - `list_student_active_attendance_sessions()` 가 학생에게 bundle card 가 아니라 session-per-slot 목록을 주는 구조로 남아 있다.
  - `student_attendance_check_in()` / roster update / history path 가 bundle parent + slot fan-out summary 보다 single `projection_key` 중심 payload 에 가깝다.

## Front

- `Front/src/App.tsx`
  - 교수 batch open 이후 `primaryProjectionKey` 기준으로 timer / roster route 를 이동한다.
  - 교수 타임라인 row 와 modal selection UI 가 slot 중심 navigation 을 전제로 한다.
  - 학생 출석 흐름도 `session_id + projection_key` 단건 카드/응답 구조에 맞춰져 있다.
- `Front/src/api.ts`
  - `AttendanceBatchResponse`, `AttendanceSessionRoster`, `StudentAttendanceSession`, `AttendanceCheckInResult` 가 bundle metadata 보다 single `projection_key` 응답을 기본 shape 로 둔다.

## Demo seed / branch hygiene

- `DB` repo 는 아직 `main` 에 dirty state 로 남아 있다.
- `DB/postgres/init/012_attendance_demo_seed.sql` 은 sample attendance seed 를 가지지만 bundle parent 기준 demo seed/proof 는 추가 검증이 필요하다.

# lane handoff 메모

- Backend/DB lane 은 `attendance_sessions` 를 bundle parent 로 재해석한 뒤 API / websocket payload 를 `session_id + projection_keys[]` 기준으로 정렬해야 한다.
- Front lane 은 professor/student route 를 projection_key 중심 path 에서 bundle `session_id` 중심 path 로 옮겨야 한다.
- report/timeline 은 bundle metadata 가 아니라 per-slot `attendance_records` final state aggregate 를 계속 truth 로 유지해야 한다.
- per-slot exception route 는 삭제 대상이 아니라 예외 수정 lane 으로 유지해야 한다.

# 다음 확인 포인트

1. Backend batch open 응답이 bundle `session_id` + ordered slot list 로 바뀌었는지
2. Student active attendance 가 bundle card 1개 + one-click check-in 으로 바뀌었는지
3. close / expire 후 professor/student timer 가 즉시 멈추는지
4. changed-only audit 가 slot 단위로만 남는지
