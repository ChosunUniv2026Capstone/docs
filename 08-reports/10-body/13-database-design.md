---
title: Database 설계
type: report-section
status: draft
updated: 2026-06-15
owners:
  - db-owner
related:
  - [[/04-architecture/data-model-overview.md]]
  - [[/03-conventions/conv-db-naming.md]]
source:
  - [[/04-architecture/data-model-overview.md]]
  - DB/postgres/init/001_schema.sql
  - DB/postgres/init/013_exam_schema.sql
  - DB/postgres/init/014_assignment_schema.sql
  - DB/postgres/init/015_object_storage_schema.sql
  - DB/postgres/init/016_selected_lms_subset.sql
  - DB/postgres/init/018_continuous_attendance_monitoring.sql
---

# 13. Database 설계

# 13.1 데이터 모델 개요

DB 는 PostgreSQL 기반이며, 사용자/강의/강의실/단말/출석/시험/인증 세션 데이터를 저장한다.
Redis snapshot 은 영속 DB 가 아니라 PresenceService 의 성능 최적화 계층으로 본다.

# 13.2 주요 테이블

| 그룹 | 테이블 | 설명 |
|---|---|---|
| 사용자 | `users` | 학생/교수/서비스관리자 계정 |
| 강의 | `courses`, `course_enrollments`, `course_schedules` | 강의, 수강, 시간표 |
| 공간/네트워크 | `classrooms`, `classroom_networks` | 강의실과 AP/SSID/gateway/threshold |
| 단말 | `registered_devices` | 학생 등록 단말 MAC |
| 인증 | `refresh_sessions` | refresh token rotation/replay/revoke 상태 |
| Presence | `presence_eligibility_logs` | 재실성 판정 요청 로그 |
| 출석 | `attendance_sessions`, `attendance_session_slots`, `attendance_records`, `attendance_status_audit_logs` | bundle session, slot membership, 학생별 상태, 감사 로그 |
| 시험 | `exams`, `exam_questions`, `exam_question_options`, `exam_submissions`, `exam_submission_answers` | 시험 마스터, 문항, 선택지, 응시, 답안 |
| 공지 | `notices` | 강의 공지 |
| 과제 | `assignments`, `assignment_submissions`, `assignment_submission_attachments` | 과제 마스터, 학생 제출, 제출 첨부 |
| 학습자료 | `learning_items`, `learning_item_attachments`, `learning_progress` | 강의자료/영상, 인증 다운로드, 학습 진도 |
| Q&A/성적 | `course_qna_threads`, `course_qna_posts`, `assignment_grade_overrides` | 강의별 질문/답변, 과제 점수/피드백 |
| Object storage | `notice_attachments`, `exam_question_attachments`, `exam_answer_attachments`, `report_exports`, `object_deletion_jobs` | 첨부 파일, 출석 CSV export, 삭제 예약 job |
| AP registry | `access_points`, `access_point_interfaces` | OpenWrt collector 대상 AP, interface, token 상태 |
| 지속 출석 | `attendance_monitoring_leases`, `attendance_monitoring_states` | continuous attendance monitoring lease/state |

초기 schema 는 `001_schema.sql` 이 담당하지만, 최종 코드 기준 데이터 모델은 `014_assignment_schema.sql`, `015_object_storage_schema.sql`, `016_selected_lms_subset.sql`, `018_continuous_attendance_monitoring.sql`까지 함께 보아야 한다. 이 파일들이 과제, 첨부/다운로드, selected LMS, 출석 CSV export, 지속 출석 모니터링을 실제 테이블로 확장한다.

# 13.3 ERD

```mermaid
---
title: Smart Class Database ERD
---
erDiagram
    USERS ||--o{ COURSES : teaches
    USERS ||--o{ COURSE_ENROLLMENTS : enrolls
    USERS ||--o{ NOTICES : writes
    USERS ||--o{ REGISTERED_DEVICES : owns
    USERS ||--o{ REFRESH_SESSIONS : authenticates
    USERS ||--o{ PRESENCE_ELIGIBILITY_LOGS : requested_for
    USERS ||--o{ ATTENDANCE_SESSIONS : opens
    USERS ||--o{ ATTENDANCE_RECORDS : receives
    USERS |o--o{ ATTENDANCE_RECORDS : finalizes
    USERS ||--o{ ATTENDANCE_STATUS_AUDIT_LOGS : target_student
    USERS ||--o{ ATTENDANCE_STATUS_AUDIT_LOGS : acts
    USERS ||--o{ EXAM_SUBMISSIONS : submits

    COURSES ||--o{ COURSE_ENROLLMENTS : has
    COURSES ||--o{ COURSE_SCHEDULES : scheduled_as
    COURSES ||--o{ NOTICES : publishes
    COURSES ||--o{ PRESENCE_ELIGIBILITY_LOGS : checks_for
    COURSES ||--o{ ATTENDANCE_SESSIONS : opens
    COURSES ||--o{ EXAMS : contains

    CLASSROOMS ||--o{ COURSE_SCHEDULES : hosts
    CLASSROOMS ||--o{ CLASSROOM_NETWORKS : maps_network
    CLASSROOMS ||--o{ PRESENCE_ELIGIBILITY_LOGS : observed_in
    CLASSROOMS ||--o{ ATTENDANCE_SESSIONS : hosts
    CLASSROOMS ||--o{ ATTENDANCE_SESSION_SLOTS : hosts_slot

    ATTENDANCE_SESSIONS ||--o{ ATTENDANCE_SESSION_SLOTS : contains
    ATTENDANCE_SESSIONS ||--o{ ATTENDANCE_RECORDS : records
    ATTENDANCE_SESSIONS ||--o{ ATTENDANCE_STATUS_AUDIT_LOGS : audits

    EXAMS ||--o{ EXAM_QUESTIONS : has
    EXAMS ||--o{ EXAM_SUBMISSIONS : receives
    EXAMS ||--o{ EXAM_SUBMISSION_ANSWERS : scopes
    EXAM_QUESTIONS ||--o{ EXAM_QUESTION_OPTIONS : offers
    EXAM_QUESTIONS ||--o{ EXAM_SUBMISSION_ANSWERS : answered_by
    EXAM_SUBMISSIONS ||--o{ EXAM_SUBMISSION_ANSWERS : contains
    EXAM_QUESTION_OPTIONS |o--o{ EXAM_SUBMISSION_ANSWERS : selected_as

    USERS {
        bigint id PK "user id"
        string student_id UK "student login id"
        string professor_id UK "professor login id"
        string admin_id UK "admin login id"
        string name "display name"
        string role "student professor admin"
        string password "password hash"
        timestamp created_at "created time"
        timestamp updated_at "updated time"
    }

    CLASSROOMS {
        bigint id PK "classroom id"
        string classroom_code UK "room code"
        string name "classroom name"
        string building "building"
        string floor_label "floor"
        timestamp created_at "created time"
        timestamp updated_at "updated time"
    }

    COURSES {
        bigint id PK "course id"
        string course_code UK "course code"
        string title "course title"
        bigint professor_user_id FK "professor user id"
        timestamp created_at "created time"
        timestamp updated_at "updated time"
    }

    COURSE_ENROLLMENTS {
        bigint id PK "enrollment id"
        bigint course_id FK "course id"
        bigint student_user_id FK "student user id"
        string status "active etc"
        timestamp created_at "created time"
    }

    COURSE_SCHEDULES {
        bigint id PK "schedule id"
        bigint course_id FK "course id"
        bigint classroom_id FK "classroom id"
        int day_of_week "0 to 6"
        time starts_at "slot start"
        time ends_at "slot end"
        timestamp created_at "created time"
    }

    NOTICES {
        bigint id PK "notice id"
        bigint course_id FK "course id"
        bigint author_user_id FK "author user id"
        string title "notice title"
        string body "notice body"
        timestamp created_at "created time"
    }

    CLASSROOM_NETWORKS {
        bigint id PK "network id"
        bigint classroom_id FK "classroom id"
        string ap_id "access point id"
        string ssid "wifi ssid"
        string gateway_host "router host"
        int signal_threshold_dbm "minimum signal"
        string collection_mode "openwrt ssh etc"
        timestamp created_at "created time"
    }

    REGISTERED_DEVICES {
        bigint id PK "device id"
        bigint user_id FK "student user id"
        string label "device label"
        string mac_address UK "device mac"
        string status "active etc"
        timestamp created_at "created time"
        timestamp updated_at "updated time"
    }

    PRESENCE_ELIGIBILITY_LOGS {
        bigint id PK "presence log id"
        bigint student_user_id FK "student user id"
        bigint course_id FK "course id"
        bigint classroom_id FK "classroom id"
        string purpose "attendance exam etc"
        boolean eligible "presence decision"
        string reason_code "decision reason"
        string matched_device_mac "matched mac"
        json evidence "raw evidence"
        timestamp observed_at "observed time"
        int snapshot_age_seconds "snapshot age"
        timestamp created_at "created time"
    }

    REFRESH_SESSIONS {
        bigint id PK "refresh session id"
        string session_key UK "session key"
        bigint user_id FK "user id"
        string current_token_hash "refresh token hash"
        timestamp expires_at "expiry time"
        timestamp revoked_at "revoked time"
        timestamp replay_detected_at "replay detected time"
        timestamp last_rotated_at "last rotation time"
        timestamp created_at "created time"
        timestamp updated_at "updated time"
    }

    ATTENDANCE_SESSIONS {
        bigint id PK "attendance session id"
        string projection_key "bundle or slot key"
        bigint course_id FK "course id"
        bigint classroom_id FK "classroom id"
        date session_date "class date"
        time slot_start_at "representative start"
        time slot_end_at "representative end"
        string mode "manual smart canceled"
        string status "active closed expired canceled"
        bigint opened_by_user_id FK "professor user id"
        timestamp opened_at "opened time"
        timestamp closed_at "closed time"
        timestamp expires_at "expiry time"
        int latest_version "audit version"
        timestamp created_at "created time"
        timestamp updated_at "updated time"
    }

    ATTENDANCE_SESSION_SLOTS {
        bigint id PK "attendance slot id"
        bigint attendance_session_id FK "parent session id"
        string projection_key "slot projection key"
        bigint classroom_id FK "classroom id"
        date session_date "class date"
        time slot_start_at "slot start"
        time slot_end_at "slot end"
        int slot_order "bundle order"
        timestamp created_at "created time"
    }

    ATTENDANCE_RECORDS {
        bigint id PK "attendance record id"
        bigint attendance_session_id FK "session id"
        string projection_key "slot projection key"
        bigint student_user_id FK "student user id"
        string final_status "present absent late official sick"
        string attendance_reason "manual reason"
        bigint finalized_by_user_id FK "finalizer user id"
        timestamp finalized_at "finalized time"
        timestamp created_at "created time"
        timestamp updated_at "updated time"
    }

    ATTENDANCE_STATUS_AUDIT_LOGS {
        bigint id PK "attendance audit id"
        bigint attendance_session_id FK "session id"
        string projection_key "slot projection key"
        bigint student_user_id FK "student user id"
        bigint actor_user_id FK "actor user id"
        string actor_role "actor role"
        string change_source "manual smart system"
        string previous_status "before status"
        string new_status "after status"
        string reason "change reason"
        timestamp changed_at "changed time"
        int version "session version"
    }

    EXAMS {
        bigint id PK "exam id"
        bigint course_id FK "course id"
        string title "exam title"
        string description "exam description"
        string exam_type "quiz midterm final practice custom"
        string status "draft published open closed archived"
        timestamp starts_at "exam starts"
        timestamp ends_at "exam ends"
        int duration_minutes "time limit minutes"
        boolean requires_presence "presence required"
        boolean late_entry_allowed "late entry allowed"
        boolean auto_submit_enabled "auto submit enabled"
        boolean shuffle_questions "shuffle questions"
        boolean shuffle_options "shuffle options"
        int max_attempts "max attempts"
        timestamp created_at "created time"
        timestamp updated_at "updated time"
    }

    EXAM_QUESTIONS {
        bigint id PK "question id"
        bigint exam_id FK "exam id"
        int question_order "display order"
        string question_type "multiple choice true false"
        string prompt "question prompt"
        decimal points "question points"
        string correct_answer_text "canonical answer"
        string explanation "answer explanation"
        boolean is_required "required flag"
        timestamp created_at "created time"
        timestamp updated_at "updated time"
    }

    EXAM_QUESTION_OPTIONS {
        bigint id PK "option id"
        bigint question_id FK "question id"
        int option_order "display order"
        string option_text "option text"
        boolean is_correct "correct option flag"
        timestamp created_at "created time"
    }

    EXAM_SUBMISSIONS {
        bigint id PK "submission id"
        bigint exam_id FK "exam id"
        bigint student_user_id FK "student user id"
        int attempt_no "attempt number"
        string status "in progress submitted graded etc"
        timestamp started_at "started time"
        timestamp submitted_at "submitted time"
        timestamp expires_at "personal deadline"
        int time_limit_snapshot_minutes "snapshotted duration"
        decimal score "total score"
        timestamp created_at "created time"
        timestamp updated_at "updated time"
    }

    EXAM_SUBMISSION_ANSWERS {
        bigint id PK "answer id"
        bigint exam_id FK "exam id consistency key"
        bigint submission_id FK "submission id"
        bigint question_id FK "question id"
        bigint selected_option_id FK "selected option id"
        string answer_text "free text answer"
        boolean is_correct "grading result"
        decimal awarded_score "awarded score"
        timestamp answered_at "answered time"
        timestamp created_at "created time"
        timestamp updated_at "updated time"
    }
```


# 13.4 출석 모델 상세

출석 모델은 projected slot 과 bundle parent session 을 분리한다.
교수는 여러 projected slot 을 선택해 하나의 parent session 을 열 수 있고, 각 slot 은 `attendance_session_slots` 로 parent 아래에 저장된다.
학생 출석 결과는 slot 단위 `attendance_records` 로 저장하므로 리포트와 통계는 bundle metadata 가 아니라 slot별 final state 를 기준으로 계산한다.

중요 제약:

- `attendance_records` 는 `(attendance_session_id, projection_key, student_user_id)` 기준으로 유일하다.
- `attendance_status_audit_logs` 는 append-only 변경 이력이다.
- self check-in 재시도는 idempotent 해야 한다.
- 교수 수동 수정은 reason 을 요구한다.
- `canceled` 는 학생 출석 상태가 아니라 session lifecycle 또는 mode 로 취급한다.

# 13.5 시험 모델 상세

시험 MVP 는 객관식/진위형 중심이다.
시험은 강의에 속하고, 문제와 선택지를 가진다.
학생이 시험을 시작하면 `exam_submissions` row 가 생성되거나 진행 중 row 를 재사용한다.
답안은 `exam_submission_answers` 에 저장되고, 제출 시 객관식/진위형은 자동 채점할 수 있다.

# 13.6 데이터 무결성 원칙

- 사용자 role 은 학생/교수/서비스관리자 권한 분기의 근거다.
- 단말 MAC 은 전역 유일하게 관리한다.
- refresh session 은 replay detection 과 logout revocation 을 지원해야 한다.
- exam answer 는 같은 exam 에 속한 submission/question/option 만 참조해야 한다.
- 출석 audit 은 덮어쓰지 않고 누적한다.
- object storage 파일은 도메인 테이블의 메타데이터와 삭제 outbox 로 추적한다.
- collector token 은 원문을 저장하지 않고 hash/version/revoked 시점으로 관리한다.
