---
title: OpenWrt unified SSID current configuration
type: status
status: active
updated: 2026-05-16
owners:
  - presence-team
related:
  - [[/04-architecture/network-topology.md]]
  - [[/02-decisions/adr-0013-openwrt-local-collector-push.md]]
  - [[/05-work-items/task-openwrt-gateway-prototype.md]]
source:
  - 2026-05-16 live OpenWrt SSH inspection after unified SSID fix
---

# Summary

2026-05-16 기준 데모 OpenWrt AP 3대는 하나의 SSID `SmartClass-Demo` 로 통일되어 있다.
단말 LAN / AP 관리 LAN 은 `192.168.97.0/24` 로 통일하며, `openwrt-a` 만 gateway / DHCP owner 로 둔다.
`openwrt-b` 와 `openwrt-c` 는 WAN 포트를 `br-lan` 에 포함한 bridge AP 이며 DHCP 를 제공하지 않는다.

# Current AP configuration

| AP | Tailnet | Management IP | Role | SSID | Security | Channel / width | DHCP | Collector |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `openwrt-a` | `100.78.116.89` | `192.168.97.1` | gateway, DHCP owner, AP | `SmartClass-Demo` | `sae-mixed`, key `capstone_D2V` | ch36 / HE20 | enabled, `100-249`, `12h` | running |
| `openwrt-b` | `100.86.49.51` | `192.168.97.2` | bridge AP | `SmartClass-Demo` | `sae-mixed`, key `capstone_D2V` | ch44 / HE20 | disabled (`dhcp.lan.ignore=1`) | running |
| `openwrt-c` | `100.99.237.79` | `192.168.97.3` | bridge AP | `SmartClass-Demo` | `sae-mixed`, key `capstone_D2V` | ch48 / HE20 | disabled (`dhcp.lan.ignore=1`) | running |

# Verified state

- All three APs expose `phy1-ap0` as AP interface with SSID `SmartClass-Demo`.
- `openwrt-a` route: default via WAN uplink, `192.168.97.0/24` on `br-lan`.
- `openwrt-b` and `openwrt-c` route: default via `192.168.97.1` on `br-lan`.
- Demo service `/collector/aps/health` reports:
  - `openwrt-a` online for `B101`
  - `openwrt-b` online for `B102`
  - `openwrt-c` online for `C201`
- Live DB AP registry and DB seed/migration metadata were aligned through DB PR #21 so B/C management IPs and shared SSID do not revert on seed replay.

# Important operational notes

- 2.4 GHz `radio0` remains disabled on the current APs.
- Current APs use 5 GHz only. If a test handset does not support or scan 5 GHz, it will not see the SSID.
- Keep `bss_transition` and `wnm_sleep_mode` unset on this OpenWrt build. Setting them caused hostapd `unknown configuration item` errors and prevented AP startup.
- Keep `openwrt-c` away from channel 149 in the current regulatory/driver state. Hostapd reported `Primary frequency not allowed`; ch48 is the verified working channel.
- 802.11k neighbor / beacon report flags may remain enabled. 802.11r fast transition is not enabled.
- Routine presence collection remains local collector push, not SSH polling.

# Evidence commands

```bash
uci show network.lan
uci show dhcp.lan
uci show wireless.radio1
uci show wireless.default_radio1
iw dev
ip route
ps w | grep -E 'presence-collec' | grep -v grep
curl -fsS https://smart-class.org/collector/aps/health
```
