---
title: 학생 기능 요구사항
type: requirement
status: active
updated: 2026-04-09
owners:
  - frontend-team
  - backend-team
related:
  - [[/01-requirements/req-attendance-presence.md]]
  - [[/01-requirements/req-device-auth.md]]
  - [[/02-decisions/adr-0009-attendance-bundle-session-parent.md]]
  - [[/04-architecture/service-map.md]]
  - [[/04-architecture/attendance-workflow-architecture.md]]
  - [[/04-architecture/exam-mvp-contract.md]]
source:
  - [[/06-meetings/raw/2026-03-19-capstone-proposal.md]]
  - [[/06-meetings/raw/2026-03-25-kickoff-work-items.md]]
  - [[/06-meetings/raw/2026-04-07-capstone-demo-planning.md]]
  - [[/02-decisions/adr-0009-attendance-bundle-session-parent.md]]
  - [[/04-architecture/attendance-workflow-architecture.md]]
---

# 목표

학생 사용자가 수강 중인 강의의 학습, 과제, 시험, 출석 관련 기능을 웹에서 수행할 수 있어야 한다.

# 필수 기능

- 회원가입 / 로그인
- 강의 목록 조회
- 수강신청 또는 수강 강의 확인
- 강의영상 시청
- 강의자료 다운로드
- 과제 제출
- 퀴즈 / 시험 응시
- 공지사항 확인
- 공지사항 상세 조회
- 출석 확인 및 출석 요청
- 성적 확인
- 질문게시판 / 문의

# 출석 관련 요구

- 학생은 자신의 수강 강의와 현재 수업 시간에만 출석 요청을 할 수 있어야 한다.
- 출석 요청 시 재실성 판별과 등록 단말 여부를 함께 확인해야 한다.
- 학생은 출석 요청과 별개로 선택 강의의 강의실 기준 인접성 확인을 강의 시간과 관계없이 실행할 수 있어야 한다.
- 인접성 확인 결과는 버튼 아래에 한 줄 요약으로 표시하며, 성공은 `강의실 인접 확인됨`, 실패는 `강의실 인접 확인불가` 로 표현한다.
- 출석 불가 시 사유를 사용자에게 이해 가능한 형태로 반환해야 한다.
- 학생은 열린 출석 세션만 볼 수 있어야 한다.
- 여러 차시가 함께 열린 smart attendance 는 bundle 카드 1개로 보여줘야 한다.
- bundle 카드는 포함된 차시 목록과 공통 남은 시간을 함께 보여줘야 한다.
- 학생은 bundle 당 출석 버튼 1개만 눌러 전체 대상 차시에 대해 self check-in 을 수행해야 한다.
- 학생 self check-in 은 같은 열린 세션에 대해 idempotent 해야 한다.
- 학생이 이미 처리된 bundle 에서 다시 출석을 눌러도 중복 audit 는 생기면 안 되며, 이미 처리된 차시는 success/no-op 로 취급해야 한다.
- 학생 출석 탭에는 학기 전체 출석 결과를 주차 x 차시 표로 보여주는 semester matrix 가 있어야 한다.
- semester matrix 는 상태별로 구분 가능한 시각 표시를 제공해야 한다.

# 시험 관련 요구

- 시험 접근은 로그인 상태를 전제로 한다.
- 재실성 조건이 필요한 시험은 별도 접근 제어 규칙을 적용할 수 있어야 한다.

# 수용 기준

- 학생은 자신의 강의와 무관한 자료나 시험에 접근할 수 없어야 한다.
- 학생은 공지 목록에서 상세 화면으로 이동해 제목, 본문, 작성자, 등록일을 확인할 수 있어야 한다.
- 출석 가능 여부는 수업 시간표, 강의실, 재실성 판별 결과를 반영해야 한다.
- 정상 상태와 실패 상태가 UI 에서 구분 가능해야 한다.
- 열린 세션이 없으면 `SESSION_NOT_OPEN` 으로 거부되어야 한다.
- 이미 성공한 self check-in 을 다시 눌러도 성공 응답은 유지되지만 중복 이력은 생기지 않아야 한다.
- 학생 active attendance UI 는 같은 bundle 의 차시들을 개별 버튼 여러 개로 분리해 보여주면 안 된다.
- bundle 종료 또는 만료가 발생하면 학생 타이머와 버튼 상태가 즉시 갱신되어야 한다.
