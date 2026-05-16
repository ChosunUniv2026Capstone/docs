---
title: 서비스 맵
type: architecture
status: active
updated: 2026-05-16
owners:
  - architecture-owner
related:
  - [[/02-decisions/adr-0002-service-boundary.md]]
  - [[/02-decisions/adr-0004-attendance-authorization-flow.md]]
  - [[/02-decisions/adr-0005-presence-snapshot-cache.md]]
  - [[/02-decisions/adr-0013-openwrt-local-collector-push.md]]
  - [[/01-requirements/req-student-features.md]]
  - [[/04-architecture/local-runtime-topology.md]]
  - [[/02-decisions/adr-0011-service-repo-runtime-orchestration.md]]
  - [[/03-conventions/conv-release-and-deployment.md]]
source:
  - [[/06-meetings/raw/2026-03-19-capstone-proposal.md]]
  - [[/06-meetings/raw/2026-03-25-kickoff-work-items.md]]
  - [[/06-meetings/raw/2026-03-30-presence-logic-clarification.md]]
---

# 서비스 구성

- `Front`
  - 학생 / 교수 / 관리자 웹 UI
- `Nginx`
  - 외부 reverse proxy
  - Front / Backend path routing
  - `/`, `/api/`, `/ws/`, `/health` 단일 origin 라우팅
- `Backend`
  - 사용자, 강의, 과제, 시험, 공지, 출석 API
- `PresenceService`
  - 재실성 판정 보조, 단말 연결 정보 처리, Redis snapshot 캐시 관리
- `DB`
  - 스키마, 마이그레이션, 데이터 계약
- `docs`
  - 요구사항, ADR, 규약, 회의록
- `Service`
  - canonical runtime orchestration, compose, nginx config, service release manifests, demo deploy scripts
- `CodexKit`
  - workspace bootstrap, repo helper, shared hook, workflow governance
  - runtime compose/nginx/env 는 소유하지 않고 `Service` 로 위임

# 기본 상호작용

1. 사용자는 `Nginx` 를 통해 로그인하고 LMS 기능을 사용한다.
2. `Nginx` 는 `/` 를 Front 로, `/api/`, `/ws/`, `/health` 를 Backend 로 전달한다.
3. Front 는 same-origin 경로 기준으로 LMS 도메인 REST 요청과 출석 WebSocket 을 Backend 로 전달한다.
4. 출석 또는 시험 접근 시 Backend 는 PresenceService 에 `purpose` 포함 eligibility 판정을 요청한다.
5. 실제 OpenWrt AP 데이터는 AP local collector 가 주기적으로 PresenceService collector endpoint 로 push 하고, PresenceService 는 Redis 의 최신 collector snapshot 을 읽는다. user-triggered 요청은 routine 경로에서 OpenWrt SSH/pull 수집을 유발하지 않는다.
6. demo source 를 명시적으로 선택한 경우에만 PresenceService 는 demo baseline/overlay snapshot 을 사용한다. real collector snapshot 과 demo snapshot 은 운영 의미를 섞지 않는다.
7. Backend 는 시간표, 강의실, 수강 정보, PresenceService 결과를 결합해 최종 판단한다.
8. Backend 와 PresenceService 는 필요한 데이터를 DB 또는 해당 데이터 소스에 반영한다.
9. 인증 복구가 필요한 경우 Front 는 refresh/bootstrap 경로를 통해 Backend 에 세션 복구를 요청한다.

# 경계 요약

- Service 는 런타임 오케스트레이션, edge nginx 설정, 이미지 기반 실행, manifest release, demo deploy wrapper 를 소유한다.
- CodexKit 은 workspace bootstrap/governance 를 소유하고 runtime 실행은 Service 로 위임한다.
- Nginx 는 외부 진입점과 path routing 을 소유한다. `/ws/` WebSocket upgrade 도 edge nginx 에서 Backend 로 전달한다.
- Front 는 판정 결과를 소비한다.
- Backend 는 최종 도메인 판단을 한다.
- PresenceService 는 네트워크 / 단말 판정 근거를 제공한다.
- DB 는 저장 구조와 변경 이력을 관리한다.

# 공개 경계

- 공개 URL 은 `Nginx` 가 단일 origin 으로 제공한다. 로컬 / 시연 Host 패턴 필터링은 접근 호환성 정책이며 TLS 기반 보안 경계가 아니다.
- Postgres / Redis 는 기본적으로 host port 없이 Docker 네트워크 내부 의존 서비스로만 둔다. 신뢰된 LAN 임시 디버깅이 필요할 때만 compose 의 debug port 예시를 명시적으로 해제한다.
- `PresenceService` 는 외부 공개 없이 Backend 내부 의존 경로로만 사용한다.
- Front 의 page/route 권한은 Backend bootstrap/guard 결과를 소비해야 하며, 직접 신뢰하면 안 된다.
