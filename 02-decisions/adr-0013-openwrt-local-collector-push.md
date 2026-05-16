---
title: ADR-0013 OpenWrt local collector push 방식 채택
type: decision
status: accepted
updated: 2026-05-16
date: 2026-05-16
deciders:
  - team
supersedes:
  - [[/02-decisions/adr-0003-openwrt-device-collection.md]]
superseded_by: null
related:
  - [[/01-requirements/req-attendance-presence.md]]
  - [[/01-requirements/req-device-auth.md]]
  - [[/04-architecture/network-topology.md]]
  - [[/04-architecture/presence-eligibility-api.md]]
  - [[/04-architecture/data-model-overview.md]]
source:
  - 2026-05-16 OpenWrt local collector push deep-interview / ralplan
---

# Context

초기 OpenWrt 수집 구조는 PresenceService 가 요청 시 OpenWrt 에 SSH 로 접속해 station list 를 가져오는 pull 방식이었다.
데모 AP 3개를 실제 서비스에 붙이는 단계에서는 사용자 요청이 OpenWrt polling 을 유발하지 않고, AP 측에서 낮은 주기로 최신 snapshot 을 밀어주는 구조가 더 예측 가능하다.

# Decision

OpenWrt 장비에는 lightweight local collector 를 두고, collector 가 로컬 `ubus` / hostapd client 정보를 읽어 PresenceService 로 주기적으로 push 한다.

- 기본 push interval 은 AP 당 약 3초다.
- PresenceService 는 user-triggered request 경로에서 OpenWrt 로 SSH 접속하거나 polling 하지 않는다.
- AP 가 약 10초 동안 유효 snapshot/heartbeat 를 보내지 않으면 offline 으로 본다.
- 강의실에 매핑된 online AP 가 0개이면 PresenceService 는 eligibility 를 `AP_OFFLINE` 으로 거부한다.
- 강의실에 매핑된 AP 중 하나 이상 online 이면 online AP snapshot 만 사용해 기존 단말/MAC/신호세기 판정을 수행한다.

# AP identity / mapping

- `collector_ap_id`: 물리 OpenWrt 노드 ID. 예: `openwrt-a`.
- `interface_id`: OpenWrt 내부 AP/BSS interface ID. 예: `phy0-ap0`.
- `classroom_networks.ap_id`: eligibility evidence 와 threshold 적용 대상이 되는 interface/network ID 로 유지한다.
- Collector payload 의 classroom field 는 diagnostic 전용이며 authoritative mapping 으로 사용하지 않는다.
- PresenceService 는 Backend internal registry 또는 cached registry 를 통해 DB 의 canonical AP/interface/classroom mapping 을 확인해야 한다.

# Token lifecycle

- DB 는 AP registry 와 per-AP token hash 를 소유한다.
- Backend 는 API/CLI 기반 token issue/revoke/rotate 를 소유한다.
- Token plaintext 는 생성 응답 직후에만 노출하고 저장/로그에 남기지 않는다.
- Token hash 는 고엔트로피 token + server-side pepper/secret 기반 SHA-256 digest 로 저장한다.
- PresenceService 는 push 요청에서 AP ID, token, timestamp/nonce 를 검증하고 revoked/stale/replay/mismatch push 는 상태 갱신 없이 거부한다.

# API / UI behavior

- Backend check-in API 는 AP offline 으로 인한 거부를 transport success 로 반환하되, 출석 기록을 생성하지 않고 slot 결과를 `rejected` + reason `AP_OFFLINE` 으로 표시한다.
- Front 는 Backend 가 반환한 `can_check_in=false` 및 reason `AP_OFFLINE` 을 사용해 스마트 출석 버튼을 비활성화하고 AP 연결 끊김 안내를 표시한다.
- Front 는 AP 상태를 직접 추론하지 않는다.

# Consequences

- OpenWrt SSH 는 설치/운영 진단용으로 유지할 수 있지만 routine presence data path 가 아니다.
- PresenceService 는 collector ingestion endpoint, AP health cache, registry cache, replay 방지 nonce/timestamp 검증을 가져야 한다.
- Backend/DB 는 AP registry/token lifecycle API 와 migration/seed 를 가져야 한다.
- Demo seed 는 실제 AP 3개와 매칭되는 강의실/과목/교수/학생 visibility 를 보장해야 한다.

# Rejected alternatives

- SSH pull 유지: 사용자 요청 fan-out 과 OpenWrt 부하/지연이 커지고 offline semantics 가 불안정하다.
- Static env token only: demo 는 빠르지만 production-leaning 요구와 revoke/rotate 요구를 만족하지 못한다.
- Collector-supplied classroom trust: spoof/misconfiguration 위험이 있어 canonical DB mapping 원칙에 맞지 않는다.
