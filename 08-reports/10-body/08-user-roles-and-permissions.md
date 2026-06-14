---
title: 사용자 분류 및 권한 구성
type: report-section
status: draft
updated: 2026-06-15
owners:
  - team
related:
  - [[/01-requirements/req-student-features.md]]
  - [[/01-requirements/req-professor-features.md]]
  - [[/01-requirements/req-admin-features.md]]
  - [[/03-conventions/conv-auth-and-session.md]]
source:
  - [[/01-requirements/req-student-features.md]]
  - [[/01-requirements/req-professor-features.md]]
  - [[/01-requirements/req-admin-features.md]]
  - Backend/app/main.py
---

# 8. 사용자 분류 및 권한 구성

# 8.1 기본 사용자 분류

프로젝트는 학교 하나를 기준으로 사용자를 세 가지로 나눈다.

1. 학생
2. 교수
3. 서비스관리자

이 분류는 기능 설계, 권한 검사, 화면 구성, 보고서 목차의 기본 축이다.

# 8.2 권한 원칙

- 사용자는 로그인해야 보호된 API 를 사용할 수 있다.
- Front route 접근은 Backend bootstrap 이 반환하는 권한 정보를 기준으로 제한한다.
- Backend 는 path parameter 의 `student_id`, `professor_id` 가 로그인 주체와 일치하는지 검사해야 한다.
- 학생은 자신의 수강 강의에 대해서만 조회/응시/출석할 수 있다.
- 교수는 자신이 담당하는 강의에 대해서만 공지/시험/출석을 운영할 수 있다.
- 서비스관리자는 사용자, 강의실, AP, 재실성 데모 제어 같은 운영 기능을 담당한다.

# 8.3 역할별 기능 권한표

| 기능 | 학생 | 교수 | 서비스관리자 |
|---|---:|---:|---:|
| 로그인/세션 복구 | O | O | O |
| 내 강의 목록 조회 | O | O | - |
| 공지 목록/상세 조회 | O | O | O(운영 조회) |
| 공지 작성 | - | O | - |
| 강의자료 조회/다운로드 | O | O | - |
| 강의자료 등록/삭제 | - | O | - |
| 과제 제출/수정 | O | - | - |
| 과제 채점/피드백 | - | O | - |
| 성적/Q&A/학습진도 | O | O(담당 강의) | - |
| 단말 등록/삭제 | O | - | 운영 정책 관리 |
| 출석 세션 열기/닫기 | - | O | - |
| 출석 self check-in | O | - | - |
| 출석 roster/status 수정 | - | O | - |
| 출석 리포트 조회 | O(본인) | O(담당 강의) | - |
| 시험 목록/응시 | O | - | - |
| 시험 생성/수정/게시/종료 | - | O | - |
| 사용자 목록 조회 | - | - | O |
| 강의실/AP 매핑 조회/수정 | - | - | O |
| 재실성 데모 overlay 제어 | - | - | O |
| 서비스 상태 확인 | - | - | 일부 구현 |

# 8.4 인증 구조

현재 Backend 는 다음 인증 흐름을 제공한다.

- `POST /api/auth/login`: 로그인
- `POST /api/auth/refresh`: access token 갱신
- `GET /api/auth/bootstrap`: 세션 복구 + route access 반환
- `GET /api/auth/me`: bootstrap alias
- `POST /api/auth/logout`: refresh session revoke

Access token 은 API 요청의 `Authorization: Bearer` 헤더로 사용하고, refresh token 은 HttpOnly cookie 로 운영하는 설계다.

# 8.5 권한 실패 처리

권한 실패는 사용자 경험과 보안 측면 모두에서 명확해야 한다.

- 인증 없음: 로그인 화면으로 이동
- 자기 리소스가 아님: 접근 금지
- 수강/담당 강의가 아님: 강의 리소스 접근 거부
- 출석/시험 조건 불충족: 거부 사유 코드와 설명 표시
- 만료된 세션: refresh 시도 후 실패 시 로그아웃 처리
