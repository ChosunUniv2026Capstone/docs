---
title: 공지 조회 및 작성 API 계약
type: architecture
status: active
updated: 2026-04-05
owners:
  - backend-team
  - frontend-team
related:
  - [[/01-requirements/req-student-features.md]]
  - [[/01-requirements/req-professor-features.md]]
  - [[/03-conventions/conv-api-response.md]]
  - [[/03-conventions/conv-auth-and-session.md]]
  - [[/05-work-items/task-phase-2-academic-read-model.md]]
source:
  - docs-first cross-repo notice-detail alignment, 2026-04-05
---

# 목적

현재 학사 조회 슬라이스에서 사용하는 공지 목록 조회, 상세 조회, 작성의 request/response/error 계약을 정의한다.

# 범위

- `GET /api/notices/{login_id}`
- `GET /api/notices/{login_id}/{notice_id}`
- `POST /api/professors/{professor_id}/notices`

# 인증 / 권한 규칙

- Front 는 로그인 응답의 `access_token` 을 `Authorization: Bearer <token>` 형태로 전송한다.
- Backend 는 토큰 주체와 path parameter 의 사용자 식별자가 일치하는지 확인해야 한다.
- 학생은 자신이 수강 중인 강의 범위의 공지만 조회할 수 있다.
- 교수는 자신이 작성한 공지만 조회하고 작성할 수 있다.
- 관리자용 공지 조회/작성 흐름은 이번 범위에 포함하지 않는다.

# 목록 조회

## Request

`GET /api/notices/{login_id}`

## Success response

```json
{
  "success": true,
  "data": [
    {
      "id": 101,
      "title": "중간고사 범위 안내",
      "body": "5주차까지 학습 내용을 범위로 합니다.",
      "course_code": "CSE101",
      "author_name": "김교수",
      "created_at": "2026-04-05T09:00:00+09:00"
    }
  ],
  "message": "ok",
  "meta": {
    "login_id": "20201234",
    "count": 1
  }
}
```

# 상세 조회

## Request

`GET /api/notices/{login_id}/{notice_id}`

## Success response

상세 조회는 현재 단계에서 목록 조회와 동일한 필드를 반환한다.
추가 필드가 필요해지면 docs 를 먼저 갱신한 뒤 Backend / Front 를 함께 수정한다.

```json
{
  "success": true,
  "data": {
    "id": 101,
    "title": "중간고사 범위 안내",
    "body": "5주차까지 학습 내용을 범위로 합니다.",
    "course_code": "CSE101",
    "author_name": "김교수",
    "created_at": "2026-04-05T09:00:00+09:00"
  },
  "message": "ok",
  "meta": {
    "login_id": "20201234"
  }
}
```

# 작성

## Request

`POST /api/professors/{professor_id}/notices`

```json
{
  "title": "보강 수업 안내",
  "body": "금요일 3교시에 온라인 보강을 진행합니다.",
  "course_code": "CSE101"
}
```

## Success response

```json
{
  "success": true,
  "data": {
    "id": 102,
    "title": "보강 수업 안내",
    "body": "금요일 3교시에 온라인 보강을 진행합니다.",
    "course_code": "CSE101",
    "author_name": "김교수",
    "created_at": "2026-04-05T11:00:00+09:00"
  },
  "message": "created",
  "meta": {
    "professor_id": "PRF001"
  }
}
```

# 오류 코드

- `UNAUTHENTICATED`
- `FORBIDDEN`
- `NOTICE_NOT_FOUND`
- `PROFESSOR_NOT_FOUND`
- `COURSE_NOT_FOUND`

# 임시 학습 자료 / 동영상 스캐폴드와의 관계

- 공지 조회/상세/작성은 실제 Backend 계약을 가진다.
- 강의자료 / 동영상 영역은 이번 단계에서 Front 임시 스캐폴드만 허용되며, 이 문서의 범위에 포함되지 않는다.
