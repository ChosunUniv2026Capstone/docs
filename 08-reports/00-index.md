---
title: 캡스톤 보고서 목차
type: report
status: draft
updated: 2026-04-12
owners:
  - team
related:
  - [[/00-overview/project-summary.md]]
  - [[/04-architecture/service-map.md]]
  - [[/05-work-items/epic-full-lms-delivery-plan.md]]
source:
  - [[/00-overview/project-summary.md]]
  - [[/01-requirements/req-student-features.md]]
  - [[/01-requirements/req-professor-features.md]]
  - [[/01-requirements/req-admin-features.md]]
  - [[/01-requirements/req-attendance-presence.md]]
  - [[/04-architecture/service-map.md]]
  - [[/04-architecture/local-runtime-topology.md]]
  - [[/04-architecture/data-model-overview.md]]
  - [[/04-architecture/attendance-workflow-architecture.md]]
  - [[/04-architecture/exam-mvp-contract.md]]
---

# 캡스톤 보고서 목차

`08-reports` 는 차세대 사이버캠퍼스 프로젝트의 캡스톤 **주간 / 중간 / 최종 보고서**를 작성하기 위한 보고서 영역이다.
기존 `00-overview` ~ `07-status` 문서는 프로젝트 source of truth 이고, 이 영역은 그 내용을 제출용 보고서 형식으로 재구성한다.

# 작성 원칙

- 보고서는 **본문**과 **부록**으로 나눈다.
- 주간보고서, 중간보고서, 최종보고서는 같은 양식을 공유한다.
- 중간보고서는 목표 대비 달성치 중심으로 작성한다.
- 최종보고서는 같은 틀에서 모든 항목이 최종 완료 상태로 정리된 문서로 마무리한다.
- 섹션별 파일은 편집 단위이고, `99-combined-report.md` 는 본문과 부록 내용을 한 파일에 모은 제출/검토용 통합본이다.
- 구현 완료와 설계/계획은 반드시 구분해서 적는다.
- 전체 소스코드 원문, 회의록 원문, 커밋 로그 전체는 본문에 복붙하지 않고 필요한 핵심 요약과 링크만 둔다.
- `08-reports` 는 제출용 보고서 snapshot 이므로 모든 docs 변경마다 자동으로 동기화하지 않는다.
- `08-reports` 갱신은 명시적인 보고서 업데이트 요청이 있을 때만 수행한다. 예: 주간보고서 작성, 중간보고서 갱신, 최종보고서 정리, `08-reports` 반영 요청.
- 평소에는 `00-overview` ~ `07-status` 의 current truth 문서를 먼저 최신으로 유지하고, 보고서는 다음 명시적 보고서 갱신 시점에 해당 내용을 요약/재구성한다.

# 파일 구조

## 공통

- [[/08-reports/00-index.md]]: 보고서 영역 목차와 작성 원칙
- [[/08-reports/01-report-template.md]]: 주간/중간/최종 공통 보고서 양식
- [[/08-reports/99-combined-report.md]]: 본문/부록 통합본

## 본문

1. [[/08-reports/10-body/01-overview.md]]
2. [[/08-reports/10-body/02-goals.md]]
3. [[/08-reports/10-body/03-necessity-and-background.md]]
4. [[/08-reports/10-body/04-target-users-and-adoption.md]]
5. [[/08-reports/10-body/05-design-philosophy.md]]
6. [[/08-reports/10-body/06-system-architecture.md]]
7. [[/08-reports/10-body/07-service-infrastructure.md]]
8. [[/08-reports/10-body/08-user-roles-and-permissions.md]]
9. [[/08-reports/10-body/09-feature-catalog.md]]
10. [[/08-reports/10-body/10-frontend-screens.md]]
11. [[/08-reports/10-body/11-backend-api-and-flows.md]]
12. [[/08-reports/10-body/12-presence-service-flows.md]]
13. [[/08-reports/10-body/13-database-design.md]]
14. [[/08-reports/10-body/14-key-code.md]]
15. [[/08-reports/10-body/15-deliverables.md]]
16. [[/08-reports/10-body/16-schedule-and-wbs.md]]
17. [[/08-reports/10-body/17-ci-cd-design.md]]
18. [[/08-reports/10-body/18-verification-and-test.md]]
19. [[/08-reports/10-body/19-limitations-and-future-work.md]]
20. [[/08-reports/10-body/20-conclusion.md]]

## 제출 인스턴스

- [[/08-reports/20-weekly/00-weekly-report-template.md]]
- [[/08-reports/20-weekly/2026-04-12-weekly-report-draft.md]]
- [[/08-reports/30-midterm/midterm-report-draft.md]]
- [[/08-reports/40-final/final-report-draft.md]]

## 부록

- [[/08-reports/90-appendix/01-source-map.md]]
- [[/08-reports/90-appendix/02-screenshot-checklist.md]]
- [[/08-reports/90-appendix/03-api-endpoint-inventory.md]]
- [[/08-reports/90-appendix/04-diagram-inventory.md]]

# 명명 규칙

기존 `docs` repo 는 `req-*`, `adr-*`, `conv-*`, `task-*` 같은 영문 slug 파일명을 사용한다.
따라서 `08-reports` 도 파일 시스템 호환성과 링크 안정성을 위해 **두 자리 순번 + 영문 slug** 를 사용한다.
문서 제목과 본문 목차는 한국어로 작성한다.
