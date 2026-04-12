---
title: API Endpoint Inventory
type: report-appendix
status: draft
updated: 2026-04-12
owners:
  - backend-team
related:
  - [[/08-reports/10-body/11-backend-api-and-flows.md]]
source:
  - Backend/app/main.py
  - PresenceService/app/main.py
---

# 부록 C. API Endpoint Inventory

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
