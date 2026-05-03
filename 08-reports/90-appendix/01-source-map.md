---
title: 보고서 출처 맵
type: report-appendix
status: draft
updated: 2026-04-12
owners:
  - team
related:
  - [[/08-reports/00-index.md]]
---

# 부록 A. 보고서 출처 맵

# A.1 문서 출처

| 보고서 항목 | 주요 출처 |
|---|---|
| 개요/목표/필요성 | [[/00-overview/project-summary.md]] |
| 학생 기능 | [[/01-requirements/req-student-features.md]] |
| 교수 기능 | [[/01-requirements/req-professor-features.md]] |
| 서비스관리자 기능 | [[/01-requirements/req-admin-features.md]] |
| 출석/재실성 | [[/01-requirements/req-attendance-presence.md]], [[/04-architecture/attendance-workflow-architecture.md]], [[/04-architecture/presence-eligibility-api.md]] |
| 단말 인증 | [[/01-requirements/req-device-auth.md]] |
| 시험 | [[/01-requirements/req-exam-workflow.md]], [[/04-architecture/exam-mvp-contract.md]], [[/04-architecture/exam-workflow-api.md]] |
| 서비스 경계 | [[/02-decisions/adr-0002-service-boundary.md]], [[/04-architecture/service-map.md]] |
| DB | [[/04-architecture/data-model-overview.md]], `DB/postgres/init/*.sql` |
| 인프라 | [[/04-architecture/local-runtime-topology.md]], `Service/compose.yml`, `Service/compose.local.yml`, `Service/compose.image.yml`, `Service/nginx/local.conf` |
| 네트워크/OpenWrt | [[/04-architecture/network-topology.md]], [[/05-work-items/task-openwrt-gateway-prototype.md]] |
| 일정/WBS | [[/05-work-items/epic-full-lms-delivery-plan.md]], [[/07-status/implementation-roadmap.md]] |

# A.2 코드 출처

| Repo | 파일 | 보고서 사용처 |
|---|---|---|
| Front | `src/App.tsx` | 화면/상태/역할별 기능 설명 |
| Front | `src/api.ts` | API client, 타입, 인증 refresh 설명 |
| Front | `src/router.ts` | path routing 설명 |
| Backend | `app/main.py` | API endpoint, 권한, WebSocket 설명 |
| Backend | `app/attendance.py` | 출석 session/report/audit 설명 |
| Backend | `app/services.py` | LMS/시험/공지/단말 도메인 설명 |
| Backend | `app/auth.py` | JWT/refresh/session 설명 |
| PresenceService | `app/main.py` | Presence API 목록 |
| PresenceService | `app/service.py` | snapshot/cache/eligibility/overlay 설명 |
| DB | `postgres/init/001_schema.sql` | LMS/출석/인증 ERD |
| DB | `postgres/init/013_exam_schema.sql` | 시험 ERD |
| CodexKit | `docker-compose.yml` | 로컬 인프라 |
| CodexKit | `nginx/default.conf` | reverse proxy routing |
