---
title: 최종보고서 증거 원장
type: report-appendix
status: draft
updated: 2026-05-22
owners:
  - team
related:
  - [[/03-conventions/conv-final-report-writing.md]]
  - [[/08-reports/40-final/final-report-draft.md]]
  - [[/08-reports/99-combined-report.md]]
  - [[/07-status/implementation-roadmap.md]]
source:
  - [[/03-conventions/conv-final-report-writing.md]]
  - [[/07-status/implementation-roadmap.md]]
  - ../../../../.omx/team-output/final-report/worker-1-evidence.md
  - ../../../../.omx/team-output/final-report/worker-2-visual-erd.md
---

# 최종보고서 증거 원장

이 문서는 최종보고서 작성 시 완료 주장에 사용할 증거를 repo `main` 기준으로 추적한다. 로컬 브랜치나 미병합 변경은 완료 근거가 아니라 진행 중 항목으로만 다룬다.

## 1. 기준 시각과 보고 기간

- 기준 시각: 2026-05-22T02:14:43.202751+09:00 (KST)
- 보고 기간 시작: 2026-05-18T09:00:00+09:00 (KST)
- 보고 기간 종료: 2026-05-22T02:14:43.202751+09:00 (KST)
- Git 조회 시작(UTC): 2026-05-18T00:00:00+00:00
- Git 조회 종료(UTC): 2026-05-21T17:14:43.202751+00:00

## 2. 제출본 source-of-truth

- 최종 제출본 원천: `docs/08-reports/40-final/final-report-draft.md`
- 통합 검토본: `docs/08-reports/99-combined-report.md`
- 신규 주간보고서는 작성하지 않는다.
- 현재 `docs` 작업 브랜치가 `main`이 아니면, 최종보고서 작성 규약 변경은 병합 전까지 `사용자 승인 작성 지시`로 취급하고 완료 증거와 분리한다.

## 3. Repo main baseline

| Repo | Current branch | HEAD | local `main` | `origin/main` | Dirty status | Weekly origin/main commits | Note |
|---|---|---|---|---|---|---:|---|
| Front | `main` | `418ae29` | `418ae29` | `418ae29` | clean | 2 | ok |
| Backend | `main` | `f06169e` | `f06169e` | `f06169e` | clean | 5 | ok |
| PresenceService | `main` | `bffda67` | `bffda67` | `bffda67` | clean | 0 | ok |
| DB | `main` | `621d712` | `621d712` | `621d712` | clean | 0 | ok |
| Service | `main` | `c36a432` | `c36a432` | `c36a432` | clean | 2 | ok |
| docs | `feat/final-report-writing-convention` | `cef3c2f` | `cef3c2f` | `cef3c2f` | dirty: final-report convention/report edits | 1 | not on main; report-writing input only |
| CodexKit | `main` | `a5a68c1` | `a5a68c1` | `a5a68c1` | clean | 0 | ok |
| DocsQuartz | `main` | `90d012b` | `90d012b` | `90d012b` | clean | 0 | ok |

## 4. Weekly origin/main commit logs

### 4.1 Front

```text
418ae29 (HEAD -> main, tag: smart-class-front-v0.6.0, origin/main, origin/HEAD) chore(main): release smart-class-front 0.6.0
73f5e09 feat(frontend): surface professor attendance CSV downloads
```

### 4.2 Backend

```text
f06169e (HEAD -> main, tag: v0.6.0, origin/main, origin/HEAD) chore(main): release 0.6.0
36e8524 feat(backend): let professors export attendance CSVs
f874e8a Keep realtime sockets connectable during slow attendance bootstrap
d121d80 Keep one-worker Backend responsive under PresenceService stalls
7f02a87 fix(backend): prevent presence waits from starving DB connections
```

### 4.3 PresenceService

- 보고 기간 내 `origin/main` commit 없음.

### 4.4 DB

- 보고 기간 내 `origin/main` commit 없음.

### 4.5 Service

```text
c36a432 (HEAD -> main, tag: v0.4.1, origin/main) chore(main): release 0.4.1
e89dcdb fix(service): pin attendance CSV demo manifest
```

### 4.6 docs

```text
cef3c2f (HEAD -> feat/final-report-writing-convention, origin/main, origin/HEAD, main) docs(attendance): align professor CSV export scope
```

### 4.7 CodexKit / DocsQuartz

- 보고 기간 내 `origin/main` commit 없음.

## 5. 검증 경계와 caveat

- Backend / PresenceService Python 테스트는 `PYTHONPATH=. pytest -q` 형태를 기준으로 기록한다. plain `pytest -q`는 import path 문제로 실패할 수 있으므로 실패 자체를 기능 실패로 과장하지 않는다.
- PresenceService 테스트 통과 시에도 Pydantic alias 관련 warning은 주의 항목으로 분리한다.
- OpenWrt / 교내 Wi-Fi 장기 현장 검증, 상용 운영 배포, 학사시스템 정식 연동, 네이티브 모바일 앱은 완료 성과가 아니라 한계 또는 후속 과제로 기록한다.
- `Service` image manifest / compose 검증은 실행 가능성 근거이지만, workflow run 또는 demo server provenance 없이는 실배포 완료 근거가 아니다.

## 6. 기능별 종합 증거 매트릭스

| Evidence ID | 기능 영역 | 완료도 | 화면 근거 | API / 코드 근거 | DB 근거 | 테스트 / 실행 근거 | 한계 / 후속 과제 |
|---|---|---|---|---|---|---|---|
| E-AUTH-01 | 인증 / 세션 | 로컬 MVP 완료 | Fig. 1-6 redbox: 로그인, 실패, 권한거부, 역할별 대시보드 | `Backend/app/main.py:920` login, `:961` refresh, `:1054` bootstrap, `:1070` logout; `Front/src/api.ts`; `Front/src/router.ts` | `DB/postgres/init/010_seed.sql` seed users, `refresh_sessions` | `Backend/tests/test_presence_admin_and_auth.py:218`, `:590`, `:683`; `Front/tests/e2e/auth-routing.spec.ts:584` | 운영 SSO/학사 인증 연동은 후속 과제 |
| E-UI-01 | 역할별 Front UI | 로컬 MVP 완료 | Fig. 4-55 redbox(역할별 UI 전체; Fig. 56은 N/A) | `Front/src/router.ts`, `Front/src/App.tsx`, `Front/src/api.ts` | 역할/수강/강의 seed tables | `Front/tests/e2e/auth-routing.spec.ts:584`, `selected-lms-subset.spec.ts:55`, `exam-workflow.spec.ts:244` | Fig. 56 OpenWrt router registration/token 화면은 N/A로 API/DB/Service 근거 대체 |
| E-LMS-01 | 강의 / 공지 / selected LMS read model | 로컬 MVP 완료 | Fig. 8-16, 26-35 redbox | `Backend/app/main.py:1102-1456`, `:1785-1843` | `courses`, `course_enrollments`, `notices`, `learning_items`, `assignments`, `course_qna_threads`, `learning_progress` | `Backend/tests/test_lms_selected_subset.py:123`, `:172`, `:200`; notice tests `test_presence_admin_and_auth.py:272` | selected-LMS 추가 화면 캡처 완료; 운영 데이터 다양화는 후속 과제 |
| E-ATT-01 | 출석 workflow | 로컬 MVP 완료 | Fig. 17-20, 40-47 redbox | `Backend/app/attendance.py`; `Backend/app/main.py:2028-2318`; WebSocket `/ws/attendance` | `attendance_sessions`, `attendance_session_slots`, `attendance_records`, `attendance_status_audit_logs`, `report_exports` | `Backend/tests/test_attendance_realtime.py:226`, `:369`, `:405`, `:498`, `:593`, `:1030`; weekly commits `36e8524`, `f874e8a`, `d121d80`, `7f02a87` | 장기 교실 현장 검증은 후속 과제 |
| E-EXAM-01 | 객관식 시험 workflow | 로컬 MVP 완료 | Fig. 21-25, 36-39 redbox | `Backend/app/main.py:1469-1710`; `Front/tests/e2e/exam-workflow.spec.ts` | `exams`, `exam_questions`, `exam_question_options`, `exam_submissions`, `exam_submission_answers` | `Backend/tests/test_exam_contract_alignment.py:147`, `:208`, `:261`, `:294`; `Front/tests/e2e/exam-workflow.spec.ts:244` | 서술형/파일형 시험과 대규모 부정행위 대응은 후속 과제 |
| E-PRES-01 | PresenceService eligibility / collector / demo overlay | 로컬 MVP 완료 | Fig. 18, 49-55 redbox; Fig. 56 N/A | `PresenceService/app/main.py:45`, `:64`, `:88`, `:100-125`; `Service/openwrt/presence-collector.sh`; Backend registry endpoints `Backend/app/main.py:1988-2028` | `classroom_networks`, `access_points`, `access_point_interfaces`, `registered_devices`, `presence_eligibility_logs` | `PresenceService/tests/test_service.py:136`, `:153`, `:203`, `:296`, `:347`, `:652`; `test_registry.py:29` | dummy overlay는 실 OpenWrt 장기 검증을 대체하지 않음 |
| E-DB-01 | DB schema / seed / ERD | 로컬 MVP 완료 | ERD-1~ERD-8 raw/redbox SVG | `DB/postgres/init/*.sql`, `DB/postgres/migrations/*.sql` | 전체 PostgreSQL schema 및 seed | `DB/postgres/tests/object_storage_triggers.sql`; Backend/Presence/Service tests가 schema 계약을 간접 검증 | ERD SVG는 보고서용 산출물이며 DB migration 실행 로그는 최종 제출 전 추가 권장 |
| E-SVC-01 | Service runtime / CI-CD | 부분 완료 | Service runtime은 diagram/manifest 중심; UI 화면 아님 | `Service/compose.yml`, `compose.local.yml`, `compose.image.yml`, `nginx/local.conf`, workflows `ci.yml`, `deploy-demo.yml` | DB 직접 테이블 없음; `report_exports` 등 ops metadata는 ERD-8 | `Service/tests/test_release_manifest_contract.py:27`, `:45`; `test_workspace_release_readiness.py:81`, `:98`; weekly commits `c36a432`, `e89dcdb` | workflow run / demo server provenance 없이는 실배포 완료로 쓰지 않음 |
| E-DOC-01 | docs / report | 부분 완료 | 본문/부록/증거 원장 갱신 | `docs/08-reports/40-final/final-report-draft.md`, `99-combined-report.md`, 부록 B-D/E | N/A | `git -C docs diff --check`, markdown sanity | docs가 feature branch/dirty 상태라 완료 증거와 작성 지시를 분리 |

## 7. Screenshot / ERD coverage gate

- 사이트 캡처는 설명 대상 UI에 빨간 사각형 테두리를 추가해야 완료 근거로 본다. 기존 37개와 추가 15개 PNG에 대한 redbox SVG는 `docs/08-reports/assets/screenshots/final/annotated/`에 생성했다.
- ERD는 전체 ERD와 부분별 ERD(user/auth, course/enrollment/notice/material, device/classroom/AP/presence, attendance/session, exam/question/submission/answer, selected LMS, service/ops N/A)를 모두 산출해야 한다. 산출물은 `docs/08-reports/assets/diagrams/final/`에 있다.
- 상세 체크리스트는 `docs/08-reports/90-appendix/02-screenshot-checklist.md` 및 `docs/08-reports/90-appendix/04-diagram-inventory.md`에 반영했다.
