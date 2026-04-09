---
title: OpenWrt 설정 및 단말 관측 절차 요약
type: meeting-summary
status: active
updated: 2026-04-08
owners:
  - team
related:
  - [[/02-decisions/adr-0003-openwrt-device-collection.md]]
  - [[/04-architecture/network-topology.md]]
  - [[/05-work-items/task-openwrt-gateway-prototype.md]]
  - [[/07-status/open-questions.md]]
source:
  - [[/06-meetings/raw/2026-04-08-openwrt-setup-and-station-inspection.md]]
---

# 회의 목적

OpenWrt 테스트베드에서 상단 공유기 하위에 장비를 연결하고, SSH 기반으로 실제 station 정보를 조회하는 최소 절차를 정리한다.

# 핵심 결정

- OpenWrt 장비는 상단 공유기 하위에 연결하고, OpenWrt 장비 자체에는 유선으로 접속해 초기 설정한다.
- OpenWrt LAN 주소는 상단 공유기 내부 대역의 static IP 로 고정한다.
- OpenWrt 에 SSH 접근을 허용한 뒤, 상단 공유기 하위 단말에서 SSH 로 접속해 station 정보를 조회한다.
- 실측 확인 명령의 기본 세트는 `iw dev`, `ubus list | grep hostapd`, `iwinfo <iface> assoclist`, `iw dev <iface> station dump` 이다.

# 새 요구사항

- PresenceService 가 파싱 대상으로 삼을 OpenWrt 조회 명령 세트는 최소한 interface 목록, hostapd 노출 여부, assoclist, station dump 를 포함해야 한다.
- 테스트베드 문서는 상단 공유기 내부 대역에 맞춘 static IP 와 SSH 접근 선행 조건을 명시해야 한다.

# 새 규약

- 새 규약으로 즉시 승격할 내용은 없다.
- OpenWrt LAN DHCP 비활성화 여부는 아직 확정하지 않고 오픈 질문으로 유지한다.

# 구조 / 아키텍처 변화

- 네트워크 토폴로지 문서에는 OpenWrt 장비가 상단 공유기 내부 대역의 static IP 와 SSH 접근을 지원해야 한다는 연결 조건만 반영한다.
- 구체적인 테스트베드 절차와 명령 예시는 작업 문서에서 관리한다.
- station dump 예시에서 관측 가능한 MAC, signal, bitrate, connected time, authorized/authenticated/associated 상태를 PresenceService 파싱 후보 필드로 본다.

# 작업 항목 / 담당자 / 기한

- `[[/05-work-items/task-openwrt-gateway-prototype.md]]`: OpenWrt 테스트베드에서 static IP / SSH / station dump 확인 절차를 재현하고 장비별 interface 차이를 정리한다. / 담당: presence-team / 기한: 미정

# 리스크

- 실제 인터페이스 이름은 `phy0-ap0` 와 다를 수 있어 장비별 확인 절차가 필요하다.
- DHCP 비활성화가 필수인지 권장인지 아직 확정되지 않았다.

# 오픈 질문

- OpenWrt LAN DHCP 를 반드시 꺼야 하는지, 아니면 상단 공유기 하위 테스트베드에서는 권장 사항 수준인지 운영 기준을 확정해야 한다.

# source

- [[/06-meetings/raw/2026-04-08-openwrt-setup-and-station-inspection.md]]
