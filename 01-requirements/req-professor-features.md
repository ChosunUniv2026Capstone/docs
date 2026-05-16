---
title: 교수 기능 요구사항
type: requirement
status: active
updated: 2026-05-16
owners:
  - frontend-team
  - backend-team
related:
  - [[/01-requirements/req-student-features.md]]
  - [[/01-requirements/req-attendance-presence.md]]
  - [[/02-decisions/adr-0009-attendance-bundle-session-parent.md]]
  - [[/04-architecture/service-map.md]]
  - [[/04-architecture/attendance-workflow-architecture.md]]
  - [[/04-architecture/exam-mvp-contract.md]]
source:
  - [[/06-meetings/raw/2026-03-25-kickoff-work-items.md]]
  - [[/06-meetings/raw/2026-04-07-capstone-demo-planning.md]]
  - [[/02-decisions/adr-0009-attendance-bundle-session-parent.md]]
  - [[/04-architecture/attendance-workflow-architecture.md]]
---

# 목표

교수 사용자는 자신의 강의를 운영하기 위한 학습 자료, 과제, 시험, 공지, 출석, 성적 기능을 사용할 수 있어야 한다.

# 현재 구현 / 유지 기능

- 강의자료 / 동영상 learning item 생성 / 삭제 / 첨부 다운로드
- 과제 생성 / 마감일 설정
- 시험 / 퀴즈 출제
- 학생 제출물 확인
- 공지 작성
- 공지 상세 조회
- 날짜 / 강의실 / 강의 기준 projected slot 조회
- projected slot 기반 bundle session 열기 / 닫기 / 휴강 / 재오픈
- bundle timer / roster / history / report 조회
- 학생 상태 수정 + 사유 입력
- 학생별 차시 이력 조회
- 학기 전체 출석 타임라인 조회
- 출석 리포트 / 대시보드 조회

# 선택 구현 대상

- 채점 / 피드백
- 출석과 별개의 학습 진도율 확인
- 성적 관리
- 질문게시판 / 문의 답변

# 후속 backlog

- 회원가입 / 계정 생성 self-service
- 수강신청 / 승인 workflow
- 전체 LMS / 관리자 CRUD 로의 확장

# 출석 운영 요구

- 교수는 자신이 담당하는 강의의 시간표에서 파생된 30분 차시만 열 수 있어야 한다.
- 교수는 같은 projected slot 에 중복된 active 출석 세션을 만들 수 없어야 한다.
- 교수는 같은 주차 안의 여러 차시를 동시에 선택해 같은 운영 모드(일반출석 / 스마트출석 / 휴강)를 적용할 수 있어야 한다.
- 여러 차시를 동시에 시작한 경우에도 내부적으로는 bundle session 1개만 생성되어야 한다.
- smart bundle 은 선택 차시 수와 무관하게 공유 10분 타이머 1개만 사용해야 한다.
- 교수의 close / expire / cancel / reopen 동작은 bundle 전체에 한 번에 적용되어야 한다.
- bundle roster 는 선택된 slot 목록을 요약해서 보여주고 학생 상태 변경은 기본적으로 bundle 대상 차시 전체에 fan-out 적용해야 한다.
- bundle roster 의 기본값은 anchor slot 기록을 따르고, anchor slot 기록이 없으면 `absent` 를 기본값으로 사용해야 한다.
- 일반출석은 session open 직후 미수정 학생을 `absent` 로 집계해야 한다.
- 스마트출석은 active 동안 미체크 학생을 `pending` 으로 보고, close / expire 시점에만 `absent` 로 확정해야 한다.
- 교수는 상태를 `출석`, `결석`, `지각`, `공가`, `병가` 로 수정할 수 있어야 한다.
- 교수의 상태 변경은 항상 사유를 포함해야 한다.
- 교수의 수동 수정은 audit history 로 남아야 한다.
- 교수는 학생 self check-in 이후에도 최신 판단으로 최종 상태를 덮어쓸 수 있어야 하며, 이전 이력은 남아야 한다.
- bundle overwrite 는 실제 값이 달라진 차시에만 changed-only audit 를 남겨야 한다.
- bundle 화면은 bulk overwrite 도구이며, 개별 차시 예외 수정은 기존 per-slot route 에서 처리할 수 있어야 한다.
- 교수는 스마트출석 시작/종료/만료와 roster, 집계, 리포트 대시보드 상태를 실시간으로 볼 수 있어야 한다.

# 수용 기준

- 교수는 자신이 담당하는 강의 범위 안에서만 운영 기능을 수행할 수 있어야 한다.
- 교수는 자신이 조회 가능한 공지의 상세 내용을 같은 강의 흐름 안에서 확인할 수 있어야 한다.
- 과제와 시험은 시작 / 종료 시점과 대상 강의를 기준으로 제어되어야 한다.
- 출석과 진도율 조회는 강의 단위로 집계 가능해야 한다.
- 교수는 projected slot 을 조회한 뒤 그 slot 에서만 출석 세션을 시작할 수 있어야 한다.
- 교수는 학생별 상태 변경 이력을 시간순으로 확인할 수 있어야 한다.
- 교수는 휴강 처리된 차시와 재오픈된 차시의 이력을 모두 추적할 수 있어야 한다.
- 교수가 multi-slot smart session 을 닫거나 만료시키면 timer / roster / report surface 가 모두 같은 bundle 상태로 즉시 수렴해야 한다.
- 교수는 bundle 화면과 별개로 projection-key 기준 예외 수정 경로를 계속 사용할 수 있어야 한다.
- 교수 출석 운영 대시보드에는 현재 선택 과목의 학기 전체를 기준으로 학생별 출석/지각/결석/공결 누계를 보여주는 학생별 통계 버튼과 표가 있어야 한다.
