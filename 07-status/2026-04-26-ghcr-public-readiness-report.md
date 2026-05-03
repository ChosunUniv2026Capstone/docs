---
title: GHCR 공개 준비성 및 잔여 리스크 보고서
type: status
status: active
updated: 2026-05-03
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

이 문서는 Smart Class demo stack 의 public GHCR 전환을 위해 필요한 secret/PII scan, demo seed 공개 허용 범위, anonymous image pull proof, demo health proof 를 한 곳에 남기는 current-truth 보고서이다. `08-reports` 는 제출 snapshot 이므로 평소에는 current-truth 갱신과 분리하지만, 2026-05-03 사용자 요청에 따라 GHCR public pull 해결 내용은 보고서 snapshot 에도 별도 반영했다.

## 결론

| Gate | Current result | Evidence |
|---|---|---|
| Secret/PII scan doc | PASS with accepted demo fixtures | 2026-04-26 local scan covered tracked files in `Backend`, `PresenceService`, `DB`, `Front`, `Service`, `docs`; Docker build context inputs; Service env examples; DB seed files. No private key, GitHub token, AWS key, Slack token, or real OpenAI key pattern was found after classifying documented `sk-*` slugs as non-secret identifiers. |
| Public pull proof | PASS | 2026-05-03 anonymous `docker manifest inspect` succeeded for all four manifest-pinned images in `Service/manifests/releases/v0.1.0.yml`: Backend, Front, PresenceService, and DB. The newer public release tags `backend:v0.2.0`, `front:v0.2.1`, `presence-service:v0.2.0`, and `db:v0.2.0` also succeeded without `docker login`. |
| Component Release Please | PASS by static file review; live run proof pending | `Backend`, `PresenceService`, and `DB` have `release-please-config.json`, `.release-please-manifest.json`, `version.txt`, `CHANGELOG.md`, and `.github/workflows/release-please.yml` using `release-type: simple`. `Front` has `release-type: node`, `package.json` version `0.1.0`, `CHANGELOG.md`, manifest/config, and workflow. Workflows include release PR permissions plus `packages: write` for same-workflow image publication. GitHub Actions evidence for an actual Release Please-created release remains external evidence to collect. |
| Service manifest release | PASS by local validation | `Service/scripts/validate-release-manifest.sh Service/manifests/releases/v0.1.0.yml` and `Service/scripts/render-release-env.sh Service/manifests/releases/v0.1.0.yml` passed. Manifest pins image, tag, digest, version, release/action link for each component and `components.db.resetRequired: true`. |
| Demo health proof | PASS for current public endpoint | `curl -fsS -D /tmp/smart-class-health.headers https://smart-class.org/health` returned HTTP 200 and body `{"status":"ok"}` on 2026-04-26. Public image access is now separately proven by anonymous manifest inspection. |

Overall status: **PUBLIC GHCR PULL BLOCKER RESOLVED**. The demo domain is healthy, local static gates are in place, and anonymous manifest inspection now succeeds for every Service-manifest image. Remaining external evidence is demo deploy workflow/server provenance, not GHCR package visibility.

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

Manifest-pinned refs from `Service/manifests/releases/v0.1.0.yml` were rechecked without `docker login` on 2026-05-03:

```text
$ docker manifest inspect ghcr.io/chosununiv2026capstone/backend:sha-bb73a03@sha256:f03cdaf2dec73eb3571432b51e1af5e8728813c7c95784eea75591397b3b253a
exit=0

$ docker manifest inspect ghcr.io/chosununiv2026capstone/front:sha-3d28ed1@sha256:11c1e7891126cfad87e3534daea5b272489d98a6956c93a8a969ae93507aa89a
exit=0

$ docker manifest inspect ghcr.io/chosununiv2026capstone/presence-service:sha-aad4327@sha256:ede8fdd5642f5b76160b28442bf47e63d5512bd7301573a2b09657da3871692d
exit=0

$ docker manifest inspect ghcr.io/chosununiv2026capstone/db:sha-c4773d4@sha256:b3d5179295bd99e10f6510781c2c7f16f0daf7e886afa9e73bb7e136092f69af
exit=0
```

The original public-readiness blocker is resolved. Private `GHCR_READ_TOKEN` remains documented only as a fallback path and is not required for the current public pull proof.

Current release tags were also checked without `docker login` on 2026-05-03:

```text
$ docker manifest inspect ghcr.io/chosununiv2026capstone/backend:v0.2.0
exit=0

$ docker manifest inspect ghcr.io/chosununiv2026capstone/front:v0.2.1
exit=0

$ docker manifest inspect ghcr.io/chosununiv2026capstone/presence-service:v0.2.0
exit=0

$ docker manifest inspect ghcr.io/chosununiv2026capstone/db:v0.2.0
exit=0
```

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

The public endpoint is healthy as of 2026-04-26. Anonymous image access is now proven separately as of 2026-05-03; the remaining proof to capture is the final demo deployment workflow/server provenance for the exact deployed Service release.

## Residual public risk

| Risk | Status | Mitigation / next action |
|---|---|---|
| GHCR public package visibility | RESOLVED | 2026-05-03 anonymous `docker manifest inspect` succeeded for Backend, Front, PresenceService, and DB manifest-pinned refs plus current release tags. |
| Demo DB seed is public | ACCEPTED | Keep fixture disclosure in this report. Block future public release if real-data evidence appears. |
| Local/demo default secrets are weak | ACCEPTED FOR DEMO | Do not reuse defaults outside demo. Production secret automation is explicitly out of scope. |
| Same-workflow release publish has not run on a real Release Please-created release in this local evidence | PENDING EXTERNAL EVIDENCE | Capture GitHub Actions run URL and release image digest during first component release. |
| Demo deploy workflow/server provenance | PENDING EXTERNAL EVIDENCE | Public pull now succeeds. Capture deploy workflow summary, component refs, reset flag, GHCR access result, and health body for the exact deployed Service release. |

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
