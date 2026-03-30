---
title: Git 브랜치와 PR 규약
type: convention
status: active
updated: 2026-03-30
owners:
  - team
applies_to:
  - docs
  - frontend
  - backend
  - presence
  - db
related:
  - [[/02-decisions/adr-0001-docs-source-of-truth.md]]
source:
  - [[/06-meetings/raw/2026-03-25-kickoff-work-items.md]]
---

# 브랜치

- 형식: `<type>/<scope>/<slug>`
- 허용 scope: `docs`, `frontend`, `backend`, `presence`, `db`, `infra`
- 예시: `feat/backend/attendance-check-api`

# 커밋

- 형식: `<type>(<scope>): <subject>`
- 예시: `feat(backend): add attendance eligibility endpoint`
- 한 commit 은 하나의 리뷰 가능한 논리 단위로 유지한다.

# PR

- 하나의 목적에 집중한다.
- 참고 문서, 테스트 결과, docs 변경 여부를 반드시 적는다.
- docs 와 code 가 같이 바뀌면 docs 를 먼저 정리한다.

# 금지 규칙

- 문서 없는 규약을 추측해서 구현하기
- 여러 repo 변경을 하나의 commit 으로 묶기
- `git add .` 로 무차별 staging 하기
- 명시 승인 없이 `main` 직접 push 하기
