---
title: Presence eligibility API 계약
type: architecture
status: active
updated: 2026-04-07
owners:
  - backend-team
  - presence-team
related:
  - [[/02-decisions/adr-0004-attendance-authorization-flow.md]]
  - [[/02-decisions/adr-0005-presence-snapshot-cache.md]]
  - [[/02-decisions/adr-0007-demo-presence-overlay-and-attendance-session-flow.md]]
  - [[/01-requirements/req-attendance-presence.md]]
  - [[/01-requirements/req-device-auth.md]]
source:
  - [[/06-meetings/raw/2026-03-30-presence-logic-clarification.md]]
  - [[/06-meetings/raw/2026-04-07-capstone-demo-planning.md]]
---

# 목적

Backend 가 출석 또는 시험 접근 시점에 PresenceService 로부터 재실성 eligibility 결과를 조회하는 기본 계약을 정의한다.
또한 capstone demo mode 에서 PresenceService 가 baseline + overlay 기반 effective snapshot 을 소유한다는 점을 명시한다.

# 호출 방향

- `Backend -> PresenceService`
- `PresenceService -> Redis`
- `PresenceService -> OpenWrt (필요 시)`
- `PresenceService -> baseline dummy snapshot + overlay merge (demo mode)`

# 요청

## Endpoint

`POST /eligibility/check`

## Request body

```json
{
  "studentId": "20201239",
  "courseId": "CSE116",
  "classroomId": "B101",
  "purpose": "attendance",
  "registeredDevices": [
    {
      "deviceId": "1",
      "label": "Choi Phone",
      "mac": "52:54:00:12:34:56"
    }
  ]
}
```

## 필드 규칙

- `purpose` 는 최소 `attendance`, `exam` 을 지원한다.
- Backend 는 수강 여부와 인증 상태를 먼저 확인한 뒤 PresenceService 를 호출한다.
- PresenceService 는 `classroomId` 에 매핑된 여러 AP 를 조회할 수 있어야 한다.
- `registeredDevices` 는 PresenceService 가 device presence candidate 를 판단하는 입력이다.

# 응답

```json
{
  "eligible": true,
  "reasonCode": "OK",
  "matchedDeviceMac": "52:54:00:12:34:56",
  "observedAt": "2026-04-07T15:05:00+09:00",
  "snapshotAgeSeconds": 2,
  "evidence": {
    "classroomId": "B101",
    "matchedApIds": ["phy3-ap0"],
    "signalDbm": -47,
    "associated": true,
    "authenticated": true,
    "authorized": true,
    "cacheHit": false
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

1. PresenceService 는 baseline snapshot 과 overlay state 를 합쳐 effective snapshot 을 만든다.
2. demo mode 에서는 overlay state 의 mutation 결과가 해당 classroom 에 대해 read-after-write 로 바로 보여야 한다.
3. Redis 에서 60초 이내 effective snapshot 을 조회한다.
4. effective snapshot 이 없거나 만료되었으면 baseline + overlay 를 기반으로 새 snapshot 을 구성한다.
5. 학생 등록 단말 중 하나라도 강의실 AP 목록에서 `associated=true` 상태로 관측되면 `eligible=true` 후보가 된다.
6. PresenceService 는 network / device eligibility 까지만 판단하고 최종 도메인 허용 여부는 Backend 가 결정한다.

# Demo mode 제어 계약

- Front 는 PresenceService 를 직접 호출하지 않는다.
- Front 관리자 패널은 Backend admin demo endpoint 를 통해 classroom overlay 를 변경한다.
- PresenceService 는 overlay write -> cache eviction -> recompute/prewarm -> success 반환 순서를 보장한다.
- 같은 classroom 에 대한 concurrent edit 는 last-write-wins 로 처리할 수 있다.

# 향후 확장

- `purpose=exam` 에 대한 추가 판정 규칙
- refresh lock / retry 전략 강화
- batch eligibility 조회
- observational field 를 semantic field 로 승격할지 여부 검토
