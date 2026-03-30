---
title: OpenWrt 게이트웨이 기반 단말 목록 수집 검토
type: task
status: todo
updated: 2026-03-30
owners:
  - presence-team
related:
  - [[/02-decisions/adr-0003-openwrt-device-collection.md]]
  - [[/04-architecture/network-topology.md]]
source:
  - [[/06-meetings/raw/2026-03-25-kickoff-work-items.md]]
---

# 작업

OpenWrt 게이트웨이 또는 연계 장비를 통해 수집 가능한 단말 연결 정보와 수집 방식을 검토한다.

# 확인 항목

- 수집 가능한 식별자 종류
- 수집 주기와 지연
- 강의실별 네트워크 매핑 방법
- PresenceService 로 전달할 최소 데이터 형식

# 완료 기준

- 테스트베드에서 얻을 수 있는 필드 목록 정리
- 판정에 사용할 수 있는 필드와 한계 정리
- 후속 구현에 필요한 API 또는 데이터 계약 초안 정리
