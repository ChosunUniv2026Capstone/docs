---
title: 릴리스와 배포 규약
type: convention
status: active
updated: 2026-04-26
owners:
  - team
applies_to:
  - frontend
  - backend
  - presence
  - db
  - service
  - codexkit
related:
  - [[/02-decisions/adr-0011-service-repo-runtime-orchestration.md]]
  - [[/04-architecture/local-runtime-topology.md]]
  - [[/04-architecture/service-map.md]]
source:
  - .omx/plans/prd-ci-cd-service-repo-versioning.md
  - .omx/plans/test-spec-ci-cd-service-repo-versioning.md
  - .omx/plans/prd-ghcr-public-risk-versioning.md
  - .omx/plans/test-spec-ghcr-public-risk-versioning.md
---

# 목적

Smart Class runtime component 와 whole-service demo release 의 version, image, manifest, deploy evidence 를 일관되게 남기기 위한 규약이다.

# Component release

- `Backend`, `PresenceService`, `DB` 는 Release Please `simple` 전략을 사용한다.
- `Front` 는 Release Please `node` 전략을 사용해 `package.json` 과 changelog 를 함께 갱신한다.
- `Backend`, `PresenceService`, `DB`, `Service` 의 파일 기반 release truth 는 `version.txt` 와 `CHANGELOG.md` 이다.
- Backend FastAPI metadata version 은 첫 pass 에서 release truth 가 아니다.
- Conventional Commit 기반 release note 를 유지한다.

# Component image

- 각 runtime repo 는 PR 에서 image build 를 검증하되 push 하지 않는다.
- `main` push 는 `sha-<shortsha>` 와 `main` 또는 `edge` 태그를 GHCR 에 publish 한다.
- Release Please 가 실제 release 를 만들 때는 같은 workflow 안에서 `vX.Y.Z`, `vX.Y`, `sha-<shortsha>` 태그를 publish 한다. `vX` major tag 는 `X > 0` 인 경우에만 publish 한다.
- default `GITHUB_TOKEN` 으로 생성된 tag/release 가 downstream workflow 를 자동으로 깨운다는 가정은 금지한다.
- OCI label 에 source, version, revision 을 기록한다.

# GHCR access

- 첫 pass 정책은 public GHCR package 이며 demo server 는 anonymous pull 을 우선 사용한다.
- public-readiness 완료 조건은 Service release manifest 의 모든 component image 에 대해 로그인 없는 `docker manifest inspect` 또는 `docker pull` 이 성공하는 것이다.
- public package 가 허용되지 않는 경우에만 `GHCR_READ_TOKEN` private fallback 을 사용한다.
- private fallback 은 unauthenticated pull failure 와 authenticated pull success evidence 를 함께 남기되, public completion gate 를 대체하지 않는다.

# Service manifest release

- Service release 는 component image ref 를 모은 manifest release 이다.
- `manifests/releases/vX.Y.Z.yml` 은 Service release PR branch 에 포함되어야 한다.
- manifest 의 `serviceVersion` 은 `version.txt` 의 SemVer 값에 `v` prefix 를 붙인 값과 같아야 한다.
- manifest 는 Backend, Front, PresenceService, DB 의 image, version, tag, digest, release link 를 포함한다.
- DB component 는 `resetRequired` 를 명시한다.
- deploy 입력은 `latest` 나 floating tag 가 아니라 manifest-pinned tag/digest 를 사용한다.

# Demo deploy

- GitHub Actions demo deploy 는 `demo-production` environment 를 사용한다.
- required secrets/vars: `DEMO_SSH_HOST`, `DEMO_SSH_USER`, `DEMO_SSH_KEY`, `DEMO_PUBLIC_URL=https://smart-class.org`.
- `GHCR_READ_TOKEN` 은 private GHCR fallback 에서만 optional 로 사용한다.
- deploy input `service_version` 은 `vX.Y.Z` 형식이어야 한다.
- deploy input `reset_demo_data` 는 기본 `false` 이다.
- DB digest 변경과 `components.db.resetRequired: true` 가 동시에 관찰되면 `reset_demo_data=true` 없이는 compose apply 전에 실패해야 한다.
- reset 이 승인되어도 Service project 로 생성된 DB volume 만 제거할 수 있다.
- deploy evidence 는 service version, component refs, reset flag, GHCR pull/access result, host health, `https://smart-class.org/health` 결과를 포함한다.

# CodexKit delegation

- `CodexKit` 은 workspace bootstrap, helper install, shared hooks, repo templates 를 관리한다.
- runtime compose, nginx config, env example, release manifest, demo deploy source of truth 는 `Service` 에 둔다.
- CodexKit runtime wrapper 는 Service 가 없으면 actionable error 를 내고, 있으면 Service script 로 위임한다.
