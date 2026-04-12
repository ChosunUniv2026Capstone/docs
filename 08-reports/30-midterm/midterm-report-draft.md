---
title: 캡스톤 중간보고서 초안
type: midterm-report
status: draft
updated: 2026-04-12
owners:
  - team
related:
  - [[/08-reports/99-combined-report.md]]
  - [[/08-reports/01-report-template.md]]
source:
  - [[/08-reports/10-body/01-overview.md]]
  - [[/08-reports/10-body/02-goals.md]]
  - [[/08-reports/10-body/16-schedule-and-wbs.md]]
---

# 캡스톤 중간보고서 초안

# 1. 보고서 정보

- 보고서 종류: 중간보고서
- 기준일: 2026-04-12
- 평가 기준: 목적과 달성치
- 작성 방식: `08-reports/10-body` 섹션을 기반으로 중간 시점 달성 내용을 요약

# 2. 중간보고 요약

본 프로젝트는 차세대 사이버캠퍼스 프로토타입을 목표로 하며, 기존 LMS 기능과 Wi-Fi/단말 기반 출석 신뢰성 강화를 함께 설계한다.
중간 시점에는 문서 기반 요구사항, 서비스 경계, DB 스키마, 로컬 실행 환경, 주요 API와 화면 흐름이 정리되었다.

# 3. 목표 대비 달성치

| 목표 | 중간 달성 내용 | 달성률 | 근거 | 남은 작업 |
|---|---|---:|---|---|
| 문서 기반 개발 체계 | docs source of truth, ADR, 요구사항 정리 | 80% | docs 00~07, 08-reports | 최종보고 보강 |
| LMS 기본 기능 | 로그인, 강의/공지, 단말 관리, 서비스관리자 조회 | 70% | Front/Backend/API | 과제/성적/문의 확장 |
| 출석 신뢰성 | PresenceService eligibility, attendance model | 60% | 출석 API/DB/문서 | 실 OpenWrt/운영 검증 |
| 시험 MVP | 시험 schema/API/UI 일부 구현 | 55% | exam contract/schema/API | 문항 유형/채점 확장 |
| 인프라 | Docker Compose + Nginx + DB/Redis | 70% | CodexKit compose | CI/CD/staging |
| 보고서 | 본문/부록/통합본 초안과 주요 화면 캡처 37개 반영 | 65% | 08-reports, assets/screenshots | 잔여 캡처/최종 검수 |

# 4. 중간 산출물

- `docs` 요구사항/ADR/아키텍처 문서
- Front React/Vite 프로토타입
- Backend FastAPI API
- PresenceService FastAPI + Redis cache 구조
- PostgreSQL schema/seed
- Docker Compose 로컬 실행 환경
- Mermaid diagram/ERD 초안
- 캡스톤 보고서 구조 초안

# 5. 중간 시점 리스크

- 실제 OpenWrt 수집 안정성 검증 필요
- 실패/권한/제출 완료 등 잔여 사용자 시나리오 증거 보강 필요
- CI/CD 는 아직 설계 단계
- 과제/성적/질문 등 LMS 전체 기능은 후속 구현 필요

# 6. 다음 단계

1. 중간보고 피드백 반영
2. 체크리스트 미완 항목 중심으로 잔여 화면 캡처 추가
3. 출석/시험 end-to-end 검증 강화
4. CI/CD workflow 설계와 최소 자동화 도입
5. 최종보고서 문장/그림/표 정리
