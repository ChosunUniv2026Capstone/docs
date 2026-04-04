---
title: 전체 LMS 구현 로드맵
type: task
status: doing
updated: 2026-03-30
owners:
  - team
related:
  - [[/01-requirements/req-student-features.md]]
  - [[/01-requirements/req-professor-features.md]]
  - [[/01-requirements/req-admin-features.md]]
  - [[/04-architecture/service-map.md]]
  - [[/04-architecture/local-runtime-topology.md]]
source:
  - [[/06-meetings/raw/2026-03-19-capstone-proposal.md]]
  - [[/06-meetings/raw/2026-03-25-kickoff-work-items.md]]
  - [[/06-meetings/raw/2026-03-30-presence-logic-clarification.md]]
---

# 목표

학생, 교수, 관리자 기능 전체를 단계적으로 구현하면서, 재실성 기반 출석/시험 가드를 모든 관련 기능에 안전하게 연결한다.

# 구현 단계

## Phase 1. Foundation

- 역할별 로그인
- 학생 단말 등록/삭제
- 출석/시험 eligibility 확인
- 로컬 Docker 기반 통합 실행
- CSV seed 기반 초기 데이터 구성

## Phase 2. Academic Read Model

- 학생 강의 목록 조회
- 교수 담당 강의 목록 조회
- 관리자 사용자 / 강의실 / AP 매핑 조회
- 공지사항 조회 / 상세 조회 / 작성

## Phase 3. Learning Content

- 강의자료 업로드 / 다운로드
- 동영상 메타데이터 등록 / 재생 링크
- 학생 강의자료/동영상 조회

## Phase 2-3 Bridge

- 학습 자료 / 동영상은 정식 Phase 3 계약 전까지 강의 상세 화면 안의 Front 임시 스캐폴드로만 미리보기할 수 있다.
- 이 bridge 단계는 Backend / DB 계약이 준비된 것으로 간주하지 않는다.

## Phase 4. Assignment and Quiz

- 교수 과제 생성 / 마감일 설정
- 학생 과제 제출
- 교수 제출물 조회 / 피드백
- 교수 퀴즈 / 시험 출제
- 학생 퀴즈 / 시험 응시

## Phase 5. Attendance and Grade Record

- 출석 기록 저장 / 조회
- 교수 출석 / 진도율 조회
- 성적 조회 / 관리
- 관리자 운영 지표

# 현재 실행 슬라이스

다음 구현 우선순위는 아래 세 축이다.

1. 역할별 강의 목록 조회
2. 공지사항 조회 / 상세 조회 / 작성
3. 강의 상세 화면 안의 학습 자료 / 동영상 임시 프론트 스캐폴드
4. 관리자 사용자 / 강의실 / 와이파이 목록 조회

# 비기능 원칙

- docs-first 유지
- 모든 역할 기능은 Docker Compose로 로컬 실행 가능해야 함
- 학생/교수/관리자 공통 로그인은 dev seed로 바로 검증 가능해야 함
- 출석/시험 정책은 PresenceService eligibility 가드를 재사용함
