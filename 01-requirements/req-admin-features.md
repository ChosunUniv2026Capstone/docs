---
title: 관리자 기능 요구사항
type: requirement
status: active
updated: 2026-04-07
owners:
  - backend-team
  - frontend-team
related:
  - [[/04-architecture/service-map.md]]
  - [[/04-architecture/data-model-overview.md]]
  - [[/04-architecture/attendance-workflow-architecture.md]]
source:
  - [[/06-meetings/raw/2026-03-25-kickoff-work-items.md]]
  - [[/06-meetings/raw/2026-04-07-capstone-demo-planning.md]]
---

# 목표

관리자는 사용자, 강의, 강의실, 교수자 정보를 운영할 수 있어야 하며,
캡스톤 데모에서는 더미 모드 기반 재실 관제 패널을 통해 네트워크 상태를 시연할 수 있어야 한다.

# 필수 기능

- 학생 목록 관리
- 교수자 관리
- 강의 목록 관리
- 강의실 목록 관리
- 강의실별 와이파이 / AP 목록 관리
- 강의실별 관측 단말 시각화
- 더미 모드에서 강의실별 단말 관측 입력값 제어
- 더미 overlay reset / baseline 복구

# 수용 기준

- 관리자 기능은 일반 학생 / 교수 기능과 분리된 권한 체계를 사용해야 한다.
- 강의실과 강의 시간표 정보는 출석 판정에서 재사용 가능한 형태로 관리되어야 한다.
- 강의실별 와이파이 / AP 매핑 정보는 운영 화면에서 조회 및 수정 가능해야 한다.
- 관리자 관제 패널은 기본 관리자 대시보드 / classroom-network 관리 surface 안에 녹아들어야 한다.
- 관리자 관제 패널의 강의실별 관측 단말 시각화는 classroom 목록을 먼저 보여주고, 사용자가 강의실을 선택했을 때 해당 강의실 snapshot 을 lazy loading 해야 한다.
- 강의실 상세에는 AP / 공유기별 현재 관측 단말 목록과 등록 학생 정보(매칭되는 경우)를 함께 보여야 한다.
- 관리자 관제 패널은 기본적으로 PresenceService/Redis 에 있는 최신 snapshot 정보를 표시하고, 사용자가 강의실 단위로 수동 새로고침할 수 있어야 한다.
- 관리자 관제 패널은 강의실별로 10초 자동 새로고침 on/off 를 제공해야 하며, 자동 새로고침은 OpenWrt SSH polling 을 유발하지 않고 Redis snapshot 재조회만 수행해야 한다.
- `강의실 및 네트워크 현황` 은 여러 강의실 카드를 동시에 펼쳐 볼 수 있어야 하며, 다른 강의실을 펼쳐도 기존 펼침 상태를 닫지 않아야 한다.
- demo mode 에서는 실제 OpenWrt AP 와 별개로 demo AP snapshot 을 같은 카드 UI 로 모니터링할 수 있어야 한다.
- demo AP snapshot 은 강의실 단위로 전체 ON/OFF 할 수 있어야 하며, OFF 는 demo 관측 단말을 모두 제거한 상태로 표현한다.
- 더미 제어 기능은 demo mode 전용이어야 하며, 운영 환경 기능처럼 보이게 만들면 안 된다.
- 더미 제어는 판정 결과 override 가 아니라 입력값 조작 방식이어야 한다.
