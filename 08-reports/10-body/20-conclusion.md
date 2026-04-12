---
title: 결론
type: report-section
status: draft
updated: 2026-04-12
owners:
  - team
related:
  - [[/00-overview/project-summary.md]]
  - [[/08-reports/00-index.md]]
source:
  - [[/00-overview/project-summary.md]]
  - [[/07-status/implementation-roadmap.md]]
---

# 20. 결론

차세대 사이버캠퍼스 프로젝트는 기존 LMS 기능을 단순히 복제하는 것이 아니라, 대학 수업 현장에서 반복적으로 발생하는 출석 신뢰성 문제를 기술적으로 개선하는 것을 목표로 한다.
학생, 교수, 서비스관리자 세 역할을 중심으로 기능과 권한을 나누고, Front / Backend / PresenceService / DB 의 서비스 경계를 분리하여 확장 가능한 구조를 설계했다.

핵심 차별점은 출석과 시험 접근 제어에 등록 단말과 강의실 네트워크 관측 정보를 결합한다는 점이다.
PresenceService 는 OpenWrt 또는 dummy snapshot 을 통해 재실성 근거를 제공하고, Backend 는 수강 정보와 시간표, 강의실, 출석 세션 상태를 결합해 최종 판정을 수행한다.
DB 는 출석 상태뿐 아니라 변경 이력과 시험 응시 데이터를 구조화하여 추적성을 확보한다.

중간 단계에서는 로그인, 강의/공지 조회, 단말 관리, eligibility, 출석/시험 모델, Docker 실행 환경 등 핵심 기반을 마련했다.
최종 단계에서는 모든 역할별 화면 캡처, API 상세, Mermaid 다이어그램, DB ERD, 주요 코드 설명, 테스트 결과, CI/CD 설계, 조선대학교 및 타 학교 도입 가능성까지 포함해 완성된 보고서로 정리한다.

남은 과제는 실제 OpenWrt 수집 안정화, 과제/성적/질문 등 LMS 기능 확장, CI/CD 자동화, 운영 정책 정리다.
이 과제를 해결하면 본 프로젝트는 조선대학교 테스트베드뿐 아니라 다른 학교 환경에도 적용 가능한 재실성 기반 LMS 프로토타입으로 발전할 수 있다.
