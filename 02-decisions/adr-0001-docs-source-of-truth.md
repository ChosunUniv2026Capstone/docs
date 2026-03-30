---
title: ADR-0001 docs 레포를 프로젝트 truth source 로 사용
type: decision
status: accepted
updated: 2026-03-30
date: 2026-03-30
deciders:
  - team
supersedes: []
superseded_by: null
related:
  - [[/00-overview/project-summary.md]]
  - [[/03-conventions/conv-git-branch-and-pr.md]]
source:
  - [[/06-meetings/raw/2026-03-19-capstone-proposal.md]]
  - [[/06-meetings/raw/2026-03-25-kickoff-work-items.md]]
---

# Context

레포가 Front, Backend, PresenceService, DB, docs 로 분리되면 요구사항과 서비스 경계가 코드보다 먼저 정리되어야 한다.

# Decision

문서 레포 `docs` 를 프로젝트의 source of truth 로 사용한다.
요구사항, ADR, convention, architecture, meeting note, work item 은 모두 docs 레포에서 관리한다.

# Consequences

- 코드 변경 전에 관련 문서를 먼저 확인해야 한다.
- 문서 없는 규약은 구현하지 않는다.
- cross-repo 작업은 docs 갱신이 선행될 수 있다.
