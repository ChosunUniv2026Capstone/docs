---
title: Backend API 및 흐름
type: report-section
status: draft
updated: 2026-04-12
owners:
  - backend-team
related:
  - [[/04-architecture/service-map.md]]
  - [[/04-architecture/attendance-workflow-architecture.md]]
  - [[/04-architecture/exam-mvp-contract.md]]
source:
  - Backend/app/main.py
  - Backend/app/attendance.py
  - Backend/app/services.py
  - Backend/app/auth.py
---

# 11. Backend API 및 흐름

# 11.1 Backend 책임

Backend 는 LMS 도메인의 중심 서비스다.
인증, 권한 검사, 강의/공지/단말/시험/출석 API, 출석과 시험 접근의 최종 판단을 담당한다.
PresenceService 는 재실성 근거를 제공하지만, 최종 허용 여부는 Backend 가 수강 정보, 시간표, 강의실, 세션 상태와 함께 판단한다.

# 11.2 API 그룹

| 그룹 | Endpoint 예시 | 설명 |
|---|---|---|
| Health | `GET /health` | 서비스 상태 확인 |
| Auth | `/api/auth/login`, `/refresh`, `/bootstrap`, `/logout` | 로그인, 토큰 갱신, 세션 복구, 로그아웃 |
| Course | `/api/students/{id}/courses`, `/api/professors/{id}/courses` | 학생/교수 강의 목록 |
| Notice | `/api/notices/{login_id}`, `/api/professors/{id}/notices` | 공지 조회/작성 |
| Device | `/api/students/{id}/devices` | 학생 등록 단말 관리 |
| Admin | `/api/admin/users`, `/classrooms`, `/classroom-networks` | 운영 데이터 조회/수정 |
| Presence admin | `/api/admin/presence/classrooms/{code}/snapshot`, `/dummy-controls` | 관리자 재실성 snapshot/demo 제어 |
| Attendance eligibility | `POST /api/attendance/eligibility` | 출석/시험 eligibility 판정 |
| Attendance session | `/attendance/timeline`, `/sessions/batch`, `/roster`, `/check-in` | 교수/학생 출석 세션 운영 |
| Exam | `/courses/{course_code}/exams` | 학생 시험 응시, 교수 시험 운영 |
| Realtime | `WEBSOCKET /ws/attendance` | 출석 bootstrap/incremental event |

# 11.3 인증 흐름

```mermaid
sequenceDiagram
  participant F as Front
  participant B as Backend
  participant D as DB

  F->>B: POST /api/auth/login
  B->>D: users 조회 및 비밀번호 검증
  B->>D: refresh_sessions 생성 또는 갱신
  B-->>F: access token + refresh cookie
  F->>B: GET /api/auth/bootstrap
  B-->>F: user + route_access
  F->>B: 보호 API 호출 Authorization: Bearer
  alt access token expired
    F->>B: POST /api/auth/refresh
    B->>D: refresh token rotation 검증
    B-->>F: new access token
  end
```

# 11.4 출석 세션 흐름

```mermaid
sequenceDiagram
  participant P as 교수 Front
  participant B as Backend
  participant D as DB
  participant W as WebSocket Broker
  participant S as 학생 Front

  P->>B: POST /attendance/sessions/batch
  B->>D: projected slot 유효성/중복 active session 검사
  B->>D: attendance_sessions + attendance_session_slots 저장
  B->>W: attendance.session.batch_applied event
  W-->>P: 교수 timeline 갱신
  W-->>S: 학생 active session 갱신
  S->>B: POST /attendance/sessions/{session_id}/check-in
  B->>D: session/course/enrollment 조회
  B->>B: Presence eligibility 확인
  B->>D: attendance_records slot fan-out 저장
  B->>D: changed-only audit 저장
  B->>W: attendance.student.checked_in event
  W-->>P: roster/report 갱신
  W-->>S: check-in 결과 갱신
```

# 11.5 시험 흐름

```mermaid
flowchart TD
  A[교수 시험 초안 생성] --> B[문항/선택지 구성]
  B --> C[게시 조건 검증]
  C --> D[시험 published/open]
  D --> E[학생 시험 목록 조회]
  E --> F{응시 시작 가능?}
  F -- 아니오 --> G[거부 사유 반환]
  F -- 예 --> H[exam_submissions in_progress 생성/재사용]
  H --> I[학생 답안 저장]
  I --> J[시험 제출]
  J --> K[객관식/진위형 자동 채점]
  K --> L[submitted/auto_submitted 상태 저장]
```

# 11.6 주요 API 상세 초안

## 인증

| Method | Path | Request | Response | 권한 |
|---|---|---|---|---|
| POST | `/api/auth/login` | login_id, password | access token, user, refresh cookie | public |
| POST | `/api/auth/refresh` | refresh cookie | new access token | refresh session |
| GET | `/api/auth/bootstrap` | access 또는 refresh | user, route_access | authenticated |
| POST | `/api/auth/logout` | refresh cookie | success | authenticated |

## 출석

| Method | Path | 설명 |
|---|---|---|
| GET | `/api/professors/{professor_id}/courses/{course_code}/attendance/timeline` | 교수 출석 timeline/bootstrap |
| POST | `/api/professors/{professor_id}/courses/{course_code}/attendance/sessions/batch` | projected slot 묶음 출석 세션 열기 |
| POST | `/api/professors/{professor_id}/attendance/sessions/{session_id}/close` | 출석 세션 닫기 |
| GET | `/api/professors/{professor_id}/attendance/sessions/{session_id}/roster` | roster 조회 |
| PATCH | `/api/professors/{professor_id}/attendance/sessions/{session_id}/students/{student_id}` | 학생 출석 상태 수정 |
| GET | `/api/students/{student_id}/courses/{course_code}/attendance/active-sessions` | 학생 active 출석 세션 조회 |
| POST | `/api/students/{student_id}/attendance/sessions/{session_id}/check-in` | 학생 self check-in |

## 시험

| Method | Path | 설명 |
|---|---|---|
| GET | `/api/students/{student_id}/courses/{course_code}/exams` | 학생 시험 목록 |
| GET | `/api/students/{student_id}/courses/{course_code}/exams/{exam_id}` | 학생 시험 상세 |
| POST | `/api/students/{student_id}/courses/{course_code}/exams/{exam_id}/start` | 응시 시작 |
| PUT | `/api/students/{student_id}/courses/{course_code}/exams/{exam_id}/submissions/{submission_id}/answers/{question_id}` | 답안 저장 |
| POST | `/api/students/{student_id}/courses/{course_code}/exams/{exam_id}/submit` | 시험 제출 |
| POST | `/api/professors/{professor_id}/courses/{course_code}/exams` | 교수 시험 생성 |
| POST | `/api/professors/{professor_id}/courses/{course_code}/exams/{exam_id}/publish` | 시험 게시 |
| POST | `/api/professors/{professor_id}/courses/{course_code}/exams/{exam_id}/close` | 시험 종료 |

# 11.7 Backend 설계 특징

- API path 에 학생/교수 식별자가 포함되더라도 Backend 는 토큰 주체와 일치하는지 검증한다.
- 출석 session lifecycle 은 active, closed, expired, canceled 를 구분한다.
- 교수 수동 수정은 사유를 요구하고 audit log 를 남긴다.
- WebSocket 은 bootstrap 이후 incremental event 를 발행해 화면 간 상태를 맞춘다.
- 시험 응시 시작은 exam 상태, 시간 창, attempt 제한, 등록 단말 조건을 함께 확인한다.
