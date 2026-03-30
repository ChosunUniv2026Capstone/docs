---
title: 재실 판정 로직 확정 요약
type: meeting-summary
status: active
updated: 2026-03-30
owners:
  - team
related:
  - [[/01-requirements/req-attendance-presence.md]]
  - [[/01-requirements/req-device-auth.md]]
  - [[/02-decisions/adr-0005-presence-snapshot-cache.md]]
source:
  - [[/06-meetings/raw/2026-03-30-presence-logic-clarification.md]]
---

# 회의 목적

재실 판정 로직의 실제 개발 착수 기준을 정하고, 장치 등록 정책과 캐시 전략을 확정한다.

# 핵심 결정

- 단말 식별 기준은 MAC 주소 1개다.
- 학생은 최대 5개 단말까지 등록 가능하다.
- 동일 단말은 여러 학생에게 중복 등록할 수 없다.
- 강의실에는 여러 AP 가 매핑될 수 있다.
- Presence snapshot 유효 시간은 60초다.
- OpenWrt 데이터 수집은 요청 시 수행한다.
- OpenWrt 직접 조회 결과는 Redis 캐시를 두고 재사용한다.
- 출석과 시험은 동일한 eligibility 가드를 공유하되 목적별 세부 규칙은 분리 가능하게 둔다.

# 새 요구사항

- 학생은 자신의 등록 단말 목록을 직접 등록 / 삭제할 수 있어야 한다.
- PresenceService 는 강의실 단위 station snapshot 을 Redis 에 캐시할 수 있어야 한다.
- Backend 는 `purpose` 값을 포함해 eligibility 를 요청할 수 있어야 한다.

# 구조 / 아키텍처 변화

- `Backend -> PresenceService -> Redis/OpenWrt` 흐름을 기본으로 한다.
- PresenceService 는 강의실별 AP 목록을 기준으로 station list 를 병합한다.

# 리스크

- 랜덤 MAC 을 사용하면 등록 단말 매칭이 깨질 수 있다.
- 실제 OpenWrt 장비에서 얻을 수 있는 필드가 모델 가정보다 적을 수 있다.

# 오픈 질문

- 출석과 시험의 목적별 추가 규칙을 어디에서 분기할 것인가
- OpenWrt 수집 실패 시 재시도 정책을 어느 수준으로 둘 것인가

# source

- [[/06-meetings/raw/2026-03-30-presence-logic-clarification.md]]
