---
title: ADR-0006 학습 자료와 동영상은 정식 계약 전까지 프론트 임시 스캐폴드로만 제공
type: decision
status: accepted
updated: 2026-04-03
date: 2026-04-03
deciders:
  - team
related:
  - [[/01-requirements/req-student-features.md]]
  - [[/01-requirements/req-professor-features.md]]
  - [[/03-conventions/conv-service-boundary.md]]
  - [[/05-work-items/epic-full-lms-delivery-plan.md]]
source:
  - [[/01-requirements/req-student-features.md]]
  - [[/01-requirements/req-professor-features.md]]
  - [[/05-work-items/epic-full-lms-delivery-plan.md]]
---

# Context

강의자료 업로드/다운로드와 동영상 등록/시청 기능은 요구사항에 존재하지만, 현재 워크스페이스에는 이를 위한 정식 DB 모델과 Backend API 계약이 아직 없다.
동시에 강의 상세 화면 설계와 사용자 흐름 검증은 지금 단계에서도 필요하다.

# Decision

- 강의자료 및 동영상 기능은 정식 계약이 준비되기 전까지 `Front` 중심의 **임시 UI 스캐폴드** 로만 제공한다.
- 교수는 같은 강의 상세 페이지 안에서 자료/동영상 등록 UI 를 사용할 수 있다.
- 학생은 같은 강의 상세 페이지 안에서 자료/동영상 목록과 열람용 링크 UI 를 사용할 수 있다.
- 관련 DB 모델과 정식 API 계약이 준비되기 전까지 이 기능은 세션 범위의 프론트 상태를 사용한다.
- `Backend` 와 `DB` 는 이번 기능에 대해 저장소/영속성 책임을 새로 갖지 않는다.
- 이 결정은 정식 `data model`, `API contract`, `migration/rollback` 문서가 준비되는 시점에 교체되어야 한다.

# Replacement Trigger

아래 세 조건이 모두 충족되면 이 ADR 은 더 이상 적용되지 않고 후속 문서가 우선한다.

1. 학습 자료/동영상용 데이터 모델 문서가 추가된다.
2. Backend API request/response/error 계약이 문서화된다.
3. DB migration 및 rollback 기준이 문서화된다.

# Consequences

- 요구사항 탐색과 UX 검증은 앞당길 수 있다.
- 새로고침 이후 데이터 유지나 사용자 간 공유는 아직 보장되지 않는다.
- 사용자는 이 영역을 실제 저장 기능이 아닌 임시 미리보기로 인지할 수 있어야 한다.
- 정식 도입 시에는 DB 모델, API 계약, 권한 검증, 파일 저장 정책 문서화가 필요하다.
