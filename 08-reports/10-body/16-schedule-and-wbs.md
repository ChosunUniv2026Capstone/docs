---
title: 일정 및 WBS
type: report-section
status: draft
updated: 2026-04-12
owners:
  - team
related:
  - [[/05-work-items/epic-full-lms-delivery-plan.md]]
  - [[/07-status/implementation-roadmap.md]]
source:
  - [[/05-work-items/epic-full-lms-delivery-plan.md]]
  - [[/07-status/implementation-roadmap.md]]
---

# 16. 일정 및 WBS

# 16.1 단계별 일정 초안

| Phase | 기간 | 목표 | 주요 산출물 | 상태 |
|---|---|---|---|---|
| 1. Foundation | 3월 | 로그인, 기본 데이터, Docker 실행 | 기본 앱, seed, compose | 완료/보강 |
| 2. Academic Read Model | 3월~4월 | 강의/공지/서비스관리자 조회 | 강의/공지/서비스관리자 UI/API | 일부 완료 |
| 3. Presence & Attendance | 4월 | 재실성 판정, 출석 세션 | eligibility, attendance session, audit | 구현/검증 중 |
| 4. Exam MVP | 4월 | 시험 생성/응시/제출 | exam API/UI/DB | 구현/검증 중 |
| 5. Full LMS Expansion | 4월~5월 | 자료/영상/과제/성적/문의 | 추가 기능 | 계획 |
| 6. Infrastructure & CI/CD | 5월 | 자동 빌드/테스트/배포 | CI workflow, staging plan | 계획 |
| 7. Final Report & Demo | 5월~6월 | 최종 보고/시연 | 최종보고서, 캡처, 시연 영상 | 계획 |

# 16.2 WBS

| WBS | 작업 | 세부 작업 | 담당 | 산출물 | 상태 |
|---|---|---|---|---|---|
| 1.0 | 요구사항 정리 | 사용자/기능/권한 요구 정리 | team | req 문서 | 진행 |
| 1.1 | 학생 요구 | 강의, 공지, 단말, 출석, 시험 | frontend/backend | req-student | 진행 |
| 1.2 | 교수 요구 | 공지, 시험, 출석 운영 | frontend/backend | req-professor | 진행 |
| 1.3 | 서비스관리자 요구 | 사용자, 강의실, AP, 재실성 운영 | frontend/backend/presence | req-admin | 진행 |
| 2.0 | 아키텍처 | 서비스 경계, 로컬 토폴로지 | team | service-map, topology | 진행 |
| 2.1 | 데이터 모델 | 사용자/강의/출석/시험 schema | db-owner | schema, ERD | 진행 |
| 2.2 | API 계약 | Backend/Presence API | backend/presence | API docs | 진행 |
| 3.0 | Front 구현 | 역할별 화면 | frontend | React app | 진행 |
| 3.1 | 학생 UI | 강의/공지/단말/출석/시험 | frontend | 화면 캡처 | 진행 |
| 3.2 | 교수 UI | 공지/시험/출석 운영 | frontend | 화면 캡처 | 진행 |
| 3.3 | 서비스관리자 UI | 사용자/강의실/AP/overlay | frontend | 화면 캡처 | 진행 |
| 4.0 | Backend 구현 | 인증/LMS/출석/시험 API | backend | FastAPI app | 진행 |
| 5.0 | Presence 구현 | snapshot/eligibility/overlay/OpenWrt | presence | service + tests | 진행 |
| 6.0 | DB 구현 | schema/seed/검증 | db-owner | SQL init/seed | 진행 |
| 7.0 | 테스트 | unit/e2e/docker smoke | team | 테스트 결과 | 진행 |
| 8.0 | CI/CD | lint/test/build 자동화 | team | workflow 설계/구현 | 계획 |
| 9.0 | 보고서 | 주간/중간/최종 보고서 | team | 08-reports | 진행 |

# 16.3 목표 대비 달성치 작성 방식

매주/중간 보고서에서는 아래 표를 기준으로 업데이트한다.

| 목표 | 계획 | 실제 달성 | 달성률 | 근거 | 다음 조치 |
|---|---|---|---:|---|---|
| 재실성 eligibility 구현 | 등록 단말 + snapshot 비교 | Backend/PresenceService dummy path 구현 | 70% | API/tests/docs | 실 OpenWrt collector 확장 |
| 출석 세션 운영 | 교수 open + 학생 check-in | bundle session 설계/일부 구현 | 60% | schema/API/UI | 실시간/캡처 보강 |
| 시험 MVP | 객관식 시험 생성/응시 | schema/API/UI 일부 구현 | 60% | exam docs/tests | 화면/검증 보강 |
| 보고서 체계 | 본문+부록+통합본 | 08-reports 초안 작성 | 40% | 본 문서 | 피드백 반영 |
