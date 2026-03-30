---
title: API 응답 규약
type: convention
status: active
updated: 2026-03-30
owners:
  - backend-team
applies_to:
  - frontend
  - backend
  - presence
related:
  - [[/01-requirements/req-attendance-presence.md]]
  - [[/01-requirements/req-device-auth.md]]
source:
  - [[/06-meetings/raw/2026-03-19-capstone-proposal.md]]
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

# 초기 사유 코드 예시

- `UNAUTHENTICATED`
- `FORBIDDEN`
- `COURSE_NOT_FOUND`
- `OUTSIDE_CLASS_WINDOW`
- `NETWORK_NOT_ELIGIBLE`
- `DEVICE_NOT_REGISTERED`
- `DEVICE_MISMATCH`
