---
title: 데이터 모델 개요
type: architecture
status: active
updated: 2026-03-30
owners:
  - db-owner
related:
  - req-attendance-presence
  - req-device-auth
  - conv-db-naming
  - adr-0005-presence-snapshot-cache
source:
  - 06-meetings/raw/2026-03-19-capstone-proposal.md
  - 06-meetings/raw/2026-03-30-presence-logic-clarification.md
---

# 핵심 엔티티

- `users`
  - 학생 / 교수 / 관리자
- `courses`
  - 강의 기본 정보
- `course_enrollments`
  - 수강 관계
- `classrooms`
  - 강의실 정보
- `course_schedules`
  - 강의 시간표와 강의실 배정
- `classroom_networks`
  - 강의실별 허용 Wi-Fi / AP / 게이트웨이 정보
- `registered_devices`
  - 사용자 등록 단말
- `network_snapshots`
  - 네트워크 수집 결과
- `presence_eligibility_logs`
  - 출석 / 시험 eligibility 요청 로그
- `attendance_records`
  - 출석 판정 결과와 사유

# 관계 요약

- 한 사용자는 여러 강의를 수강할 수 있다.
- 한 강의는 여러 시간표 슬롯을 가질 수 있다.
- 한 시간표 슬롯은 하나의 강의실에 연결된다.
- 한 강의실은 하나 이상의 허용 네트워크를 가질 수 있다.
- 한 사용자는 하나 이상의 등록 단말을 가질 수 있다.
- 한 사용자는 최대 5개의 등록 단말을 가질 수 있다.
- 하나의 등록 단말 MAC 은 하나의 사용자에게만 속해야 한다.
- 출석 기록은 사용자, 강의, 시간표, 네트워크 판정 결과를 참조한다.

# 설계 원칙

- 강의실, 네트워크, 단말 정보를 분리 저장한다.
- 출석 결과뿐 아니라 판정 근거도 추적 가능해야 한다.
- 시험 접근 제어에도 재사용 가능한 모델을 지향한다.
- Redis snapshot 캐시는 영속 저장소가 아니라 성능 최적화 계층으로 취급한다.
