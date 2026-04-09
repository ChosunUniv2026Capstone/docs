---
title: OpenWrt AP 모드 DHCP 비활성화 기준 확인 메모
type: meeting-raw
status: active
updated: 2026-04-09
owners:
  - team
related:
  - [[/04-architecture/network-topology.md]]
  - [[/05-work-items/task-openwrt-gateway-prototype.md]]
  - [[/02-decisions/adr-0003-openwrt-device-collection.md]]
source:
  - user-note
---

# 원문

- 동일 서브넷으로만 운영한다.
- 상단 게이트웨이가 IP 를 관리한다.
- 하단 OpenWrt 는 AP / bridge 역할만 한다.
- 따라서 OpenWrt LAN DHCP 비활성화가 기본 설정이다.
