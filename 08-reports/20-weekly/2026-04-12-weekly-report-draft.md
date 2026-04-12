---
title: 2026-04-12 주간 보고서 초안
type: weekly-report
status: draft
updated: 2026-04-12
owners:
  - team
related:
  - [[/08-reports/01-report-template.md]]
  - [[/08-reports/10-body/09-feature-catalog.md]]
source:
  - [[/07-status/implementation-roadmap.md]]
  - Local workspace scan on 2026-04-12
---

# 2026-04-12 주간 보고서 초안

# 1. 기본 정보

- 보고서 종류: 주간 보고서
- 기준일: 2026-04-12
- 대상 프로젝트: 차세대 사이버캠퍼스 프로토타입
- 기준 문서: `docs` main + `08-reports` 초안

# 2. 이번 주 목표

| 목표 | 계획 산출물 | 우선순위 |
|---|---|---|
| 캡스톤 보고서 체계 구축 | `08-reports` 폴더, 본문/부록/통합본 | 높음 |
| 기능/권한/서비스 구조 정리 | 사용자별 기능 목록, 서비스별 설계 | 높음 |
| 기술 상세 초안 작성 | API, Mermaid, ERD, 주요 코드 설명 | 높음 |
| 화면 캡처 현황 정리 | 역할별 주요 기능 캡처 체크리스트와 37개 실제 PNG 캡처 반영 | 중간 |

# 3. 수행 내용

| 작업 | 내용 | 관련 서비스 | 산출물 |
|---|---|---|---|
| 보고서 구조 설계 | 본문/부록, 주간/중간/최종 공통 양식 정의 | docs | `08-reports/00-index.md` |
| 본문 초안 | 목표, 필요성, 사용자, 설계, 기능, API, DB 등 작성 | docs/code repos | `10-body/*` |
| 부록 초안 | 출처 맵, 캡처 체크리스트, API inventory, diagram inventory | docs | `90-appendix/*` |
| 통합본 생성 | 본문 섹션을 한 파일로 모음 | docs | `99-combined-report.md` |

# 4. 목표 대비 달성치

| 목표 | 달성 내용 | 달성률 | 근거 | 미달성 사유/대응 |
|---|---|---:|---|---|
| 보고서 구조 구축 | 08-reports 폴더와 목차 초안 작성 | 80% | 파일 구조 생성 | 피드백 후 세부 조정 |
| 상세 본문 초안 | API/DB/인프라/기능/권한/설계 초안과 실제 화면 캡처 반영 | 70% | 본문 파일, `assets/screenshots/` | 잔여 실패/완료 화면 캡처 보강 필요 |
| 다이어그램 | Backend/Presence/DB Mermaid 초안 작성 | 70% | Mermaid code block | 실제 최신 구현 반영 검토 필요 |
| 화면 캡처 | Playwright 기반 주요 화면 37개 캡처 및 본문 삽입 | 70% | screenshot checklist, `assets/screenshots/` | OpenWrt router 화면 등 잔여 증거 보강 필요 |

# 5. 증거

- 기존 docs 구조: `00-overview` ~ `07-status`
- 새 보고서 구조: `08-reports`
- API 근거: `Backend/app/main.py`, `Front/src/api.ts`, `PresenceService/app/main.py`
- DB 근거: `DB/postgres/init/001_schema.sql`, `DB/postgres/init/013_exam_schema.sql`

# 6. 이슈와 리스크

| 이슈 | 영향 | 대응 |
|---|---|---|
| 잔여 화면 캡처 미완 | 실패/권한/제출 완료 등 일부 시나리오 증거 부족 | 체크리스트의 미완 항목만 추가 촬영 |
| 구현 완료/계획 혼재 | 평가자가 현 상태를 오해할 수 있음 | 각 표에 상태 컬럼 유지 |
| CI/CD 미구현 | 운영 완성도 부족 | CI/CD 설계 장을 계획 항목으로 명시 |

# 7. 다음 계획

1. 사용자 피드백 반영
2. 잔여 실패/권한/완료 시나리오 화면 캡처 추가
3. 각 API request/response 예시 보강
4. DB ERD 세부 cardinality 보강
5. 중간보고서 제출용 문장 다듬기
