---
title: 시험 MVP API 및 데이터 계약
type: architecture
status: active
updated: 2026-04-10
owners:
  - backend-team
  - frontend-team
  - db-owner
related:
  - [[/01-requirements/req-student-features.md]]
  - [[/01-requirements/req-professor-features.md]]
  - [[/01-requirements/req-attendance-presence.md]]
  - [[/03-conventions/conv-api-response.md]]
  - [[/03-conventions/conv-auth-and-session.md]]
  - [[/04-architecture/data-model-overview.md]]
  - [[/04-architecture/presence-eligibility-api.md]]
source:
  - docs-first exam MVP alignment, 2026-04-09
  - 2026-04-10 docs lane contract hardening against backend/front bundle review
---

# 목적

시험 기능의 첫 구현 단계에서 Front, Backend, DB 가 같은 범위와 같은 제약을 기준으로 움직이도록 학생 응시, 교수 운영, 접근 제어, 데이터 무결성의 최소 계약을 정의한다.

# 범위

- 학생 시험 목록 조회
- 학생 시험 상세 조회
- 학생 시험 응시 시작
- 학생 문항 답안 저장
- 학생 시험 제출
- 교수 시험 초안 생성
- 교수 문항 구성
- 교수 시험 게시
- 교수 시험 종료

첫 MVP 에서는 객관식(`multiple_choice`)과 진위형(`true_false`) 문항을 우선 지원한다.
`short_answer`, `essay`, 수동 채점, 성적표 공개 플로우는 후속 단계로 분리한다.

# 권한과 소유권

- 시험은 강의에 종속된다.
- 시험 소유 교수는 `courses.professor_user_id` 로부터 파생한다.
- `exams` 에 별도 `professor_user_id` 를 중복 저장하지 않는 것을 기본 계약으로 한다.
- 학생은 자신이 수강 중인 강의의 시험만 조회하거나 응시할 수 있다.
- 교수는 자신이 담당하는 강의의 시험만 생성, 수정, 게시, 종료할 수 있다.

# 접근 제어

- 시험 접근은 로그인 상태를 전제로 한다.
- 시험 응시 시작 시 Backend 는 다음 조건을 함께 검증해야 한다.
- 강의 수강 여부
- 시험 상태와 시간 창
- 최대 응시 횟수
- 시험 응시 시작 시점에는 학생 계정에 active registered device 가 최소 1개 있어야 하며, course classroom 기준 PresenceService eligibility 를 통과해야 한다.
- 로컬 시험 정책은 현재 수업 시간 여부를 시험 시작의 필수 조건으로 요구하지 않는다. 강의실 재실 evidence 는 설정된 presence source 를 따르며, `demo` evidence 는 collector evidence 와 같은 판정 지위를 가진다.
- 응시가 시작된 뒤 같은 submission 을 이어서 저장하거나 제출할 때는 재실성 재검사를 기본 요구로 두지 않는다.
- 등록 단말 또는 PresenceService eligibility 실패 시 stable error code 는 `PRESENCE_INELIGIBLE` 를 사용한다.
- 시작 시각 이후 새 응시를 허용하지 않는 시험은 `EXAM_LATE_ENTRY_NOT_ALLOWED` 로 거부한다.

# 상태 모델

## Exam status

- `draft`: 교수만 볼 수 있고 학생은 접근할 수 없다.
- `published`: 학생이 시험 정보를 볼 수 있지만 아직 응시 시작 가능 시간 전이다.
- `open`: 현재 시간 창에서 응시 시작이 가능하다.
- `closed`: 새 응시 시작이 불가능하다.
- `archived`: 활성 화면에서 숨긴다.

## Submission status

- `in_progress`: 응시 진행 중
- `submitted`: 학생이 직접 제출
- `auto_submitted`: 제한 시간 또는 시험 종료 시각으로 자동 제출
- `graded`: 후속 단계 확장용 상태
- `expired`: legacy compatibility 상태로만 유지하고, 새 MVP 구현에서는 `auto_submitted` 를 우선 사용한다.

# 시간 규칙

- 시험은 `starts_at`, `ends_at`, `duration_minutes` 를 가진다.
- 학생 개인 만료 시각은 `min(started_at + duration_minutes, exams.ends_at)` 로 계산한다.
- `late_entry_allowed=false` 이면 `now > starts_at` 시점의 신규 응시 시작을 허용하지 않는다.
- `late_entry_allowed=true` 이어도 `now >= ends_at` 이후에는 신규 응시를 허용하지 않는다.

# 데이터 모델

## `exams`

- 강의 소속 시험 마스터
- 주요 필드: `course_id`, `title`, `description`, `exam_type`, `status`, `starts_at`, `ends_at`, `duration_minutes`, `requires_presence`, `late_entry_allowed`, `auto_submit_enabled`, `shuffle_questions`, `shuffle_options`, `max_attempts`
- `requires_presence` 필드는 shared schema compatibility 를 위해 유지하며, 시험 생성 기본값은 `true` 이지만 생성/수정 시 명시된 `false` 값을 보존한다.

## `exam_questions`

- 시험 문항
- `(exam_id, question_order)` 는 유일해야 한다.
- MVP 에서는 `multiple_choice`, `true_false` 만 활성 사용한다.

## `exam_question_options`

- 문항 선택지
- `(question_id, option_order)` 는 유일해야 한다.
- 선택지는 반드시 자신의 `question_id` 범위 안에서만 사용되어야 한다.

## `exam_submissions`

- 학생별 시험 응시 attempt
- `(exam_id, student_user_id, attempt_no)` 는 유일해야 한다.
- 응시 시작 시 `time_limit_snapshot_minutes` 와 `expires_at` 를 고정해 이후 시험 수정이 과거 응시에 영향을 주지 않게 한다.

## `exam_submission_answers`

- 응시 내 문항별 최종 답안
- `(submission_id, question_id)` 는 유일해야 한다.
- 답안은 반드시 같은 submission 의 시험에 속한 question 만 참조할 수 있어야 한다.
- `selected_option_id` 는 반드시 같은 `question_id` 에 속한 option 만 참조할 수 있어야 한다.

# 학생 API 범위

## `GET /api/students/{student_id}/courses/{course_code}/exams`

- 학생이 자신의 강의 시험 목록을 조회한다.
- 응답에는 `id`, `title`, `exam_type`, `status`, `starts_at`, `ends_at`, `duration_minutes`, `requires_presence`, `max_attempts`, `attempts_used` 가 포함되어야 한다.
- 현재 로컬 UI 는 이 `requires_presence` 값을 설정용 토글로 사용하지 않는다.

## `GET /api/students/{student_id}/courses/{course_code}/exams/{exam_id}`

- 학생이 시험 상세를 조회한다.
- 시험이 `draft` 이면 학생에게 공개하면 안 된다.

## `POST /api/students/{student_id}/courses/{course_code}/exams/{exam_id}/start`

- 새 응시를 시작한다.
- `requires_presence=true` 인 시험은 `purpose=exam` 으로 PresenceService eligibility 를 확인한 뒤 응시를 생성한다.
- 성공 시 `submission_id`, `attempt_no`, `started_at`, `expires_at`, `status` 를 반환한다.
- 이미 진행 중인 응시가 있으면 기존 `in_progress` submission 을 재사용하는 것을 첫 MVP 기본 정책으로 한다.

## `PUT /api/students/{student_id}/courses/{course_code}/exams/{exam_id}/submissions/{submission_id}/answers/{question_id}`

- 문항 답안을 저장한다.
- 제출 완료 상태에서는 `EXAM_SUBMISSION_ALREADY_FINALIZED` 로 거부한다.

## `POST /api/students/{student_id}/courses/{course_code}/exams/{exam_id}/submit`

- 시험을 제출한다.
- 현재 로컬 MVP 는 학생별/시험별 active `in_progress` submission 하나만 유지하므로 submit route 는 `submission_id` 대신 exam-scoped endpoint 를 사용한다.
- 객관식/진위형만 포함된 MVP 시험은 제출 시 즉시 score 계산이 가능해야 한다.

# 교수 API 범위

## `GET /api/professors/{professor_id}/courses/{course_code}/exams`

- 담당 강의의 시험 목록을 조회한다.

## `POST /api/professors/{professor_id}/courses/{course_code}/exams`

- 시험 초안을 생성한다.
- 첫 MVP 에서는 문항과 선택지를 포함한 payload 생성 또는 생성 후 문항 추가 방식 둘 다 가능하지만, Backend 와 Front 는 한 방식을 문서 기준으로 고정해야 한다.

## `POST /api/professors/{professor_id}/courses/{course_code}/exams/{exam_id}/publish`

- 초안을 게시한다.
- 게시 시점에는 최소 1개 이상의 문항, 객관식/진위형의 경우 유효한 선택지와 정답 구성이 있어야 한다.

## `POST /api/professors/{professor_id}/courses/{course_code}/exams/{exam_id}/close`

- 시험을 종료한다.
- `auto_submit_enabled=true` 이면 진행 중 응시를 자동 제출 처리한다.

# 에러 코드

- `UNAUTHENTICATED`
- `FORBIDDEN`
- `COURSE_NOT_FOUND`
- `EXAM_NOT_FOUND`
- `EXAM_NOT_OPEN`
- `EXAM_ATTEMPT_LIMIT_REACHED`
- `EXAM_LATE_ENTRY_NOT_ALLOWED`
- `EXAM_SUBMISSION_NOT_FOUND`
- `EXAM_SUBMISSION_ALREADY_FINALIZED`
- `PRESENCE_INELIGIBLE`

# 구현 순서

1. docs 기준 고정
2. DB schema 반영
3. Backend model / schema / route 반영
4. Front API client / route / screen 반영

# DB 설계 메모

- `exam_submission_answers` 의 무결성 제약은 application validation 만으로 끝내지 않고 DB constraint 로도 보강한다.
- `selected_option_id` 와 `question_id` 정합성도 DB constraint 로 보강한다.
- 시험 소유 교수는 강의 소유권으로부터 파생하므로 DB 와 Backend 에서 중복 source of truth 를 만들지 않는다.
