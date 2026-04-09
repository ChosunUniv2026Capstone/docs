---
title: OpenWrt AP 모드 DHCP 비활성화 기준 요약
type: meeting-summary
status: active
updated: 2026-04-09
owners:
  - team
related:
  - [[/04-architecture/network-topology.md]]
  - [[/05-work-items/task-openwrt-gateway-prototype.md]]
  - [[/02-decisions/adr-0003-openwrt-device-collection.md]]
source:
  - [[/06-meetings/raw/2026-04-09-openwrt-ap-mode-dhcp-clarification.md]]
---

# 회의 목적

동일 서브넷 AP/브리지 운영 전제에서 OpenWrt LAN DHCP 설정을 확정한다.

# 핵심 결정

- 상단 게이트웨이가 IP 를 관리하고 하단 OpenWrt 가 AP / bridge 역할만 하는 동일 서브넷 구조로 운영한다.
- 이 구조에서는 OpenWrt LAN DHCP 비활성화가 기본 설정이다.

# 새 요구사항

- OpenWrt 테스트베드 문서는 동일 서브넷 AP/브리지 운영을 기본 전제로 설명해야 한다.
- OpenWrt 장비 설정 절차에는 LAN DHCP 비활성화를 명시해야 한다.

# 새 규약

- 동일 서브넷에서 상단 게이트웨이가 IP 를 관리하는 AP / bridge 구성에서는 하단 OpenWrt 의 LAN DHCP 서버를 비활성화한다.

# 구조 / 아키텍처 변화

- 네트워크 토폴로지 문서에 동일 서브넷 AP/브리지 구조와 DHCP 비활성화 전제를 current truth 로 반영한다.
- OpenWrt 작업 문서의 절차를 DHCP 비활성화가 포함된 기본 절차로 갱신한다.

# 작업 항목 / 담당자 / 기한

- `[[/05-work-items/task-openwrt-gateway-prototype.md]]`: 실제 OpenWrt 장비에서 동일 서브넷 AP/브리지 설정과 DHCP 비활성화 절차를 재현하고 점검한다. / 담당: presence-team / 기한: 미정

# 리스크

- OpenWrt 가 AP / bridge 가 아니라 별도 라우터 모드로 운용될 경우 DHCP 정책이 달라질 수 있다.

# 오픈 질문

- 없음

# source

- [[/06-meetings/raw/2026-04-09-openwrt-ap-mode-dhcp-clarification.md]]
