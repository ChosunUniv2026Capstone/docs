---
title: 산출물
type: report-section
status: draft
updated: 2026-05-03
owners:
  - team
related:
  - [[/05-work-items/epic-full-lms-delivery-plan.md]]
  - [[/07-status/implementation-roadmap.md]]
source:
  - [[/05-work-items/epic-full-lms-delivery-plan.md]]
  - [[/07-status/implementation-roadmap.md]]
---

# 15. 산출물

# 15.1 중간 산출물

| 산출물 | 설명 | 상태 |
|---|---|---|
| 요구사항 문서 | 학생/교수/서비스관리자, 출석, 단말, 시험 요구사항 | 작성됨 |
| ADR | 서비스 경계, OpenWrt, 출석 판정, Redis cache, attendance bundle 등 결정 기록 | 작성됨 |
| 아키텍처 문서 | 서비스 맵, 로컬 토폴로지, 데이터 모델, 출석/시험 API 계약 | 작성됨 |
| Front 프로토타입 | 로그인, 역할별 화면, 공지/단말/출석/시험 일부 UI | 구현/확장 중 |
| Backend API | 인증, 강의, 공지, 단말, 서비스관리자, 출석, 시험 API | 구현/확장 중 |
| PresenceService | snapshot cache, dummy overlay, eligibility | 구현/실 장비 확장 계획 |
| DB 스키마/seed | 사용자/강의/단말/출석/시험 schema 및 seed | 구현됨 |
| Docker 환경 | Nginx, Front, Backend, PresenceService, PostgreSQL, Redis | 구현됨 |
| Service runtime | local source mode, GHCR image mode, release manifest, demo deploy script | 구현/검증 진행 |
| 릴리스 이미지 | Backend/Front/PresenceService/DB GHCR public image publish 및 anonymous pull proof | 구현됨 |
| 테스트 | Backend pytest, PresenceService pytest, Front lint/build/e2e | 일부 구현 |

# 15.2 최종 산출물

최종 산출물은 다음을 목표로 한다.

- 통합 실행 가능한 차세대 사이버캠퍼스 프로토타입
- 학생/교수/서비스관리자 전체 기능 화면 캡처
- 출석/시험 신뢰성 강화 시나리오 시연
- API/DB/인프라/CI/CD 설계 및 검증 문서
- Mermaid 기반 sequence/flowchart/ERD
- 테스트 결과와 한계 분석
- 조선대학교 및 타 학교 도입 가능성 정리
- 최종보고서와 발표자료

# 15.3 산출물 평가 기준

| 기준 | 설명 |
|---|---|
| 기능성 | 요구된 역할별 기능이 실제 화면/API로 제공되는가 |
| 신뢰성 | 출석/시험 접근 제어가 단순 클릭이 아니라 근거 기반인가 |
| 추적성 | 출석 상태 변경, 시험 응시, eligibility 판단 근거가 남는가 |
| 확장성 | 학교별 네트워크/학사 데이터에 맞게 확장 가능한가 |
| 문서성 | 요구사항, 설계, 구현, 검증, 한계가 연결되어 있는가 |
