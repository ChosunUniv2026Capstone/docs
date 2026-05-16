---
title: 구현 로드맵 상태
type: status
status: active
updated: 2026-05-16
owners:
  - team
related:
  - [[/05-work-items/epic-full-lms-delivery-plan.md]]
  - [[/05-work-items/task-phase-2-academic-read-model.md]]
  - [[/04-architecture/attendance-workflow-architecture.md]]
  - [[/04-architecture/exam-workflow-api.md]]
  - [[/04-architecture/exam-mvp-contract.md]]
source:
  - [[/06-meetings/raw/2026-03-30-presence-logic-clarification.md]]
  - current code/test audit, 2026-04-25
---


# 2026-05-14 current issue-resolution checkpoint

Active May 2026 issue-fix branches must use [[/07-status/2026-05-14-current-issue-resolution-contracts.md]] as the docs-first merge checkpoint.
The checkpoint records which contracts are already source-of-truth, which fixes are evidenced by worker branches, and which DB/Service or PR/merge evidence remains pending.
Do not close the initial open issues or merge the code branches solely from the checkpoint; attach branch/PR/test evidence for each issue closure.

# 2026-04-25 현재 구현 스냅샷

이 문서는 `docs` current truth 가 실제 구현보다 뒤처진 부분을 보정하기 위해 갱신했다.
`docs/08-reports/` 는 제출 snapshot 이므로 이 문서의 current truth 와 다를 수 있다.

## 검증된 현재 상태

- Front
  - React/Vite 기반 역할별 UI가 로그인, 프로필/단말 관리, 강의 목록, 공지, 관리자 조회, 출석, 시험 화면을 포함한다.
  - `npm run build` 통과.
  - `npm run lint` 통과.
- Backend
  - FastAPI 기반 auth/session, course, notice, admin, device, attendance, objective exam workflow API가 구현되어 있다.
  - `PYTHONPATH=. pytest -q` 기준 60개 테스트 통과.
- PresenceService
  - health, classroom snapshot, eligibility, admin dummy overlay/reset API가 구현되어 있다.
  - Redis collector snapshot cache, OpenWrt local collector push ingestion/health, demo baseline/overlay provider, AP threshold 판정 흐름이 있다.
  - `PYTHONPATH=. pytest -q` 기준 8개 테스트 통과.
- DB
  - 초기 schema/seed, presence threshold patch, attendance demo seed, exam MVP schema가 init asset 으로 존재한다.

## 단계별 상태

- Phase 1 — Foundation: 완료
  - 로그인, 세션 복구/refresh/logout, 학생 단말 관리, eligibility, Docker 기반 로컬 실행 자산, CSV seed 기반 초기 데이터 구성이 구현되어 있다.
- Phase 2 — Academic Read Model: 완료
  - 학생/교수 강의 목록, 공지 목록/상세/작성, 관리자 사용자/강의실/AP 매핑 조회가 구현되어 있다.
- Phase 2-3 Bridge — Learning Content UI scaffold: 완료(Front 임시 스캐폴드)
  - 강의 상세 화면 안에서 학습 자료/동영상 영역을 임시 UI로 노출한다.
  - Backend/DB 계약이 준비된 정식 Phase 3 구현으로 간주하지 않는다.
- Attendance demo / bundle session workflow: 완료(로컬 MVP)
  - bundle parent attendance session, slot fan-out, professor timeline/roster/history/stats, student active session/self check-in/semester matrix 흐름이 구현되어 있다.
- Objective exam workflow: 완료(로컬 MVP)
  - 교수 시험 생성/수정/삭제/게시/마감, 학생 시험 목록/상세/시작/답안 저장/제출, start guard, per-attempt deadline, deterministic question shuffle 흐름이 구현되어 있다.
  - 시험은 현재 로컬 정책상 `requires_presence=true` schema compatibility 를 유지하지만 start guard 의 세부 정책은 [[/04-architecture/exam-workflow-api.md]] 와 [[/04-architecture/exam-mvp-contract.md]] 를 따른다.
- Phase 3+ 선택 LMS 보강: 계획 유지, 일부 선택 구현 대상
  - 이미 구현된 과제/시험/공지/학습자료/출석 흐름 위에 성적 조회/관리, 과제 채점/피드백, Q&A/문의, 학습 진도율을 선택 구현 대상으로 둔다.
  - 회원가입/self-registration, 수강신청/승인 workflow, 전체 관리자 CRUD 는 후속 backlog 로 유지한다.

## 주의할 검증 경계

- Python 서비스 테스트는 현재 `PYTHONPATH=. pytest -q` 형태로 검증했다. plain `pytest -q` 는 import path 설정 없이 실행하면 `ModuleNotFoundError: No module named 'app'` 로 실패한다.
- PresenceService 테스트는 통과하지만 Pydantic alias 관련 warning 이 남아 있다.
- 실제 OpenWrt/교내 Wi-Fi 현장 장기 수집 안정성은 데모 AP 3대 collector push 검증과 별개의 후속 검증 항목이다.
