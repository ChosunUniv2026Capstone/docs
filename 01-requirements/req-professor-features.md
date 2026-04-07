---
title: 교수 기능 요구사항
type: requirement
status: active
updated: 2026-04-07
owners:
  - frontend-team
  - backend-team
related:
  - [[/01-requirements/req-student-features.md]]
  - [[/01-requirements/req-attendance-presence.md]]
  - [[/04-architecture/service-map.md]]
  - [[/04-architecture/attendance-workflow-architecture.md]]
source:
  - [[/06-meetings/raw/2026-03-25-kickoff-work-items.md]]
  - [[/06-meetings/raw/2026-04-07-capstone-demo-planning.md]]
---

# 목표

교수 사용자는 자신의 강의를 운영하기 위한 학습 자료, 과제, 시험, 공지, 출석, 성적 기능을 사용할 수 있어야 한다.

# 필수 기능

- 강의자료 업로드
- 동영상 업로드
- 과제 생성 / 마감일 설정
- 시험 / 퀴즈 출제
- 학생 제출물 확인
- 채점 / 피드백
- 공지 작성
- 공지 상세 조회
- 출석 / 진도율 확인
- 성적 관리
- 날짜 / 강의실 / 강의 기준 projected slot 조회
- projected slot 기반 출석 세션 열기 / 닫기
- 학생 roster 조회
- 학생 상태 수정 + 사유 입력
- 학생별 차시 이력 조회

# 출석 운영 요구

- 교수는 자신이 담당하는 강의의 시간표에서 파생된 30분 차시만 열 수 있어야 한다.
- 교수는 같은 projected slot 에 중복된 active 출석 세션을 만들 수 없어야 한다.
- 교수는 상태를 `출석`, `결석`, `지각`, `공가`, `병가` 로 수정할 수 있어야 한다.
- 교수의 상태 변경은 항상 사유를 포함해야 한다.
- 교수의 수동 수정은 audit history 로 남아야 한다.

# 수용 기준

- 교수는 자신이 담당하는 강의 범위 안에서만 운영 기능을 수행할 수 있어야 한다.
- 교수는 자신이 조회 가능한 공지의 상세 내용을 같은 강의 흐름 안에서 확인할 수 있어야 한다.
- 과제와 시험은 시작 / 종료 시점과 대상 강의를 기준으로 제어되어야 한다.
- 출석과 진도율 조회는 강의 단위로 집계 가능해야 한다.
- 교수는 projected slot 을 조회한 뒤 그 slot 에서만 출석 세션을 시작할 수 있어야 한다.
- 교수는 학생별 상태 변경 이력을 시간순으로 확인할 수 있어야 한다.
