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
| 2. Academic Read Model | 3월~4월 | 강의/공지/서비스관리자 조회 | 강의/공지/서비스관리자 UI/API | 완료 |
| 3. Presence & Attendance | 4월~5월 | 재실성 판정, 출석 세션 | eligibility, attendance session, audit, CSV, semester matrix | 완료/운영 보강 |
| 4. Exam MVP | 4월 | 시험 생성/응시/제출 | exam API/UI/DB | 완료 |
| 5. Full LMS Expansion | 4월~5월 | 자료/영상/과제/성적/문의 | selected LMS API/UI/DB, object storage | 완료 |
| 6. Infrastructure & CI/CD | 5월 | 자동 빌드/테스트/배포 | CI workflow, GHCR image, release manifest, demo deploy script | 일부 완료 |
| 7. Final Report & Demo | 5월~6월 | 최종 보고/시연 | 최종보고서, 캡처, 시연 영상, QR | 완료 |

# 16.2 WBS

| WBS | 작업 | 세부 작업 | 담당 | 산출물 | 상태 |
|---|---|---|---|---|---|
| 1.0 | 요구사항 정리 | 사용자/기능/권한 요구 정리 | team | req 문서 | 완료 |
| 1.1 | 학생 요구 | 강의, 공지, 단말, 출석, 시험, 과제, Q&A | frontend/backend | req-student | 완료 |
| 1.2 | 교수 요구 | 공지, 자료, 과제, 시험, 출석 운영 | frontend/backend | req-professor | 완료 |
| 1.3 | 서비스관리자 요구 | 사용자, 강의실, AP, 재실성 운영 | frontend/backend/presence | req-admin | 완료 |
| 2.0 | 아키텍처 | 서비스 경계, 로컬 토폴로지 | team | service-map, topology | 완료 |
| 2.1 | 데이터 모델 | 사용자/강의/출석/시험/selected LMS/object storage schema | db-owner | schema, ERD | 완료 |
| 2.2 | API 계약 | Backend/Presence API | backend/presence | API docs | 완료 |
| 3.0 | Front 구현 | 역할별 화면 | frontend | React app | 완료 |
| 3.1 | 학생 UI | 강의/공지/단말/출석/시험/과제/Q&A | frontend | 화면 캡처 | 완료 |
| 3.2 | 교수 UI | 공지/자료/과제/시험/출석 운영 | frontend | 화면 캡처 | 완료 |
| 3.3 | 서비스관리자 UI | 사용자/강의실/AP/overlay | frontend | 화면 캡처 | 완료 |
| 4.0 | Backend 구현 | 인증/LMS/출석/시험/API/export | backend | FastAPI app | 완료 |
| 5.0 | Presence 구현 | snapshot/eligibility/overlay/OpenWrt collector | presence | service + tests | 완료/운영 보강 |
| 6.0 | DB 구현 | schema/seed/검증 | db-owner | SQL init/seed | 완료 |
| 7.0 | 테스트 | unit/e2e/docker smoke | team | 테스트 결과 | 진행 |
| 8.0 | CI/CD | lint/test/build 자동화, image/demo mode | team | workflow 설계/구현 | 일부 완료 |
| 9.0 | 보고서 | 주간/중간/최종 보고서 | team | 08-reports | 완료 |

# 16.3 목표 대비 달성치 작성 방식

매주/중간 보고서에서는 아래 표를 기준으로 업데이트한다.

| 목표 | 계획 | 실제 달성 | 달성률 | 근거 | 다음 조치 |
|---|---|---|---:|---|---|
| 재실성 eligibility 구현 | 등록 단말 + snapshot 비교 | Backend/PresenceService collector/demo path 구현 | 90% | API/tests/docs | 장기 실장비 안정화 |
| 출석 세션 운영 | 교수 open + 학생 check-in | bundle session, roster, CSV, semester matrix 구현 | 90% | schema/API/UI | 운영 정책 보강 |
| 시험 MVP | 객관식 시험 생성/응시 | schema/API/UI 구현 | 90% | exam docs/tests | 문제 유형 확장 |
| 보고서 체계 | 본문+부록+통합본 | 최종 보고서/HWP/PDF 작성 | 95% | 본 문서, 산출물 | 제출 전 형식 검수 |
