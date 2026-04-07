---
title: 재실성 기반 출석 요구사항
type: requirement
status: active
updated: 2026-04-07
owners:
  - backend-team
  - presence-team
  - frontend-team
related:
  - [[/01-requirements/req-device-auth.md]]
  - [[/01-requirements/req-student-features.md]]
  - [[/01-requirements/req-professor-features.md]]
  - [[/01-requirements/req-admin-features.md]]
  - [[/02-decisions/adr-0003-openwrt-device-collection.md]]
  - [[/02-decisions/adr-0004-attendance-authorization-flow.md]]
  - [[/02-decisions/adr-0005-presence-snapshot-cache.md]]
  - [[/02-decisions/adr-0007-demo-presence-overlay-and-attendance-session-flow.md]]
  - [[/04-architecture/network-topology.md]]
  - [[/04-architecture/attendance-workflow-architecture.md]]
source:
  - [[/06-meetings/raw/2026-03-19-capstone-proposal.md]]
  - [[/06-meetings/raw/2026-03-30-presence-logic-clarification.md]]
  - [[/06-meetings/raw/2026-04-07-capstone-demo-planning.md]]
---

# 목표

학생의 실제 강의실 인접 여부를 반영하는 재실성 기반 출석 인증 체계를 제공하고,
교수의 출석 운영 흐름과 관리자 데모 제어 흐름까지 포함한 캡스톤 시연이 가능해야 한다.

# 입력 요소

- 수강 정보
- 강의 시간표
- 강의실 정보
- 강의실별 허용 Wi-Fi / AP / 게이트웨이 정보
- 사용자 현재 Wi-Fi 정보
- 공유기 또는 게이트웨이에서 수집한 단말 연결 정보
- 사용자 등록 단말 정보
- 요청 목적(`attendance` 또는 `exam`)
- 교수의 출석 세션 오픈 상태
- 출석 대상 날짜와 30분 단위 차시 정보

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

# 캡스톤 데모용 추가 규칙

- 관리자 화면에는 **더미 모드 전용** 재실 제어 패널이 있어야 한다.
- 더미 제어 패널은 학생의 재실성 입력값을 바꿔 eligibility 결과가 자연스럽게 변하는 장면을 보여줄 수 있어야 한다.
- 더미 제어는 판정 결과를 직접 override 하면 안 되고, 입력되는 AP / 연결 상태 / 단말 관측 상태를 바꾸는 방식이어야 한다.
- 학생 재실 확인 화면은 현재 보고 있는 강의 기준으로 자동 확인되어야 하며, 강의 / 강의실 / 목적 입력칸을 별도로 노출하지 않아야 한다.
- Backend 는 학생이 선택한 현재 강의 기준으로 classroom 을 결정해야 하며, 프론트가 보낸 classroom 입력값을 신뢰하면 안 된다.
- 관리자 재실 제어는 학생 목록이 아니라 디바이스 선택 중심으로 구성되어야 한다.
- 디바이스 선택은 학번, 이름, 기기이름, MAC 을 함께 보여주는 드롭다운이어야 한다.
- AP 별 신호세기 threshold 는 관리자 패널에서 수정 가능해야 하며 DB 에 저장되어야 한다.
- AP threshold 가 비어 있으면 fallback `-65 dBm` 을 사용한다.
- 재실 허용은 연결 상태와 신호세기 기준을 함께 만족해야 한다.
- 교수는 강의 / 날짜 / 차시 기준으로 출석 세션을 열 수 있어야 한다.
- 학생 출석 성공 조건은 아래 두 가지를 동시에 만족해야 한다.
  1. 교수의 출석 세션이 열려 있다.
  2. 현재 재실 판정이 eligible 이다.
- 교수는 출석 상태를 `출석`, `결석`, `지각`, `공가`, `병가` 로 수정할 수 있어야 한다.
- 학생의 첫 self check-in 과 교수의 수동 수정은 모두 변경 이력으로 남아야 한다.
- 같은 열린 세션에 대한 학생의 반복 self check-in 은 idempotent 해야 하며, 추가적인 `present` 이력 중복이 생기면 안 된다.

# 결과 요구

- 출석 허용 / 거부 결과를 반환해야 한다.
- 거부 시 사유 코드를 남겨야 한다.
- 이후 감사와 분석을 위해 판정 근거를 저장할 수 있어야 한다.
- 어떤 AP 와 어떤 단말 매칭으로 판단했는지 추적 가능해야 한다.
- 출석 상태 변경 이력에는 actor, reason, changed_at, previous_status, new_status 가 포함되어야 한다.

# 수용 기준

- 강의실과 무관한 네트워크에서의 요청은 허용되면 안 된다.
- 미등록 단말 또는 비정상 접속은 별도 사유 코드로 구분되어야 한다.
- Backend 와 PresenceService 의 역할이 문서화된 경계 안에서 유지되어야 한다.
- 강의실에 매핑된 AP 중 하나라도 학생 등록 단말이 관측되면 재실 후보로 판정할 수 있어야 한다.
- 관리자는 더미 모드에서 특정 학생/단말의 재실 입력값을 바꾼 뒤 학생 화면에서 eligibility 결과가 바뀌는 것을 시연할 수 있어야 한다.
- 관리자 패널은 `사용자 현황`, `강의실 및 네트워크 현황`, `재실 시연 제어(demo)` 탭으로 분리되어야 한다.
- `강의실 및 네트워크 현황` 의 관측 시각은 시:분:초까지 표시되어야 한다.
- 교수는 날짜와 차시 기준으로 출석 세션을 열고 학생 roster 와 상태 변경 이력을 조회할 수 있어야 한다.
- 학생은 열린 세션이 아닐 때 `SESSION_NOT_OPEN` 으로 거부되어야 한다.
- 교수가 허용되지 않은 시간표 밖 차시를 열려고 하면 `SESSION_SLOT_INVALID` 로 거부되어야 한다.
- 열린 세션이 있어도 재실 판정이 부적합하면 `PRESENCE_INELIGIBLE` 로 거부되어야 한다.
