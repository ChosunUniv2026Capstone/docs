---
title: 캡스톤 최종보고서 초안
type: final-report
status: draft
updated: 2026-04-12
owners:
  - team
related:
  - [[/08-reports/99-combined-report.md]]
  - [[/08-reports/01-report-template.md]]
source:
  - [[/08-reports/10-body/01-overview.md]]
  - [[/08-reports/10-body/20-conclusion.md]]
---

# 캡스톤 최종보고서 초안

# 1. 보고서 정보

- 보고서 종류: 최종보고서
- 기준일: 최종 제출 시점에 갱신
- 작성 방식: `08-reports/99-combined-report.md` 를 기준으로 완성 상태를 정리

# 2. 최종보고 작성 원칙

최종보고서는 중간보고서와 같은 큰 구조를 유지하되, 모든 항목을 최종 완료 상태로 정리한다.
구현되지 않은 기능은 “계획”으로 남기지 않고, 최종 범위에서 제외되었는지 또는 후속 과제로 분리되었는지를 명확히 적는다.

# 3. 최종보고 필수 보강 항목

- 주요 Front 기능 화면 캡처 37개 반영 상태를 검수하고, 체크리스트 미완 항목 추가 촬영
- Backend API request/response 예시 보강
- PresenceService 실 장비 또는 더미 snapshot 검증 결과 보강
- DB ERD 최종화
- 테스트 실행 결과 표 삽입
- Docker 실행/health check 결과 삽입
- CI/CD 구현 여부와 workflow 결과 삽입
- 조선대학교 적용 시나리오와 타 학교 확장 조건 정리
- 한계와 향후 계획 최종 정리

# 4. 최종 산출물 체크리스트

| 항목 | 완료 여부 | 근거 |
|---|---|---|
| 최종 통합 보고서 | 미완 | `99-combined-report.md` 보강 필요 |
| 화면 캡처 | 부분 완료 | `assets/screenshots/` 37개 반영, OpenWrt router 화면 추가 필요 |
| API 상세 | 초안 | request/response 예시 보강 필요 |
| Mermaid diagrams | 초안 | 최신 구현 재검토 필요 |
| DB ERD | 초안 | 관계/제약 보강 필요 |
| 테스트 결과 | 미완 | 최종 실행 결과 필요 |
| CI/CD | 계획 | workflow 구현 여부 확인 필요 |

# 5. 최종 결론 초안

본 프로젝트는 차세대 사이버캠퍼스의 핵심 LMS 기능과 재실성 기반 출석/시험 접근 제어를 결합한 프로토타입이다.
학생, 교수, 서비스관리자 세 역할을 기준으로 기능을 분리하고, Front/Backend/PresenceService/DB 의 책임을 나누어 확장 가능한 구조를 설계했다.
최종 제출 시점에는 실제 구현 범위와 검증 결과를 반영해 본 문서를 완성한다.
