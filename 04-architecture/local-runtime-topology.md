---
title: 로컬 런타임 토폴로지
type: architecture
status: active
updated: 2026-05-16
owners:
  - architecture-owner
related:
  - [[/04-architecture/service-map.md]]
  - [[/04-architecture/presence-eligibility-api.md]]
  - [[/01-requirements/req-attendance-presence.md]]
  - [[/02-decisions/adr-0011-service-repo-runtime-orchestration.md]]
  - [[/02-decisions/adr-0013-openwrt-local-collector-push.md]]
  - [[/03-conventions/conv-release-and-deployment.md]]
source:
  - [[/06-meetings/raw/2026-03-30-presence-logic-clarification.md]]
---

# 목적

개발용 vertical slice 를 로컬에서 한 번에 띄울 수 있는 런타임 구성을 정의한다.

# 서비스

- `front`
  - Docker / compose runtime: Vite build 산출물을 nginx 로 정적으로 제공
  - 기본 컨테이너 포트 `80`
  - 직접 개발 실행 시: Vite dev server 포트 `3000`
- `backend`
  - FastAPI
  - 기본 컨테이너 포트 `8000`
- `presence-service`
  - FastAPI + Redis cache
  - 기본 컨테이너 포트 `8001`
- `nginx`
  - 외부 진입점 reverse proxy
  - 기본 호스트 포트 `3100`
- `postgres`
  - PostgreSQL
  - 기본 컨테이너 포트 `5432`
  - 기본적으로 host port 를 열지 않고 Docker 네트워크 내부에만 노출
- `redis`
  - Redis
  - 기본 컨테이너 포트 `6379`
  - 기본적으로 host port 를 열지 않고 Docker 네트워크 내부에만 노출

# 실행 위치

- 로컬 오케스트레이션의 canonical owner 는 `Service` repo 이다.
- 로컬 source build 는 `Service/compose.yml` + `Service/compose.local.yml` 조합으로 실행한다.
- 이미지 기반 실행은 `Service/compose.yml` + `Service/compose.image.yml` 조합으로 실행한다.
- 데모 배포는 `Service/compose.yml` + `Service/compose.image.yml` + `Service/compose.demo.yml` 조합과 manifest-pinned 이미지 ref 를 사용한다.
- 각 서비스 코드는 local mode 에서 sibling repo build context(`../Backend`, `../Front`, `../PresenceService`, `../DB`) 로 연결한다.
- `CodexKit` 은 runtime compose/nginx/env 의 source of truth 가 아니며, 필요한 경우 `Service` wrapper 로 위임한다.

# 흐름

1. 사용자는 `nginx` 의 외부 포트로 접속한다.
2. `nginx` 는 `/` 요청을 `front` 로 전달한다.
3. `nginx` 는 `/api/`, `/ws/`, `/health` 요청을 `backend` 로 전달한다.
4. Front 는 same-origin 경로로 Backend REST / WebSocket 을 호출한다.
5. Backend 가 학생 단말과 수강 / 시간표를 검증한다.
6. Backend 가 PresenceService 에 eligibility 를 요청한다.
7. PresenceService 는 routine real-data 경로에서 Redis 에 저장된 collector-push snapshot 을 읽는다. snapshot 은 OpenWrt local collector 가 약 3초 주기로 push 하며, user-triggered 요청은 OpenWrt SSH/pull 수집을 유발하지 않는다.
8. demo source 를 명시한 관리자/demo 흐름만 demo baseline/overlay snapshot 을 사용한다.
9. Backend 가 최종 허용 / 거부를 반환한다.

# 외부 노출 원칙

- 외부에서 직접 노출하는 서비스는 기본적으로 `nginx` 하나다.
- 로컬 기본 진입점은 `localhost:3100` 이며, 이는 edge nginx 컨테이너의 `80` 포트로 매핑된다.
- Docker 네트워크 안에서 edge nginx 는 Front 를 `front:80`, Backend 를 `backend:8000` 으로 호출한다.
- `backend`, `front`, `presence-service`, `postgres`, `redis` 는 Docker 네트워크 내부 통신을 기본으로 한다.
- Postgres / Redis host port 는 기본 런타임에서는 닫혀 있으며, 신뢰된 LAN 에서 임시 디버깅이 필요할 때만 compose 파일의 주석 처리된 debug port 예시를 해제한다.
- `presence-service` 는 Backend 의 내부 의존 서비스로 취급하며, 외부 사용자가 직접 접속하는 공개 진입점으로 두지 않는다.


# Host 접근 정책

- 로컬 / 시연 환경에서는 `smart-class.org`, `localhost`, `127.0.0.1`, 사설 IPv4 형식 Host 패턴의 접근을 허용한다.
- 이 Host 필터링은 로컬 / 시연 접근 호환성을 위한 edge routing 정책이며, TLS / 인증서 기반 운영 보안 경계가 아니다.
- HTTPS, 인증서, 443 리스너, HTTP -> HTTPS redirect 는 `Service` 데모 배포 문서와 manifest release 절차에서 다룬다.

# 현재 범위

- 학생 / 교수 / 관리자 개발용 로그인
- 로그인 페이지 분리
- 우측 상단 계정 요약
- 프로필 페이지
- 학생 단말 등록 / 삭제
- 출석 / 시험 eligibility 확인
- 학생 강의 목록 조회
- 교수 담당 강의 목록 조회
- 공지사항 조회 / 상세 조회 / 작성
- 강의자료 / 동영상 임시 프론트 스캐폴드
- 관리자 사용자 / 강의실 / AP 매핑 조회
- 강의 상세 페이지와 우측 기능 바
- 실제 OpenWrt local collector push snapshot 기반 판정
- demo mode 전용 baseline/overlay snapshot 기반 관제

# 개발용 seed 데이터

- 학생 10명
- 교수 2명
- 관리자 2명
- 과목 20개
- 강의실 3개
- AP / 공유기 10개

# 개발용 로그인 규칙

- 학생, 교수, 관리자 모두 로그인 가능하다.
- dev seed 의 기본 비밀번호는 `devpass123` 이다.
- 학생은 로그인 후 단말 관리와 eligibility 확인 기능을 사용한다.
- 교수는 로그인 후 담당 강의, 공지 상세 조회, 공지 작성, 학습 자료 / 동영상 임시 스캐폴드를 사용할 수 있다.
- 관리자는 로그인 후 사용자 / 강의실 / AP 매핑 조회 기능을 사용한다.

# 후속 작업

- OpenWrt collector 운영 안정성 / 장기 장애 대응 검증
- 정식 인증 / 권한 체계 연결
- 시험 목적 추가 규칙 세분화
