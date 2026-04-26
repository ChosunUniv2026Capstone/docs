---
title: GHCR 공개 준비성 및 잔여 리스크 보고서
type: status
status: active
updated: 2026-04-26
owners:
  - team
related:
  - [[/03-conventions/conv-release-and-deployment.md]]
  - [[/07-status/2026-04-26-ci-cd-security-verification-evidence.md]]
source:
  - .omx/plans/prd-ghcr-public-risk-versioning.md
  - .omx/plans/test-spec-ghcr-public-risk-versioning.md
---

# GHCR public-readiness report

이 문서는 Smart Class demo stack 의 public GHCR 전환을 위해 필요한 secret/PII scan, demo seed 공개 허용 범위, anonymous image pull proof, demo health proof 를 한 곳에 남기는 current-truth 보고서이다. `08-reports` 는 제출 snapshot 이므로 이번 current-truth 갱신에서는 변경하지 않는다.

## 결론

| Gate | Current result | Evidence |
|---|---|---|
| Secret/PII scan doc | PASS with accepted demo fixtures | 2026-04-26 local scan covered tracked files in `Backend`, `PresenceService`, `DB`, `Front`, `Service`, `docs`; Docker build context inputs; Service env examples; DB seed files. No private key, GitHub token, AWS key, Slack token, or real OpenAI key pattern was found after classifying documented `sk-*` slugs as non-secret identifiers. |
| Public pull proof | BLOCKED | Anonymous `docker manifest inspect` returned `denied` for all four manifest-pinned images in `Service/manifests/releases/v0.1.0.yml`. GHCR packages still need public visibility or an explicit private fallback proof; public completion requires anonymous success. |
| Component Release Please | PASS by static file review | `Backend`, `PresenceService`, and `DB` have `release-please-config.json`, `.release-please-manifest.json`, `version.txt`, `CHANGELOG.md`, and `.github/workflows/release-please.yml` using `release-type: simple`. `Front` has `release-type: node`, `package.json` version `0.1.0`, `CHANGELOG.md`, manifest/config, and workflow. Workflows include release PR permissions plus `packages: write` for same-workflow image publication. |
| Service manifest release | PASS by local validation | `Service/scripts/validate-release-manifest.sh Service/manifests/releases/v0.1.0.yml` and `Service/scripts/render-release-env.sh Service/manifests/releases/v0.1.0.yml` passed. Manifest pins image, tag, digest, version, release/action link for each component and `components.db.resetRequired: true`. |
| Demo health proof | PASS for current public endpoint; image-mode provenance still blocked by GHCR pull | `curl -fsS -D /tmp/smart-class-health.headers https://smart-class.org/health` returned HTTP 200 and body `{"status":"ok"}` on 2026-04-26. Because anonymous GHCR pulls are denied, this proves endpoint health but not final public anonymous image-mode completion. |

Overall status: **BLOCKED on public GHCR package visibility**. The demo domain is healthy and local static gates are in place, but the public-first release cannot be called complete until anonymous manifest inspect or pull succeeds for every Service-manifest image.

## Scan scope

### Tracked files

Scanned tracked files in:

- `Backend`
- `PresenceService`
- `DB`
- `Front`
- `Service`
- `docs`

Excluded generated or local dependency/cache trees for signal quality: `.git`, `node_modules`, `.venv`, `dist`, `test-results`, `.pytest_cache`.

Blocking patterns checked:

- PEM/private-key headers
- GitHub token prefixes (`ghp_`, `gho_`, `ghu_`, `ghs_`, `ghr_`)
- AWS access key IDs (`AKIA...`)
- Slack token prefixes (`xox...`)
- OpenAI-style `sk-...` tokens
- high-entropy credential assignments after manual classification

Classification notes:

- `dev-token:*` strings in tests are local demo auth fixtures, not external bearer credentials.
- `sk-openwrt-gateway-prototype`, `sk-capstone-demo-presence-attendance`, `sk-phase-2-academic-read-model`, and similar `sk-*` strings in docs are work-item or source-map slugs, not API keys.
- `DOCSQUARTZ_DISPATCH_TOKEN`, `GHCR_READ_TOKEN`, and GitHub secret references are secret names in workflow configuration, not committed secret values.
- `Service/compose.yml` default `smartclass` / `smart-class-dev-jwt-secret` and `Service/.env.demo.example` `change-me` are demo/local placeholders; production-grade secret provisioning remains a non-goal.

### Docker build contexts

| Component | Docker context reviewed | `.dockerignore` posture | Public-risk note |
|---|---|---|---|
| Backend | `Backend/Dockerfile`, tracked `Backend/**` context | excludes `.git`, `.venv`, caches, README | No committed secret files observed in build context. |
| PresenceService | `PresenceService/Dockerfile`, tracked `PresenceService/**` context | excludes `.git`, `.venv`, caches, README | No committed secret files observed in build context. |
| DB | `DB/Dockerfile`, `DB/postgres/**` seed context | excludes `.git`, README | Public DB seed is intentionally baked into demo image; accepted fixtures are listed below. |
| Front | `Front/Dockerfile`, tracked app/nginx context | excludes `node_modules`, `dist`, `.git`, npm logs | `Front/.env.example` contains empty `VITE_BACKEND_URL`; no secret values observed. |
| Service | No runtime image build context in this plan | env examples and deploy scripts reviewed | Service pulls manifest-pinned component images and may use `GHCR_READ_TOKEN` only as private fallback. |

### Service env examples

Reviewed:

- `Service/.env.example`
- `Service/.env.demo.example`
- `Front/.env.example`
- `Service/.github/workflows/deploy-demo.yml`
- `Service/scripts/deploy-demo.sh`

Allowed placeholders:

- `POSTGRES_PASSWORD=smartclass` for local-only example
- `POSTGRES_PASSWORD=change-me` for demo example
- `JWT_SECRET` default in compose for local/demo scaffolding
- `GHCR_READ_USER` / `GHCR_READ_TOKEN` references as optional private fallback input names

## Accepted demo fixtures

The following are intentionally public demo fixtures under the approved non-goals and must not be treated as production data unless new evidence proves otherwise:

- `DB/postgres/seed/users.csv`: synthetic student/professor/admin IDs, English demo names, roles, and shared `devpass123` password.
- `DB/postgres/seed/registered_devices.csv`: synthetic labels and demo MAC addresses.
- `DB/postgres/seed/classroom_networks.csv`: RFC1918 gateway examples and classroom AP identifiers.
- `DB/postgres/seed/course_*`, `courses.csv`, `notices.csv`, `classrooms.csv`: synthetic course, schedule, notice, and classroom fixtures.
- Backend/Front tests using `dev-token:*` values for local auth simulation.

If any seed row is later confirmed to be real student, staff, MAC, host, or credential data, public-readiness must move to **BLOCKED** and the DB image must not be promoted as public until the data is replaced and evidence is refreshed.

## Anonymous public pull proof

Manifest-pinned refs from `Service/manifests/releases/v0.1.0.yml` were checked without `docker login`:

```text
$ docker manifest inspect ghcr.io/chosununiv2026capstone/backend:sha-bb73a03@sha256:f03cdaf2dec73eb3571432b51e1af5e8728813c7c95784eea75591397b3b253a
exit=1
stderr: denied

$ docker manifest inspect ghcr.io/chosununiv2026capstone/front:sha-3d28ed1@sha256:11c1e7891126cfad87e3534daea5b272489d98a6956c93a8a969ae93507aa89a
exit=1
stderr: denied

$ docker manifest inspect ghcr.io/chosununiv2026capstone/presence-service:sha-aad4327@sha256:ede8fdd5642f5b76160b28442bf47e63d5512bd7301573a2b09657da3871692d
exit=1
stderr: denied

$ docker manifest inspect ghcr.io/chosununiv2026capstone/db:sha-c4773d4@sha256:b3d5179295bd99e10f6510781c2c7f16f0daf7e886afa9e73bb7e136092f69af
exit=1
stderr: denied
```

This is a blocking public-readiness failure. Private `GHCR_READ_TOKEN` fallback can be documented and separately proven for demo continuity, but it does **not** satisfy the public completion gate.

## Demo health proof

```text
$ curl -fsS -D /tmp/smart-class-health.headers https://smart-class.org/health -o /tmp/smart-class-health.body
exit=0
HTTP/2 200
content-type: application/json
content-length: 15
x-served-by: smart-class.org
body={"status":"ok"}
```

The public endpoint is healthy as of 2026-04-26. Because public GHCR pulls are currently denied, this health check must be recorded as endpoint health proof only; final public anonymous image-mode proof remains blocked.

## Residual public risk

| Risk | Status | Mitigation / next action |
|---|---|---|
| GHCR packages remain private | ACTIVE BLOCKER | Make `backend`, `front`, `presence-service`, and `db` packages public in GHCR or capture private fallback proof separately. Re-run anonymous `docker manifest inspect` after visibility changes. |
| Demo DB seed is public | ACCEPTED | Keep fixture disclosure in this report. Block future public release if real-data evidence appears. |
| Local/demo default secrets are weak | ACCEPTED FOR DEMO | Do not reuse defaults outside demo. Production secret automation is explicitly out of scope. |
| Same-workflow release publish has not run on a real Release Please-created release in this local evidence | PENDING EXTERNAL EVIDENCE | Capture GitHub Actions run URL and release image digest during first component release. |
| Demo health does not yet prove anonymous image-mode provenance | ACTIVE BLOCKER | After public pull succeeds, deploy manifest-pinned image mode and recapture deploy summary plus health body. |

## Required refresh commands

Run these before declaring final public completion:

```bash
cd /home/koreaplayer99/smart-class

# Static gates
for repo in Backend PresenceService DB Front Service; do
  python3 -m json.tool "$repo/release-please-config.json" >/dev/null
  python3 -m json.tool "$repo/.release-please-manifest.json" >/dev/null
done
cd Service
./scripts/validate-release-manifest.sh manifests/releases/v0.1.0.yml
./scripts/render-release-env.sh manifests/releases/v0.1.0.yml

# Public pull gate, without docker login
docker manifest inspect ghcr.io/chosununiv2026capstone/backend:sha-bb73a03@sha256:f03cdaf2dec73eb3571432b51e1af5e8728813c7c95784eea75591397b3b253a
docker manifest inspect ghcr.io/chosununiv2026capstone/front:sha-3d28ed1@sha256:11c1e7891126cfad87e3534daea5b272489d98a6956c93a8a969ae93507aa89a
docker manifest inspect ghcr.io/chosununiv2026capstone/presence-service:sha-aad4327@sha256:ede8fdd5642f5b76160b28442bf47e63d5512bd7301573a2b09657da3871692d
docker manifest inspect ghcr.io/chosununiv2026capstone/db:sha-c4773d4@sha256:b3d5179295bd99e10f6510781c2c7f16f0daf7e886afa9e73bb7e136092f69af

# Demo health gate after manifest-pinned image-mode deploy
curl -fsS -D /tmp/smart-class-health.headers https://smart-class.org/health -o /tmp/smart-class-health.body
cat /tmp/smart-class-health.body
```
