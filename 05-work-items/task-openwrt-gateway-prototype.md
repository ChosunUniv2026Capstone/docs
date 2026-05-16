---
title: OpenWrt 게이트웨이 기반 단말 목록 수집 검토
type: task
status: todo
updated: 2026-05-16
owners:
  - presence-team
related:
  - [[/02-decisions/adr-0003-openwrt-device-collection.md]]
  - [[/04-architecture/network-topology.md]]
  - [[/07-status/open-questions.md]]
source:
  - [[/06-meetings/raw/2026-03-25-kickoff-work-items.md]]
  - [[/06-meetings/raw/2026-04-08-openwrt-setup-and-station-inspection.md]]
  - [[/06-meetings/raw/2026-04-09-openwrt-ap-mode-dhcp-clarification.md]]
---

# 작업

OpenWrt 게이트웨이 또는 연계 장비를 통해 수집 가능한 단말 연결 정보와 수집 방식을 검토한다.

# 현재 확보된 테스트베드 절차

1. 상단 공유기 아래에 OpenWrt 가 설치된 공유기를 연결한다.
2. OpenWrt 장비에는 유선으로 직접 접속해 초기 설정을 진행한다.
3. OpenWrt LAN 주소를 상단 공유기 내부 대역의 static IP 로 고정한다.
4. 동일 서브넷 AP / bridge 운영 전제에서 OpenWrt LAN DHCP 서버를 비활성화한다.
5. SSH 접근을 허용한다.
6. 상단 공유기 하위에 연결된 다른 단말에서 OpenWrt 의 static IP 로 SSH 접속한다.
7. 아래 명령으로 interface 와 station 정보를 확인한다.

```bash
iw dev
ubus list | grep hostapd
iwinfo <iface> assoclist
iw dev <iface> station dump
```

# 확인 항목

- 수집 가능한 식별자 종류
- soft TTL `3초`, hard TTL `30초` 정책에서의 수집 주기와 지연
- refresh lock 적용 시 동일 OpenWrt/AP target 에 대한 실제 최대 수집 빈도
- 강의실별 네트워크 매핑 방법
- PresenceService 로 전달할 최소 데이터 형식
- 장비별 실제 interface 이름과 출력 차이

# 완료 기준

- 테스트베드에서 얻을 수 있는 필드 목록 정리
- 판정에 사용할 수 있는 필드와 한계 정리
- 후속 구현에 필요한 API 또는 데이터 계약 초안 정리
- refresh lock, stale-while-revalidate, stale-if-error 동작의 구현 기준 정리
- 장비별로 재현 가능한 OpenWrt 확인 절차 정리
