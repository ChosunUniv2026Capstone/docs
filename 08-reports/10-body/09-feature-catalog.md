---
title: 기능 상세 목록
type: report-section
status: draft
updated: 2026-06-15
owners:
  - team
related:
  - [[/01-requirements/req-student-features.md]]
  - [[/01-requirements/req-professor-features.md]]
  - [[/01-requirements/req-admin-features.md]]
  - [[/05-work-items/epic-full-lms-delivery-plan.md]]
source:
  - [[/01-requirements/req-student-features.md]]
  - [[/01-requirements/req-professor-features.md]]
  - [[/01-requirements/req-admin-features.md]]
  - [[/07-status/implementation-roadmap.md]]
---

# 9. 기능 상세 목록

# 9.1 기능 상태 범례

| 상태 | 의미 |
|---|---|
| 구현 | 현재 로컬 코드에서 동작하는 기능 |
| 일부 구현 | 주요 흐름은 있으나 운영 완성도 또는 일부 세부 기능이 남은 기능 |
| 설계 | 문서/데이터 계약이 있으나 구현이 완료되지 않은 기능 |
| 계획 | 요구사항에는 있으나 후속 단계로 남은 기능 |

# 9.2 학생 기능

| 기능 | 설명 | 상태 |
|---|---|---|
| 로그인 | 학생 계정으로 로그인하고 세션을 유지한다. | 구현 |
| 강의 목록 조회 | 수강 중인 강의 목록을 조회한다. | 구현 |
| 공지 목록/상세 조회 | 강의 또는 사용자 기준 공지 목록과 상세를 확인한다. | 구현 |
| 단말 등록/삭제 | 출석/시험 인증에 사용할 단말 MAC 을 등록/삭제한다. | 구현 |
| 재실성 eligibility 확인 | 강의실 네트워크와 등록 단말 기준으로 출석/시험 가능 여부를 확인한다. | 구현 |
| 출석 self check-in | 열린 출석 세션에 학생이 직접 출석 요청한다. | 구현 |
| 출석 학기 매트릭스 | 학기 전체 출석 상태를 차시별로 확인한다. | 구현 |
| 시험 목록/상세 | 강의별 시험 목록과 상세를 확인한다. | 구현 |
| 시험 응시/답안 저장/제출 | 시험을 시작하고 답안을 저장/제출한다. | 구현 |
| 강의자료/동영상 | 강의자료와 영상 자료를 조회하고 인증된 다운로드/진도 갱신을 수행한다. | 구현 |
| 과제/성적/질문 | 과제 제출·수정, 성적/피드백 확인, Q&A 문의 흐름을 사용한다. | 구현 |

# 9.3 교수 기능

| 기능 | 설명 | 상태 |
|---|---|---|
| 로그인 | 교수 계정으로 로그인한다. | 구현 |
| 담당 강의 조회 | 담당 강의 목록을 확인한다. | 구현 |
| 공지 작성/조회 | 담당 강의 공지를 작성하고 상세를 확인한다. | 구현 |
| 시험 초안 생성 | 객관식/진위형 중심 시험 초안을 만든다. | 구현 |
| 시험 게시/종료 | 시험을 학생에게 공개하거나 종료한다. | 구현 |
| 출석 projected slot 조회 | 날짜/강의/강의실 기준 출석 가능 차시를 확인한다. | 구현 |
| bundle 출석 세션 운영 | 여러 projected slot 을 하나의 parent session 으로 연다. | 구현 |
| roster/status 수정 | 학생별 출석 상태를 수정하고 사유를 기록한다. | 구현 |
| 출석 리포트 | slot aggregate, 학생별 통계, 이력, CSV export 를 확인한다. | 구현 |
| 자료/영상/과제/성적 | 학습 콘텐츠 등록/삭제, 과제 생성/채점, 성적/진도/Q&A 관리를 수행한다. | 구현 |

# 9.4 서비스관리자 기능

| 기능 | 설명 | 상태 |
|---|---|---|
| 로그인 | 서비스관리자 계정으로 로그인한다. | 구현 |
| 사용자 목록 | 학생/교수/서비스관리자 목록을 조회한다. | 구현 |
| 강의실 목록 | 강의실 정보를 조회한다. | 구현 |
| classroom network 조회/수정 | AP, SSID, gateway, threshold 정보를 조회/수정한다. | 구현 |
| 재실성 snapshot 조회 | 강의실별 관측 단말 상태를 확인한다. | 구현 |
| demo overlay 제어 | 더미 재실성 입력값을 변경해 시연한다. | 구현 |
| OpenWrt 장비 등록/토큰 | Backend AP registry/token API, DB registry, Service collector script 로 토큰 기반 수집 경계를 제공한다. 전용 Front UI 는 후속 과제다. | 일부 구현 |
| 운영 모니터링 | Backend/PresenceService health, readiness, collector health, snapshot 상태를 확인한다. 통합 observability 는 후속 과제다. | 일부 구현 |

# 9.5 공통 기능

- 문서 기반 개발 프로세스
- Docker 기반 로컬 실행
- Nginx 기반 단일 origin 라우팅
- Redis 캐시 기반 snapshot 재사용
- PostgreSQL 기반 영속 데이터 관리
- API/테스트/문서 동기화
