---
title: 데이터베이스 네이밍 규약
type: convention
status: active
updated: 2026-03-30
owners:
  - db-owner
applies_to:
  - db
  - backend
related:
  - data-model-overview
source:
  - 06-meetings/raw/2026-03-19-capstone-proposal.md
---

# 테이블 / 컬럼

- 테이블명은 `snake_case` 를 사용한다.
- 컬럼명도 `snake_case` 를 사용한다.
- 기본 키는 `id` 를 사용한다.
- 외래 키는 `<target>_id` 형식을 사용한다.

# 시간 / 상태

- 생성 시각은 `created_at`
- 수정 시각은 `updated_at`
- 상태 컬럼은 의미가 명확한 값 집합을 사용한다.

# 도메인별 예시

- `users`
- `courses`
- `classrooms`
- `course_schedules`
- `registered_devices`
- `attendance_records`
- `network_snapshots`

# 운영 규칙

- breaking schema 변경은 migration 과 rollback 설명이 필요하다.
- 서비스 경계에 영향을 주는 컬럼 변경은 docs 와 architecture 문서를 함께 갱신한다.
