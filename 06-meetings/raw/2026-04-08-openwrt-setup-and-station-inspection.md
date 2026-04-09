---
title: OpenWrt 설정 및 단말 관측 절차 메모
type: meeting-raw
status: active
updated: 2026-04-08
owners:
  - team
related:
  - [[/02-decisions/adr-0003-openwrt-device-collection.md]]
  - [[/04-architecture/network-topology.md]]
  - [[/05-work-items/task-openwrt-gateway-prototype.md]]
source:
  - user-note
---

# 원문

1. OpenWrt 설정
   1. 상단 공유기 아래에 OpenWrt 가 설치된 공유기를 연결한다.
   2. OpenWrt 공유기에 유선으로 접속해 설정한다.
      1. Static IP
         1. LAN 쪽을 static IP 로 고정해야 한다. 상단 공유기 내부 대역으로 들어가기만 하면 된다.
         2. DHCP 는 꺼야 하는 것으로 보이지만, 켜져 있어도 큰 문제는 없을 수 있다.
      2. SSH 를 허용해야 한다.
   3. 상단 공유기 아래에 물려 있는 단말을 통해 SSH 연결한다.
   4. 연결 후 실제 단말 정보 확인 방법

```bash
iw dev
ubus list | grep hostapd
iwinfo phy0-ap0 assoclist
iw dev phy0-ap0 station dump
```

예시:

```text
root@OpenWrt:~# iw dev phy0-ap0 station dump
Station 36:68:99:4f:01:db (on phy0-ap0)
        inactive time:  25210 ms
        rx bytes:       141910
        rx packets:     672
        tx bytes:       193632
        tx packets:     471
        tx retries:     0
        tx failed:      0
        rx drop misc:   1
        signal:         -25 [-29, -26] dBm
        signal avg:     -24 [-29, -26] dBm
        tx bitrate:     216.6 MBit/s HE-MCS 9 HE-NSS 2 HE-GI 1 HE-DCM 0
        tx duration:    127989 us
        rx bitrate:     6.0 MBit/s
        rx duration:    367505 us
        last ack signal:-25 dBm
        avg ack signal: -25 dBm
        airtime weight: 256
        authorized:     yes
        authenticated:  yes
        associated:     yes
        preamble:       short
        WMM/WME:        yes
        MFP:            no
        TDLS peer:      no
        DTIM period:    2
        beacon interval:100
        short preamble: yes
        short slot time:yes
        connected time: 123 seconds
        associated at [boottime]:       949.482s
        associated at:  1738625112005 ms
        current time:   1738625235069 ms
```
