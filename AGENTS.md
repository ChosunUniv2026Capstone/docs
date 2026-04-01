# docs AGENTS

이 repo 는 프로젝트의 source of truth 이다.

## 역할
- 프로젝트 개요
- requirement
- decision(ADR)
- convention
- architecture
- work item
- meeting raw / digested
- status / risk / open question

## 필수 원칙
- 원본 회의록은 `06-meetings/raw/` 에 보존한다.
- 회의 요약은 `06-meetings/digested/` 에 둔다.
- requirement / convention / architecture 는 current truth 유지
- status / meeting summary 는 latest-first 유지
- ADR 은 한 문서 = 한 결정
- 불확실한 논의는 requirement / convention 으로 승격하지 않는다.

## 작업 시작 전
- `git checkout main`
- `git pull --ff-only origin main`
- `main` 에서 직접 commit 하지 않는다. bootstrap 이 설치한 shared hook 이 이를 차단한다.
- 기능 시작은 `./start_feature.sh <slug>` 또는 `./start_feature.sh --worktree <slug>` 를 우선 사용한다.

## 권장 skill
- 회의록 분해: `$meeting-doc-router`
- Git 규약 확인: `$git-governance`

## 파일명 규칙
- requirement: `req-<slug>.md`
- convention: `conv-<slug>.md`
- decision: `adr-####-<slug>.md`
- task: `task-<slug>.md`
- meeting raw: `YYYY-MM-DD-<slug>.md`
- meeting digested: `YYYY-MM-DD-<slug>-summary.md`

## 커밋/PR
- `docs(docs): ...`, `feat(docs): ...`, `chore(docs): ...` 형태 사용
- raw/digested summary 와 requirement/ADR/convention 변경은 가능하면 분리 commit
- PR 본문에는 source 문서와 변경 이유를 남긴다
