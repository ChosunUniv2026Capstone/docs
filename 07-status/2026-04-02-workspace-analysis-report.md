---
title: 2026-04-02 워크스페이스 분석 리포트
type: status
status: active
updated: 2026-04-02
owners:
  - team
related:
  - [[/00-overview/project-summary.md]]
  - [[/04-architecture/service-map.md]]
  - [[/04-architecture/local-runtime-topology.md]]
  - [[/05-work-items/epic-full-lms-delivery-plan.md]]
  - [[/05-work-items/task-phase-2-academic-read-model.md]]
  - [[/07-status/implementation-roadmap.md]]
source:
  - Local workspace scan on 2026-04-02
---

# 요약

2026-04-02 기준 현재 워크스페이스는 **Phase 1 완료 + Phase 2 일부 구현 상태**로 보인다.
핵심 vertical slice 는 이미 동작 가능한 수준이다.

- Front: 로그인, 역할별 대시보드, 학생 단말 관리, 공지 조회/작성, eligibility 확인 구현
- Backend: 로그인, 강의 목록, 공지, 관리자 조회, 단말 등록/삭제, attendance eligibility API 구현
- PresenceService: 더미 OpenWrt snapshot + Redis 캐시 기반 eligibility 보조 구현
- DB: vertical slice 를 위한 스키마/seed 준비 완료

반면 아래는 아직 본격 미구현 상태다.

- 강의자료 / 동영상
- 과제 / 제출물
- 퀴즈 / 시험 상세 플로우
- 성적
- 질문 / 문의
- 관리자 수정형 운영 기능

# 문서 동기화 확인

작업 시작 전 `docs` repo 에서 `main` 브랜치를 확인했고, 2026-04-02 에 `git pull --ff-only origin main` 기준 최신 상태를 맞췄다.
문서상 현재 기준은 다음과 같다.

- 로드맵: `docs/07-status/implementation-roadmap.md`
- 전체 단계: `docs/05-work-items/epic-full-lms-delivery-plan.md`
- 현재 실행 슬라이스: `docs/05-work-items/task-phase-2-academic-read-model.md`

문서 기준으로도 현재 우선순위는 다음 3축이다.

1. 역할별 강의 목록 조회
2. 공지사항 조회 / 작성
3. 관리자 사용자 / 강의실 / AP 매핑 조회

즉, 현재 구현은 문서의 **Phase 2 Academic Read Model** 방향과 대체로 맞는다.

# 워크스페이스 구조 관찰

- `/home/da14n/capstone/smart-class` 자체는 git repo 가 아님
- 아래 하위 폴더들이 각각 독립 repo 임
  - `docs`
  - `Front`
  - `Backend`
  - `PresenceService`
  - `DB`
- 네 개 코드 repo 와 docs repo 는 모두 `main` 브랜치 기준으로 보였음
- `Front` 에만 추적되지 않은 `.env` 가 1개 있었음

# 현재 구현 상태

## 1. Front

### 확인된 구현
- React + TypeScript + Vite 단일 앱
- `App.tsx` 중심의 단일 화면형 MVP 구조
- 공통 로그인
- 학생 강의 목록 조회
- 학생 공지 조회
- 학생 단말 등록 / 삭제
- 학생 attendance / exam eligibility 확인
- 교수 담당 강의 조회
- 교수 공지 작성
- 관리자 사용자 목록 조회
- 관리자 강의실 / AP 매핑 조회

### 검증 결과
- `npm run build` 성공

### 해석
현재 Front 는 문서의 Phase 2 범위를 **빠르게 검증하기 위한 MVP** 로는 적절하다.
다만 구조가 `App.tsx` 1파일 중심이라 이후 기능 확장 시 유지보수 비용이 급격히 커질 가능성이 높다.

## 2. Backend

### 확인된 구현
- FastAPI 기반
- 구현 endpoint
  - `POST /api/auth/login`
  - `GET /health`
  - `GET /api/students/{student_id}/courses`
  - `GET /api/professors/{professor_id}/courses`
  - `GET /api/notices/{login_id}`
  - `POST /api/professors/{professor_id}/notices`
  - `GET /api/admin/users`
  - `GET /api/admin/classrooms`
  - `GET /api/admin/classroom-networks`
  - `GET/POST/DELETE /api/students/{student_id}/devices...`
  - `POST /api/attendance/eligibility`
- DB 연동, 수강 여부 확인, 시간표 확인, 등록 단말 확인 후 PresenceService 호출

### 검증 결과
- `python3 -m compileall app` 성공

### 해석
Backend 는 현재 vertical slice 의 중심 역할을 잘 수행하고 있다.
특히 문서의 service boundary 대로 **최종 판정은 Backend, 네트워크 근거는 PresenceService** 로 나뉘어 있다.

## 3. PresenceService

### 확인된 구현
- FastAPI 기반
- Redis snapshot cache
- dummy OpenWrt snapshot provider
- `GET /health`
- `GET /snapshots/classrooms/{classroom_id}`
- `POST /eligibility/check`
- 등록 단말 MAC 과 AP station 목록 매칭

### 검증 결과
- `python3 -m compileall app` 성공

### 해석
문서의 실 OpenWrt 연동 전 단계로서 충분한 프로토타입 상태다.
즉, 현재는 **실장비 연동 전 검증용 presence stub** 에 가깝다.

## 4. DB

### 확인된 구현
- PostgreSQL init schema
- seed CSV 기반 초기 데이터
- users / classrooms / courses / schedules / enrollments / notices / registered_devices / classroom_networks / presence_eligibility_logs 테이블 존재

### 해석
vertical slice 를 뒷받침할 최소 스키마는 준비되어 있다.
특히 `presence_eligibility_logs` 테이블이 이미 있으므로, Backend 가 이후 판정 로그를 저장하는 방향으로 확장하기 쉽다.

# 핵심 갭 / 리스크

## 1. API 응답 규약과 실제 구현 불일치
문서 `docs/03-conventions/conv-api-response.md` 는 `success/data/error` envelope 를 요구한다.
하지만 현재 Front/Backend 는 대부분 raw JSON 배열/객체를 바로 주고받는다.

이건 Front/Backend 를 동시에 맡는 입장에서 **가장 먼저 정리해야 하는 계약 이슈** 다.
이 상태로 기능을 늘리면 이후 전면 수정 비용이 커진다.

## 2. 인증/세션 규약은 문서 대비 부분 구현
문서 `docs/03-conventions/conv-auth-and-session.md` 는 인증과 도메인 접근 제어를 분리한다.
현재는 로그인 응답에 `access_token` 이 있지만 Front 가 저장/재사용하지 않고, 보호 API 호출에 토큰 기반 인증도 아직 없다.

즉, 현재 로그인은 사실상 개발용 간편 인증 단계다.

## 3. Front 구조가 단일 파일 중심
`Front/src/App.tsx` 에 역할별 화면, 공지, 프로필, eligibility, 관리자 조회가 집중돼 있다.
Phase 3~5 기능을 넣기 시작하면 분리 없이는 속도가 급격히 떨어질 가능성이 높다.

## 4. 문서 참조 갭 1건
`Front/AGENTS.md` 가 요구하는 `docs/03-conventions/conv-frontend-experience-design.md` 파일이 현재 없다.
즉, 큰 UI 확장 전에 frontend experience convention 문서를 먼저 보강하는 것이 안전하다.

## 5. 출석 판정 로그 저장은 아직 미완성
DB 에는 `presence_eligibility_logs` 테이블이 있으나, 현재 Backend 서비스 코드에서는 저장 흐름이 보이지 않는다.
문서의 "판정 근거 저장 / 추적 가능" 요구를 완전히 만족하려면 이 부분이 이어져야 한다.

## 6. Presence API 문서와 실제 요청 계약 차이
문서 `docs/04-architecture/presence-eligibility-api.md` 의 요청 예시는 `studentId`, `courseId`, `classroomId`, `purpose` 중심이다.
하지만 실제 구현에서는 Backend 가 PresenceService 로 `registeredDevices` 배열도 함께 전달하고, PresenceService 는 이를 전제로 동작한다.

즉, 이 계약은 docs 에 명시적으로 반영하는 것이 좋다.

## 7. 역할별 기능 범위는 아직 절반 이하
문서 요구사항에는 강의자료, 동영상, 과제, 시험, 성적, 문의가 포함되지만 현재 구현은 조회형 MVP 중심이다.
따라서 지금은 "전체 LMS" 보다는 "출석 vertical slice + 학사 조회 MVP" 로 보는 것이 정확하다.

# Front 담당으로 어떻게 이어갈지

## 우선순위 1. 문서/계약 먼저 고정
먼저 아래 2개를 정리하는 것이 좋다.

1. API 응답을 envelope 로 바꿀지 여부 결정
2. `conv-frontend-experience-design.md` 문서 추가

이 두 가지 없이 화면을 대거 늘리면 나중에 공통 UX 와 응답 파싱을 전부 다시 맞춰야 한다.

## 우선순위 2. 구조 분리
추천 순서:

1. 라우팅 도입
2. `pages/`, `components/`, `features/`, `shared/api/` 정도로 분리
3. `auth`, `courses`, `notices`, `attendance`, `admin` 단위 분리

최소한 아래 정도는 쪼개는 것이 좋다.

- 로그인 페이지
- 학생 대시보드
- 교수 대시보드
- 관리자 대시보드
- 강의 상세 페이지
- 프로필/단말 관리 페이지
- 공통 API client

## 우선순위 3. 현재 슬라이스 UX 마감
기능 추가 전에도 아래는 바로 개선 가치가 있다.

- `reason_code` 를 사용자 친화 문구로 변환
- 로딩/에러/빈 상태를 역할별로 정리
- 교수 공지 작성 폼 validation 추가
- 관리자 목록 화면을 읽기 쉬운 표/카드 구조로 정리
- eligibility 결과에서 사유 코드와 근거를 UI 상 명확히 분리

## 우선순위 4. Phase 3 기능 준비
Front 는 다음 순서가 현실적이다.

1. 강의 상세 탭 구조 확장
   - 공지
   - 자료
   - 동영상
   - 과제
   - 시험
   - 성적
2. 학생 읽기 기능 먼저
3. 교수 작성 기능 다음
4. 관리자 운영 화면은 마지막

즉, **학생 조회형 UX → 교수 작성 UX → 관리자 수정 UX** 순서가 안전하다.

# Backend 담당으로 어떻게 이어갈지

## 우선순위 1. API 계약 정리
가장 먼저 아래를 정리해야 한다.

1. `conv-api-response` 를 실제 코드에 맞출지
2. 아니면 코드를 문서 규약에 맞춰 `success/data/error` envelope 로 통일할지

개인적으로는 지금 단계에서 **문서 규약에 맞춰 Backend 를 통일** 하는 편이 낫다.
Front/PresenceService 연계부도 함께 맞추면 이후 기능 확장이 훨씬 안정적이다.

## 우선순위 2. 공통 인증/권한 골격 추가
현재는 login endpoint 만 있고 실제 보호 API 인증 체계는 약하다.
다음이 필요하다.

- 토큰 검증 의존성
- 역할 기반 접근 제어
- 학생/교수/관리자 권한 guard
- login user 와 path parameter 일치 검증

특히 지금은 path parameter 만 알면 다른 사용자의 데이터를 조회할 여지가 있어 보이므로, 실제 보호 규칙을 먼저 넣는 것이 좋다.

## 우선순위 3. 현재 vertical slice 완성도 올리기
다음 3개는 비교적 작은 단위인데 가치가 크다.

1. `presence_eligibility_logs` 저장
2. attendance/exam 거부 reason code 체계 정리
3. 공지 / 강의 / 관리자 조회 endpoint 의 응답 형식 통일

## 우선순위 4. Phase 3 backend 설계 선행
바로 코딩보다 먼저 docs 를 보강하고 아래 순서로 가는 것이 적절하다.

1. 강의자료/동영상 데이터 모델 문서화
2. 관련 API contract 문서화
3. DB 영향 검토
4. 그 다음 read endpoint
5. 마지막으로 professor write endpoint

즉, **문서 → 읽기 API → 쓰기 API** 순서가 좋다.

## 우선순위 5. 시험/과제/성적은 묶어서 보지 말고 분할
문서상 범위가 넓어서 한 번에 구현하면 경계가 무너질 가능성이 크다.
추천 분해는 아래와 같다.

1. 강의자료 / 동영상
2. 과제
3. 퀴즈 / 시험
4. 출석 기록 저장
5. 성적

특히 시험은 재실성 조건과 엮이므로 출석보다도 계약을 더 조심해서 잡아야 한다.

# Front + Backend 둘 다 맡는 기준의 추천 진행 순서

## Step 1. 문서 정리
- `conv-frontend-experience-design.md` 추가
- API envelope 적용 여부 결정
- Presence eligibility 요청 계약(`registeredDevices`) 문서 반영
- 필요 시 docs 에 Front/Backend contract 문서 보강

## Step 2. 기존 슬라이스 정리
- Backend 응답 규약 통일
- Front API client 통일
- 인증/권한 골격 추가
- eligibility reason 표시 UX 개선

## Step 3. Phase 3 착수
- 강의자료 / 동영상부터 시작
- 학생 조회 API + UI 먼저
- 교수 업로드/등록은 다음

## Step 4. 그 다음 과제/시험
- 과제는 일반 LMS 흐름으로 먼저
- 시험은 eligibility 와의 결합 규칙을 문서 먼저 확정 후 진행

# 내가 추천하는 바로 다음 1주 작업안

## Front
- 라우팅 도입
- `App.tsx` 분리
- 공통 API client/error handling 정리
- eligibility 사유 코드 메시지 매핑 추가

## Backend
- 응답 envelope 통일 여부 결정 및 반영
- auth guard / role guard 추가
- `presence_eligibility_logs` 저장 추가
- 공지/강의/관리자 조회 endpoint 정리

## 공동
- docs 에 frontend UX convention 추가
- 자료/동영상 Phase 3 API 초안 문서화

# 참고 파일

## 문서
- `docs/00-overview/project-summary.md`
- `docs/01-requirements/req-student-features.md`
- `docs/01-requirements/req-professor-features.md`
- `docs/01-requirements/req-admin-features.md`
- `docs/01-requirements/req-attendance-presence.md`
- `docs/01-requirements/req-device-auth.md`
- `docs/02-decisions/adr-0004-attendance-authorization-flow.md`
- `docs/02-decisions/adr-0005-presence-snapshot-cache.md`
- `docs/03-conventions/conv-api-response.md`
- `docs/03-conventions/conv-auth-and-session.md`
- `docs/03-conventions/conv-service-boundary.md`
- `docs/04-architecture/service-map.md`
- `docs/04-architecture/local-runtime-topology.md`
- `docs/04-architecture/network-topology.md`
- `docs/04-architecture/presence-eligibility-api.md`
- `docs/05-work-items/epic-full-lms-delivery-plan.md`
- `docs/05-work-items/task-phase-2-academic-read-model.md`
- `docs/07-status/implementation-roadmap.md`
- `docs/07-status/open-questions.md`
- `docs/07-status/risks-and-issues.md`

## 코드
- `Front/src/App.tsx`
- `Front/src/api.ts`
- `Front/package.json`
- `Backend/app/main.py`
- `Backend/app/services.py`
- `Backend/app/models.py`
- `Backend/app/schemas.py`
- `Backend/app/presence_client.py`
- `PresenceService/app/main.py`
- `PresenceService/app/service.py`
- `PresenceService/app/models.py`
- `DB/postgres/init/001_schema.sql`
- `DB/postgres/init/010_seed.sql`
