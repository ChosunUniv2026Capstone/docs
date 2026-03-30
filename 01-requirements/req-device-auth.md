---
title: 단말 인증 요구사항
type: requirement
status: active
updated: 2026-03-30
owners:
  - backend-team
  - presence-team
related:
  - [[/01-requirements/req-attendance-presence.md]]
  - [[/02-decisions/adr-0003-openwrt-device-collection.md]]
  - [[/02-decisions/adr-0004-attendance-authorization-flow.md]]
  - [[/02-decisions/adr-0005-presence-snapshot-cache.md]]
source:
  - [[/06-meetings/raw/2026-03-19-capstone-proposal.md]]
  - [[/06-meetings/raw/2026-03-30-presence-logic-clarification.md]]
---

# 목표

사용자별 등록 단말을 기준으로 접속 기기를 식별하고 비정상 접속 시도를 판별할 수 있어야 한다.

# 핵심 요구

- 사용자별 등록 단말 정보를 관리할 수 있어야 한다.
- 수집된 단말 정보와 사용자 등록 단말 정보를 비교할 수 있어야 한다.
- 미등록 단말, 중복 단말, 비정상 접속 시도를 구분할 수 있어야 한다.
- 단말 판별 결과는 출석 및 시험 접근 제어에 재사용 가능해야 한다.
- 단말 식별 기준은 단말별 MAC 주소 1개를 사용한다.
- 학생은 최대 5개의 단말까지 등록할 수 있어야 한다.
- 학생은 자신의 등록 단말을 직접 등록하고 삭제할 수 있어야 한다.
- 하나의 단말 MAC 은 동시에 여러 학생에게 등록될 수 없어야 한다.

# 운영 요구

- 학생은 랜덤 MAC 을 직접 끄도록 안내받아야 한다.
- 단말 등록과 변경 절차는 추후 UX 와 정책으로 구체화하되, 데이터 모델은 이를 수용할 수 있어야 한다.
- 개인정보와 보안 영향을 고려해 단말 식별자 저장 정책을 별도 검토해야 한다.

# 수용 기준

- 사용자 요청 시 현재 접속 단말이 등록 단말인지 판별 가능해야 한다.
- 등록 단말 매칭 실패와 네트워크 불일치를 별도 상태로 구분해야 한다.
- 등록 가능한 단말 수 제한을 초과하면 추가 등록이 거부되어야 한다.
- 같은 MAC 을 다른 학생이 등록하려고 하면 거부되어야 한다.
