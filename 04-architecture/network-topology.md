---
title: 네트워크 토폴로지 개요
type: architecture
status: active
updated: 2026-05-16
owners:
  - presence-team
related:
  - [[/02-decisions/adr-0003-openwrt-device-collection.md]]
  - [[/02-decisions/adr-0005-presence-snapshot-cache.md]]
  - [[/01-requirements/req-attendance-presence.md]]
  - [[/05-work-items/task-openwrt-gateway-prototype.md]]
  - [[/07-status/2026-05-16-openwrt-demo-tailnet-verification.md]]
source:
  - [[/06-meetings/raw/2026-03-19-capstone-proposal.md]]
  - [[/06-meetings/raw/2026-03-25-kickoff-work-items.md]]
  - [[/06-meetings/raw/2026-03-30-presence-logic-clarification.md]]
  - [[/06-meetings/raw/2026-04-08-openwrt-setup-and-station-inspection.md]]
  - [[/06-meetings/raw/2026-04-09-openwrt-ap-mode-dhcp-clarification.md]]
  - [[/06-meetings/raw/2026-05-16-openwrt-demo-sdn-tailnet.md]]
  - [[/07-status/2026-05-16-openwrt-demo-tailnet-verification.md]]
---

# 목표

강의실별 Wi-Fi 환경과 연결 단말 정보를 수집해 재실성 판정에 활용할 수 있는 테스트베드 구조를 정의한다.

# 구성 요소

- 강의실
- 강의실별 AP 또는 공유기
- OpenWrt 기반 게이트웨이 또는 연계 장비
- 학생 단말
- PresenceService
- Redis
- Backend

# 데이터 흐름

1. 학생 단말이 강의실 네트워크에 연결된다.
2. Backend 가 출석 또는 시험 접근 시 PresenceService 에 eligibility 확인을 요청한다.
3. PresenceService 는 강의실 매핑 기준으로 Redis 의 60초 이내 snapshot 을 먼저 조회한다.
4. snapshot 이 없거나 만료되었으면 PresenceService 가 OpenWrt 장비에 SSH 로 접속해 station list 를 수집한다.
5. 수집 결과는 Redis 에 저장된다.
6. PresenceService 는 강의실 / Wi-Fi / 단말 매칭 결과를 만든다.
7. Backend 는 이를 수강 정보와 시간표와 결합해 최종 판단한다.

# 운영 전제

- OpenWrt 장비는 상단 공유기 내부 대역의 static IP 와 SSH 접근이 가능해야 한다.
- 동일 서브넷에서 상단 게이트웨이가 IP 를 관리하고 OpenWrt 가 AP / bridge 역할만 할 때는 OpenWrt LAN DHCP 서버를 비활성화해야 한다.
- PresenceService 는 `iw dev`, `ubus`, `iwinfo <iface> assoclist`, `iw dev <iface> station dump` 계열 명령 결과를 파싱할 수 있어야 한다.
- 구체적인 테스트베드 연결 절차와 장비별 명령 예시는 `[[/05-work-items/task-openwrt-gateway-prototype.md]]` 에서 관리한다.

# 데모 SDN overlay 구성

데모 환경에서는 서비스 존과 AP 존이 서로 다른 장소에 있어도 하나의 시연 환경처럼 동작하도록 Tailscale Tailnet 을 SDN overlay 로 사용한다.
이 구성은 demo service 용 구성이다. 운영망 표준 배포 구조나 보안 경계가 아니라, 분리된 장소의 서비스와 AP 를 시연 목적으로 연결하기 위한 구조다.

## 역할

- `capstone-service` 는 서비스 존의 Tailnet 노드다.
- `openwrt-a`, `openwrt-b`, `openwrt-c` 는 AP 존을 대표하는 OpenWrt 노드다.
- 각 OpenWrt 노드는 자신의 AP subnet 을 Tailnet 에 광고하는 subnet router 로 동작한다.
- 각 OpenWrt 노드는 `0.0.0.0/0`, `::/0` 도 광고해 데모 중 외부 경로 검증용 exit node 후보로 동작한다.
- 현재 OpenWrt 노드는 IP forwarding 이 켜져 있고, Tailscale subnet route 는 기본 SNAT 모드로 동작한다. 따라서 AP subnet 에서 보는 원격 접근 출발지는 원 단말 IP 가 아니라 OpenWrt subnet router 쪽으로 보일 수 있다.

## Tailnet 주소

| Machine | Tailscale address | Version | OS / Kernel | Status | Demo role |
| --- | --- | --- | --- | --- | --- |
| `openwrt-a` | `100.78.116.89` | `1.80.3-1 (OpenWrt)` | `Linux 6.6.119` | Connected | AP zone A subnet router / exit node |
| `openwrt-b` | `100.86.49.51` | `1.80.3-1 (OpenWrt)` | `Linux 6.6.119` | Connected | AP zone B subnet router / exit node |
| `openwrt-c` | `100.99.237.79` | `1.80.3-1 (OpenWrt)` | `Linux 6.6.119` | Connected | AP zone C subnet router / exit node |
| `capstone-service` | `100.109.206.1` | `1.98.2` | `Linux 6.8.0-110-generic` | Connected | Demo service node |

## 현장 사설망 주소

| Label | OpenWrt management IP | AP subnet advertised to Tailnet |
| --- | --- | --- |
| A | `192.168.97.1` | `192.168.97.0/24` |
| B | `192.168.98.1` | `192.168.98.0/24` |
| C | `192.168.99.1` | `192.168.99.0/24` |

## 데모 운영 메모

- Tailnet 주소(`100.x.y.z`)는 SDN overlay 접근 주소이며, 현장 사설망 주소(`192.168.x.y`)는 OpenWrt 관리와 AP zone 내부 접근 주소다.
- Tailscale Admin Console 에서 각 OpenWrt 노드의 subnet route 와 exit node 를 승인해야 원격 클라이언트가 해당 경로를 사용할 수 있다.
- Linux 기반 원격 클라이언트는 승인된 subnet route 를 실제 라우팅 테이블에 반영하려면 `sudo tailscale set --accept-routes=true` 가 필요하다. 이 설정이 꺼져 있으면 Tailnet 에 route 가 보여도 `192.168.97.0/24`, `192.168.98.0/24`, `192.168.99.0/24` 로 직접 접근할 수 없다.
- PresenceService 가 AP 존과 다른 장소에서 실행되더라도 Tailnet route 승인과 클라이언트 route 수락 후에는 광고된 AP subnet 으로 접근할 수 있어야 한다. 2026-05-16 검증에서는 `192.168.97.1`, `192.168.98.1`, `192.168.99.1` 의 ICMP, SSH `22/tcp`, HTTP `80/tcp` 접근이 성공했다.

# 주의점

- 실제로 어떤 단말 식별자가 수집 가능한지는 테스트베드 검증이 필요하다.
- 교내 네트워크 정책과 장비 배치 제약을 별도 확인해야 한다.
- 강의실과 Wi-Fi 매핑 정보는 운영 데이터로 관리해야 한다.
- 강의실은 여러 AP 와 매핑될 수 있다.
- 캐시가 만료된 시점의 동시 요청 폭주를 막기 위한 lock 전략이 필요하다.
