---
title: 차세대 사이버캠퍼스 프로젝트 요약
type: overview
status: active
updated: 2026-03-30
owners:
  - team
related:
  - [[/01-requirements/req-student-features.md]]
  - [[/01-requirements/req-attendance-presence.md]]
  - [[/02-decisions/adr-0003-openwrt-device-collection.md]]
  - [[/02-decisions/adr-0004-attendance-authorization-flow.md]]
source:
  - [[/06-meetings/raw/2026-03-19-capstone-proposal.md]]
  - [[/06-meetings/raw/2026-03-25-kickoff-work-items.md]]
---

# 프로젝트 개요

조선대학교 기존 사이버캠퍼스를 개선한 차세대 사이버캠퍼스 프로토타입을 제작한다.
핵심 방향은 두 가지다.

1. 기존 LMS 핵심 기능을 현대적인 웹 서비스 구조로 재구성한다.
2. Wi-Fi 기반 위치 판별과 디바이스 인증을 결합한 재실성 기반 출석체크를 추가한다.

# 왜 필요한가

- 기존 출석 방식은 로그인이나 버튼 입력 중심이라 대리출석과 비정상 출석 시도를 막기 어렵다.
- 시험과 출석은 공정성과 신뢰성이 중요하므로 실제 강의실 인접 여부와 등록 단말 여부를 함께 보는 인증 체계가 필요하다.
- 기존 시스템은 기능 확장성과 유지보수 편의성 측면에서 개선 여지가 있다.

# 목표

- 학생, 교수, 관리자 기능을 포함한 웹 기반 LMS 프로토타입 구현
- Wi-Fi 및 디바이스 인증 기반 출석체크 모듈 구현
- 시험 및 출석 기능에 연동 가능한 접근 제어 로직 구현
- 테스트베드 기반 검증 결과와 개선 방향 정리

# 예상 서비스 구성

- `Front`: 학생/교수/관리자 웹 UI
- `Backend`: LMS 도메인과 수업, 과제, 시험, 출석 API
- `PresenceService`: 재실성 판별 보조와 단말 정보 수집 결과 처리
- `DB`: 사용자, 강의, 단말, 네트워크, 출석 관련 데이터 모델
- `docs`: 요구사항, 규약, ADR, 아키텍처, 회의록

# 기술 방향

- Wi-Fi 기반 재실성 판별
- Docker 기반 MSA 운영 구조
- OpenWrt 기반 단말 장치 정보 획득
- Python / FastAPI 기반 백엔드 우선 검토

# 현재 범위

- 공지사항
- 강의자료
- 온라인 강의
- 과제 제출
- 시험 / 퀴즈
- 출석
- 성적 확인
- 질문 / 문의

# 비범위

- 실제 학사 시스템과의 정식 운영 연동
- 완전 자동 네트워크 인프라 구축
- 모바일 네이티브 앱 구현
