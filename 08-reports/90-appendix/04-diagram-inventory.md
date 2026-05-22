---
title: 다이어그램 목록
type: report-appendix
status: draft
updated: 2026-05-22
owners:
  - team
  - db-owner
related:
  - [[/08-reports/10-body/06-system-architecture.md]]
  - [[/08-reports/10-body/11-backend-api-and-flows.md]]
  - [[/08-reports/10-body/12-presence-service-flows.md]]
  - [[/08-reports/10-body/13-database-design.md]]
  - [[/08-reports/90-appendix/05-evidence-ledger.md]]
---

# 부록 D. 다이어그램 목록

이 부록은 본문에서 참조할 아키텍처/UML/ERD 그림의 출처와 캡처 상태를 관리한다. 2026-05-22 통합에서는 사용자 요구에 따라 **전체 ERD 1개와 부분 ERD 7개**를 SVG 산출물로 만들고, 각 그림의 redbox 주석본도 함께 생성했다.

## D.1 본문 포함 다이어그램

| 위치 | 유형 | 목적 | 최종보고 처리 |
|---|---|---|---|
| `06-system-architecture.md` | Mermaid flowchart | 전체 논리 아키텍처 | Backend ↔ PresenceService ↔ DB/Redis 경계를 본문에서 설명 |
| `06-system-architecture.md` | Mermaid sequenceDiagram | 로그인/세션 복구 | 인증/세션 구현 절에서 참조 |
| `06-system-architecture.md` | Mermaid sequenceDiagram | 출석 eligibility | 출석 알고리즘 절에서 참조 |
| `06-system-architecture.md` | Mermaid flowchart | 출석 세션 운영 | bundle attendance session 설명에 사용 |
| `07-service-infrastructure.md` | Mermaid flowchart | Docker/Nginx 로컬 인프라 | Service runtime 구조와 함께 설명 |
| `11-backend-api-and-flows.md` | Mermaid sequenceDiagram | Backend 인증 흐름 | API 구현 절에서 참조 |
| `11-backend-api-and-flows.md` | Mermaid sequenceDiagram | 출석 세션 흐름 | 실험/결과 절의 출석 workflow와 연결 |
| `11-backend-api-and-flows.md` | Mermaid flowchart | 시험 흐름 | 시험 workflow 구현 절에서 참조 |
| `12-presence-service-flows.md` | Mermaid flowchart | Presence eligibility 판정 | Redis cache / demo overlay 분리 설명 |
| `12-presence-service-flows.md` | Mermaid sequenceDiagram | Presence snapshot/cache | 성능/한계 절에서 참조 |
| `12-presence-service-flows.md` | Mermaid sequenceDiagram | Demo overlay | 로컬 MVP와 실 장비 검증 한계 분리 |
| `13-database-design.md` | Mermaid erDiagram | DB ERD | 아래 D.2 산출물로 보강 |
| `17-ci-cd-design.md` | Mermaid flowchart | CI pipeline | CI/CD는 workflow/server provenance가 부족하면 부분 완료로 표현 |

## D.2 ERD 전체/부분 캡처 산출물

| 그림 | 목적 | raw SVG | redbox SVG | redbox/callout 대상 | 포함 테이블/노드 |
|---|---|---|---|---|---|
| ERD-1 | Full Smart Class PostgreSQL ERD | `assets/diagrams/final/raw/erd-1-full-smart-class-erd.svg` | `assets/diagrams/final/annotated/erd-1-full-smart-class-erd-redbox.svg` | LMS + presence/attendance + assessment domains | users, courses, course_enrollments, course_schedules, classrooms, classroom_networks, access_points, access_point_interfaces, registered_devices, refresh_sessions, attendance_sessions, attendance_session_slots, attendance_records, attendance_status_audit_logs, presence_eligibility_logs, exams, exam_questions, exam_question_options, exam_submissions, exam_submission_answers, assignments, assignment_submissions, learning_items, learning_progress, course_qna_threads, course_qna_posts, report_exports, object_deletion_jobs |
| ERD-2 | User / auth / registered-device ERD | `assets/diagrams/final/raw/erd-2-user-auth-device.svg` | `assets/diagrams/final/annotated/erd-2-user-auth-device-redbox.svg` | users.id relationships to sessions/devices | users, refresh_sessions, registered_devices |
| ERD-3 | Course / enrollment / notice / material ERD | `assets/diagrams/final/raw/erd-3-course-enrollment-notice-material.svg` | `assets/diagrams/final/annotated/erd-3-course-enrollment-notice-material-redbox.svg` | course ownership/enrollment and attachment relations | courses, course_enrollments, course_schedules, notices, learning_items, learning_item_attachments, notice_attachments |
| ERD-4 | Device / classroom / AP / presence ERD | `assets/diagrams/final/raw/erd-4-device-classroom-ap-presence.svg` | `assets/diagrams/final/annotated/erd-4-device-classroom-ap-presence-redbox.svg` | classroom network mapping and AP registry evidence | classrooms, classroom_networks, access_points, access_point_interfaces, registered_devices, presence_eligibility_logs |
| ERD-5 | Attendance session / record / audit ERD | `assets/diagrams/final/raw/erd-5-attendance-session-record-audit.svg` | `assets/diagrams/final/annotated/erd-5-attendance-session-record-audit-redbox.svg` | bundle parent, slot fan-out, record/audit history | attendance_sessions, attendance_session_slots, attendance_records, attendance_status_audit_logs, users, courses, classrooms |
| ERD-6 | Exam / question / submission / answer ERD | `assets/diagrams/final/raw/erd-6-exam-question-submission-answer.svg` | `assets/diagrams/final/annotated/erd-6-exam-question-submission-answer-redbox.svg` | exam-question-option and submission-answer consistency | exams, exam_questions, exam_question_options, exam_submissions, exam_submission_answers, exam_question_attachments, exam_answer_attachments |
| ERD-7 | Selected LMS / assignment / Q&A / progress ERD | `assets/diagrams/final/raw/erd-7-selected-lms-assignment-qna-progress.svg` | `assets/diagrams/final/annotated/erd-7-selected-lms-assignment-qna-progress-redbox.svg` | grading fields, Q&A threads/posts, progress ownership | assignments, assignment_submissions, assignment_submission_attachments, course_qna_threads, course_qna_posts, learning_progress, learning_items, users, courses |
| ERD-8 | Service / ops metadata ERD and N/A boundary | `assets/diagrams/final/raw/erd-8-service-ops-metadata.svg` | `assets/diagrams/final/annotated/erd-8-service-ops-metadata-redbox.svg` | report exports, object deletion outbox, Service runtime N/A boundary | report_exports, object_deletion_jobs, learning_item_attachments, notice_attachments, assignment_submission_attachments, Service runtime: N/A PostgreSQL entity |

## D.3 ERD source-of-truth

| Source | Coverage |
|---|---|
| `DB/postgres/init/001_schema.sql` | users, courses, enrollments, schedules, notices, classroom networks, registered devices, presence eligibility logs, refresh sessions, attendance sessions/slots/records/audit, access points/interfaces |
| `DB/postgres/init/013_exam_schema.sql` | exams, questions, options, submissions, answers |
| `DB/postgres/init/014_assignment_schema.sql` | assignments, assignment submissions, assignment attachments |
| `DB/postgres/init/015_object_storage_schema.sql` | learning items, learning item attachments, notice/exam attachments, report exports, object deletion jobs |
| `DB/postgres/init/016_selected_lms_subset.sql` | assignment grading fields, Q&A threads/posts, learning progress |
| `DB/postgres/migrations/016_openwrt_collector_registry.sql` | OpenWrt collector registry migration reference |
| `docs/04-architecture/data-model-overview.md` | relationship prose and Redis/cache N/A caveats |

## D.4 N/A 및 주의 경계

- Redis snapshot/cache는 PostgreSQL 테이블이 아니므로 ERD에 억지로 넣지 않고 PresenceService 흐름도에서 설명한다.
- Service runtime orchestration은 DB 엔티티가 아니므로 ERD-8에서 N/A 경계를 명시하고, compose/nginx/manifest 증거로 별도 설명한다.
- OpenWrt 장기 현장 검증과 운영 배포는 구현 완료 성과가 아니라 한계/개선 방향으로 분리한다.
