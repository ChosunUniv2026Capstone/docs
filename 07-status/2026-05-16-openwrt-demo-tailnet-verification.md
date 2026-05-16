---
title: OpenWrt 데모 Tailnet 검증 기록
type: status
status: active
updated: 2026-05-16
owners:
  - presence-team
related:
  - [[/04-architecture/network-topology.md]]
  - [[/05-work-items/task-openwrt-gateway-prototype.md]]
  - [[/06-meetings/digested/2026-05-16-openwrt-demo-sdn-tailnet-summary.md]]
source:
  - [[/06-meetings/raw/2026-05-16-openwrt-demo-sdn-tailnet.md]]
  - Tailscale live status and read-only connectivity checks, 2026-05-16
  - https://tailscale.com/docs/features/subnet-routers
  - https://tailscale.com/docs/features/exit-nodes
---

# 검증 범위

OpenWrt A/B/C 가 데모 SDN overlay 에서 실제로 Tailnet peer, subnet router, exit node 후보로 동작하는지 확인했다.
검증은 현재 Tailnet 에 가입된 개발 장비에서 읽기 전용 명령과 포트 연결 확인으로 수행했다.

# 공식 문서 기준

- Tailscale subnet router 는 route 광고만으로 끝나지 않고, Admin Console 승인 또는 `autoApprovers`, ACL / grants, 클라이언트 route 수락이 함께 필요하다.
- Linux 클라이언트는 기본적으로 Tailscale IP 만 자동 사용하므로 subnet route 사용에는 `sudo tailscale set --accept-routes=true` 가 필요하다.
- Exit node 는 장비가 exit node 를 광고하고, Admin Console 에서 허용되고, 사용하는 클라이언트가 명시적으로 선택해야 동작한다.

# Tailnet 상태 확인

`tailscale status --json` 기준으로 세 OpenWrt 노드는 모두 online 이며 AP subnet 이 PrimaryRoute 로 잡혀 있다.
`tailscale exit-node list` 기준으로 세 OpenWrt 노드는 exit node 후보로 표시된다.

| Machine | Tailnet IP | Primary subnet route | Exit node candidate | Online |
| --- | --- | --- | --- | --- |
| `openwrt-a` | `100.78.116.89` | `192.168.97.0/24` | yes | yes |
| `openwrt-b` | `100.86.49.51` | `192.168.98.0/24` | yes | yes |
| `openwrt-c` | `100.99.237.79` | `192.168.99.0/24` | yes | yes |

# OpenWrt 장비 읽기 전용 확인

SSH 로 각 OpenWrt 장비에 접속해 커널, Tailscale 버전, LAN 주소, 라우팅 전제를 확인했다.

| Machine | SSH target | Kernel | Tailscale CLI | LAN address | IPv4 forwarding | Advertised routes |
| --- | --- | --- | --- | --- | --- | --- |
| `openwrt-a` | `100.78.116.89` | `6.6.119` | `1.80.3` | `192.168.97.1/24` | `1` | `0.0.0.0/0`, `::/0`, `192.168.97.0/24` |
| `openwrt-b` | `100.86.49.51` | `6.6.119` | `1.80.3` | `192.168.98.1/24` | `1` | `0.0.0.0/0`, `::/0`, `192.168.98.0/24` |
| `openwrt-c` | `100.99.237.79` | `6.6.119` | `1.80.3` | `192.168.99.1/24` | `1` | `0.0.0.0/0`, `::/0`, `192.168.99.0/24` |

# 접근성 검증

`--accept-routes=false` 상태에서는 `192.168.97.1`, `192.168.98.1`, `192.168.99.1` 로 직접 ping / SSH 접근이 실패했다.
`sudo tailscale set --accept-routes=true` 를 임시 적용한 뒤에는 세 AP 관리 IP 모두 ICMP, SSH `22/tcp`, HTTP `80/tcp` 접근이 성공했다.
검증 후 개발 장비 설정은 다시 `--accept-routes=false` 로 되돌렸다.

| Target | ICMP | SSH `22/tcp` | HTTP `80/tcp` |
| --- | --- | --- | --- |
| `192.168.97.1` | pass | pass | pass |
| `192.168.98.1` | pass | pass | pass |
| `192.168.99.1` | pass | pass | pass |

# Exit node smoke test

세 OpenWrt 노드를 각각 exit node 로 선택하는 smoke test 를 수행했다.
각 선택 후 외부 IPv4 확인 요청이 성공했고, 테스트 후 exit node 설정을 해제했다.
다만 세 장비가 같은 현장 NAT 뒤에 있을 수 있어 public IP 변화만으로 장비별 물리 위치를 구분하지는 않는다.

# 결론

데모 문서의 핵심 전제인 `서비스 존과 AP 존이 서로 다른 장소에 있어도 Tailnet overlay 로 AP 관리 subnet 에 접근할 수 있다` 는 현재 구성에서 재현 가능하다.
단, Linux 기반 PresenceService 실행 호스트에서는 Tailnet route 승인만으로는 부족하고 `--accept-routes` 설정이 필요하다.
