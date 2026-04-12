---
title: 전체 시스템 설계
type: report-section
status: draft
updated: 2026-04-12
owners:
  - team
related:
  - [[/04-architecture/service-map.md]]
  - [[/04-architecture/local-runtime-topology.md]]
  - [[/04-architecture/attendance-workflow-architecture.md]]
source:
  - [[/04-architecture/service-map.md]]
  - [[/04-architecture/local-runtime-topology.md]]
  - [[/04-architecture/attendance-workflow-architecture.md]]
---

# 6. 전체 시스템 설계

# 6.1 논리 아키텍처

```mermaid
flowchart LR
  User[학생 / 교수 / 서비스관리자] --> Nginx[Nginx Reverse Proxy]
  Nginx --> Front[Front React/Vite]
  Front -->|/api, /ws| Nginx
  Nginx --> Backend[Backend FastAPI]
  Backend --> DB[(PostgreSQL)]
  Backend --> Presence[PresenceService FastAPI]
  Presence --> Redis[(Redis Snapshot Cache)]
  Presence --> OpenWrt[OpenWrt / AP Station Source]
  Backend --> WS[Attendance WebSocket Broker]
  WS --> Front
  Docs[docs Source of Truth] -. guides .-> Front
  Docs -. guides .-> Backend
  Docs -. guides .-> Presence
  Docs -. guides .-> DB
```

# 6.2 서비스별 책임

| 서비스 | 책임 | 외부 노출 |
|---|---|---|
| Front | 역할별 화면, 입력 검증, API 호출, WebSocket 구독 | Nginx `/` |
| Backend | 인증, 권한, LMS API, 출석/시험 최종 판단 | Nginx `/api`, `/ws`, `/health` |
| PresenceService | 재실성 근거, snapshot cache, overlay/demo control | Docker 내부, Backend 의존 경로 |
| PostgreSQL | 영속 데이터 저장 | Docker 내부 |
| Redis | Presence snapshot/overlay/cache | Docker 내부 |
| Nginx | 단일 origin reverse proxy | 호스트 포트 3100 |

# 6.3 핵심 데이터 흐름

## 로그인/세션 복구

```mermaid
sequenceDiagram
  participant U as 사용자
  participant F as Front
  participant B as Backend
  participant D as DB

  U->>F: 로그인 정보 입력
  F->>B: POST /api/auth/login
  B->>D: 사용자/비밀번호 확인
  B-->>F: access token + refresh cookie
  F->>B: GET /api/auth/bootstrap
  B-->>F: 사용자 정보 + route access
```

## 출석 eligibility

```mermaid
sequenceDiagram
  participant S as 학생
  participant F as Front
  participant B as Backend
  participant P as PresenceService
  participant R as Redis
  participant D as DB

  S->>F: 출석/시험 접근 요청
  F->>B: POST /api/attendance/eligibility
  B->>D: 수강/강의실/등록 단말 조회
  B->>P: POST /eligibility/check
  P->>R: classroom snapshot 조회
  alt cache miss
    P->>P: dummy/OpenWrt snapshot 생성 또는 수집
    P->>R: snapshot 저장
  end
  P-->>B: eligible + reasonCode + evidence
  B->>D: eligibility log 저장
  B-->>F: 최종 허용/거부 결과
```

## 출석 세션 운영

```mermaid
flowchart TD
  A[교수 projected slot 선택] --> B[Backend slot 유효성 검증]
  B --> C[attendance_sessions parent 생성]
  C --> D[attendance_session_slots membership 저장]
  D --> E[학생 active session 조회]
  E --> F{Presence eligible?}
  F -- 예 --> G[slot별 attendance_records present 저장]
  F -- 아니오 --> H[거부 사유 반환]
  G --> I[attendance_status_audit_logs 기록]
  I --> J[WebSocket event 발행]
  J --> K[교수/학생/리포트 화면 갱신]
```

# 6.4 구현 상태와 계획

| 영역 | 현재 상태 | 계획 |
|---|---|---|
| 로그인/세션 | JWT access + refresh cookie 기반 구현 | 운영 환경 secret/만료 정책 강화 |
| LMS 기본 조회 | 강의/공지/서비스관리자 조회 구현 | 과제/성적/질문 확장 |
| 출석 | eligibility + attendance session API/모델 구현 | 실 장비 수집, 운영 정책 강화 |
| 시험 | 객관식/진위형 MVP 계약/구현 | 수동 채점, 성적 공개, 문제 유형 확장 |
| 인프라 | Docker Compose + Nginx | CI/CD, staging/prod 분리 |
