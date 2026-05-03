---
title: CI/CD 설계
type: report-section
status: draft
updated: 2026-05-03
owners:
  - team
related:
  - [[/04-architecture/local-runtime-topology.md]]
source:
  - Backend/.github
  - Front/.github
  - PresenceService/.github
  - DB/.github
  - Service/.github
  - docs/.github
  - [[/03-conventions/conv-release-and-deployment.md]]
  - [[/07-status/2026-04-26-ghcr-public-readiness-report.md]]
---

# 17. CI/CD 설계

# 17.1 현재 상태

현재 프로젝트는 `Service` repository 를 기준으로 local source mode, GHCR image mode, demo deployment mode 를 분리한다.
CI/CD 는 초기 계획 단계에서 벗어나 component image publish, Release Please 설정, Service release manifest 검증까지 구현되었다.
다만 실제 Release Please-created release run 과 demo-production 환경의 배포 workflow/server provenance 는 최종 증거로 추가 수집해야 한다.

# 17.2 목표 CI 파이프라인

```mermaid
flowchart LR
  A[Pull Request] --> B[Docs validation]
  A --> C[Backend lint/test]
  A --> D[PresenceService lint/test]
  A --> E[Front lint/build/e2e]
  A --> F[DB init validation]
  B --> G[Review]
  C --> G
  D --> G
  E --> G
  F --> G
  G --> H[Merge to main]
```

# 17.3 Repository별 CI 설계

| Repo | CI 작업 | 성공 기준 |
|---|---|---|
| docs | markdown frontmatter, wiki link, diff check | 깨진 링크/문법 없음 |
| Front | npm install, lint, build, Playwright e2e | lint/build/e2e 통과 |
| Backend | Python compile, pytest | 전체 테스트 통과 |
| PresenceService | Python compile, pytest | 전체 테스트 통과 |
| DB | PostgreSQL container init, schema/seed smoke | init script 성공, 핵심 row count 확인 |
| Service | compose config validation, manifest validation, nginx config test | local/image/demo 설정 유효 |
| CodexKit | bootstrap/governance helper test | runtime source of truth 를 Service 로 위임 |

# 17.4 CD 구현 상태

초기 CD 는 운영 배포보다 시연 환경 재현성을 우선한다.
구현된 흐름은 다음과 같다.

1. component repo main/release 에서 Docker image build 및 GHCR publish
2. Release Please 로 component version, changelog, release tag 관리
3. Service release manifest 로 Backend/Front/PresenceService/DB image ref 와 digest 고정
4. image mode 에서 local build context 없이 공개 GHCR 이미지로 실행
5. demo deploy script 에서 manifest render, DB reset guard, healthcheck 수행

2026-05-03 기준 Backend `v0.2.0`, Front `v0.2.1`, PresenceService `v0.2.0`, DB `v0.2.0` public image 는 로그인 없는 `docker manifest inspect` 가 통과했다.
기존 Service `v0.1.0` manifest 의 digest 포함 image ref 도 anonymous manifest inspect 가 통과했다.

# 17.5 보안 고려사항

- GitHub Secrets 로 DB password, JWT secret, sync token 관리
- PresenceService 는 public ingress 로 노출하지 않음
- `/api/internal` 은 Nginx 에서 외부 차단
- refresh token 은 HttpOnly cookie 사용
- OpenWrt token 은 UI 노출 시 prompt 방식 기본, inline reveal 은 명시적 동작으로 제한

# 17.6 향후 완료 기준

- 모든 PR 에서 repo별 CI 가 자동 실행된다.
- DB schema 변경은 container init smoke 를 통과해야 한다.
- Front e2e 는 로그인/권한/출석/시험 핵심 경로를 포함한다.
- 최종보고서에는 CI 실행 결과 캡처, workflow run 링크, Service demo deploy summary, public healthcheck 결과를 첨부한다.
