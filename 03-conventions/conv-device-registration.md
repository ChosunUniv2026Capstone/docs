---
title: 단말 등록 규약
type: convention
status: active
updated: 2026-03-30
owners:
  - backend-team
applies_to:
  - frontend
  - backend
  - db
related:
  - req-device-auth
  - adr-0004-attendance-authorization-flow
source:
  - 06-meetings/raw/2026-03-30-presence-logic-clarification.md
---

# 식별 기준

- 단말 식별 기준은 MAC 주소 1개다.
- 랜덤 MAC 은 허용하지 않으며, 학생이 OS 설정에서 직접 끄도록 안내한다.

# 등록 규칙

- 학생은 최대 5개의 단말까지 등록할 수 있다.
- 학생은 자신의 단말 목록을 등록하고 삭제할 수 있어야 한다.
- 하나의 MAC 주소는 동시에 여러 학생에게 등록될 수 없다.

# 운영 규칙

- 등록 실패 사유는 사용자에게 이해 가능한 형태로 보여줄 수 있어야 한다.
- 랜덤 MAC 이 의심되면 등록 안내 또는 경고를 제공할 수 있어야 한다.
- 삭제된 단말은 즉시 eligibility 판단 대상에서 제외된다.
