---
title: Presence eligibility API 계약
type: architecture
status: active
updated: 2026-03-30
owners:
  - backend-team
  - presence-team
related:
  - [[/02-decisions/adr-0004-attendance-authorization-flow.md]]
  - [[/02-decisions/adr-0005-presence-snapshot-cache.md]]
  - [[/01-requirements/req-attendance-presence.md]]
  - [[/01-requirements/req-device-auth.md]]
source:
  - [[/06-meetings/raw/2026-03-30-presence-logic-clarification.md]]
---

# 목적

Backend 가 출석 또는 시험 접근 시점에 PresenceService 로부터 재실성 eligibility 결과를 조회하는 기본 계약을 정의한다.

# 호출 방향

- `Backend -> PresenceService`
- `PresenceService -> Redis`
- `PresenceService -> OpenWrt (필요 시)`

# 요청

## Endpoint

`POST /eligibility/check`

## Request body

```json
{
  "studentId": "20201234",
  "courseId": "CSE101",
  "classroomId": "B101",
  "purpose": "attendance"
}
```

## 필드 규칙

- `purpose` 는 최소 `attendance`, `exam` 을 지원한다.
- Backend 는 수강 여부와 인증 상태를 먼저 확인한 뒤 PresenceService 를 호출한다.
- PresenceService 는 `classroomId` 에 매핑된 여러 AP 를 조회할 수 있어야 한다.

# 응답

```json
{
  "eligible": true,
  "reasonCode": "OK",
  "matchedDeviceMac": "36:68:99:4f:01:db",
  "observedAt": "2026-03-30T10:15:00+09:00",
  "snapshotAgeSeconds": 12,
  "evidence": {
    "classroomId": "B101",
    "matchedApIds": ["phy0-ap0"],
    "signalDbm": -25,
    "associated": true,
    "authenticated": true,
    "authorized": true
  }
}
```

# 기본 reasonCode

- `OK`
- `CLASSROOM_NOT_MAPPED`
- `SNAPSHOT_UNAVAILABLE`
- `SNAPSHOT_STALE`
- `DEVICE_NOT_REGISTERED`
- `DEVICE_NOT_PRESENT`
- `NETWORK_NOT_ELIGIBLE`

# PresenceService 내부 처리 규칙

1. Redis 에서 60초 이내 snapshot 을 조회한다.
2. snapshot 이 없거나 만료되었으면 OpenWrt 에서 새로 수집한다.
3. 학생 등록 단말 5개 중 하나라도 강의실 AP 목록에서 관측되면 `eligible=true` 후보가 된다.
4. PresenceService 는 network / device eligibility 까지만 판단하고 최종 도메인 허용 여부는 Backend 가 결정한다.

# 향후 확장

- `purpose=exam` 에 대한 추가 판정 규칙
- refresh lock / retry 전략
- batch eligibility 조회
