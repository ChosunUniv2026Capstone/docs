---
title: 검증 및 테스트
type: report-section
status: draft
updated: 2026-04-12
owners:
  - team
related:
  - [[/07-status/implementation-roadmap.md]]
source:
  - Backend/tests
  - PresenceService/tests
  - Front/tests/e2e
  - DB/postgres/init
---

# 18. 검증 및 테스트

# 18.1 검증 전략

프로젝트 검증은 서비스별 단위 검증과 통합 시나리오 검증을 함께 사용한다.
출석/시험 기능은 Front 화면, Backend API, PresenceService eligibility, DB audit/state 가 연결되므로 단일 계층 테스트만으로 충분하지 않다.

# 18.2 Backend 테스트

Backend 테스트는 다음 범위를 포함한다.

- 인증/세션/권한 guard
- 학생 단말 등록 제한과 중복 MAC 거부
- Presence admin/demo endpoint
- attendance realtime/session flow
- exam contract alignment

예상 명령:

```bash
cd Backend
PYTHONPATH=. pytest -q
python3 -m compileall app
```

# 18.3 PresenceService 테스트

PresenceService 테스트는 다음 범위를 포함한다.

- snapshot cache hit/miss
- refresh lock
- dummy overlay 적용/초기화
- registered device matching
- signal threshold 판정
- eligibility reason code

예상 명령:

```bash
cd PresenceService
PYTHONPATH=. pytest -q
python3 -m compileall app
```

# 18.4 Front 테스트

Front 검증은 lint/build/e2e 를 조합한다.

```bash
cd Front
npm run lint
npm run build
npx playwright test
```

주요 e2e 범위:

- 로그인/세션 복구/route guard
- presence demo
- attendance route
- exam workflow

# 18.5 DB 검증

DB 검증은 PostgreSQL container 에 init script 를 실제 적용해 확인한다.

검증 대상:

- schema 생성 성공
- seed import 성공
- 출석/시험 핵심 테이블 존재
- unique/foreign key 제약 동작
- demo tuple seed 확인

# 18.6 통합 시나리오

## 출석 시나리오

1. 서비스관리자가 강의실 AP/threshold 를 확인한다.
2. 학생이 등록 단말을 관리한다.
3. 교수가 projected slot 을 선택해 출석 세션을 연다.
4. 학생이 self check-in 을 시도한다.
5. Backend 가 PresenceService eligibility 를 확인한다.
6. 출석 record/audit 이 DB 에 저장된다.
7. 교수 roster/report 와 학생 화면이 갱신된다.

## 시험 시나리오

1. 교수가 시험 초안을 만든다.
2. 문항과 선택지를 구성한다.
3. 시험을 게시한다.
4. 학생이 시험을 시작한다.
5. 답안을 저장한다.
6. 시험을 제출한다.
7. 제출 상태와 점수가 반영된다.

# 18.7 보고서 검증 자료

최종보고서에는 다음 증거를 첨부한다.

- Front 화면 캡처
- Mermaid diagram
- API endpoint inventory
- DB ERD
- 테스트 명령과 결과 요약
- Docker compose health check 결과
- 주요 한계와 미완성 항목
