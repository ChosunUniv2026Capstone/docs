---
title: 화면 캡처 체크리스트
type: report-appendix
status: draft
updated: 2026-05-22
owners:
  - frontend-team
  - report-team
related:
  - [[/08-reports/10-body/10-frontend-screens.md]]
  - [[/08-reports/90-appendix/05-evidence-ledger.md]]
---

# 부록 B. 화면 캡처 체크리스트

최종보고서에는 Front End의 주요 기능 화면을 본문 또는 부록에서 참조한다. 2026-05-22 통합에서는 기존 원본 캡처 `docs/08-reports/assets/screenshots/*.png`를 보존하고, 각 설명 대상 UI를 **빨간 사각형 테두리(redbox)** 로 강조한 주석 SVG를 `assets/screenshots/final/annotated/`에 생성했다.

> 주의: 기존 PNG 원본은 2026-04-12 Playwright Chromium headless 캡처이며 당시 실행 기준은 `CodexKit/docker-compose.yml`이었다. 현재 canonical runtime entrypoint는 `Service` repo이므로, 최종 제출 직전에는 `Service/compose.local.yml` 또는 `Service/compose.image.yml` 기준으로 원본을 재촬영하거나 이 부록의 N/A/재촬영 필요 항목을 한계로 명시한다.

## B.1 촬영 및 주석 기준

- 기준 URL: `http://127.0.0.1:3100`
- 사용 계정: 학생 `20201239 / devpass123`, 교수 `PRF002 / devpass123`, 서비스관리자 `ADM001 / devpass123`
- 원본 보관: `docs/08-reports/assets/screenshots/*.png`
- 최종 주석본: `docs/08-reports/assets/screenshots/final/annotated/*-redbox.svg`
- 모든 본문 사용 그림은 그림 번호, 파일 경로, 캡션, 설명 대상 UI, redbox 주석 경로를 함께 가진다.
- redbox는 UI 내용을 가리지 않는 stroke-only 사각형을 원칙으로 한다.

## B.2 원본 기반 redbox 주석본

| 그림 | 원본 파일 | redbox 주석 파일 | 강조 대상 | 상태 |
|---|---|---|---|---|
| Fig. 1 | `01-login.png` | `assets/screenshots/final/annotated/fig-1-01-login-redbox.svg` | login form and service title | redbox SVG 생성 완료 |
| Fig. 2 | `common-02-login-failure.png` | `assets/screenshots/final/annotated/fig-2-common-02-login-failure-redbox.svg` | inline login failure banner | redbox SVG 생성 완료 |
| Fig. 3 | `common-03-authorization-denied.png` | `assets/screenshots/final/annotated/fig-3-common-03-authorization-denied-redbox.svg` | authorization denied message | redbox SVG 생성 완료 |
| Fig. 4 | `student-01-dashboard.png` | `assets/screenshots/final/annotated/fig-4-student-01-dashboard-redbox.svg` | student course cards and account summary | redbox SVG 생성 완료 |
| Fig. 5 | `professor-01-dashboard.png` | `assets/screenshots/final/annotated/fig-5-professor-01-dashboard-redbox.svg` | professor course cards | redbox SVG 생성 완료 |
| Fig. 6 / Fig. 48 | `admin-01-users.png` | `assets/screenshots/final/annotated/fig-6-fig-48-admin-01-users-redbox.svg` | admin user table and role column | redbox SVG 생성 완료 |
| Fig. 7 | `student-02-profile-devices.png` | `assets/screenshots/final/annotated/fig-7-student-02-profile-devices-redbox.svg` | registered device list and controls | redbox SVG 생성 완료 |
| Fig. 8 | `student-03-course-home.png` | `assets/screenshots/final/annotated/fig-8-student-03-course-home-redbox.svg` | course header and student tabs | redbox SVG 생성 완료 |
| Fig. 9 | `student-04-learning-content.png` | `assets/screenshots/final/annotated/fig-9-student-04-learning-content-redbox.svg` | learning item cards and download area | redbox SVG 생성 완료 |
| Fig. 10 | `student-05-notices.png` | `assets/screenshots/final/annotated/fig-10-student-05-notices-redbox.svg` | notice list row and navigation | redbox SVG 생성 완료 |
| Fig. 11 | `student-06-notice-detail.png` | `assets/screenshots/final/annotated/fig-11-student-06-notice-detail-redbox.svg` | notice title, body, and metadata | redbox SVG 생성 완료 |
| Fig. 12 | `student-14-assignment-list.png` | `assets/screenshots/final/annotated/fig-12-student-14-assignment-list-redbox.svg` | assignment card, status, and detail action | redbox SVG 생성 완료 |
| Fig. 13 | `student-15-assignment-detail.png` | `assets/screenshots/final/annotated/fig-13-student-15-assignment-detail-redbox.svg` | submission body, attachment area, and current feedback | redbox SVG 생성 완료 |
| Fig. 14 | `student-16-grade-feedback.png` | `assets/screenshots/final/annotated/fig-14-student-16-grade-feedback-redbox.svg` | grade and feedback summary card | redbox SVG 생성 완료 |
| Fig. 15 | `student-17-learning-progress.png` | `assets/screenshots/final/annotated/fig-15-student-17-learning-progress-redbox.svg` | learning progress input and save action | redbox SVG 생성 완료 |
| Fig. 16 | `student-18-qna.png` | `assets/screenshots/final/annotated/fig-16-student-18-qna-redbox.svg` | Q&A form and thread status | redbox SVG 생성 완료 |
| Fig. 17 / Fig. 20 | `student-07-attendance-before-check.png` | `assets/screenshots/final/annotated/fig-17-fig-20-student-07-attendance-before-check-redbox.svg` | attendance eligibility card and semester matrix | redbox SVG 생성 완료 |
| Fig. 18 | `student-08-eligibility-result.png` | `assets/screenshots/final/annotated/fig-18-student-08-eligibility-result-redbox.svg` | eligible summary and evidence card | redbox SVG 생성 완료 |
| Fig. 19 | `student-09-check-in-result.png` | `assets/screenshots/final/annotated/fig-19-student-09-check-in-result-redbox.svg` | bundle check-in result card | redbox SVG 생성 완료 |
| Fig. 21 | `student-10-exam-list.png` | `assets/screenshots/final/annotated/fig-21-student-10-exam-list-redbox.svg` | exam list card status and policy | redbox SVG 생성 완료 |
| Fig. 22 | `student-11-exam-taking.png` | `assets/screenshots/final/annotated/fig-22-student-11-exam-taking-redbox.svg` | question prompt, options, countdown | redbox SVG 생성 완료 |
| Fig. 23 | `student-12-exam-answer-selected.png` | `assets/screenshots/final/annotated/fig-23-student-12-exam-answer-selected-redbox.svg` | selected option and save state | redbox SVG 생성 완료 |
| Fig. 24 | `student-19-exam-missing-answer-warning.png` | `assets/screenshots/final/annotated/fig-24-student-19-exam-missing-answer-warning-redbox.svg` | missing-answer warning or submit guard state | redbox SVG 생성 완료 |
| Fig. 25 | `student-13-exam-submit-result.png` | `assets/screenshots/final/annotated/fig-25-student-13-exam-submit-result-redbox.svg` | submission completion status | redbox SVG 생성 완료 |
| Fig. P2 | `professor-02-profile.png` | `assets/screenshots/final/annotated/fig-p2-professor-02-profile-redbox.svg` | professor profile summary | redbox SVG 생성 완료 |
| Fig. 26 | `professor-03-course-home.png` | `assets/screenshots/final/annotated/fig-26-professor-03-course-home-redbox.svg` | professor course header and action tabs | redbox SVG 생성 완료 |
| Fig. 27 | `professor-04-learning-content-manage.png` | `assets/screenshots/final/annotated/fig-27-professor-04-learning-content-manage-redbox.svg` | material upload/create controls | redbox SVG 생성 완료 |
| Fig. 28 | `professor-05-notices.png` | `assets/screenshots/final/annotated/fig-28-professor-05-notices-redbox.svg` | professor notice list | redbox SVG 생성 완료 |
| Fig. 29 | `professor-06-course-manage-notice-form.png` | `assets/screenshots/final/annotated/fig-29-professor-06-course-manage-notice-form-redbox.svg` | notice form and submit action | redbox SVG 생성 완료 |
| Fig. 30 | `professor-17-assignment-create.png` | `assets/screenshots/final/annotated/fig-30-professor-17-assignment-create-redbox.svg` | assignment creation/list management area | redbox SVG 생성 완료 |
| Fig. 31 | `professor-18-submission-review.png` | `assets/screenshots/final/annotated/fig-31-professor-18-submission-review-redbox.svg` | submission roster and selected student detail | redbox SVG 생성 완료 |
| Fig. 32 | `professor-19-assignment-grading.png` | `assets/screenshots/final/annotated/fig-32-professor-19-assignment-grading-redbox.svg` | score/status/feedback grading controls | redbox SVG 생성 완료 |
| Fig. 33 | `professor-20-grade-overview.png` | `assets/screenshots/final/annotated/fig-33-professor-20-grade-overview-redbox.svg` | student grade rows and average percent | redbox SVG 생성 완료 |
| Fig. 34 | `professor-21-learning-progress.png` | `assets/screenshots/final/annotated/fig-34-professor-21-learning-progress-redbox.svg` | student-by-material learning progress table | redbox SVG 생성 완료 |
| Fig. 35 | `professor-22-qna-answer.png` | `assets/screenshots/final/annotated/fig-35-professor-22-qna-answer-redbox.svg` | answer textarea, close checkbox, and save action | redbox SVG 생성 완료 |
| Fig. 36 | `professor-07-exam-manage.png` | `assets/screenshots/final/annotated/fig-36-professor-07-exam-manage-redbox.svg` | exam draft/list management card | redbox SVG 생성 완료 |
| Fig. 37 | `professor-08-exam-detail.png` | `assets/screenshots/final/annotated/fig-37-professor-08-exam-detail-redbox.svg` | exam policy and question list | redbox SVG 생성 완료 |
| Fig. 38 | `professor-16-exam-publish-result.png` | `assets/screenshots/final/annotated/fig-38-professor-16-exam-publish-result-redbox.svg` | exam publish status result | redbox SVG 생성 완료 |
| Fig. 39 | `professor-15-exam-close-result.png` | `assets/screenshots/final/annotated/fig-39-professor-15-exam-close-result-redbox.svg` | exam close result status | redbox SVG 생성 완료 |
| Fig. 40 | `professor-09-attendance-timeline.png` | `assets/screenshots/final/annotated/fig-40-professor-09-attendance-timeline-redbox.svg` | weekly attendance timeline rows | redbox SVG 생성 완료 |
| Fig. 41 | `professor-23-attendance-start-modal.png` | `assets/screenshots/final/annotated/fig-41-professor-23-attendance-start-modal-redbox.svg` | attendance start modal mode options | redbox SVG 생성 완료 |
| Fig. 42 | `professor-11-attendance-timer.png` | `assets/screenshots/final/annotated/fig-42-professor-11-attendance-timer-redbox.svg` | smart attendance timer and close button | redbox SVG 생성 완료 |
| Fig. 43 | `professor-12-attendance-roster.png` | `assets/screenshots/final/annotated/fig-43-professor-12-attendance-roster-redbox.svg` | student status table and reason inputs | redbox SVG 생성 완료 |
| Fig. 44 | `professor-13-attendance-slot-roster.png` | `assets/screenshots/final/annotated/fig-44-professor-13-attendance-slot-roster-redbox.svg` | slot-specific roster controls | redbox SVG 생성 완료 |
| Fig. 45 | `professor-14-attendance-edit-save-result.png` | `assets/screenshots/final/annotated/fig-45-professor-14-attendance-edit-save-result-redbox.svg` | save success and updated status row | redbox SVG 생성 완료 |
| Fig. 46 | `professor-10-attendance-student-stats.png` | `assets/screenshots/final/annotated/fig-46-professor-10-attendance-student-stats-redbox.svg` | student stats table and CSV buttons | redbox SVG 생성 완료 |
| Fig. 47 | `professor-24-attendance-history.png` | `assets/screenshots/final/annotated/fig-47-professor-24-attendance-history-redbox.svg` | immutable attendance audit history list | redbox SVG 생성 완료 |
| Fig. 49 / Fig. 50 / Fig. 51 | `admin-02-classrooms-networks.png` | `assets/screenshots/final/annotated/fig-49-fig-50-fig-51-admin-02-classrooms-networks-redbox.svg` | classroom/AP mapping, station list, threshold controls | redbox SVG 생성 완료 |
| Fig. 52 | `admin-03-presence-demo-control.png` | `assets/screenshots/final/annotated/fig-52-admin-03-presence-demo-control-redbox.svg` | demo source label and overlay controls | redbox SVG 생성 완료 |
| Fig. 53 | `admin-04-presence-demo-applied.png` | `assets/screenshots/final/annotated/fig-53-admin-04-presence-demo-applied-redbox.svg` | applied overlay station state | redbox SVG 생성 완료 |
| Fig. 54 | `admin-05-presence-demo-reset-result.png` | `assets/screenshots/final/annotated/fig-54-admin-05-presence-demo-reset-result-redbox.svg` | reset result and restored baseline | redbox SVG 생성 완료 |
| Fig. 55 | `admin-06-real-vs-demo-snapshots.png` | `assets/screenshots/final/annotated/fig-55-admin-06-real-vs-demo-snapshots-redbox.svg` | real/demo snapshot separation labels | redbox SVG 생성 완료 |

## B.3 N/A 근거 항목

| 그림 | 화면 | 현재 근거 | redbox 강조 대상 | 처리 |
|---|---|---|---|---|
| Fig. 56 | OpenWrt router registration/token | Front main에 전용 화면 없음 | API/DB/Service registry 근거로 대체 | N/A 근거 기록 |

## B.4 최종 제출 전 visual gate

- [x] 기존 37개 PNG에 대한 redbox SVG 주석본 생성
- [x] reviewer 지적 누락 화면 15개를 실행 중인 사이트(`http://127.0.0.1:3100`)에서 추가 촬영
- [x] 추가 15개 PNG에 대한 redbox SVG 주석본 생성
- [x] 학생/교수/관리자 핵심 흐름별 강조 대상 정의
- [x] OpenWrt router registration/token 화면은 현재 Front main 전용 화면이 없어 N/A로 분리
- [x] 신규 LMS subset 화면(과제/성적/Q&A/진도), 출석 모달/이력, real-vs-demo snapshot 원본 캡처 추가
- [ ] 최종 제출 직전 모든 원본을 동일 runtime/seed로 재촬영할지 결정
- [ ] 본문에서 참조하는 모든 그림 번호와 캡션을 최종보고서 본문/부록과 대조
