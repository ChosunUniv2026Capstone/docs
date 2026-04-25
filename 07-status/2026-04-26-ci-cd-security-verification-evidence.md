---
title: CI/CD 보안 및 검증 증거
type: status
status: active
updated: 2026-04-26
owners:
  - team
related:
  - [[/02-decisions/adr-0011-service-repo-runtime-orchestration.md]]
  - [[/03-conventions/conv-release-and-deployment.md]]
  - [[/04-architecture/local-runtime-topology.md]]
  - [[/04-architecture/service-map.md]]
source:
  - .omx/plans/prd-ci-cd-service-repo-versioning.md
  - .omx/plans/test-spec-ci-cd-service-repo-versioning.md
---

# CI/CD security and verification evidence

이 문서는 CI/CD, GHCR image, Service manifest release, demo deploy 작업의 security gate 와 verification evidence 를 추적하는 current-truth 상태 문서이다. `08-reports` 는 제출 snapshot 이므로 이 증거 수집 작업에서는 갱신하지 않는다.

## Security gate

| Gate | Required evidence | Current evidence | Status |
|---|---|---|---|
| Secrets in source | Tracked files must not contain private keys, GitHub tokens, OpenAI keys, AWS access keys, or Slack tokens. | 2026-04-26 `git grep` secret-pattern scan over tracked files in `docs`, `Backend`, `Front`, `PresenceService`, `DB`, and `CodexKit` returned no matches. | PASS |
| PR image safety | Pull requests may build images but must not push to GHCR or require package write credentials. | Backend, PresenceService, and DB image workflows gate GHCR login and push with `github.event_name != 'pull_request'`. Front and Service evidence is still pending implementation. | PARTIAL |
| GHCR least privilege | Image publish workflows use `contents: read` and `packages: write`; runtime pulls use anonymous public access or an explicit read-only fallback token. | Backend, PresenceService, and DB image workflows set `permissions: contents: read, packages: write`. `GHCR_READ_TOKEN` is documented as private fallback only in release/deploy convention. Live package visibility evidence is credential/network blocked until first publish. | PARTIAL |
| Demo deploy secrets | Demo deploy uses GitHub environment secrets/vars and must not commit SSH keys or tokens. | Required secret names are documented in `conv-release-and-deployment.md`; no private key/token patterns were found in tracked files. Service deploy workflow evidence is pending. | PARTIAL |
| DB reset safety | DB reset is opt-in and limited to Service project DB volume(s). | Convention requires `reset_demo_data=true` and named Service project volume removal only. Script-level negative/positive evidence is pending Service implementation. | PARTIAL |
| Reports gate | `docs/08-reports/**` stays untouched unless report refresh is explicitly requested. | 2026-04-26 `git -C docs status --short -- docs/08-reports` returned no changes. | PASS |

## Verification evidence matrix

| Area | Check | Latest local evidence | Status |
|---|---|---|---|
| Docs frontmatter | Status documents keep YAML frontmatter delimiters. | `python3` frontmatter check passed for the new evidence document. | PASS |
| Docs reports gate | No `08-reports` changes in docs working tree. | `git -C docs status --short -- docs/08-reports` returned empty output. | PASS |
| Secret scan | Regex scan for private keys and common token prefixes across tracked files. | No matches in `docs`, `Backend`, `Front`, `PresenceService`, `DB`, or `CodexKit`. | PASS |
| Component workflow security | PRs do not push images; main/tag publishes via GHCR login. | Verified in current Backend, PresenceService, and DB `release-image.yml`; worker-6 support scan also found Front workflow files missing/pending in this checkout. | PARTIAL |
| Service compose validation | `docker compose --project-directory Service ... config` for local/image/demo modes. | BLOCKED: `Service/` does not exist yet in this checkout at evidence collection time. Worker-6 independently confirmed missing Service compose/nginx/manifest/deploy files in `.omx/team-evidence/worker-6-task-8-verification-checklist.md`. | BLOCKED |
| Service manifest validation | Manifest schema and `version.txt` match checks. | BLOCKED: Service manifest scripts/files not present yet; worker-6 support scan also found Service absent. | BLOCKED |
| Demo deployment | `demo-production` workflow summary, image pull evidence, host health, `https://smart-class.org/health`. | BLOCKED: requires Service workflow plus GitHub secrets/demo server access. | BLOCKED |
| GHCR package pull | Anonymous pull for public packages or authenticated pull for private fallback. | BLOCKED: requires first successful package publish and package visibility/access configuration. | BLOCKED |

## Integration support evidence

Worker-6 supplied an independent verification support checklist at `.omx/team-evidence/worker-6-task-8-verification-checklist.md` on 2026-04-26. The checklist corroborates these worker-4 gates:

- `Service/` is absent in the current integration checkout, so Service compose, nginx, manifest, and deploy checks are blocked until the Service lane lands.
- Front CI/image/release workflow files are still pending in the current checkout.
- `CodexKit` has uncommitted delegation changes plus `install/tests/__pycache__/`; the cache directory should be removed before that lane commits.
- Current-truth docs targets exist, and final verification still needs the reports gate confirmation.
- No secrets were observed by the support scan.

## Credential-blocked checks

The following checks require authority or external runtime state unavailable to local workers:

1. GitHub Actions workflow run URLs for PR CI, image publish, and Release Please release-created branches.
2. GHCR package visibility changes and anonymous/private pull proof.
3. GitHub environment `demo-production` secrets/vars.
4. Demo server SSH access and post-deploy `https://smart-class.org/health` evidence.

## Required final evidence bundle before shutdown

- Workflow links for each component repo PR CI.
- Workflow links/log excerpts for image publish and same-workflow SemVer tag publication.
- GHCR package visibility or authenticated fallback pull output.
- Service compose config output for local, image, and demo modes.
- Service manifest validation and render output.
- DB reset gate negative, positive, and reset-safe outputs.
- Demo deploy workflow summary with component refs, reset flag, GHCR evidence, and healthcheck output.
- Confirmation that `docs/08-reports/**` remained unchanged unless a user explicitly requested report refresh.
