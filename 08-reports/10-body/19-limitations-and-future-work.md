---
title: 한계 및 향후 계획
type: report-section
status: draft
updated: 2026-06-15
owners:
  - team
related:
  - [[/07-status/risks-and-issues.md]]
  - [[/07-status/open-questions.md]]
source:
  - [[/07-status/risks-and-issues.md]]
  - [[/07-status/open-questions.md]]
---

# 19. 한계 및 향후 계획

# 19.1 현재 한계

| 영역 | 한계 | 영향 |
|---|---|---|
| OpenWrt 수집 | collector push ingest 는 구현됐지만 실제 장비/학교 네트워크별 출력 차이가 있음 | 장기 station parsing 안정성 검증 필요 |
| MAC 기반 식별 | 랜덤 MAC 사용 시 매칭 실패 가능 | 학생 안내와 정책 필요 |
| 개인정보 | 단말 식별자 저장 정책 필요 | 운영 도입 전 보안/법무 검토 필요 |
| 시험 | 현재 MVP 는 객관식/진위형 중심 | 수동 채점/서술형/성적 공개 확장 필요 |
| LMS 기능 | 과제/성적/질문/자료 MVP 저장과 selected LMS 흐름은 구현됐지만 운영 수준의 정책과 예외 처리는 더 필요함 | 대규모 과목 운영과 학사시스템 연동 전 보강 필요 |
| CI/CD | component image publish 와 public pull 은 검증됨, demo deploy workflow/server provenance 는 추가 수집 필요 | 최종보고서에 실제 workflow run/healthcheck 증거 보강 필요 |
| 학교 도입 | 학교별 AP/학사 데이터 연동 방식 상이 | adapter/config 기반 확장 필요 |

# 19.2 기술적 리스크

- PresenceService snapshot 이 stale 한 상태에서 잘못된 허용/거부가 발생할 수 있다.
- Redis 또는 OpenWrt 수집 실패 시 수업 중 출석 경험이 나빠질 수 있다.
- WebSocket event ordering 이 어긋나면 교수/학생 화면의 출석 상태가 달라질 수 있다.
- DB schema 와 Front/Backend API 타입이 어긋나면 통합 오류가 발생한다.
- 권한 guard 가 누락되면 학생/교수별 리소스 접근 경계가 깨질 수 있다.

# 19.3 향후 계획

1. 실제 강의실 OpenWrt/AP 환경에서 collector push 장기 수집 검증
2. 서비스관리자용 router registration/token UI 완성
3. 출석 리포트와 통계 고도화
4. 시험 문제 유형 확장과 수동 채점/성적 공개
5. 과제 제출, 강의자료, 동영상, 질문/문의 기능의 운영 정책과 예외 처리 보강
6. GitHub Actions workflow run 증거와 demo deploy summary 수집
7. staging/prod 배포 환경 분리와 운영 secret 정책 보강
8. 조선대학교 테스트베드 운영 결과 수집
9. 타 학교 도입을 위한 설정/연동 가이드 작성

# 19.4 정책적 고려사항

- 학생 단말 MAC 주소 저장 고지와 동의 절차
- 랜덤 MAC 해제 안내
- 장애 발생 시 수동 출석 대체 절차
- 교수 수동 수정 권한과 감사 로그 보존 정책
- 시험 접근 제어 실패 시 이의 신청 절차
