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
- 인증은 JWT 기반 access / refresh 분리 구조를 기본으로 한다.

# 최소 흐름

1. 사용자는 로그인한다.
2. 로그인된 사용자는 일반 LMS 기능에 접근한다.
3. 출석 또는 시험 접근 시 Backend 가 추가 조건을 검증한다.
4. 필요 시 PresenceService 결과와 단말 등록 상태를 결합해 허용 여부를 결정한다.

# 규칙

- 보호 API 는 인증된 사용자만 호출할 수 있어야 한다.
- 역할 기반 권한은 학생 / 교수 / 관리자 구분을 유지해야 한다.
- 단말 등록 상태는 로그인 상태와 별도 정보로 취급한다.
- access token 은 짧은 만료를 가지는 bearer JWT 여야 한다.
- refresh token 은 `HttpOnly + Secure` cookie 로만 보관해야 한다.
- Front 는 refresh token 원문을 읽거나 저장하면 안 된다.
- refresh / bootstrap 은 로그인 상태 복구용이며, 출석/시험 접근 권한 자체를 자동 부여하면 안 된다.
- cookie 기반 복구를 쓰는 경로는 Front `credentials: include` 와 Backend explicit origin + `allow_credentials=true` 조합을 따라야 한다.
- reusable auth helper 를 통해 guard 를 공통화해야 한다.
  - `require_admin_role`
  - `require_professor_course_ownership`
  - `require_student_self`
- 기존 demo-critical legacy route 는 payload / path / token format 을 깨지 않고 server-side auth enforcement 를 강화한다.
- login / health endpoint 는 공개로 유지한다.

# 라우팅 / 복구 규칙

- 주요 화면은 실제 path 기반 route 로 표현해야 한다.
- 새로고침 후에는 refresh/bootstrap 으로 로그인 상태와 현재 route 를 복구할 수 있어야 한다.
- 브라우저 뒤로가기 / 앞으로가기는 실제 page navigation 처럼 동작해야 한다.
- 학생은 자신이 수강 중인 강의 route 만 접근할 수 있어야 한다.
- 교수는 자신이 담당하는 강의 route 만 접근할 수 있어야 한다.
- route 권한 체크는 프론트 힌트에만 의존하면 안 되고 Backend 가 최종 판단해야 한다.

# 출석 세션 규칙

- 교수는 자신이 소유한 강의의 projected slot 에 대해서만 session 을 열 수 있다.
- 교수는 session open / close / cancel / reopen / roster mutation 모두 자신이 소유한 강의 범위 안에서만 수행할 수 있다.
- 학생은 자기 자신의 open session 에 대해서만 self check-in 을 수행할 수 있다.
- student self check-in 은 idempotent 해야 하며, 권한 검증을 우회한 duplicate update 가 생기면 안 된다.
- websocket subscriber 권한도 같은 원칙을 따라야 한다.
  - 학생은 자기 자신의 active / recent attendance state 만 구독할 수 있다.
  - 교수는 자신이 소유한 강의 / session channel 만 구독할 수 있다.
  - 관리자/리포트 권한은 명시된 surface 에 한정해야 한다.
- reconnect 후 websocket 재인증도 같은 scope 규칙을 다시 만족해야 한다.
