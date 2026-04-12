---
title: 화면 캡처 체크리스트
type: report-appendix
status: draft
updated: 2026-04-12
owners:
  - frontend-team
related:
  - [[/08-reports/10-body/10-frontend-screens.md]]
---

# 부록 B. 화면 캡처 체크리스트

최종보고서에는 Front End의 모든 주요 기능 화면을 캡처해 본문에 삽입한다.
이미지 파일은 `08-reports/assets/screenshots/` 아래에 저장한다.

# B.1 촬영 기준

- 촬영일: 2026-04-12
- 촬영 방식: Playwright Chromium headless screenshot
- 실행 기준: 기존 Docker 컨테이너를 모두 내린 뒤 `CodexKit/docker-compose.yml` 을 현재 워크스페이스 기준으로 `up -d --build`
- 접속 URL: `http://127.0.0.1:3100`
- 사용 계정:
  - 학생: `20201239 / devpass123`
  - 교수: `PRF002 / devpass123`
  - 서비스관리자: `ADM001 / devpass123`
- 캡처용 데이터:
  - `CSE116 / Capstone Design A`
  - 캡처용 공지 1건 생성
  - 캡처용 시험 1건 생성/게시
  - 캡처용 smart attendance session 1건 생성
  - `B101` dummy presence overlay 적용

# B.2 공통

- [x] 로그인 화면 — `assets/screenshots/01-login.png`
- [x] 세션 복구 후 대시보드 — 역할별 대시보드 캡처에 포함
- [x] 로그인 실패 메시지 — `assets/screenshots/common-02-login-failure.png`
- [x] 권한 실패 메시지 — `assets/screenshots/common-03-authorization-denied.png`

# B.3 학생

- [x] 학생 강의 목록 — `assets/screenshots/student-01-dashboard.png`
- [x] 강의 상세 기본 화면 — `assets/screenshots/student-03-course-home.png`
- [x] 공지 목록 — `assets/screenshots/student-05-notices.png`
- [x] 공지 상세 — `assets/screenshots/student-06-notice-detail.png`
- [x] 단말 등록/목록 — `assets/screenshots/student-02-profile-devices.png`
- [x] eligibility 확인 전 — `assets/screenshots/student-07-attendance-before-check.png`
- [x] eligibility 성공 결과 — `assets/screenshots/student-08-eligibility-result.png`
- [x] active attendance session / self check-in 결과 — `assets/screenshots/student-09-check-in-result.png`
- [x] 출석 학기 매트릭스 — `assets/screenshots/student-07-attendance-before-check.png`
- [x] 시험 목록 — `assets/screenshots/student-10-exam-list.png`
- [x] 시험 응시 화면 — `assets/screenshots/student-11-exam-taking.png`
- [x] 답안 선택 — `assets/screenshots/student-12-exam-answer-selected.png`
- [x] 강의자료/동영상 스캐폴드 — `assets/screenshots/student-04-learning-content.png`
- [x] 시험 제출 완료 결과 — `assets/screenshots/student-13-exam-submit-result.png`

# B.4 교수

- [x] 교수 강의 목록 — `assets/screenshots/professor-01-dashboard.png`
- [x] 교수 프로필 — `assets/screenshots/professor-02-profile.png`
- [x] 강의 상세 기본 화면 — `assets/screenshots/professor-03-course-home.png`
- [x] 자료/영상 관리 — `assets/screenshots/professor-04-learning-content-manage.png`
- [x] 공지 목록 — `assets/screenshots/professor-05-notices.png`
- [x] 공지 작성 — `assets/screenshots/professor-06-course-manage-notice-form.png`
- [x] 시험 목록/작성 — `assets/screenshots/professor-07-exam-manage.png`
- [x] 시험 상세 — `assets/screenshots/professor-08-exam-detail.png`
- [x] 출석 timeline — `assets/screenshots/professor-09-attendance-timeline.png`
- [x] 학생별 출석 누계 — `assets/screenshots/professor-10-attendance-student-stats.png`
- [x] 출석 timer — `assets/screenshots/professor-11-attendance-timer.png`
- [x] 출석 roster — `assets/screenshots/professor-12-attendance-roster.png`
- [x] 차시 예외 roster — `assets/screenshots/professor-13-attendance-slot-roster.png`
- [x] 학생 출석 상태 수정 후 저장 결과 — `assets/screenshots/professor-14-attendance-edit-save-result.png`
- [x] 시험 종료 동작 후 결과 — `assets/screenshots/professor-15-exam-close-result.png`
- [x] 시험 게시 동작 후 결과 — `assets/screenshots/professor-16-exam-publish-result.png`

# B.5 서비스관리자

- [x] 사용자 목록 — `assets/screenshots/admin-01-users.png`
- [x] 강의실 및 네트워크 현황 — `assets/screenshots/admin-02-classrooms-networks.png`
- [x] AP threshold 현황 — `assets/screenshots/admin-02-classrooms-networks.png`
- [x] presence snapshot 조회 — `assets/screenshots/admin-02-classrooms-networks.png`
- [x] dummy overlay 제어 — `assets/screenshots/admin-03-presence-demo-control.png`
- [x] dummy overlay 적용 결과 — `assets/screenshots/admin-04-presence-demo-applied.png`
- [x] dummy overlay reset 결과 — `assets/screenshots/admin-05-presence-demo-reset-result.png`
- [ ] OpenWrt router registration/token 화면 — 현재 main 기준 화면 없음, 구현 후 촬영

# B.6 캡처 품질 기준

- 브라우저 화면에서 역할과 현재 기능 위치가 보이게 한다.
- 역할별 demo 계정을 사용한다.
- 성공 화면과 실패/거부 사유 화면을 최종보고 전 함께 포함한다.
- 개인정보가 포함될 경우 demo seed 데이터만 사용한다.
