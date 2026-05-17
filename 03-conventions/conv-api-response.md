---
title: API 응답 규약
type: convention
status: active
updated: 2026-05-17
owners:
  - backend-team
applies_to:
  - frontend
  - backend
  - presence
related:
  - [[/01-requirements/req-attendance-presence.md]]
  - [[/01-requirements/req-device-auth.md]]
  - [[/04-architecture/attendance-workflow-architecture.md]]
source:
  - [[/06-meetings/raw/2026-03-19-capstone-proposal.md]]
  - [[/06-meetings/raw/2026-04-07-capstone-demo-planning.md]]
  - [[/02-decisions/adr-0008-jwt-refresh-and-route-driven-attendance.md]]
---

# 성공 응답

```json
{
  "success": true,
  "data": {},
  "message": "ok",
  "meta": {}
}
```

# 실패 응답

```json
{
  "success": false,
  "error": {
    "code": "ATTENDANCE_NOT_ELIGIBLE",
    "message": "attendance is not allowed",
    "details": {}
  }
}
```

# 규칙

- 프론트가 분기할 수 있는 안정적인 `code` 를 제공한다.
- 사용자에게 보여줄 메시지와 내부 로그용 상세 정보는 분리한다.
- 출석과 시험 접근 제어 실패는 사유 코드를 남긴다.
- 기존 legacy endpoint 를 유지하는 경우에도 error envelope 와 stable reason code 는 보존한다.
- attendance session / projected slot 관련 API 는 성공 / 실패 코드를 명확히 구분해야 한다.
- auth/login/refresh/logout/bootstrap endpoint 도 가능한 한 같은 success / error envelope 규약을 따른다.
- legacy compatibility 응답을 임시로 유지하는 경우에는 sunset gate 와 최종 제거 기준을 문서화해야 한다.

# 초기 사유 코드 예시

- `UNAUTHENTICATED`
- `FORBIDDEN`
- `COURSE_NOT_FOUND`
- `OUTSIDE_CLASS_WINDOW`
- `NETWORK_NOT_ELIGIBLE`
- `DEVICE_NOT_REGISTERED`
- `DEVICE_MISMATCH`
- `SESSION_NOT_OPEN`
- `SESSION_SLOT_INVALID`
- `SESSION_ALREADY_OPEN`
- `PRESENCE_INELIGIBLE`
- `PRESENCE_SERVICE_UNAVAILABLE`
- `ATTENDANCE_CHECK_IN_OK`
- `ATTENDANCE_REASON_REQUIRED`
- `TOKEN_EXPIRED`
- `TOKEN_REVOKED`
- `REFRESH_REPLAY_DETECTED`
- `COURSE_ROUTE_FORBIDDEN`
- `EXAM_NOT_FOUND`
- `EXAM_NOT_OPEN`
- `EXAM_NOT_EDITABLE`
- `EXAM_INVALID_WINDOW`
- `EXAM_INVALID_PAYLOAD`
- `EXAM_ATTEMPT_LIMIT_REACHED`
- `EXAM_LATE_ENTRY_NOT_ALLOWED`
- `EXAM_SUBMISSION_NOT_FOUND`
- `EXAM_SUBMISSION_ALREADY_FINALIZED`

# 추가 규칙

- `ATTENDANCE_CHECK_IN_OK` 는 성공 코드이며, repeated self check-in 의 idempotent success 에도 사용될 수 있다.
- 같은 의미의 실패를 endpoint 마다 다른 `code` 로 중복 생성하면 안 된다.

# Presence dependency failure 규칙

- `PRESENCE_SERVICE_UNAVAILABLE` 은 Backend 가 PresenceService 에 연결할 수 없거나, PresenceService 가 Backend AP registry 의존 경로를 일시적으로 확인할 수 없는 경우 사용한다.
- 이 코드는 출석/시험/인접성 확인에서 실패 폐쇄(`eligible=false`) reason 으로 저장될 수 있다.
- 원인을 알 수 없는 generic 5xx 는 이 코드로 숨기지 않는다. 명시적인 timeout/request failure 또는 `COLLECTOR_REGISTRY_UNAVAILABLE` 계열 dependency unavailable 만 `PRESENCE_SERVICE_UNAVAILABLE` reason 으로 변환하고, upstream code 는 evidence 에 보존한다.
- `AP_OFFLINE` 은 강의실/AP registry 매핑은 확인됐지만 해당 강의실에 online AP snapshot 이 0개인 경우에만 사용한다.
