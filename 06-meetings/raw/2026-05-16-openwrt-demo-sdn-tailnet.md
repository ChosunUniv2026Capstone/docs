---
title: OpenWrt 데모 SDN Tailnet 구성 메모
type: meeting-raw
status: active
updated: 2026-05-16
owners:
  - team
related:
  - [[/04-architecture/network-topology.md]]
  - [[/04-architecture/local-runtime-topology.md]]
  - [[/02-decisions/adr-0003-openwrt-device-collection.md]]
  - [[/05-work-items/task-openwrt-gateway-prototype.md]]
source:
  - user-note
---

# 원문

이건 demo service 용으로 서비스와 AP 존이 다른곳에 위치하더라도 가능하도록 SDN으로 묶은 데모용 구성이다.

이미지에 들어있는 아이피 정보도 같이 문서화한다.

# 이미지에서 확인한 Tailnet 정보

| Machine | Tailscale address | Version | OS / Kernel | Status | Labels |
| --- | --- | --- | --- | --- | --- |
| `openwrt-a` | `100.78.116.89` | `1.80.3-1 (OpenWrt)` | `Linux 6.6.119` | Connected | Expiry disabled, Subnets, Exit Node |
| `openwrt-b` | `100.86.49.51` | `1.80.3-1 (OpenWrt)` | `Linux 6.6.119` | Connected | Expiry disabled, Subnets, Exit Node |
| `openwrt-c` | `100.99.237.79` | `1.80.3-1 (OpenWrt)` | `Linux 6.6.119` | Connected | Expiry disabled, Subnets, Exit Node |
| `capstone-service` | `100.109.206.1` | `1.98.2` | `Linux 6.8.0-110-generic` | Connected | Expiry disabled |

# 현장 OpenWrt 관리 주소

| Label | OpenWrt management IP | Local subnet / AP zone |
| --- | --- | --- |
| A | `192.168.97.1` | `192.168.97.0/24` |
| B | `192.168.98.1` | `192.168.98.0/24` |
| C | `192.168.99.1` | `192.168.99.0/24` |

