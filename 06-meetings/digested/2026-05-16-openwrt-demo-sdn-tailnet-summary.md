---
title: OpenWrt 데모 SDN Tailnet 구성 요약
type: meeting-summary
status: active
updated: 2026-05-16
owners:
  - team
related:
  - [[/04-architecture/network-topology.md]]
  - [[/04-architecture/local-runtime-topology.md]]
  - [[/02-decisions/adr-0003-openwrt-device-collection.md]]
  - [[/05-work-items/task-openwrt-gateway-prototype.md]]
  - [[/07-status/2026-05-16-openwrt-demo-tailnet-verification.md]]
source:
  - [[/06-meetings/raw/2026-05-16-openwrt-demo-sdn-tailnet.md]]
---

# 회의 목적

OpenWrt 기반 AP 존과 demo service 존이 물리적으로 다른 위치에 있어도 하나의 데모 네트워크처럼 연결되도록 SDN overlay 구성을 문서화한다.

# 핵심 결정

- 데모 환경에서는 Tailscale Tailnet 을 SDN overlay 로 사용해 서비스 존과 AP 존을 묶는다.
- 이 구성은 demo service 용 구성이다. 운영망 표준 배포 구조나 보안 경계가 아니라, 분리된 장소의 서비스와 AP 를 시연 목적으로 연결하기 위한 구조다.
- `openwrt-a`, `openwrt-b`, `openwrt-c` 는 각각 자신의 AP subnet 을 Tailnet 에 광고하고 exit node 로도 노출한다.
- Linux 클라이언트에서 AP subnet 으로 접근하려면 Tailnet route 승인과 별도로 `--accept-routes` 클라이언트 설정이 필요하다.
- `capstone-service` 는 서비스 존의 Tailnet 노드로 문서화한다.

# 새 요구사항

- 데모 문서에서는 서비스와 AP 존이 서로 다른 장소에 있어도 SDN overlay 로 연결 가능하다는 전제를 명시해야 한다.
- OpenWrt 장비별 Tailnet IP, 현장 관리 IP, AP subnet, exit node / subnet route 역할과 실제 접근 검증 결과를 함께 기록해야 한다.

# 새 규약

- 데모용 SDN 구성은 `demo service` 용이라는 범위를 명시한다.
- Tailnet 주소와 현장 사설망 주소를 혼동하지 않도록 별도 표로 관리한다.

# 구조 / 아키텍처 변화

- `[[/04-architecture/network-topology.md]]` 에 OpenWrt A/B/C 와 `capstone-service` 를 묶는 데모 SDN overlay 구성을 추가한다.
- OpenWrt A/B/C 는 AP 존을 대표하는 subnet router 이자 exit node 로 취급한다.

# 작업 항목 / 담당자 / 기한

- `[[/07-status/2026-05-16-openwrt-demo-tailnet-verification.md]]`: OpenWrt A/B/C subnet route, exit node 후보, 관리 IP 접근성을 검증했다. / 담당: presence-team / 완료: 2026-05-16
- `[[/05-work-items/task-openwrt-gateway-prototype.md]]`: 실제 station list 수집 필드와 PresenceService 수집 계약 검증은 계속 추적한다. / 담당: presence-team / 기한: 미정

# 리스크

- Tailnet Admin Console 에서 subnet route 또는 exit node 승인이 빠지거나 Linux 클라이언트의 `--accept-routes` 설정이 꺼져 있으면 장비는 연결되어 있어도 원격 subnet 접근이 되지 않을 수 있다.
- 데모용 exit node 구성은 운영 보안 정책과 별도로 검토해야 한다.
- OpenWrt 장비 overlay 여유 공간이 제한적이므로 추가 패키지 설치 여유가 작다.

# 오픈 질문

- `capstone-service` 가 PresenceService / Backend / 전체 compose 중 어떤 런타임 단위를 대표하는지 최종 명명 기준이 필요하다.
- 데모 당일 Tailnet route auto-approval 정책을 사용할지, 수동 승인 절차를 둘지 결정해야 한다.

# source

- [[/06-meetings/raw/2026-05-16-openwrt-demo-sdn-tailnet.md]]
