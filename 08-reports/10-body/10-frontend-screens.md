---
title: Front End 화면 설계 및 캡처 계획
type: report-section
status: draft
updated: 2026-04-12
owners:
  - frontend-team
related:
  - [[/01-requirements/req-student-features.md]]
  - [[/01-requirements/req-professor-features.md]]
  - [[/01-requirements/req-admin-features.md]]
source:
  - Front/src/App.tsx
  - Front/src/api.ts
  - Front/tests/e2e/auth-routing.spec.ts
  - Front/tests/e2e/exam-workflow.spec.ts
  - Front/tests/e2e/presence-demo.spec.ts
---

# 10. Front End 화면 설계 및 캡처 계획

# 10.1 Front End 구조

Front End 는 React + Vite 기반 단일 앱이다.
`src/App.tsx` 가 주요 화면 상태와 역할별 UI 흐름을 관리하고, `src/api.ts` 가 Backend API client 와 타입을 담당한다.
`src/router.ts` 는 로그인 이후 course detail, attendance, exam take route 를 path 기반으로 해석한다.

# 10.2 공통 화면

| 화면 | 설명 | 캡처 파일 |
|---|---|---|
| 로그인 | 학생/교수/서비스관리자 계정 로그인 | `assets/screenshots/01-login.png` |
| 세션 복구 | 새로고침 후 bootstrap 으로 사용자/권한 복구 | 역할별 대시보드 캡처에 포함 (`assets/screenshots/student-01-dashboard.png`, `assets/screenshots/professor-01-dashboard.png`) |
| 대시보드 | 로그인 사용자 역할별 첫 화면 | `assets/screenshots/student-01-dashboard.png`, `assets/screenshots/professor-01-dashboard.png`, `assets/screenshots/admin-01-users.png` |
| 프로필 | 계정 정보와 학생 단말 관리 진입 | `assets/screenshots/student-02-profile-devices.png`, `assets/screenshots/professor-02-profile.png` |

# 10.3 학생 화면

| 화면 | 주요 기능 | 캡처 파일 |
|---|---|---|
| 학생 강의 목록 | 수강 강의 조회 | `assets/screenshots/student-01-dashboard.png` |
| 강의 상세/공지 | 공지 목록 및 상세 | `assets/screenshots/student-03-course-home.png`, `assets/screenshots/student-05-notices.png`, `assets/screenshots/student-06-notice-detail.png` |
| 단말 관리 | 단말 MAC 등록/삭제/목록 | `assets/screenshots/student-02-profile-devices.png` |
| eligibility 확인 | 출석/시험 접근 가능 여부와 사유 확인 | `assets/screenshots/student-08-eligibility-result.png` |
| 출석 active sessions | 열린 출석 세션 목록 | `assets/screenshots/student-07-attendance-before-check.png` |
| 출석 self check-in | bundle session 출석 요청 결과 | `assets/screenshots/student-09-check-in-result.png` |
| 출석 학기 매트릭스 | 차시별 최종 출석 상태 | `assets/screenshots/student-07-attendance-before-check.png` |
| 시험 목록 | 강의별 시험 목록 | `assets/screenshots/student-10-exam-list.png` |
| 시험 응시 | 문항 풀이, 답안 저장, 제출 | `assets/screenshots/student-11-exam-taking.png`, `assets/screenshots/student-12-exam-answer-selected.png` |
| 자료/동영상 스캐폴드 | 임시 강의자료/영상 UI | `assets/screenshots/student-04-learning-content.png` |

# 10.4 교수 화면

| 화면 | 주요 기능 | 캡처 파일 |
|---|---|---|
| 교수 강의 목록 | 담당 강의 조회 | `assets/screenshots/professor-01-dashboard.png` |
| 공지 작성 | 담당 강의 공지 작성 | `assets/screenshots/professor-06-course-manage-notice-form.png` |
| 시험 관리 | 시험 목록, 초안 생성/수정 | `assets/screenshots/professor-07-exam-manage.png`, `assets/screenshots/professor-08-exam-detail.png` |
| 시험 게시/종료 | 시험 상태 변경 | 최종보고 전 추가 권장 |
| 출석 타임라인 | projected slot / bundle session 타임라인 | `assets/screenshots/professor-09-attendance-timeline.png` |
| 출석 열기 모달 | manual/smart/canceled mode 선택 | 스마트 세션 생성 결과는 `assets/screenshots/professor-11-attendance-timer.png` 로 확인, 모달 자체는 최종보고 전 추가 권장 |
| 출석 타이머 | active smart session timer | `assets/screenshots/professor-11-attendance-timer.png` |
| 출석 roster | 학생별 상태 수정/사유 입력 | `assets/screenshots/professor-12-attendance-roster.png`, `assets/screenshots/professor-13-attendance-slot-roster.png` |
| 학생별 이력 | 학생 차시별 변경 이력 | 최종보고 전 추가 권장 |
| 출석 리포트 | aggregate / student stats | `assets/screenshots/professor-10-attendance-student-stats.png` |

# 10.5 서비스관리자 화면

| 화면 | 주요 기능 | 캡처 파일 |
|---|---|---|
| 사용자 목록 | 학생/교수/서비스관리자 조회 | `assets/screenshots/admin-01-users.png` |
| 강의실 목록 | 강의실 정보 조회 | `assets/screenshots/admin-02-classrooms-networks.png` |
| AP 매핑 | classroom_networks 조회/threshold 수정 | `assets/screenshots/admin-02-classrooms-networks.png` |
| 재실성 snapshot | 강의실별 AP/station 상태 확인 | `assets/screenshots/admin-02-classrooms-networks.png` |
| demo overlay | 더미 재실성 입력값 조작 | `assets/screenshots/admin-03-presence-demo-control.png`, `assets/screenshots/admin-04-presence-demo-applied.png` |
| OpenWrt 장비 관리 | 장비 등록/토큰/상태 확인 | 현재 main 기준 화면 없음, 구현 후 촬영 |

# 10.6 화면 설계 원칙

- 학생은 “내가 무엇을 해야 하는지”와 “왜 실패했는지”를 즉시 이해해야 한다.
- 교수는 출석 세션 열기, 확인, 수정, 리포트 조회를 수업 중 빠르게 수행할 수 있어야 한다.
- 서비스관리자는 네트워크/AP/단말 관측 상태를 운영 데이터 관점에서 확인할 수 있어야 한다.
- 데모용 overlay 는 운영 기능처럼 보이지 않도록 demo mode 라벨과 설명을 둔다.

# 10.7 초안 상태

이 문서는 모든 기능 캡처가 들어갈 위치를 먼저 정의한다.
실제 이미지 파일은 2026-04-12 Playwright 캡처 결과로 `08-reports/assets/screenshots/` 아래에 추가되었으며, 아직 남은 일부 실패/완료 상태 화면은 체크리스트에 후속 촬영 항목으로 유지한다.

# 10.8 실제 Playwright 캡처 산출물

아래 이미지는 2026-04-12 에 기존 Docker 컨테이너를 모두 내린 뒤, 현재 워크스페이스 기준 `CodexKit/docker-compose.yml` 스택을 새로 빌드/기동하고 Playwright 로 촬영한 화면이다.
기준 URL 은 `http://127.0.0.1:3100` 이다.

## 공통 화면

| 화면 | 파일 | 미리보기 |
|---|---|---|
| 로그인 | `assets/screenshots/01-login.png` | ![](../assets/screenshots/01-login.png) |
| 로그인 실패 | `assets/screenshots/common-02-login-failure.png` | ![](../assets/screenshots/common-02-login-failure.png) |
| 권한 거부 | `assets/screenshots/common-03-authorization-denied.png` | ![](../assets/screenshots/common-03-authorization-denied.png) |

## 학생 화면

| 화면 | 파일 | 미리보기 |
|---|---|---|
| 학생 대시보드 | `assets/screenshots/student-01-dashboard.png` | ![](../assets/screenshots/student-01-dashboard.png) |
| 프로필/단말 관리 | `assets/screenshots/student-02-profile-devices.png` | ![](../assets/screenshots/student-02-profile-devices.png) |
| 강의 홈 | `assets/screenshots/student-03-course-home.png` | ![](../assets/screenshots/student-03-course-home.png) |
| 자료·영상 | `assets/screenshots/student-04-learning-content.png` | ![](../assets/screenshots/student-04-learning-content.png) |
| 공지 목록 | `assets/screenshots/student-05-notices.png` | ![](../assets/screenshots/student-05-notices.png) |
| 공지 상세 | `assets/screenshots/student-06-notice-detail.png` | ![](../assets/screenshots/student-06-notice-detail.png) |
| 출석 확인 전 | `assets/screenshots/student-07-attendance-before-check.png` | ![](../assets/screenshots/student-07-attendance-before-check.png) |
| 재실 가능 여부 결과 | `assets/screenshots/student-08-eligibility-result.png` | ![](../assets/screenshots/student-08-eligibility-result.png) |
| 스마트 출석 처리 결과 | `assets/screenshots/student-09-check-in-result.png` | ![](../assets/screenshots/student-09-check-in-result.png) |
| 시험 목록 | `assets/screenshots/student-10-exam-list.png` | ![](../assets/screenshots/student-10-exam-list.png) |
| 시험 응시 | `assets/screenshots/student-11-exam-taking.png` | ![](../assets/screenshots/student-11-exam-taking.png) |
| 시험 답안 선택 | `assets/screenshots/student-12-exam-answer-selected.png` | ![](../assets/screenshots/student-12-exam-answer-selected.png) |
| 시험 제출 결과 | `assets/screenshots/student-13-exam-submit-result.png` | ![](../assets/screenshots/student-13-exam-submit-result.png) |

## 교수 화면

| 화면 | 파일 | 미리보기 |
|---|---|---|
| 교수 대시보드 | `assets/screenshots/professor-01-dashboard.png` | ![](../assets/screenshots/professor-01-dashboard.png) |
| 교수 프로필 | `assets/screenshots/professor-02-profile.png` | ![](../assets/screenshots/professor-02-profile.png) |
| 강의 홈 | `assets/screenshots/professor-03-course-home.png` | ![](../assets/screenshots/professor-03-course-home.png) |
| 자료·영상 관리 | `assets/screenshots/professor-04-learning-content-manage.png` | ![](../assets/screenshots/professor-04-learning-content-manage.png) |
| 공지 목록 | `assets/screenshots/professor-05-notices.png` | ![](../assets/screenshots/professor-05-notices.png) |
| 강의 운영/공지 작성 | `assets/screenshots/professor-06-course-manage-notice-form.png` | ![](../assets/screenshots/professor-06-course-manage-notice-form.png) |
| 시험 관리 | `assets/screenshots/professor-07-exam-manage.png` | ![](../assets/screenshots/professor-07-exam-manage.png) |
| 시험 상세 | `assets/screenshots/professor-08-exam-detail.png` | ![](../assets/screenshots/professor-08-exam-detail.png) |
| 출석 타임라인 | `assets/screenshots/professor-09-attendance-timeline.png` | ![](../assets/screenshots/professor-09-attendance-timeline.png) |
| 학생별 출석 누계 | `assets/screenshots/professor-10-attendance-student-stats.png` | ![](../assets/screenshots/professor-10-attendance-student-stats.png) |
| 스마트 출석 타이머 | `assets/screenshots/professor-11-attendance-timer.png` | ![](../assets/screenshots/professor-11-attendance-timer.png) |
| 출석 roster | `assets/screenshots/professor-12-attendance-roster.png` | ![](../assets/screenshots/professor-12-attendance-roster.png) |
| 차시 예외 roster | `assets/screenshots/professor-13-attendance-slot-roster.png` | ![](../assets/screenshots/professor-13-attendance-slot-roster.png) |
| 출석 상태 수정 저장 결과 | `assets/screenshots/professor-14-attendance-edit-save-result.png` | ![](../assets/screenshots/professor-14-attendance-edit-save-result.png) |
| 시험 종료 결과 | `assets/screenshots/professor-15-exam-close-result.png` | ![](../assets/screenshots/professor-15-exam-close-result.png) |
| 시험 게시 결과 | `assets/screenshots/professor-16-exam-publish-result.png` | ![](../assets/screenshots/professor-16-exam-publish-result.png) |

## 서비스관리자 화면

| 화면 | 파일 | 미리보기 |
|---|---|---|
| 사용자 현황 | `assets/screenshots/admin-01-users.png` | ![](../assets/screenshots/admin-01-users.png) |
| 강의실 및 네트워크 현황 | `assets/screenshots/admin-02-classrooms-networks.png` | ![](../assets/screenshots/admin-02-classrooms-networks.png) |
| 재실 시연 제어 | `assets/screenshots/admin-03-presence-demo-control.png` | ![](../assets/screenshots/admin-03-presence-demo-control.png) |
| 재실 시연 적용 결과 | `assets/screenshots/admin-04-presence-demo-applied.png` | ![](../assets/screenshots/admin-04-presence-demo-applied.png) |
| 재실 시연 초기화 결과 | `assets/screenshots/admin-05-presence-demo-reset-result.png` | ![](../assets/screenshots/admin-05-presence-demo-reset-result.png) |
