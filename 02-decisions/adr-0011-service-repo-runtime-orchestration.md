---
title: ADR-0011 Service Repo Runtime Orchestration
type: decision
status: accepted
updated: 2026-04-26
date: 2026-04-26
deciders:
  - team
supersedes: []
superseded_by: null
related:
  - [[/04-architecture/local-runtime-topology.md]]
  - [[/04-architecture/service-map.md]]
  - [[/04-architecture/attendance-demo-seed-reset.md]]
  - [[/03-conventions/conv-release-and-deployment.md]]
source:
  - .omx/plans/prd-ci-cd-service-repo-versioning.md
  - .omx/plans/test-spec-ci-cd-service-repo-versioning.md
---

# Context

Smart Class needs a repeatable demo-production path that can run from local source builds, GHCR image refs, and manifest-pinned demo releases.
The current runtime compose/nginx/env files historically lived under `CodexKit`, but `CodexKit` also owns bootstrap, helper installation, shared hooks, and workflow governance.
Keeping runtime orchestration inside that kit blurs operational ownership and leaves no canonical home for whole-service release manifests.

# Decision

Create and use `Service` as the canonical runtime orchestration repository for Smart Class.

`Service` owns:

- root-level compose files for local, image, and demo modes;
- edge nginx runtime config for local onboarding and `smart-class.org` demo routing;
- release manifests that pin component image refs and DB reset requirements;
- scripts for local source startup, image startup, manifest rendering, demo deployment, and health checks;
- Service-level Release Please configuration and deployment workflows.

Runtime component repos (`Backend`, `Front`, `PresenceService`, `DB`) own their own PR CI, image publishing, and component release workflows.
`CodexKit` remains the workspace bootstrap/governance kit and delegates runtime startup to `Service` instead of owning compose/nginx/env source of truth.

# Locked contracts

- `Service/compose.yml` is the base compose file.
- `Service/compose.local.yml` uses sibling build contexts: `../Backend`, `../Front`, `../PresenceService`, `../DB`.
- `Service/compose.image.yml` consumes GHCR image environment variables and must not require local build contexts.
- `Service/compose.demo.yml` applies demo restart policy, demo nginx config, and the `3100` host port.
- Wrapper scripts run Docker Compose with `--project-directory "$SERVICE_ROOT"` to avoid path ambiguity.
- Demo deploy reads `manifests/releases/vX.Y.Z.yml` from the checked-out `Service` tag `vX.Y.Z`.
- DB image/digest changes that require seed replay are guarded by `components.db.resetRequired` and an explicit `reset_demo_data=true` deploy input.
- First-pass GHCR policy is public packages for anonymous demo pulls; private package fallback requires explicit read-token configuration and evidence.
- `docs/08-reports/**` is not updated as part of this current-truth change unless a report refresh is explicitly requested.

# Consequences

- A new `Service` repo/folder becomes part of the managed workspace.
- Runtime docs and onboarding references must name `Service`, not `CodexKit`, as the compose/nginx/deploy owner.
- Whole-service releases become manifest releases that record component versions, image refs, digests, reset policy, and patch notes.
- Demo deployment remains intentionally single-host and disposable; high availability, zero-downtime deployment, and automatic rollback are out of scope for this decision.
