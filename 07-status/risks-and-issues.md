---
title: 리스크와 이슈
type: status
status: active
updated: 2026-05-16
owners:
  - team
related:
  - [[/04-architecture/network-topology.md]]
  - [[/01-requirements/req-device-auth.md]]
  - [[/02-decisions/adr-0005-presence-snapshot-cache.md]]
  - [[/04-architecture/attendance-workflow-architecture.md]]
  - [[/04-architecture/exam-workflow-api.md]]
source:
  - [[/06-meetings/raw/2026-03-19-capstone-proposal.md]]
  - [[/06-meetings/raw/2026-03-30-presence-logic-clarification.md]]
  - current code/test audit, 2026-04-25
---

# 2026-05-16

## 현재 남은 리스크

- OpenWrt 수집 부하 위험은 soft TTL `3초`, hard TTL `30초`, refresh lock 정책으로 완화한다.
  - 동일 cache key 또는 동일 OpenWrt/AP target 에 대한 재수집은 많아도 약 3초에 1회 수준이어야 한다.
  - 이 제한은 전역 제한이 아니므로 여러 AP / 강의실 refresh 는 AP 수와 매핑 구조에 비례한다.
  - 실제 OpenWrt 장비에서 3초 단위 수집이 안정적인지는 현장 부하 검증이 필요하다.
- hard TTL `30초` 를 넘은 snapshot 은 새 수집 없이는 eligibility 근거로 사용하지 않는 fail-close 성격을 유지한다.

## 완화되었거나 범위가 좁아진 리스크

- Redis snapshot 캐시 만료 시 동시 요청 폭주 위험
  - refresh lock 을 필수 정책으로 승격했다.
  - stale-while-revalidate 를 사용해 soft TTL 이후에도 hard TTL 이내 기존 snapshot 으로 요청 지연을 줄일 수 있다.

# 2026-04-25

## 현재 남은 리스크

- 실제 OpenWrt 또는 교내 게이트웨이 환경에서 필요한 수준의 단말 정보를 안정적으로 수집할 수 있을지 검증이 필요하다.
  - 로컬 dummy snapshot / Redis cache / AP threshold 판정은 구현되어 테스트를 통과했다.
  - 현장 AP 모델, station 정보 형식, 권한, 갱신 주기, 장애 응답은 별도 검증해야 한다.
- 단말 식별 정보 저장은 개인정보 및 보안 정책 검토가 필요하다.
- 랜덤 MAC 을 학생이 끄지 않으면 등록 단말 매칭이 실패할 수 있다.
- 운영 수준의 수집 실패 정책이 아직 남아 있다.
  - retry/backoff, fail-close/fail-open, 관리자 알림, 로그 보존 범위를 결정해야 한다.
- PresenceService 모델에는 Pydantic alias 관련 warning 이 남아 있다.
  - `PYTHONPATH=. pytest -q` 는 통과하지만 warning 제거 여부는 후속 품질 작업으로 판단한다.
- Python 서비스 테스트 실행 명령은 import path 를 요구한다.
  - 현재 검증 명령은 `PYTHONPATH=. pytest -q` 이다.

## 완화되었거나 범위가 좁아진 리스크

- 문서보다 구현이 앞서가 서비스 경계가 섞일 위험
  - Backend 는 최종 도메인 판단, PresenceService 는 네트워크/단말 근거 제공이라는 경계를 유지하고 있다.
  - 시험/출석 관련 계약은 `exam-workflow-api`, `exam-mvp-contract`, `attendance-workflow-architecture` 로 보강되었다.
- 시험 접근 제어 범위를 성급히 넓히는 위험
  - 현재 로컬 exam MVP 는 start guard 와 submission workflow 중심으로 구현되어 있고, 운영 수준의 재실성 강제 정책은 별도 결정으로 남겼다.
- Redis snapshot 캐시 만료 시 OpenWrt 수집 부하 위험
  - Redis TTL/cache/refresh lock 개념과 dummy provider 테스트가 있으나, 실제 OpenWrt 부하 검증은 아직 필요하다.

# 2026-03-30 원본 리스크

- OpenWrt 또는 게이트웨이 환경에서 필요한 수준의 단말 정보를 안정적으로 수집할 수 있을지 검증이 필요하다.
- 단말 식별 정보 저장은 개인정보 및 보안 정책 검토가 필요하다.
- 랜덤 MAC 을 학생이 끄지 않으면 등록 단말 매칭이 실패할 수 있다.
- 문서보다 구현이 앞서가면 서비스 경계가 쉽게 섞일 수 있다.
- 시험 접근 제어 범위를 성급히 넓히면 운영 복잡도가 급격히 증가할 수 있다.
- Redis snapshot 캐시 만료 시 동시 요청이 몰리면 OpenWrt 수집 부하가 커질 수 있다.
