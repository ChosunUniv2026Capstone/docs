---
title: Git 브랜치와 PR 규약
type: convention
status: active
updated: 2026-04-06
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

- 형식: `<type>/<slug>`
- 예시: `feat/attendance-check-api`
- 예시: `fix/openwrt-client-parser`
- 예시: `docs/update-git-convention`
- 로컬 작업은 반드시 feature branch 에서 시작한다. `main` 에서의 직접 commit/push 는 로컬 hook 으로 차단된다.

# 커밋

- 형식: `<type>(<scope>): <subject>`
- 예시: `feat(backend): add attendance eligibility endpoint`
- 한 commit 은 하나의 리뷰 가능한 논리 단위로 유지한다.

# Git identity

- commit 전에는 `user.name` 과 `user.email` 이 반드시 설정되어 있어야 한다.
- bootstrap 이 설치한 shared hook 은 비어 있는 Git identity 를 차단한다.
- bootstrap 이 설치한 shared hook 은 `Codex` 계열 기본값(예: `OpenAI Codex`, `codex@openai.com`)을 차단한다.
- 사람이 직접 입력한 non-Codex 이름/이메일은 추가 allowlist 없이 허용한다.
- 차단되면 에이전트는 사용자에게 이름/이메일을 물어 아래처럼 설정한 뒤 다시 commit/push 를 진행한다.

```bash
git config user.name "Your Name"
git config user.email "your-email@example.com"
```

# PR

- 하나의 목적에 집중한다.
- 참고 문서, 테스트 결과, docs 변경 여부를 반드시 적는다.
- docs 와 code 가 같이 바뀌면 docs 를 먼저 정리한다.

# 금지 규칙

- 문서 없는 규약을 추측해서 구현하기
- 여러 repo 변경을 하나의 commit 으로 묶기
- `git add .` 로 무차별 staging 하기
- Git identity 가 비어 있거나 `Codex` 기본값인 상태로 commit/push 하기
- 명시 승인 없이 `main` 직접 push 하기
