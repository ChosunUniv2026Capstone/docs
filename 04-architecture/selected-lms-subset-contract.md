---
title: 선택 LMS 서브셋 계약
type: architecture
status: active
updated: 2026-05-16
owners:
  - backend-team
  - frontend-team
  - db-owner
related:
  - [[/01-requirements/req-student-features.md]]
  - [[/01-requirements/req-professor-features.md]]
  - [[/03-conventions/conv-api-response.md]]
  - [[/04-architecture/assignment-workflow-api.md]]
  - [[/04-architecture/data-model-overview.md]]
source:
  - GitHub Backend #36 selected LMS subset discussion
  - .omx/plans/ralplan-docs-impl-issues-approved.md
---

# 목표

데모/첫 운영 범위에서 이미 존재하는 강의, 과제, 시험, 공지, 학습자료 흐름 위에 다음 네 가지 LMS 기능만 추가한다.

1. 성적 조회 / 관리
2. 과제 채점 결과와 피드백
3. 질문게시판 / 문의
4. 학습자료 기반 진도율

# 비목표

- 회원가입 / self-registration
- 수강신청 / 승인 workflow
- 전체 관리자 CRUD
- OpenWrt pull/SSH collection 재도입
- 대형 UI redesign
- 가중치, 커브, 최종 성적 확정/공시, PDF/CSV 성적표 생성

# 공통 규칙

- 모든 `/api` JSON 응답은 [[/03-conventions/conv-api-response.md]] envelope 를 사용한다.
- 학생 route 는 authenticated student 본인과 enrollment 를 확인한다.
- 교수 route 는 authenticated professor 본인과 course ownership 을 확인한다.
- 관리자용 전체 CRUD 는 만들지 않는다.
- 새 DB 변경은 additive/idempotent migration 으로 제공하고, 기존 데모 데이터가 깨지면 안 된다.

# 성적 / 과제 채점 계약

## 데이터 모델

- `assignments.max_score`
  - 과제 만점. 기존 row 는 `100.00` 으로 보정한다.
- `assignment_submissions.score`
  - 학생 제출물 점수. `NULL` 이면 미채점이다.
- `assignment_submissions.feedback`
  - 학생에게 공개되는 교수 피드백.
- `assignment_submissions.graded_by_user_id`
  - 채점 교수 `users.id`.
- `assignment_submissions.graded_at`
  - 마지막 채점 시각.
- `assignment_submissions.grading_status`
  - `submitted`, `graded`, `returned` 중 하나.

## API

- `GET /api/students/{student_id}/courses/{course_code}/grades`
  - 학생 자신의 course grade summary 를 반환한다.
  - assignment grade 와 exam score 를 한 목록에 포함한다.
  - `overall_percent` 는 점수가 존재하는 항목들의 단순 평균이다. 가중치는 첫 범위에서 지원하지 않는다.
- `GET /api/professors/{professor_id}/courses/{course_code}/grades`
  - 교수 담당 강의의 학생별 grade summary 를 반환한다.
- `PUT /api/professors/{professor_id}/courses/{course_code}/assignments/{assignment_id}/submissions/{submission_id}/grade`
  - 과제 제출물을 채점하거나 피드백을 수정한다.
  - request: `{ "score": number | null, "feedback": string | null, "grading_status": "submitted" | "graded" | "returned" }`
  - `score` 가 있으면 `0 <= score <= assignment.max_score` 이어야 한다.
  - response 는 갱신된 professor assignment detail 또는 graded submission 을 반환할 수 있다.

## UI

- 학생은 강의 상세에서 성적/피드백을 확인할 수 있어야 한다.
- 학생은 과제 상세에서 점수와 피드백을 바로 볼 수 있어야 한다.
- 교수는 과제 제출물 상세에서 점수, 상태, 피드백을 입력/수정할 수 있어야 한다.

# 질문게시판 / 문의 계약

## 데이터 모델

- `course_qna_threads`
  - `course_id`, `student_user_id`, `title`, `body`, `status`, `created_at`, `updated_at`
  - `status`: `open`, `answered`, `closed`
- `course_qna_posts`
  - `thread_id`, `author_user_id`, `body`, `post_type`, `created_at`
  - `post_type`: `question`, `answer`, `comment`

## API

- `GET /api/students/{student_id}/courses/{course_code}/qna`
  - 학생 자신의 질문과 답변을 최신순으로 조회한다.
- `POST /api/students/{student_id}/courses/{course_code}/qna`
  - 학생이 문의를 작성한다.
  - request: `{ "title": string, "body": string }`
- `GET /api/professors/{professor_id}/courses/{course_code}/qna`
  - 담당 강의의 전체 문의를 최신순으로 조회한다.
- `POST /api/professors/{professor_id}/courses/{course_code}/qna/{thread_id}/answer`
  - 문의 답변을 등록하고 thread status 를 `answered` 로 바꾼다.
  - request: `{ "body": string, "close": boolean }`
  - `close` 가 true 이면 status 는 `closed` 이다.

## UI

- 학생은 강의 상세에서 문의 작성과 답변 확인을 할 수 있어야 한다.
- 교수는 강의 상세에서 문의 목록과 답변 입력을 할 수 있어야 한다.
- 첫 범위에서는 첨부, 검색, 태그, 관리자 moderation 을 지원하지 않는다.

# 학습 진도율 계약

## 데이터 모델

- `learning_progress`
  - `learning_item_id`, `student_user_id` 유니크
  - `progress_percent` 는 `0..100`
  - `status`: `not_started`, `in_progress`, `completed`
  - `last_viewed_at`, `completed_at`, `updated_at`

## API

- `GET /api/students/{student_id}/courses/{course_code}/learning-progress`
  - 학생 자신의 학습자료별 진도율을 반환한다.
- `PUT /api/students/{student_id}/courses/{course_code}/learning-items/{learning_item_id}/progress`
  - 학생 자신의 학습자료 진도율을 갱신한다.
  - request: `{ "progress_percent": number, "status": "not_started" | "in_progress" | "completed" }`
  - `completed` 는 `progress_percent=100` 으로 정규화할 수 있다.
- `GET /api/professors/{professor_id}/courses/{course_code}/learning-progress`
  - 담당 강의 학생별/자료별 진도율 snapshot 을 반환한다.

## UI

- 학생은 강의자료 목록에서 자료별 진도율과 상태를 볼 수 있어야 한다.
- 학생은 데모 UI 에서 자료별 진도율을 수동으로 갱신할 수 있다.
- 교수는 강의 단위로 학생별 진도율을 확인할 수 있어야 한다.

# 오류 코드

새 API 는 기존 공통 코드를 재사용하고, 필요 시 다음 코드를 사용한다.

- `ASSIGNMENT_NOT_FOUND`
- `ASSIGNMENT_SUBMISSION_NOT_FOUND`
- `ASSIGNMENT_INVALID_GRADE`
- `QNA_THREAD_NOT_FOUND`
- `QNA_INVALID_PAYLOAD`
- `LEARNING_ITEM_NOT_FOUND`
- `LEARNING_PROGRESS_INVALID_PAYLOAD`
- `FORBIDDEN`
- `UNAUTHENTICATED`

# 수용 기준

- 학생은 자신이 수강 중인 강의의 성적, 피드백, 문의, 진도만 볼 수 있다.
- 교수는 자신이 담당하는 강의의 제출물 채점, 문의 답변, 진도 조회만 할 수 있다.
- 새 API 는 envelope 계약을 따른다.
- DB migration 은 기존 volume 에 적용 가능해야 한다.
- seed/demo data 는 최소 1개의 성적, 과제 피드백, Q&A thread, learning progress 예시를 제공해야 한다.
