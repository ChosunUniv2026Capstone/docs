---
title: API 응답 규약
type: convention
status: active
updated: 2026-04-07
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
- `ATTENDANCE_CHECK_IN_OK`
- `ATTENDANCE_REASON_REQUIRED`
- `TOKEN_EXPIRED`
- `TOKEN_REVOKED`
- `REFRESH_REPLAY_DETECTED`
- `COURSE_ROUTE_FORBIDDEN`

# 추가 규칙

- `ATTENDANCE_CHECK_IN_OK` 는 성공 코드이며, repeated self check-in 의 idempotent success 에도 사용될 수 있다.
- 같은 의미의 실패를 endpoint 마다 다른 `code` 로 중복 생성하면 안 된다.
