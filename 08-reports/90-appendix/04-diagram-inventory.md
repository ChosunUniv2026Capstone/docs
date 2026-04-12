---
title: 다이어그램 목록
type: report-appendix
status: draft
updated: 2026-04-12
owners:
  - team
related:
  - [[/08-reports/10-body/06-system-architecture.md]]
  - [[/08-reports/10-body/11-backend-api-and-flows.md]]
  - [[/08-reports/10-body/12-presence-service-flows.md]]
  - [[/08-reports/10-body/13-database-design.md]]
---

# 부록 D. 다이어그램 목록

# D.1 본문 포함 다이어그램

| 위치 | 유형 | 목적 |
|---|---|---|
| `06-system-architecture.md` | Mermaid flowchart | 전체 논리 아키텍처 |
| `06-system-architecture.md` | Mermaid sequenceDiagram | 로그인/세션 복구 |
| `06-system-architecture.md` | Mermaid sequenceDiagram | 출석 eligibility |
| `06-system-architecture.md` | Mermaid flowchart | 출석 세션 운영 |
| `07-service-infrastructure.md` | Mermaid flowchart | Docker/Nginx 로컬 인프라 |
| `11-backend-api-and-flows.md` | Mermaid sequenceDiagram | Backend 인증 흐름 |
| `11-backend-api-and-flows.md` | Mermaid sequenceDiagram | 출석 세션 흐름 |
| `11-backend-api-and-flows.md` | Mermaid flowchart | 시험 흐름 |
| `12-presence-service-flows.md` | Mermaid flowchart | Presence eligibility 판정 |
| `12-presence-service-flows.md` | Mermaid sequenceDiagram | Presence snapshot/cache |
| `12-presence-service-flows.md` | Mermaid sequenceDiagram | Demo overlay |
| `13-database-design.md` | Mermaid erDiagram | DB ERD |
| `17-ci-cd-design.md` | Mermaid flowchart | CI pipeline |

# D.2 최종보고 전 보강할 다이어그램

- Front 화면 이동 구조
- Backend 권한 guard decision tree
- 시험 응시 상태 전이도
- 출석 session lifecycle state diagram
- OpenWrt push collector future flow
- 배포 환경 네트워크 구조
