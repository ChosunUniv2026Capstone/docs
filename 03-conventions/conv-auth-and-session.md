---
title: 인증과 세션 규약
type: convention
status: active
updated: 2026-04-07
owners:
  - backend-team
applies_to:
  - frontend
  - backend
  - presence
related:
  - [[/01-requirements/req-device-auth.md]]
  - [[/01-requirements/req-attendance-presence.md]]
  - [[/02-decisions/adr-0004-attendance-authorization-flow.md]]
  - [[/02-decisions/adr-0007-demo-presence-overlay-and-attendance-session-flow.md]]
source:
  - [[/06-meetings/raw/2026-03-19-capstone-proposal.md]]
  - [[/06-meetings/raw/2026-04-07-capstone-demo-planning.md]]
---

# 기본 원칙

- 로그인 인증과 출석 / 시험 접근 인증은 분리한다.
- 일반 로그인 성공만으로 출석이나 시험 접근이 자동 허용되면 안 된다.
- 출석과 시험은 추가 도메인 조건을 검증한다.

# 최소 흐름

1. 사용자는 로그인한다.
2. 로그인된 사용자는 일반 LMS 기능에 접근한다.
3. 출석 또는 시험 접근 시 Backend 가 추가 조건을 검증한다.
4. 필요 시 PresenceService 결과와 단말 등록 상태를 결합해 허용 여부를 결정한다.

# 규칙

- 보호 API 는 인증된 사용자만 호출할 수 있어야 한다.
- 역할 기반 권한은 학생 / 교수 / 관리자 구분을 유지해야 한다.
- 단말 등록 상태는 로그인 상태와 별도 정보로 취급한다.
- reusable auth helper 를 통해 guard 를 공통화해야 한다.
  - `require_admin_role`
  - `require_professor_course_ownership`
  - `require_student_self`
- 기존 demo-critical legacy route 는 payload / path / token format 을 깨지 않고 server-side auth enforcement 를 강화한다.
- login / health endpoint 는 공개로 유지한다.

# 출석 세션 규칙

- 교수는 자신이 소유한 강의의 projected slot 에 대해서만 session 을 열 수 있다.
- 학생은 자기 자신의 open session 에 대해서만 self check-in 을 수행할 수 있다.
- student self check-in 은 idempotent 해야 하며, 권한 검증을 우회한 duplicate update 가 생기면 안 된다.
