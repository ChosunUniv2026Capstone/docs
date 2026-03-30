---
title: 재실성 기반 출석 요구사항
type: requirement
status: active
updated: 2026-03-30
owners:
  - backend-team
  - presence-team
related:
  - req-device-auth
  - adr-0003-openwrt-device-collection
  - adr-0004-attendance-authorization-flow
  - adr-0005-presence-snapshot-cache
  - network-topology
source:
  - 06-meetings/raw/2026-03-19-capstone-proposal.md
  - 06-meetings/raw/2026-03-30-presence-logic-clarification.md
---

# 목표

학생의 실제 강의실 인접 여부를 반영하는 재실성 기반 출석 인증 체계를 제공한다.

# 입력 요소

- 수강 정보
- 강의 시간표
- 강의실 정보
- 강의실별 허용 Wi-Fi / AP / 게이트웨이 정보
- 사용자 현재 Wi-Fi 정보
- 공유기 또는 게이트웨이에서 수집한 단말 연결 정보
- 사용자 등록 단말 정보
- 요청 목적(`attendance` 또는 `exam`)

# 핵심 규칙

- 학생은 수업 시간 안에서만 출석 요청을 할 수 있어야 한다.
- 학생은 자신이 수강 중인 강의에만 출석 요청을 할 수 있어야 한다.
- 출석 허용 여부는 강의실 매핑 정보와 네트워크 기반 재실성 판별 결과를 반영해야 한다.
- 등록 단말 여부는 재실성 판별과 함께 출석 조건에 반영해야 한다.
- 재실성 정보가 부족하거나 모순되면 출석은 기본적으로 거부되어야 한다.
- 강의실에는 여러 AP 또는 공유기가 매핑될 수 있어야 한다.
- 재실성 snapshot 은 최근 60초 이내 데이터만 유효해야 한다.
- Presence 정보 수집은 요청 시 수행하되, 짧은 캐시를 통해 재사용할 수 있어야 한다.
- 출석과 시험은 같은 eligibility 가드를 공유하되 목적별 추가 규칙은 분리 가능해야 한다.

# 결과 요구

- 출석 허용 / 거부 결과를 반환해야 한다.
- 거부 시 사유 코드를 남겨야 한다.
- 이후 감사와 분석을 위해 판정 근거를 저장할 수 있어야 한다.
- 어떤 AP 와 어떤 단말 매칭으로 판단했는지 추적 가능해야 한다.

# 수용 기준

- 강의실과 무관한 네트워크에서의 요청은 허용되면 안 된다.
- 미등록 단말 또는 비정상 접속은 별도 사유 코드로 구분되어야 한다.
- Backend 와 PresenceService 의 역할이 문서화된 경계 안에서 유지되어야 한다.
- 강의실에 매핑된 AP 중 하나라도 학생 등록 단말이 관측되면 재실 후보로 판정할 수 있어야 한다.
