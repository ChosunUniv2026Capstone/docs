---
title: 주요 코드 설명
type: report-section
status: draft
updated: 2026-04-12
owners:
  - team
related:
  - [[/04-architecture/service-map.md]]
  - [[/04-architecture/attendance-workflow-architecture.md]]
source:
  - Front/src/App.tsx
  - Front/src/api.ts
  - Front/src/router.ts
  - Backend/app/main.py
  - Backend/app/attendance.py
  - Backend/app/auth.py
  - Backend/app/services.py
  - PresenceService/app/service.py
  - DB/postgres/init/001_schema.sql
  - DB/postgres/init/013_exam_schema.sql
---

# 14. 주요 코드 설명

이 장은 전체 소스코드를 그대로 붙여넣는 대신, 평가자가 설계 의도를 이해하는 데 필요한 핵심 코드 단위를 설명한다.
최종보고서에서는 각 코드 설명에 실제 line reference 또는 짧은 핵심 snippet 을 추가한다.

# 14.1 Front

## `Front/src/api.ts`

역할:

- Backend API request wrapper
- 인증 실패 시 refresh 재시도
- 학생/교수/서비스관리자 기능별 API client 함수 제공
- Attendance, Exam, Device, Notice, Admin Presence 타입 정의

핵심 설계:

- API response shape 를 TypeScript type 으로 고정한다.
- access token 만료 시 refresh path 를 재시도한다.
- UI 컴포넌트는 raw `fetch` 대신 `api.*` 함수를 사용한다.

## `Front/src/router.ts`

역할:

- path 기반 route parsing/building
- course detail, attendance, exam take route 해석
- 새로고침/뒤로가기/앞으로가기에서 화면 상태 복구

핵심 설계:

- route state 를 브라우저 URL 과 동기화한다.
- attendance route 는 timeline/timer/roster 같은 하위 page 를 표현한다.
- exam take route 는 `/courses/{courseCode}/exams/{examId}/take` 형태를 사용한다.

## `Front/src/App.tsx`

역할:

- 로그인/세션 bootstrap
- 역할별 hydration
- 학생/교수/서비스관리자 화면 렌더링
- 출석/시험/공지/단말/서비스관리자 상태 관리

핵심 설계:

- 학생, 교수, 서비스관리자 역할별로 필요한 데이터를 따로 hydrate 한다.
- 출석과 시험은 course detail 안에서 독립 섹션으로 동작한다.
- 관리자 demo overlay 는 PresenceService 를 직접 호출하지 않고 Backend API 를 통해 조작한다.

# 14.2 Backend

## `Backend/app/main.py`

역할:

- FastAPI app 생성
- 인증/강의/공지/단말/서비스관리자/출석/시험 endpoint 정의
- WebSocket broker 관리
- PresenceService client 와 도메인 service 연결

핵심 설계:

- route 마다 현재 사용자와 path resource owner 를 검증한다.
- 출석 관련 route 는 stale attendance session expire 를 먼저 처리한 뒤 timeline/report 를 반환한다.
- WebSocket 은 course/view 기준으로 권한 검사를 거친 연결만 허용한다.

## `Backend/app/attendance.py`

역할:

- 출석 timeline/report/student-stats 생성
- attendance session open/close/check-in/update 처리
- audit event payload 구성

핵심 설계:

- projected slot 을 기반으로 출석 가능 차시를 계산한다.
- bundle parent session 과 slot membership 을 분리한다.
- record final state 와 audit history 를 구분한다.

## `Backend/app/services.py`

역할:

- 사용자/강의/공지/단말/시험 등 LMS 도메인 query/update
- 시험 생성/게시/응시/답안 저장/제출 정책 처리

핵심 설계:

- 교수 소유권은 course professor 관계에서 파생한다.
- 학생 시험 시작은 상태/시간/attempt/device 조건을 확인한다.
- 공지/강의/단말 기능은 role guard 를 통해 접근 범위를 제한한다.

# 14.3 PresenceService

## `PresenceService/app/service.py`

역할:

- classroom snapshot 조회/생성
- Redis cache/refresh lock 사용
- demo overlay 적용/초기화
- registered device 와 station observation 비교
- eligibility reasonCode 생성

핵심 설계:

- snapshot cache hit 를 우선 사용한다.
- overlay 는 baseline snapshot 위에 merge 된다.
- 단말이 관측되어도 AP threshold 를 만족하지 못하면 eligible 이 아니다.
- PresenceService 는 network/device 근거만 반환하고 LMS 최종 판단은 하지 않는다.

# 14.4 DB

## `DB/postgres/init/001_schema.sql`

역할:

- 사용자, 강의, 강의실, 공지, 단말, 인증 세션, 출석 스키마 정의

핵심 설계:

- `registered_devices.mac_address` 는 unique 다.
- `attendance_session_slots` 는 bundle parent 아래 slot membership 을 저장한다.
- `attendance_records` 는 slot-aware unique key 를 가진다.
- `attendance_status_audit_logs` 는 변경 이력을 append-only 로 남긴다.

## `DB/postgres/init/013_exam_schema.sql`

역할:

- 시험, 문항, 선택지, 응시, 답안 스키마 정의

핵심 설계:

- 시험은 course 에 속한다.
- answer 는 submission/question/option 의 같은 exam 소속성을 제약한다.
- 진행 중 submission 은 학생/시험 기준 하나만 유지한다.
