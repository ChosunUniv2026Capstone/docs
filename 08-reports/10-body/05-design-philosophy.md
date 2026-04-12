---
title: 설계 철학
type: report-section
status: draft
updated: 2026-04-12
owners:
  - team
related:
  - [[/02-decisions/adr-0001-docs-source-of-truth.md]]
  - [[/02-decisions/adr-0002-service-boundary.md]]
  - [[/02-decisions/adr-0004-attendance-authorization-flow.md]]
source:
  - [[/02-decisions/adr-0001-docs-source-of-truth.md]]
  - [[/02-decisions/adr-0002-service-boundary.md]]
  - [[/02-decisions/adr-0004-attendance-authorization-flow.md]]
---

# 5. 설계 철학

# 5.1 문서 우선 설계

프로젝트는 `docs` repository 를 source of truth 로 사용한다.
요구사항, ADR, 규약, 아키텍처, 상태 문서를 먼저 정리하고, 코드 저장소는 해당 문서를 기준으로 구현한다.
이 방식은 Front, Backend, PresenceService, DB 처럼 저장소가 분리된 구조에서 서비스 경계가 섞이는 문제를 줄인다.

# 5.2 서비스 책임 분리

프로젝트는 기능을 하나의 서버에 모두 넣지 않고 다음 책임으로 나눈다.

- Front: 화면과 사용자 상호작용
- Backend: 도메인 규칙, 권한, 최종 판정
- PresenceService: 네트워크/단말 관측 근거
- DB: 영속 데이터와 데이터 무결성
- CodexKit/Nginx: 로컬 실행 및 reverse proxy

이 분리는 특히 출석 판정에서 중요하다.
PresenceService 가 네트워크 근거만 담당하고, Backend 가 수강 정보와 시간표를 결합해 최종 판단해야 도메인 규칙을 일관되게 유지할 수 있다.

# 5.3 근거 기반 출석 판정

출석은 단순 버튼 클릭이 아니라 다음 근거를 결합해 결정한다.

1. 로그인 사용자 본인 여부
2. 수강 여부
3. 강의 시간표와 강의실 정보
4. 교수자가 연 출석 세션 상태
5. 등록 단말 목록
6. 강의실 네트워크 관측 snapshot
7. AP별 signal threshold
8. 출석 이력과 감사 로그

# 5.4 데모 가능성과 운영 가능성의 분리

캡스톤 프로젝트는 시연 가능해야 하지만, 데모 편의를 위해 운영 구조를 왜곡하면 안 된다.
따라서 더미 재실 제어는 demo mode overlay 로 분리하고, 운영 도입 시에는 OpenWrt/네트워크 장비 수집 경로로 교체할 수 있도록 설계한다.

# 5.5 점진적 확장

처음부터 모든 LMS 기능을 완성하기보다 vertical slice 를 확보하고 확장한다.

1. 로그인, 강의 조회, 공지, 단말 등록
2. 재실성 eligibility
3. 출석 세션 운영
4. 시험 MVP
5. 과제, 성적, 질문/문의, 운영 자동화

이 순서는 캡스톤 시연 가치와 기술 위험을 동시에 고려한 것이다.
