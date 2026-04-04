---
title: ADR-0006 강의자료 및 동영상 기능은 관련 DB 모델 전까지 프론트 UI 스캐폴드로 제공
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
  - 2026-04-03 사용자 지시: DB 변경 금지, 관련 DB 없으면 프론트엔드만 구현
---

# Context

강의자료 업로드/다운로드와 동영상 등록/시청 기능은 요구사항에 존재하지만, 현재 워크스페이스의 DB 모델에는 이를 저장할 전용 테이블이 없다.
이번 작업에서는 DB 변경이 금지되었다.

# Decision

- 강의자료 및 동영상 기능은 이번 단계에서 `Front` 중심의 UI 스캐폴드로 우선 제공한다.
- 교수는 같은 강의 상세 페이지 안에서 자료/동영상 등록 UI 를 사용할 수 있다.
- 학생은 같은 강의 상세 페이지 안에서 자료/동영상 목록과 열람용 링크 UI 를 사용할 수 있다.
- 관련 DB 모델과 정식 API 계약이 준비되기 전까지 이 기능은 세션 범위의 프론트 상태를 사용한다.
- `Backend` 와 `DB` 는 이번 기능에 대해 저장소/영속성 책임을 새로 갖지 않는다.

# Consequences

- 요구사항 탐색과 UX 검증은 앞당길 수 있다.
- 새로고침 이후 데이터 유지나 사용자 간 공유는 아직 보장되지 않는다.
- 정식 도입 시에는 DB 모델, API 계약, 권한 검증, 파일 저장 정책 문서화가 필요하다.
