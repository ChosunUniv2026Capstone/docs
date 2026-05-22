---
title: API Endpoint Inventory
type: report-appendix
status: draft
updated: 2026-05-22
owners:
  - backend-team
  - report-team
related:
  - [[/08-reports/10-body/11-backend-api-and-flows.md]]
  - [[/08-reports/90-appendix/05-evidence-ledger.md]]
source:
  - Backend/app/main.py
  - PresenceService/app/main.py
---

# 부록 C. API Endpoint Inventory

이 부록은 최종보고서의 API/코드 근거를 endpoint 목록과 대표 request/response 예시로 관리한다. response 예시는 현재 Backend API envelope 규칙을 반영해 `success`, `data`, `error` 형태를 사용한다.

# C.1 Backend

| Method | Path | Function |
|---|---|---|
| GET | `/health` | `health` |
| POST | `/api/auth/login` | `login` |
| POST | `/api/auth/refresh` | `refresh_auth_session` |
| GET | `/api/auth/bootstrap` | `bootstrap_auth_session` |
| GET | `/api/auth/me` | `bootstrap_auth_session_alias` |
| POST | `/api/auth/logout` | `logout_auth_session` |
| GET | `/api/students/{student_id}/courses` | `get_student_courses` |
| GET | `/api/professors/{professor_id}/courses` | `get_professor_courses` |
| GET | `/api/notices/{login_id}` | `get_notices` |
| GET | `/api/notices/{login_id}/{notice_id}` | `get_notice` |
| POST | `/api/professors/{professor_id}/notices` | `add_notice` |
| GET | `/api/admin/users` | `get_users` |
| GET | `/api/admin/classrooms` | `get_classrooms` |
| GET | `/api/admin/classroom-networks` | `get_classroom_networks` |
| PATCH | `/api/admin/classroom-networks/{network_id}` | `patch_classroom_network_threshold` |
| GET | `/api/admin/presence/classrooms/{classroomCode}/snapshot` | `get_admin_presence_snapshot` |
| POST | `/api/admin/presence/classrooms/{classroomCode}/dummy-controls` | `apply_admin_presence_overlay` |
| POST | `/api/admin/presence/classrooms/{classroomCode}/dummy-controls/reset` | `reset_admin_presence_overlay` |
| GET | `/api/students/{student_id}/devices` | `get_devices` |
| POST | `/api/students/{student_id}/devices` | `add_device` |
| DELETE | `/api/students/{student_id}/devices/{device_id}` | `remove_device` |
| POST | `/api/attendance/eligibility` | `attendance_eligibility` |
| GET | `/api/students/{student_id}/courses/{course_code}/attendance/bootstrap` | `student_attendance_bootstrap` |
| GET | `/api/professors/{professor_id}/courses/{course_code}/attendance/bootstrap` | `professor_attendance_bootstrap` |
| GET | `/api/professors/{professor_id}/courses/{course_code}/attendance/timeline` | `professor_attendance_timeline` |
| GET | `/api/professors/{professor_id}/courses/{course_code}/attendance/report` | `professor_attendance_report` |
| GET | `/api/professors/{professor_id}/courses/{course_code}/attendance/student-stats` | `professor_attendance_student_stats` |
| POST | `/api/professors/{professor_id}/courses/{course_code}/attendance/sessions/batch` | `professor_open_attendance_sessions_batch` |
| POST | `/api/professors/{professor_id}/attendance/sessions/{session_id}/close` | `professor_close_attendance` |
| GET | `/api/professors/{professor_id}/attendance/sessions/{session_id}/roster` | `professor_attendance_roster` |
| GET | `/api/professors/{professor_id}/courses/{course_code}/attendance/slot-roster` | `professor_attendance_slot_roster` |
| PATCH | `/api/professors/{professor_id}/attendance/sessions/{session_id}/students/{student_id}` | `professor_update_attendance_record` |
| GET | `/api/professors/{professor_id}/courses/{course_code}/attendance/students/{student_id}/history` | `professor_attendance_student_history` |
| GET | `/api/students/{student_id}/courses/{course_code}/attendance/active-sessions` | `student_active_attendance_sessions` |
| GET | `/api/students/{student_id}/courses/{course_code}/attendance/semester-matrix` | `student_attendance_semester_matrix` |
| POST | `/api/students/{student_id}/attendance/sessions/{session_id}/check-in` | `student_attendance_check_in_endpoint` |
| WS | `/ws/attendance` | `attendance_websocket` |
| GET | `/api/students/{student_id}/courses/{course_code}/exams` | `get_student_course_exams` |
| GET | `/api/students/{student_id}/courses/{course_code}/exams/{exam_id}` | `get_student_course_exam_detail` |
| POST | `/api/students/{student_id}/courses/{course_code}/exams/{exam_id}/start` | `start_student_course_exam` |
| PUT | `/api/students/{student_id}/courses/{course_code}/exams/{exam_id}/submissions/{submission_id}/answers/{question_id}` | `save_student_course_exam_answer` |
| POST | `/api/students/{student_id}/courses/{course_code}/exams/{exam_id}/submit` | `submit_student_course_exam` |
| GET | `/api/professors/{professor_id}/courses/{course_code}/exams` | `get_professor_course_exams` |
| POST | `/api/professors/{professor_id}/courses/{course_code}/exams` | `create_professor_course_exam` |
| GET | `/api/professors/{professor_id}/courses/{course_code}/exams/{exam_id}` | `get_professor_course_exam_detail` |
| PUT | `/api/professors/{professor_id}/courses/{course_code}/exams/{exam_id}` | `update_professor_course_exam` |
| DELETE | `/api/professors/{professor_id}/courses/{course_code}/exams/{exam_id}` | `delete_professor_course_exam` |
| POST | `/api/professors/{professor_id}/courses/{course_code}/exams/{exam_id}/publish` | `publish_professor_course_exam` |
| POST | `/api/professors/{professor_id}/courses/{course_code}/exams/{exam_id}/close` | `close_professor_course_exam` |

# C.2 PresenceService

| Method | Path | Function |
|---|---|---|
| GET | `/health` | `health` |
| GET | `/snapshots/classrooms/{classroom_id}` | `get_snapshot` |
| POST | `/eligibility/check` | `check_eligibility` |
| GET | `/admin/dummy/classrooms/{classroom_id}/snapshot` | `get_admin_snapshot` |
| POST | `/admin/dummy/classrooms/{classroom_id}/overlay` | `apply_dummy_overlay` |
| POST | `/admin/dummy/classrooms/{classroom_id}/overlay/reset` | `reset_dummy_overlay` |


# C.3 대표 request/response 예시

## C.3.1 인증 로그인

**Request**

```http
POST /api/auth/login
Content-Type: application/json

{
  "login_id": "20201239",
  "password": "devpass123"
}
```

**Response**

```json
{
  "success": true,
  "data": {
    "access_token": "<jwt>",
    "user": {
      "login_id": "20201239",
      "role": "student",
      "name": "Demo Student"
    },
    "route_access": {
      "dashboard": true,
      "student_courses": true
    }
  },
  "error": null
}
```

근거: `Backend/app/main.py:920`, `Backend/tests/test_presence_admin_and_auth.py:590`.

## C.3.2 출석 eligibility

**Request**

```http
POST /api/attendance/eligibility
Authorization: Bearer <student-access-token>
Content-Type: application/json

{
  "student_id": "20201239",
  "course_code": "CSE116",
  "purpose": "attendance",
  "classroom_code": "B101"
}
```

**Response**

```json
{
  "success": true,
  "data": {
    "eligible": true,
    "reason": "eligible",
    "classroom_code": "B101",
    "matched_device_id": "demo-device-1",
    "evidence": {
      "source": "demo-overlay",
      "ap_id": "b101-ap-1",
      "signal_dbm": -51,
      "threshold_dbm": -65
    }
  },
  "error": null
}
```

근거: `Backend/app/main.py:2028`, `PresenceService/app/main.py:88`, `Backend/tests/test_presence_admin_and_auth.py:906`.

## C.3.3 교수 출석 CSV export

**Request**

```http
POST /api/professors/PRF002/courses/CSE116/attendance/report-exports
Authorization: Bearer <professor-access-token>
Content-Type: application/json

{
  "format": "csv",
  "scope": "course-semester"
}
```

**Response**

```json
{
  "success": true,
  "data": {
    "id": 42,
    "course_code": "CSE116",
    "format": "csv",
    "status": "ready",
    "download_path": "/api/professors/PRF002/courses/CSE116/attendance/report-exports/42/download"
  },
  "error": null
}
```

근거: `Backend/app/main.py:2091`, `:2104`, `:2115`, weekly Backend commit `36e8524`, Front commit `73f5e09`.

## C.3.4 학생 시험 시작 및 답안 저장

### 시험 시작

**Request**

```http
POST /api/students/20201239/courses/CSE116/exams/1/start
Authorization: Bearer <student-access-token>
```

**Response**

```json
{
  "success": true,
  "data": {
    "submission_id": 1001,
    "exam_id": 1,
    "status": "in_progress",
    "started_at": "2026-05-22T02:00:00+09:00"
  },
  "error": null
}
```

### 답안 저장

**Request**

```http
PUT /api/students/20201239/courses/CSE116/exams/1/submissions/1001/answers/10
Authorization: Bearer <student-access-token>
Content-Type: application/json

{
  "selected_option_id": 44
}
```

**Response**

```json
{
  "success": true,
  "data": {
    "submission_id": 1001,
    "question_id": 10,
    "selected_option_id": 44,
    "is_answered": true,
    "saved_at": "2026-05-22T02:03:15+09:00"
  },
  "error": null
}
```

근거: `Backend/app/main.py:1492`, `:1682`, `:1706`, `Backend/tests/test_exam_contract_alignment.py:261`, `Front/tests/e2e/exam-workflow.spec.ts:244`.

## C.3.5 selected LMS: Q&A / learning progress / grade feedback

### Q&A 질문 등록

**Request**

```http
POST /api/students/20201239/courses/CSE116/qna
Authorization: Bearer <student-access-token>
Content-Type: application/json

{
  "title": "과제 제출 형식 문의",
  "body": "첨부파일 형식 제한이 있나요?"
}
```

**Response**

```json
{
  "success": true,
  "data": {
    "thread_id": 15,
    "course_code": "CSE116",
    "title": "과제 제출 형식 문의",
    "status": "open",
    "latest_post": {
      "author_login_id": "20201239",
      "body": "첨부파일 형식 제한이 있나요?"
    }
  },
  "error": null
}
```

### 학습 진도 저장

**Request**

```http
PUT /api/students/20201239/courses/CSE116/learning-items/7/progress
Authorization: Bearer <student-access-token>
Content-Type: application/json

{
  "progress_percent": 80
}
```

**Response**

```json
{
  "success": true,
  "data": {
    "learning_item_id": 7,
    "student_login_id": "20201239",
    "progress_percent": 80,
    "updated_at": "2026-05-22T02:04:20+09:00"
  },
  "error": null
}
```

### 성적·피드백 조회

**Request**

```http
GET /api/students/20201239/courses/CSE116/grades
Authorization: Bearer <student-access-token>
```

**Response**

```json
{
  "success": true,
  "data": {
    "assignments": [
      {
        "assignment_id": 3,
        "score": 92,
        "max_score": 100,
        "grading_status": "published",
        "feedback": "요구사항 분석이 구체적입니다."
      }
    ]
  },
  "error": null
}
```

근거: `Backend/app/main.py:1280`, `:1302`, `:1313`, `:1371`, `:1382`, `Backend/tests/test_lms_selected_subset.py:123`, `:172`, `:200`.

## C.3.6 PresenceService collector snapshot ingest

**Request**

```http
POST /collector/aps/b101-ap-1/snapshot
X-Collector-Token: <collector-token>
Content-Type: application/json

{
  "classroom_id": "B101",
  "interfaces": [
    {
      "interface_id": "wlan0",
      "stations": [
        {"mac": "AA:BB:CC:DD:EE:FF", "signal_dbm": -51, "connected": true}
      ]
    }
  ]
}
```

**Response**

```json
{
  "accepted": true,
  "collector_ap_id": "b101-ap-1",
  "stored_interfaces": 1,
  "stored_stations": 1
}
```

근거: `PresenceService/app/main.py:64`, `PresenceService/tests/test_service.py:296`, `DB/postgres/migrations/016_openwrt_collector_registry.sql`.
