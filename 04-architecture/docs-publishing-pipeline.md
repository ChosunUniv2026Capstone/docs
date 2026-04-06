# Docs publishing pipeline

## 목적

- `docs`를 문서 source of truth 로 유지한다.
- `docs/main` 변경이 `DocsQuartz` 기반 정적 사이트 배포로 자동 이어지게 한다.
- `DocsQuartz/content`에는 mirror commit 을 남기지 않고, 빌드 시점에만 최신 문서를 주입한다.

## 저장소 책임

### `docs`

- 문서 원본 저장소
- `main` push 시 `DocsQuartz` 배포 workflow 를 트리거한다.
- PR preview 는 이번 범위에 포함하지 않는다.

### `DocsQuartz`

- Quartz 설정과 GitHub Pages 배포를 담당한다.
- `repository_dispatch` 또는 수동 `workflow_dispatch` 를 받으면 `docs`를 checkout 해 `content/`를 구성하고 build/deploy 한다.

## 배포 흐름

1. `docs/main` 에 push 가 발생한다.
2. `docs/.github/workflows/dispatch-docsquartz-deploy.yml` 이 `repository_dispatch` 이벤트를 `DocsQuartz`로 보낸다.
3. `DocsQuartz/.github/workflows/deploy-docs-site.yml` 이 이벤트를 받아 실행된다.
4. workflow 는 `docs` 저장소를 별도 경로에 checkout 한다.
5. 아래 문서 섹션을 `DocsQuartz/content/` 로 동기화한다.
   - `00-overview`
   - `01-requirements`
   - `02-decisions`
   - `03-conventions`
   - `04-architecture`
   - `05-work-items`
   - `06-meetings`
   - `07-status`
6. Quartz 가 `public/` 정적 산출물을 만든다.
7. GitHub Pages artifact 업로드 후 `docs.smart-class.org` 로 배포한다.

## 필요한 GitHub Secrets

### `docs` 저장소

- `DOCSQUARTZ_DISPATCH_TOKEN`
  - 용도: `DocsQuartz` 에 `repository_dispatch` 전송
  - 권장: `DocsQuartz` 저장소에만 접근 가능한 최소 권한 토큰

### `DocsQuartz` 저장소

- `DOCS_REPO_READ_TOKEN`
  - 용도: private `docs` 저장소 checkout
  - 권장: `docs` 저장소 read-only 토큰

> GitHub Docs 기준으로 기본 `GITHUB_TOKEN` 으로 부족한 권한이 필요하면 GitHub App 토큰 또는 PAT 을 별도 secret 으로 써야 한다.

## GitHub Pages 설정

`DocsQuartz` 저장소에서 아래를 수동 설정해야 한다.

1. **Settings → Pages → Source** 를 `GitHub Actions` 로 설정
2. **Custom domain** 을 `docs.smart-class.org` 로 저장
3. DNS 에 아래 CNAME 추가
   - `docs.smart-class.org -> chosununiv2026capstone.github.io`
4. DNS 반영 후 필요하면 **Enforce HTTPS** 활성화

## 운영 규칙

- production 배포 자동 트리거는 `docs/main` push 하나만 사용한다.
- PR 생성/수정만으로는 production deploy 하지 않는다.
- 수동 재배포가 필요하면 `DocsQuartz` 의 `Deploy docs site` workflow 를 `workflow_dispatch` 로 다시 실행한다.
- `repository_dispatch` 와 `workflow_dispatch` workflow 파일은 `DocsQuartz`의 default branch 에 유지해야 한다.

## 현재 확인된 주의사항

- 2026-04-06 기준 GitHub 저장소 메타데이터에서는 `ChosunUniv2026Capstone/DocsQuartz` 의 default branch 가 `main` 으로 보인다.
- 따라서 local Quartz 작업 브랜치가 `v4` 여도, 실제 자동화를 활성화하려면 workflow 와 Quartz 코드가 GitHub 의 default branch 에 올라가 있어야 한다.

## 알려진 제한

- PR preview 가 없으므로 링크/빌드 오류는 merge 후 `docs/main` 배포 시점에 발견될 수 있다.
- custom domain/DNS 적용은 코드만으로 완료되지 않는다.
- 새 최상위 문서 섹션을 공개하려면 `DocsQuartz` 배포 workflow 의 동기화 목록도 함께 갱신해야 한다.
