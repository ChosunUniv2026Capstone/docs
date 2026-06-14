---
title: 보고서 개요
type: report-section
status: draft
updated: 2026-06-15
owners:
  - team
related:
  - [[/00-overview/project-summary.md]]
  - [[/08-reports/00-index.md]]
source:
  - [[/00-overview/project-summary.md]]
  - [[/04-architecture/service-map.md]]
---

# 1. 개요

본 프로젝트는 조선대학교 기존 사이버캠퍼스의 핵심 기능을 현대적인 웹 서비스 구조로 재구성하고, Wi-Fi 기반 재실성 판별과 등록 단말 인증을 결합한 출석/시험 접근 제어 기능을 제공하는 차세대 사이버캠퍼스 프로토타입이다.

기존 LMS는 강의자료, 공지, 과제, 시험, 출석, 성적과 같은 기본 기능을 제공하지만, 출석과 시험의 신뢰성은 여전히 사용자 입력이나 단순 로그인 여부에 많이 의존한다.
본 프로젝트는 강의실 네트워크에 실제로 접속한 학생 단말을 관측하고, 학생이 사전에 등록한 단말 정보와 비교하여 출석 및 시험 접근 가능 여부를 판단한다.

# 보고서 목적

이 보고서는 캡스톤 중간/최종 평가와 매주 제출되는 진행 보고를 위해 작성한다.
단순 구현 목록이 아니라 다음 내용을 함께 설명한다.

- 프로젝트 목표와 필요성
- 학생, 교수, 서비스관리자 관점의 기능 요구
- 조선대학교 및 타 학교 도입 가능성
- Front / Backend / PresenceService / DB 서비스 설계
- API, 데이터 모델, 화면, 주요 코드, 테스트, 인프라, CI/CD 계획
- 중간 산출물과 최종 산출물
- 일정, WBS, 목표 대비 달성치

# 현재 작성 기준

이 문서는 2026-06-15 제출 기준으로 실제 코드와 `docs` source of truth 를 다시 대조해 작성했다.
구현 완료 항목과 운영 단계에서 더 보강해야 할 항목은 문서 안에서 구분한다.

- 구현/검증된 축: 로그인, 역할별 강의 조회, 공지 조회/작성, 학생 단말 관리, 재실성 eligibility, 출석 세션, 출석 리포트/CSV, 시험 MVP, 과제 제출/채점, 강의자료, 성적, Q&A, 학습 진도, Docker 기반 로컬 실행
- 일부 구현/운영 보강 축: OpenWrt collector 장기 안정화, router registration/token 전용 UI, demo deploy workflow/server provenance, 운영 모니터링, 타 학교 도입 패키징
- 2026-06-15 갱신 축: collector push ingest, Backend AP registry/token API, selected LMS API/UI/DB, object storage/report export, continuous attendance monitoring schema, Service manifest 기반 image/demo mode 실행 구조

# 서비스 구성 요약

| 서비스 | 역할 |
|---|---|
| Front | 학생/교수/서비스관리자 웹 UI, 역할별 화면, 출석/시험/공지/단말 관리 화면 |
| Backend | 인증, LMS 도메인 API, 출석/시험 최종 판정, 권한 검사, 실시간 이벤트 |
| PresenceService | 강의실 네트워크 snapshot, 등록 단말 매칭, 재실성 eligibility 근거 제공 |
| DB | 사용자, 강의, 강의실, 단말, 출석, 시험, 인증 세션 데이터 저장 |
| Service | 로컬 source build, GHCR image mode, Nginx reverse proxy, release manifest, demo deploy |
| CodexKit | bootstrap, repo template, workflow/governance helper |
| docs | 요구사항, ADR, 아키텍처, 상태, 보고서 source of truth |

# 보고서 구성

본문은 평가자가 프로젝트의 목적, 구조, 구현 상세, 검증 근거를 순서대로 따라갈 수 있도록 구성한다.
부록은 본문을 보조하는 API 목록, 캡처 체크리스트, 다이어그램 목록, 출처 맵을 제공한다.
