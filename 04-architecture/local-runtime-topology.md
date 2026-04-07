---
title: 로컬 런타임 토폴로지
type: architecture
status: active
updated: 2026-04-07
owners:
  - architecture-owner
related:
  - [[/04-architecture/service-map.md]]
  - [[/04-architecture/presence-eligibility-api.md]]
  - [[/01-requirements/req-attendance-presence.md]]
source:
  - [[/06-meetings/raw/2026-03-30-presence-logic-clarification.md]]
---

# 목적

개발용 vertical slice 를 로컬에서 한 번에 띄울 수 있는 런타임 구성을 정의한다.

# 서비스

- `front`
  - React + Vite
  - 기본 컨테이너 포트 `3000`
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
  - 기본 호스트 포트 `5432`
- `redis`
  - Redis
  - 기본 호스트 포트 `6379`

# 실행 위치

- 로컬 오케스트레이션은 `CodexKit/docker-compose.yml` 에서 담당한다.
- 각 서비스 코드는 sibling repo 에서 build context 로 연결한다.

# 흐름

1. 사용자는 `nginx` 의 외부 포트로 접속한다.
2. `nginx` 는 `/` 요청을 `front` 로 전달한다.
3. `nginx` 는 `/api/` 와 `/health` 요청을 `backend` 로 전달한다.
4. Front 는 same-origin 경로로 Backend 를 호출한다.
5. Backend 가 학생 단말과 수강 / 시간표를 검증한다.
6. Backend 가 PresenceService 에 eligibility 를 요청한다.
7. PresenceService 는 Redis 캐시를 먼저 보고, 필요 시 더미 OpenWrt snapshot 을 새로 만든다.
8. Backend 가 최종 허용 / 거부를 반환한다.

# 외부 노출 원칙

- 외부에서 직접 노출하는 서비스는 기본적으로 `nginx` 하나다.
- `backend`, `presence-service`, `postgres`, `redis` 는 Docker 네트워크 내부 통신을 기본으로 한다.
- `presence-service` 는 Backend 의 내부 의존 서비스로 취급하며, 외부 사용자가 직접 접속하는 공개 진입점으로 두지 않는다.

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
- OpenWrt 더미 snapshot 기반 판정

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

- 실 OpenWrt 명령 수집기로 교체
- 정식 인증 / 권한 체계 연결
- 시험 목적 추가 규칙 세분화
