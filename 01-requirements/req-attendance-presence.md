---
title: 재실성 기반 출석 요구사항
type: requirement
status: active
updated: 2026-05-16
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
  - [[/02-decisions/adr-0009-attendance-bundle-session-parent.md]]
  - [[/04-architecture/network-topology.md]]
  - [[/04-architecture/attendance-workflow-architecture.md]]
source:
  - [[/06-meetings/raw/2026-03-19-capstone-proposal.md]]
  - [[/06-meetings/raw/2026-03-30-presence-logic-clarification.md]]
  - [[/06-meetings/raw/2026-04-07-capstone-demo-planning.md]]
  - [[/02-decisions/adr-0007-demo-presence-overlay-and-attendance-session-flow.md]]
  - [[/02-decisions/adr-0009-attendance-bundle-session-parent.md]]
  - [[/04-architecture/attendance-workflow-architecture.md]]
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
- 재실성 snapshot 은 soft TTL `3초`, hard TTL `30초` 를 가져야 한다.
- Presence 정보 수집은 요청 시 수행하되, 짧은 캐시를 통해 재사용할 수 있어야 한다.
- soft TTL 이후 refresh 는 cache key 또는 OpenWrt/AP target 단위 refresh lock 으로 보호되어야 하며, lock 이 이미 잡혀 있으면 중복 OpenWrt 수집을 시작하면 안 된다.
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
- 교수 출석 UI 는 학기 전체 수업 날짜를 주차별로 구분하고, 각 주 안에서는 30분 단위 차시를 한 줄씩 표시해야 한다.
- 각 차시는 상태 아이콘, 차시 표기, 교수 정보, 출석/지각/결석/공결 집계를 함께 보여줘야 한다.
- 미체크 차시에서 교수는 `일반출석`, `스마트출석`, `휴강` 중 하나를 선택해 출석 운영을 시작할 수 있어야 한다.
- 같은 주차 안에서는 여러 projected slot 을 동시에 선택해 일괄 처리할 수 있어야 한다.
- 여러 projected slot 을 한 번에 선택해 시작한 경우에도 내부 lifecycle authority 는 `bundle session` 1개여야 한다.
- bundle session 은 선택된 slot 목록, 공통 타이머, 공통 close/expire 상태를 하나의 묶음으로 소유해야 한다.
- 학생 출석 성공 조건은 아래 두 가지를 동시에 만족해야 한다.
  1. 교수의 출석 세션이 열려 있다.
  2. 현재 재실 판정이 eligible 이다.
- 학생 화면은 열린 smart bundle 을 차시별 카드 여러 개가 아니라 bundle 카드 1개로 보여줘야 한다.
- 학생의 bundle check-in 1회는 bundle 대상 차시 전체에 fan-out 적용되어야 한다.
- 교수는 출석 상태를 `출석`, `결석`, `지각`, `공가`, `병가` 로 수정할 수 있어야 한다.
- 교수의 수동 상태 변경에는 항상 사유가 포함되어야 한다.
- bundle roster 편집 기본값은 선택 anchor slot 기준으로 로드해야 하며, anchor slot 기록이 없으면 `결석(absent)` 을 기본값으로 사용해야 한다.
- 일반출석은 세션을 시작한 직후부터 미수정 학생을 `결석(absent)` 으로 간주해야 한다.
- 스마트출석은 진행 중 미체크 학생을 `pending` 으로 간주하고, 교수 종료 또는 만료 시점에만 `결석(absent)` 으로 확정해야 한다.
- 학생의 첫 self check-in 과 교수의 수동 수정은 모두 변경 이력으로 남아야 한다.
- 같은 열린 세션에 대한 학생의 반복 self check-in 은 idempotent 해야 하며, 추가적인 `present` 이력 중복이 생기면 안 된다.
- bundle overwrite 는 대상 차시 전체에 동일 상태를 적용하되, 실제 값이 바뀐 차시에만 audit row 를 남겨야 한다.
- 최신 교수 수정값이 최종 출석 상태(source of truth) 가 되어야 하며, 이전 self check-in / 수동 수정 이력은 삭제되면 안 된다.
- 스마트출석은 서버 기준 10분 활성 윈도우를 가져야 하며, 학생 화면에는 남은 시간과 출석 버튼 활성 상태가 실시간으로 보여야 한다.
- 교수 화면의 slot 상태, roster, 집계와 리포트 대시보드는 학생 화면과 같은 최종 상태로 실시간 동기화되어야 한다.

# 결과 요구

- 출석 허용 / 거부 결과를 반환해야 한다.
- 거부 시 사유 코드를 남겨야 한다.
- 이후 감사와 분석을 위해 판정 근거를 저장할 수 있어야 한다.
- 어떤 AP 와 어떤 단말 매칭으로 판단했는지 추적 가능해야 한다.
- 출석 상태 변경 이력에는 actor, reason, changed_at, previous_status, new_status 가 포함되어야 한다.
- bundle session 이 포함한 slot membership 과 anchor projection key 를 추적할 수 있어야 한다.
- 출석 리포트 / 대시보드 집계는 attendance record 의 최종 상태를 기준으로 계산되어야 한다.

# 수용 기준

- 강의실과 무관한 네트워크에서의 요청은 허용되면 안 된다.
- 미등록 단말 또는 비정상 접속은 별도 사유 코드로 구분되어야 한다.
- Backend 와 PresenceService 의 역할이 문서화된 경계 안에서 유지되어야 한다.
- 강의실에 매핑된 AP 중 하나라도 학생 등록 단말이 관측되면 재실 후보로 판정할 수 있어야 한다.
- 관리자는 더미 모드에서 특정 학생/단말의 재실 입력값을 바꾼 뒤 학생 화면에서 eligibility 결과가 바뀌는 것을 시연할 수 있어야 한다.
- 관리자 패널은 `사용자 현황`, `강의실 및 네트워크 현황`, `재실 시연 제어(demo)` 탭으로 분리되어야 한다.
- `강의실 및 네트워크 현황` 의 관측 시각은 시:분:초까지 표시되어야 한다.
- 교수는 날짜와 차시 기준으로 출석 세션을 열고 학생 roster 와 상태 변경 이력을 조회할 수 있어야 한다.
- 교수는 학생별 전체 출석 이력을 UI 에서 삭제 없이 조회할 수 있어야 한다.
- 스마트출석 시작/만료/교수 수정 이후 학생/교수/리포트 화면이 새로고침 없이 같은 최종 상태로 수렴해야 한다.
- 학생 출석 탭에는 학기 전체 차시를 주차 x 차시 표로 요약한 semester matrix 가 있어야 하며, 확정 상태는 색상으로 표시되어야 한다.
- 교수 출석 운영 대시보드에는 현재 과목 기준 학생별 출석/지각/결석/공결 누계를 표로 보여주는 학생별 통계 화면이 있어야 한다.
- 학생 active attendance 화면에는 여러 slot 이 열려 있어도 bundle 단위 버튼 1개만 보여야 한다.
- bundle 종료 또는 만료 시 교수/학생 타이머는 둘 다 즉시 멈춰야 한다.
- 학생은 열린 세션이 아닐 때 `SESSION_NOT_OPEN` 으로 거부되어야 한다.
- 교수가 허용되지 않은 시간표 밖 차시를 열려고 하면 `SESSION_SLOT_INVALID` 로 거부되어야 한다.
- 같은 projection_key 에 이미 active session 이 있으면 `SESSION_ALREADY_OPEN` 으로 거부되어야 한다.
- 열린 세션이 있어도 재실 판정이 부적합하면 `PRESENCE_INELIGIBLE` 로 거부되어야 한다.
- 교수가 상태 변경 사유 없이 수동 수정하려고 하면 `ATTENDANCE_REASON_REQUIRED` 로 거부되어야 한다.
- bundle 화면과 별도로 projection-key 기반 예외 수정 경로가 유지되어야 한다.
