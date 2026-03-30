---
title: 재실 판정 로직과 장치 등록 정책 확정 메모
type: meeting-raw
status: active
updated: 2026-03-30
owners:
  - team
related:
  - req-attendance-presence
  - req-device-auth
  - adr-0005-presence-snapshot-cache
source:
  - user-note
---

# 원문

- 학생 단말 식별은 단말별 MAC 하나를 기준으로 한다.
- 학생당 여러 기기를 등록할 수 있고 최대 5개까지 허용한다.
- 학생은 자신의 기기 리스트에 기기를 등록, 삭제할 수 있어야 한다.
- 하나의 단말이 여러 학생에게 등록될 수는 없다.
- 랜덤 MAC 은 학생이 직접 끄도록 안내한다.
- 강의실당 AP 공유기는 여러 대일 수 있다.
- 스냅샷 유효 시간은 최근 60초 이내로 설정한다.
- OpenWrt 수집 방식은 요청시 수집으로 한다.
- 시험 / 출석은 로직은 유사하지만 완전히 동일하지는 않다. 목적별 세부 규칙은 추후 확장한다.
- Backend 가 시험 시작 또는 출석 시점에 학생 단말이 강의실 단위 공유기 리스트 내부에 있는지 확인한다.
- PresenceService 가 공유기에서 데이터를 받아오고 Backend 요청 시 정보를 제공하는 구조로 간다.
- 매 요청마다 공유기에서 전체 목록을 직접 가져오는 대신 Redis 에 저장하고 60초 이상 지나면 다시 요청하는 방식을 검토한다.
- OpenWrt 에서 확인 가능한 예시는 `iw dev`, `ubus list | grep hostapd`, `iwinfo phy0-ap0 assoclist`, `iw dev phy0-ap0 station dump` 이다.
