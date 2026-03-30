---
title: 캡스톤 프로젝트 제안 요약
type: meeting-summary
status: active
updated: 2026-03-19
owners:
  - team
related:
  - [[/00-overview/project-summary.md]]
  - [[/01-requirements/req-attendance-presence.md]]
  - [[/01-requirements/req-device-auth.md]]
source:
  - [[/06-meetings/raw/2026-03-19-capstone-proposal.md]]
---

# 회의 목적

캡스톤 프로젝트 주제, 목적, 수행 범위, 기대효과를 정리하고 차세대 사이버캠퍼스 방향을 확정한다.

# 핵심 결정

- 프로젝트 주제는 차세대 사이버캠퍼스 프로토타입 구현이다.
- 차별화 포인트는 Wi-Fi 기반 재실성 판별과 디바이스 인증을 결합한 출석 인증이다.
- LMS 핵심 기능과 출석 / 시험 접근 제어를 함께 설계한다.

# 새 요구사항

- 학생, 교수, 관리자 관점의 LMS 핵심 기능을 제공해야 한다.
- 출석 허용 여부는 강의실 인접 여부와 등록 단말 여부를 반영해야 한다.
- 시험과 출석 기능은 강화된 인증 흐름을 사용해야 한다.

# 새 규약

- 문서와 구현은 분리된 레포 구조를 사용한다.
- 재실성 판별은 네트워크 정보와 단말 정보의 결합 결과를 사용한다.

# 구조 / 아키텍처 변화

- Front / Backend / PresenceService / DB / docs 로 레포를 분리한다.
- OpenWrt 기반 게이트웨이 또는 AP 구조를 통해 단말 연결 정보를 수집한다.

# 작업 항목 / 담당자 / 기한

- LMS 기능 조사: 심재혁, 박준완 / 금요일
- OpenWrt 게이트웨이 단말 목록 수집 방식 검토: 담당 미정

# 리스크

- 교내 Wi-Fi 환경에서 얻을 수 있는 단말 정보의 범위가 불명확하다.
- 디바이스 인증 정책과 예외 처리 기준이 아직 확정되지 않았다.

# 오픈 질문

- 출석 최종 판정은 Backend 가 할지 PresenceService 가 할지 어디까지 분리할 것인가
- 시험 접근 제어에 재실성 조건을 어느 수준까지 강제할 것인가
- 실제 운영 시 단말 등록과 변경 절차를 어떤 UX 로 제공할 것인가

# source

- [[/06-meetings/raw/2026-03-19-capstone-proposal.md]]
