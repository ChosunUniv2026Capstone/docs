---
title: Smart Class 최종보고서 부록
type: final-report-appendix
status: final-appendix
updated: 2026-06-01
owners:
  - team
source:
  - ../../output/full-report-2026-06-01/source/SmartClass_Appendix_Revised.md
---

# Smart Class 최종보고서 부록

> 이 파일은 최종보고서의 두 번째이자 유일한 부록 문서 산출물이다. 최종보고서 본문(`99-combined-report.md`)과 이 부록만 열면 프로젝트의 화면, ERD, API, 코드, DB, 검증 근거를 모두 확인할 수 있도록 구성했다. 화면/ERD asset은 두 문서에 직접 연결된 증거 자료이며, 기존 작성 근거 문서는 내부 검증 자료로만 유지한다. 최종 독자가 프로젝트를 이해하기 위해 열어야 하는 문서 산출물은 보고서와 이 부록 두 파일뿐이다.

# A. 두 파일 산출물 계약

- 보고서 문서 산출물: `docs/08-reports/99-combined-report.md`
- 부록 문서 산출물: `docs/08-reports/99-combined-report-appendix.md`
- 증거 asset: 화면/ERD SVG·PNG는 위 두 문서에 직접 연결되어 본문 흐름 안에서 표시되는 보조 증거 자료다.
- 산출물 원칙: 보고서에서 필요한 스크린샷은 본문 가까이에 직접 이미지로 연결하고, 코드 근거는 코드블록으로 삽입하며, DB 설계는 ERD 이미지와 SQL excerpt로 즉시 확인 가능하게 둔다.
- 비범위: 상용 운영 배포, 장기 교내 Wi-Fi 현장 검증, 학사시스템 정식 연동, 네이티브 모바일 앱 구현은 완료 성과가 아니라 한계/개선 방향이다.

# B. 기준 시각, repo baseline, 기능별 증거 매트릭스

## 1. 기준 시각과 보고 기간

- 기준 시각: 2026-05-22 16:33 KST
- 보고 기간 시작: 2026-05-18 09:00 KST
- 보고 기간 종료: 2026-05-22 16:33 KST
- 시간 표기 원칙: 모든 보고서 시간은 KST 기준 `YYYY-MM-DD HH:MM KST` 형식으로 적고, UTC offset 표기는 본문 기준 시각 표기에서 제외한다.

## 2. 제출본 source-of-truth

- 보고서 산출물: `docs/08-reports/99-combined-report.md`
- 부록 산출물: `docs/08-reports/99-combined-report-appendix.md`
- 신규 주간보고서는 작성하지 않는다.
- 현재 `docs` 작업 브랜치가 `main`이 아니면, 최종보고서 작성 규약 변경은 병합 전까지 `사용자 승인 작성 지시`로 취급하고 완료 증거와 분리한다.

## 3. Repo main baseline

이번 주 변경사항은 각 repository의 `origin/main`을 기준으로 다시 확인했다. 아래 표의 HEAD와 PR 수는 보고서 작성용 임시 상태가 아니라 **main에 실제 반영된 결과**만 반영한다.

| Repo | 기준 branch | `origin/main` HEAD | local main sync | Weekly merged PRs / main changes | Note |
|---|---|---|---|---:|---|
| Front | `main` | `a2b1b8f` | synced | 4 | PR #45, #41, #46, #47 |
| Backend | `main` | `9e8ba35` | synced | 5 | PR #48, #49, #47, #50, #51 |
| PresenceService | `main` | `bffda67` | synced | 0 | no merged PR in period |
| DB | `main` | `621d712` | synced | 0 | no merged PR in period |
| Service | `main` | `290820f` | synced | 4 | PR #26, #27, #28, #29 |
| docs | `main` | `a675519` | synced | 3 PR + 6 report follow-up commits | PR #36, #38, #37은 보고 기간 안의 기능/계약 문서 변경이다. `9c33d29`~`a675519`는 2026-05-22 16:33 KST 이후 main에 반영된 보고서 asset/rendering 보정이며 기능 구현 PR 수에는 포함하지 않는다. |
| CodexKit | `main` | `a5a68c1` | synced | 0 | no merged PR in period |
| DocsQuartz | `main` | `90d012b` | synced | 0 | no merged PR in period |

## 4. 이번 주 개발 진행 내용(PR branch 기준)

이번 주 개발내용은 단순히 `origin/main`에 찍힌 commit 시각만 보지 않고, **main으로 merge된 PR branch**를 기준으로 산정한다. PR의 merge 시각이 보고 기간 안에 있으면 이번 주 개발내용으로 포함하고, 개발 기간은 해당 PR branch의 첫 commit 시각부터 PR merge 시각까지로 적는다. 아래에서는 먼저 평가자가 바로 이해할 수 있도록 자연어로 진행 내용을 설명하고, 그 뒤에 추적 가능한 PR 근거 표를 둔다.

### 4.1 이번 주 진행사항 요약

이번 주의 핵심 개발은 출석 운영 안정성 보강, 교수자용 출석 CSV export 완성, 과제 제출 수정/첨부 삭제 흐름 보강, 종료된 Q&A thread의 추가 답변 차단, 그리고 이 기능들이 포함된 demo/release manifest 고정이다. 단순히 PR이 여러 개 merge된 것이 아니라, 실제 사용자가 겪을 수 있는 병목·데이터 수정·권한/상태 불일치 문제를 발견하고 Backend, Front, Service, docs가 같은 계약으로 맞춰진 주간이다.

첫 번째로 Backend에서는 출석 화면을 열거나 학생이 체크인할 때 PresenceService 응답이 느려지면 Backend의 DB connection이 오래 점유되고, 단일 worker demo 환경에서 `/health`, `/api/auth/bootstrap`, attendance WebSocket까지 함께 지연되는 문제가 확인되었다. Backend #48은 이 문제를 운영성 결함으로 보고 고쳤다. `/health`를 DB 의존 없는 liveness endpoint로 분리하고, `/ready`를 DB readiness 확인용으로 따로 두었으며, SQLAlchemy pool timeout을 구조화된 503 오류로 바꾸었다. 또한 출석 hot path에서 느린 PresenceService 호출이나 WebSocket publish를 기다리는 동안 request DB session을 붙잡지 않도록 정리했고, 학생 check-in은 eligibility를 먼저 수집한 뒤 durable DB write를 수행하도록 조정했다. 결과적으로 출석 bootstrap과 realtime socket 연결이 느린 presence 경로에 의해 함께 멈추는 위험을 줄였다.

두 번째로 교수 출석 CSV export를 실제 사용 가능한 기능으로 연결했다. Backend #49에서는 교수자가 담당 과목의 출석 현황을 별도 수작업 없이 다운로드할 수 있도록 `attendance_summary_csv`와 `attendance_full_csv` export contract를 추가했다. 기존 report-export/object-storage 다운로드 경로를 재사용하여 권한, 저장, 인증 다운로드 흐름을 유지했고, UTF-8 BOM, summary/full variant filename, `sick` 상태의 공결 합산, 차시별 상태 라벨, 잘못된 export type 거부, 비담당 교수 접근 거부까지 테스트로 고정했다. Front #45는 이 Backend export를 교수 출석 화면의 실제 버튼으로 노출했다. 학생별 출석 누계 표를 출석 차시 목록 하단에 기본 표시하고, `요약본 CSV`와 `전체본 CSV` 즉시 다운로드 버튼을 추가했으며, 다운로드 object URL 정리를 `finally`에서 처리하도록 보강했다. 따라서 이번 주 기능 변화는 단순 API 추가가 아니라, 교수자가 화면에서 출석 통계를 보고 바로 CSV를 내려받는 end-to-end 사용 흐름으로 연결되었다.

세 번째로 과제 제출 수정과 첨부파일 제거 흐름을 보강했다. docs #37은 학생 과제 제출 multipart contract에 `remove_attachment_ids`를 추가하고, 이 값이 학생 자신의 현재 제출물에 속한 첨부만 참조해야 한다는 제약을 문서화했다. Backend #50은 이 계약에 맞춰 재제출 시 기존 첨부를 유지·삭제·추가하는 경로를 구현하고, 텍스트만 수정할 때 파일 교체를 강제하지 않도록 했다. Front #46은 학생 과제 상세/수정 화면에서 기존 첨부를 표시하고 제거할 수 있게 하며, 본문만 수정하는 저장 흐름도 사용자에게 자연스럽게 보이도록 다듬었다. 이 변경으로 학생은 제출 후 오타나 첨부 실수를 고칠 때 전체 제출을 다시 만들 필요 없이 필요한 첨부만 제거하거나 유지할 수 있다.

네 번째로 Q&A와 summary card UI의 상태 일관성을 보강했다. Backend #50은 닫힌 Q&A thread에 교수자가 추가 답변을 남기지 못하도록 차단하고 테스트로 잠갔다. Front #46은 교수 Q&A 답변 화면의 thread 종료 checkbox 배치를 정리하고, 닫힌 thread에서 추가 답변 UI가 남아 있는 문제를 함께 막았다. 동시에 dashboard/profile summary card는 label을 값 위에 배치하고 긴 텍스트·compact status wrapping을 개선해 좁은 화면에서도 정보가 덜 깨지도록 polish했다.

다섯 번째로 Service와 release PR들이 기능 조합을 demo 단위로 고정했다. Backend #47/Front #41/Service #26/#27은 출석 CSV export가 포함된 Backend v0.6.0, Front v0.6.0, Service v0.4.1 조합을 고정했다. 이어 Backend #51/Front #47/Service #28/#29는 과제 첨부 삭제와 닫힌 Q&A guard가 포함된 Backend v0.7.0, Front v0.6.1, Service v0.4.2 조합을 고정했다. 두 release line 모두 DB reset이 필요 없는 UI/API-only 변경으로 기록되어, demo 환경에서 재현할 수 있는 버전 조합이 명확해졌다.

마지막으로 docs #36, #37, #38이 교수 출석 CSV export scope, 과제 제출 API contract, 최종보고서 두 파일 산출물 구조를 main에 고정했다. 특히 docs #38은 보고서 본문과 부록만 열어도 화면·ERD·API·코드·DB 근거가 보이도록 최종보고서를 self-contained 구조로 재작성했다. 본 업데이트는 직전 작성 이후 추가로 merge된 assignment/Q&A/release PR까지 포함해, 이번 주 진행사항이 PR 번호 나열이 아니라 “무엇을 고쳤고 사용 흐름이 어떻게 달라졌는지”로 읽히도록 다시 정리한 것이다.

### 4.2 기능/문제 중심 상세 내용

| 구분 | 이번 주 진행 내용 | 고친 부분 / 구현 포인트 | 사용자에게 보이는 변화 | 근거 PR |
|---|---|---|---|---|
| 출석 안정성 | PresenceService 지연·장애 시 Backend 단일 worker가 같이 멈추는 문제를 완화 | DB session을 외부 wait 경로에서 조기 release, `/health`와 `/ready` 분리, pool timeout을 503 `DB_POOL_EXHAUSTED`로 구조화, WebSocket bootstrap을 느린 작업과 분리 | 출석 화면/체크인/실시간 roster 연결이 느린 presence 응답 때문에 전체적으로 멈추는 위험 감소 | Backend #48 |
| 교수 출석 CSV export | 교수자가 출석 현황을 요약본/전체본 CSV로 다운로드하는 기능 구현 | `attendance_summary_csv`, `attendance_full_csv`, legacy alias, UTF-8 BOM, variant filename, 공결 합산, 상태 라벨, 권한 검증 추가 | 교수 출석 페이지에서 학생별 누계를 확인하고 바로 CSV를 내려받을 수 있음 | Backend #49, Front #45 |
| 과제 제출 수정/첨부 삭제 | 학생 과제 재제출 시 기존 첨부를 유지·삭제·추가할 수 있도록 contract와 구현을 맞춤 | `remove_attachment_ids` 문서화, 현재 제출물 첨부만 제거 가능하도록 제약, 텍스트-only 수정 시 파일 교체 강제 제거, Backend/Frontend test 추가 | 학생이 과제 본문만 수정하거나 잘못 올린 첨부만 제거할 수 있음 | docs #37, Backend #50, Front #46 |
| Q&A 종료 상태 일관성 | 닫힌 Q&A thread에 추가 답변이 남는 상태 불일치를 차단 | Backend에서 closed thread 추가 답변 거부, Front에서 close-thread checkbox/UI 흐름 정리와 닫힌 thread 답변 방지 | 교수자가 Q&A를 종료하면 화면과 API가 같은 상태로 동작해 중복 답변 위험 감소 | Backend #50, Front #46 |
| UI polish / summary card | dashboard/profile summary card와 긴 텍스트/compact status 표시 개선 | label을 값 위에 배치, 긴 문구 wrapping, compact 상태 요소 visual polish | 좁은 화면에서 학생/교수 정보 카드와 상태 값이 더 읽기 쉬움 | Front #46 |
| release / demo manifest | 출석 CSV export와 과제/Q&A 보강이 포함된 Backend/Front 이미지를 demo stack manifest에 고정 | Backend v0.6.0/v0.7.0, Front v0.6.0/v0.6.1, Service v0.4.1/v0.4.2 digest pin; DB reset 불필요 명시 | 같은 manifest로 이번 주 기능 포함 demo 조합 재현 가능 | Backend #47/#51, Front #41/#47, Service #26/#27/#28/#29 |
| 문서/보고서 정렬 | 기능 요구사항, API contract, 보고서 증거를 최신 구현과 맞춤 | CSV export scope, assignment submission multipart field, self-contained final report, 두 파일 산출물 원칙 정리 | 교수님이 최종보고서에서 이번 주 개발 내용을 기능 변화와 문제 해결 과정으로 읽을 수 있음 | docs #36/#37/#38, 현재 보고서 작업 |
| 변화 없음으로 확인한 영역 | PresenceService, DB, CodexKit, DocsQuartz는 이번 주 보고 기간 안에 main merge PR 없음 | 기존 구현/ERD/test 근거는 유지하되 이번 주 신규 개발 성과로 과장하지 않음 | 완료도 평가는 기존 로컬 MVP 근거를 유지하고, 신규 변경 없음은 명확히 분리 | PR 없음 |

### 4.3 PR 추적 근거 표

아래 표는 위 자연어 설명의 추적 근거다. 평가자가 기능 변화를 먼저 읽고, 필요할 때 PR 번호와 개발 기간을 확인하는 용도다.

| Repo | PR | PR branch | 제목 | 개발 기간 산정(KST) | commits | merge commit | 보고서상 의미 |
|---|---:|---|---|---|---:|---|---|
| Backend | [#48](https://github.com/ChosunUniv2026Capstone/Backend/pull/48) | `feat/fix/db-pool-exhaustion-demo` | fix(backend): keep one-worker demo responsive under DB pressure | 2026-05-18 13:50 KST ~ 2026-05-20 11:37 KST | 3 | `f874e8a` | PresenceService 지연 시 DB pool 고갈·health/auth/bootstrap timeout·WebSocket 지연 위험 완화 |
| docs | [#36](https://github.com/ChosunUniv2026Capstone/docs/pull/36) | `docs/attendance-csv-export` | docs(attendance): align professor CSV export scope | 2026-05-22 00:46 KST ~ 2026-05-22 00:49 KST | 1 | `cef3c2f` | CSV export 요구사항·non-goal·UI 배치·object-storage 경로 문서 정렬 |
| Backend | [#49](https://github.com/ChosunUniv2026Capstone/Backend/pull/49) | `feat/attendance-csv-export` | feat(backend): let professors export attendance CSVs | 2026-05-22 00:46 KST ~ 2026-05-22 00:49 KST | 1 | `36e8524` | 교수 출석 요약본/전체본 CSV export API와 report-export 저장/다운로드 경로 구현 |
| Front | [#45](https://github.com/ChosunUniv2026Capstone/Front/pull/45) | `feat/attendance-csv-export` | feat(frontend): surface professor attendance CSV downloads | 2026-05-22 00:46 KST ~ 2026-05-22 00:49 KST | 1 | `73f5e09` | 교수 출석 화면에 학생별 누계 표와 CSV 다운로드 버튼 노출 |
| Backend | [#47](https://github.com/ChosunUniv2026Capstone/Backend/pull/47) | `release-please--branches--main` | chore(main): release 0.6.0 | 2026-05-22 00:50 KST ~ 2026-05-22 00:51 KST | 1 | `f06169e` | Backend #48/#49를 포함한 v0.6.0 release 고정 |
| Front | [#41](https://github.com/ChosunUniv2026Capstone/Front/pull/41) | `release-please--branches--main--components--smart-class-front` | chore(main): release smart-class-front 0.6.0 | 2026-05-22 00:50 KST ~ 2026-05-22 00:51 KST | 1 | `418ae29` | Front #45를 포함한 smart-class-front v0.6.0 release 고정 |
| Service | [#26](https://github.com/ChosunUniv2026Capstone/Service/pull/26) | `fix/attendance-csv-demo-release` | fix(service): pin attendance CSV demo manifest | 2026-05-22 00:56 KST ~ 2026-05-22 00:57 KST | 1 | `e89dcdb` | attendance CSV demo rollout용 Backend/Front image digest와 DB reset 불필요 조건 고정 |
| Service | [#27](https://github.com/ChosunUniv2026Capstone/Service/pull/27) | `release-please--branches--main` | chore(main): release 0.4.1 | 2026-05-22 00:58 KST ~ 2026-05-22 00:58 KST | 1 | `c36a432` | Service v0.4.1 release로 attendance CSV demo manifest 변경 고정 |
| docs | [#38](https://github.com/ChosunUniv2026Capstone/docs/pull/38) | `feat/final-report-writing-convention` | docs(reports): make final report self-contained | 2026-05-22 14:22 KST ~ 2026-05-22 14:25 KST | 1 | `615b8e0` | 최종보고서와 부록을 두 파일 산출물로 재구성하고 화면·ERD·API·코드·DB 근거를 본문에 직접 배치 |
| docs | [#37](https://github.com/ChosunUniv2026Capstone/docs/pull/37) | `docs/assignment-api-update` | docs(assignment): update assignment submission api fields | 2026-05-22 14:04 KST ~ 2026-05-22 15:45 KST | 2 | `90e62db` | `remove_attachment_ids`와 현재 제출물 첨부 제거 제약을 assignment submission contract에 반영 |
| Backend | [#50](https://github.com/ChosunUniv2026Capstone/Backend/pull/50) | `feat/assignment-qna-guard` | feat: support assignment attachment removal and block closed… | 2026-05-22 14:04 KST ~ 2026-05-22 15:49 KST | 2 | `95465c1` | 과제 첨부 유지·삭제·추가 재제출 경로와 닫힌 Q&A thread 추가 답변 차단 구현 |
| Front | [#46](https://github.com/ChosunUniv2026Capstone/Front/pull/46) | `fix/student-assignment-qna-ui` | fix: polish assignment, qna, and summary card UI | 2026-05-22 14:04 KST ~ 2026-05-22 15:57 KST | 2 | `0c555e0` | 과제 첨부 표시/삭제 UI, content-only 저장 흐름, Q&A 종료 UI, summary card readability 개선 |
| Backend | [#51](https://github.com/ChosunUniv2026Capstone/Backend/pull/51) | `release-please--branches--main` | chore(main): release 0.7.0 | 2026-05-22 15:49 KST ~ 2026-05-22 16:16 KST | 1 | `9e8ba35` | Backend #50을 포함한 v0.7.0 release 고정 |
| Front | [#47](https://github.com/ChosunUniv2026Capstone/Front/pull/47) | `release-please--branches--main--components--smart-class-front` | chore(main): release smart-class-front 0.6.1 | 2026-05-22 15:57 KST ~ 2026-05-22 16:16 KST | 1 | `a2b1b8f` | Front #46을 포함한 smart-class-front v0.6.1 release 고정 |
| Service | [#28](https://github.com/ChosunUniv2026Capstone/Service/pull/28) | `fix/assignment-attachment-demo-release` | fix(service): pin assignment workflow demo release | 2026-05-22 16:19 KST ~ 2026-05-22 16:20 KST | 1 | `7b934a3` | assignment attachment removal/closed-Q&A fixes가 포함된 Backend/Front image digest를 Service v0.4.2 manifest에 고정 |
| Service | [#29](https://github.com/ChosunUniv2026Capstone/Service/pull/29) | `release-please--branches--main` | chore(main): release 0.4.2 | 2026-05-22 16:20 KST ~ 2026-05-22 16:21 KST | 1 | `290820f` | Service v0.4.2 release로 assignment workflow demo manifest 변경 고정 |

## 5. 검증 경계와 caveat

- Backend / PresenceService Python 테스트는 `PYTHONPATH=. pytest -q` 형태를 기준으로 기록한다. plain `pytest -q`는 import path 문제로 실패할 수 있으므로 실패 자체를 기능 실패로 과장하지 않는다.
- PresenceService 테스트 통과 시에도 Pydantic alias 관련 warning은 주의 항목으로 분리한다.
- OpenWrt / 교내 Wi-Fi 장기 현장 검증, 상용 운영 배포, 학사시스템 정식 연동, 네이티브 모바일 앱은 완료 성과가 아니라 한계 또는 후속 과제로 기록한다.
- `Service` image manifest / compose 검증은 실행 가능성 근거이지만, workflow run 또는 demo server provenance 없이는 상용 배포 근거가 아니다.

## 6. 기능별 종합 증거 매트릭스

| Evidence ID | 기능 영역 | 완료도 | 화면 근거 | API / 코드 근거 | DB 근거 | 테스트 / 실행 근거 | 한계 / 후속 과제 |
|---|---|---|---|---|---|---|---|
| E-AUTH-01 | 인증 / 세션 | 로컬 MVP 완료 | Fig. 1-6 주요 영역: 로그인, 실패, 권한거부, 역할별 대시보드 | `Backend/app/main.py:920` login, `:961` refresh, `:1054` bootstrap, `:1070` logout; `Front/src/api.ts`; `Front/src/router.ts` | `DB/postgres/init/010_seed.sql` seed users, `refresh_sessions` | `Backend/tests/test_presence_admin_and_auth.py:218`, `:590`, `:683`; `Front/tests/e2e/auth-routing.spec.ts:584` | 운영 SSO/학사 인증 연동은 후속 과제 |
| E-UI-01 | 역할별 Front UI | 로컬 MVP 완료 | Fig. 4-55 주요 영역(역할별 UI 전체; Fig. 56은 N/A) | `Front/src/router.ts`, `Front/src/App.tsx`, `Front/src/api.ts`; weekly merged PR Front #46 (`0c555e0`) | 역할/수강/강의 seed tables | `Front/tests/e2e/auth-routing.spec.ts:584`, `selected-lms-subset.spec.ts:55`, `exam-workflow.spec.ts:244`; PR #46 manual/docker-build evidence | Fig. 56 OpenWrt router registration/token 화면은 N/A로 API/DB/Service 근거 대체 |
| E-LMS-01 | 강의 / 공지 / 과제 / Q&A / selected LMS read model | 로컬 MVP 완료 | Fig. 8-16, 26-35 주요 영역; 과제/Q&A UI 변경은 Fig. 12-16/35 계열 화면과 weekly PR evidence로 추적 | `Backend/app/main.py:1102-1456`, `:1785-1843`; `Backend/app/assignments.py`; `Backend/app/lms_selected.py`; `Front/src/App.tsx`; `Front/src/api.ts` | `courses`, `course_enrollments`, `notices`, `learning_items`, `assignments`, `assignment_submissions`, `assignment_submission_attachments`, `course_qna_threads`, `course_qna_posts`, `learning_progress` | `Backend/tests/test_lms_selected_subset.py:123`, `:172`, `:200`; `Backend/tests/test_assignment_contract.py`; `Front/tests/e2e/assignment-workflow.spec.ts`; `Front/tests/e2e/selected-lms-subset.spec.ts`; weekly merged PRs docs #37, Backend #50, Front #46 (`90e62db`, `95465c1`, `0c555e0`) | selected-LMS 추가 화면 캡처 완료; 운영 데이터 다양화는 후속 과제 |
| E-ATT-01 | 출석 workflow | 로컬 MVP 완료 | Fig. 17-20, 40-47 주요 영역 | `Backend/app/attendance.py`; `Backend/app/main.py:2030-2367`; WebSocket `/ws/attendance` | `attendance_sessions`, `attendance_session_slots`, `attendance_records`, `attendance_status_audit_logs`, `report_exports` | `Backend/tests/test_attendance_realtime.py:226`, `:369`, `:405`, `:498`, `:593`, `:1030`; weekly merged PRs Backend #48/#49 (`f874e8a`, `36e8524`) | 장기 교실 현장 검증은 후속 과제 |
| E-EXAM-01 | 객관식 시험 workflow | 로컬 MVP 완료 | Fig. 21-25, 36-39 주요 영역 | `Backend/app/main.py:1469-1710`; `Front/tests/e2e/exam-workflow.spec.ts` | `exams`, `exam_questions`, `exam_question_options`, `exam_submissions`, `exam_submission_answers` | `Backend/tests/test_exam_contract_alignment.py:147`, `:208`, `:261`, `:294`; `Front/tests/e2e/exam-workflow.spec.ts:244` | 서술형/파일형 시험과 대규모 부정행위 대응은 후속 과제 |
| E-PRES-01 | PresenceService eligibility / collector / demo overlay | 로컬 MVP 완료 | Fig. 18, 49-55 주요 영역; Fig. 56 N/A | `PresenceService/app/main.py:45`, `:64`, `:88`, `:100-125`; `Service/openwrt/presence-collector.sh`; Backend registry endpoints `Backend/app/main.py:1990-2027` | `classroom_networks`, `access_points`, `access_point_interfaces`, `registered_devices`, `presence_eligibility_logs` | `PresenceService/tests/test_service.py:136`, `:153`, `:203`, `:296`, `:347`, `:652`; `test_registry.py:29` | dummy overlay는 실 OpenWrt 장기 검증을 대체하지 않음 |
| E-DB-01 | DB schema / seed / ERD | 로컬 MVP 완료 | ERD-1 portrait overview + ERD-2~ERD-8 ERD SVG | `DB/postgres/init/*.sql`, `DB/postgres/migrations/*.sql` | 전체 PostgreSQL schema 및 seed | `DB/postgres/tests/object_storage_triggers.sql`; Backend/Presence/Service tests가 schema 계약을 간접 검증 | ERD SVG는 보고서용 산출물이며 실제 운영 migration 로그는 후속 운영 검증에서 보강 |
| E-SVC-01 | Service runtime / CI-CD | 부분 완료 | Service runtime은 diagram/manifest 중심; UI 화면 아님 | `Service/compose.yml`, `compose.local.yml`, `compose.image.yml`, `nginx/local.conf`, `Service/manifests/releases/v0.4.1.yml`, `v0.4.2.yml`, workflows `ci.yml`, `deploy-demo.yml` | DB 직접 테이블 없음; `report_exports` 등 ops metadata는 ERD-8 | `Service/tests/test_release_manifest_contract.py:27`, `:45`; `test_workspace_release_readiness.py:81`, `:98`; weekly merged PRs Service #26/#27/#28/#29 (`e89dcdb`, `c36a432`, `7b934a3`, `290820f`) | workflow run / demo server provenance 없이는 상용 배포로 쓰지 않음 |
| E-DOC-01 | docs / report | 2파일 산출물 작성 완료 | 보고서/부록/증거 원장 갱신 | `docs/04-architecture/assignment-workflow-api.md`; `docs/08-reports/99-combined-report.md`; `docs/08-reports/99-combined-report-appendix.md` | N/A | docs #36/#37/#38 merged evidence와 `9c33d29`~`a675519` report asset/rendering follow-up; `git -C docs diff --check`, markdown/link sanity | 보고서 렌더링/asset 보정은 main 반영 완료이며 기능 구현 성과와 분리 |

# C. UI 사용 흐름 전체표

| 흐름 | 정확한 클릭/입력 경로 | 화면에서 확인할 것 | 관련 그림 |
|---|---|---|---|
| 공통 로그인 | 브라우저에서 `/login` 또는 `/` 접속 → 아이디 입력칸 클릭 → `20201239`, `PRF002`, `ADM001` 중 하나 입력 → 비밀번호 `devpass123` 입력 → `로그인` 버튼 클릭 | 역할별 dashboard로 이동하고 상단 사용자 정보와 강의/관리 카드가 보인다. | Fig. 1, 4, 5, 6 |
| 학생 단말 관리 | 학생 로그인 → 상단/프로필 진입 → `/profile` → 단말 MAC 입력 영역 또는 등록 단말 목록 확인 → 추가/삭제 버튼 사용 | 등록 단말 목록이 출석/시험 eligibility의 기초 근거가 된다. | Fig. 7 |
| 학생 강의·공지 확인 | 학생 로그인 → 대시보드 강의 카드 `Capstone Design A` 클릭 → 강의 홈 → `공지` 탭 클릭 → 공지 row 클릭 | 강의 홈, 공지 목록, 공지 상세가 순서대로 표시된다. | Fig. 8, 10, 11 |
| 학생 과제 제출/피드백 확인 | 학생 로그인 → 강의 카드 클릭 → `과제` 탭 클릭 → 과제 카드의 `상세 보기` 클릭 → 제출 본문/첨부 영역 확인 → `/lms` 탭에서 성적·피드백 확인 | 과제 상태, 제출 본문, 채점 점수/피드백이 이어진다. | Fig. 12, 13, 14 |
| 학생 학습 진도/Q&A | 학생 로그인 → 강의 상세 → `LMS` 탭 클릭 → `학습 진도율` 입력 후 저장 → `질문게시판·문의` 입력/상태 확인 | 진도율과 Q&A thread 상태가 저장/표시된다. | Fig. 15, 16 |
| 학생 스마트 출석 | 학생 로그인 → 강의 상세 → `출석` 탭 클릭 → eligibility 카드 확인 → 교수가 연 smart session 카드에서 `출석` 버튼 클릭 | registered device/AP/RSSI 근거가 만족되면 출석 결과 카드와 학기 matrix에 반영된다. | Fig. 17, 18, 19, 20 |
| 학생 시험 응시 | 학생 로그인 → 강의 상세 → `시험` 탭 클릭 → 시험 카드 클릭/응시 시작 → 객관식 보기 클릭 → 저장 상태 확인 → 제출 버튼 클릭 | 미응답이면 warning이 나오고, 제출 완료 시 결과 카드가 표시된다. | Fig. 21, 22, 23, 24, 25 |
| 교수 공지/자료 관리 | 교수 로그인 → 담당 강의 카드 클릭 → `공지` 또는 `강의 운영` 탭 클릭 → 제목/본문 입력 → 저장 버튼 클릭 | 교수용 공지 목록과 작성 form이 표시된다. | Fig. 26, 27, 28, 29 |
| 교수 과제/성적/Q&A 관리 | 교수 로그인 → 강의 상세 → `과제` 탭 클릭 → 과제 등록/제출 현황 확인 → 학생 제출 선택 → 점수/피드백 입력 후 저장 → `LMS` 탭에서 성적/진도/Q&A 확인 | 과제 등록, 제출 검토, 채점, 성적/진도/Q&A 응답 흐름이 보인다. | Fig. 30, 31, 32, 33, 34, 35 |
| 교수 시험 운영 | 교수 로그인 → 강의 상세 → `시험` 탭 클릭 → 시험 작성/상세 이동 → 게시 버튼 클릭 → 필요 시 종료 버튼 클릭 | 시험 상태 pill, 문제 목록, 게시/종료 결과가 표시된다. | Fig. 36, 37, 38, 39 |
| 교수 출석 운영 | 교수 로그인 → 강의 상세 → `출석` 탭 클릭 → timeline에서 차시 선택 → 출석 열기 modal에서 일반/스마트/휴강 선택 → timer/roster 이동 → 학생 상태 radio와 사유 입력 후 저장 → 이력 확인 | bundle session, timer, roster, slot exception, 저장 결과, immutable audit history가 표시된다. | Fig. 40, 41, 42, 43, 44, 45, 46, 47 |
| 서비스관리자 네트워크/재실성 운영 | 관리자 로그인 → dashboard → 사용자/강의실/네트워크 탭 이동 → AP mapping/station/threshold 확인 → demo overlay control에서 값을 바꾼 뒤 적용/초기화 클릭 | 강의실/AP 매핑, observed station, demo overlay 적용/초기화 결과, real/demo snapshot 분리가 보인다. | Fig. 48, 49-55 |

# D. 전체 화면 캡처 및 주요 영역 갤러리

모든 그림은 원본 PNG와 주요 영역을 표시한 화면 캡처를 함께 둔다. 보고서 본문에서 특정 기능을 설명할 때는 이 부록의 그림 번호를 그대로 사용한다.

## Fig. 1 — login form and service title


<figure class="figure screenshot"><img src="assets/screenshots/final/html-redbox/fig-1-01-login-redbox.png" alt="Fig. 1 — 로그인 화면과 서비스 제목"><figcaption>Fig. 1 — 로그인 화면과 서비스 제목</figcaption></figure>

## Fig. 2 — inline login failure banner


<figure class="figure screenshot"><img src="assets/screenshots/final/html-redbox/fig-2-common-02-login-failure-redbox.png" alt="Fig. 2 — 로그인 실패 안내 배너"><figcaption>Fig. 2 — 로그인 실패 안내 배너</figcaption></figure>

## Fig. 3 — authorization denied message


<figure class="figure screenshot"><img src="assets/screenshots/final/html-redbox/fig-3-common-03-authorization-denied-redbox.png" alt="Fig. 3 — 권한 없는 경로 접근 안내"><figcaption>Fig. 3 — 권한 없는 경로 접근 안내</figcaption></figure>

## Fig. 4 — student course cards and account summary


<figure class="figure screenshot"><img src="assets/screenshots/final/html-redbox/fig-4-student-01-dashboard-redbox.png" alt="Fig. 4 — 학생 대시보드의 강의 카드와 계정 요약"><figcaption>Fig. 4 — 학생 대시보드의 강의 카드와 계정 요약</figcaption></figure>

## Fig. 5 — professor course cards


<figure class="figure screenshot"><img src="assets/screenshots/final/html-redbox/fig-5-professor-01-dashboard-redbox.png" alt="Fig. 5 — 교수 대시보드의 담당 강의 카드"><figcaption>Fig. 5 — 교수 대시보드의 담당 강의 카드</figcaption></figure>

## Fig. 6 / Fig. 48 — admin user table and role column


<figure class="figure screenshot"><img src="assets/screenshots/final/html-redbox/fig-6-fig-48-admin-01-users-redbox.png" alt="Fig. 6 / Fig. 48 — 관리자 사용자 목록과 역할 컬럼"><figcaption>Fig. 6 / Fig. 48 — 관리자 사용자 목록과 역할 컬럼</figcaption></figure>

## Fig. 7 — registered device list and controls


<figure class="figure screenshot"><img src="assets/screenshots/final/html-redbox/fig-7-student-02-profile-devices-redbox.png" alt="Fig. 7 — 학생 등록 단말 목록과 관리 버튼"><figcaption>Fig. 7 — 학생 등록 단말 목록과 관리 버튼</figcaption></figure>

## Fig. 8 — course header and student tabs


<figure class="figure screenshot"><img src="assets/screenshots/final/html-redbox/fig-8-student-03-course-home-redbox.png" alt="Fig. 8 — 학생 강의 홈 헤더와 탭 구조"><figcaption>Fig. 8 — 학생 강의 홈 헤더와 탭 구조</figcaption></figure>

## Fig. 9 — learning item cards and download area


<figure class="figure screenshot"><img src="assets/screenshots/final/html-redbox/fig-9-student-04-learning-content-redbox.png" alt="Fig. 9 — 학습자료 카드와 다운로드 영역"><figcaption>Fig. 9 — 학습자료 카드와 다운로드 영역</figcaption></figure>

## Fig. 10 — notice list row and navigation


<figure class="figure screenshot"><img src="assets/screenshots/final/html-redbox/fig-10-student-05-notices-redbox.png" alt="Fig. 10 — 공지 목록 행과 상세 이동"><figcaption>Fig. 10 — 공지 목록 행과 상세 이동</figcaption></figure>

## Fig. 11 — notice title, body, and metadata


<figure class="figure screenshot"><img src="assets/screenshots/final/html-redbox/fig-11-student-06-notice-detail-redbox.png" alt="Fig. 11 — 공지 제목·본문·작성 메타데이터"><figcaption>Fig. 11 — 공지 제목·본문·작성 메타데이터</figcaption></figure>

## Fig. 12 — assignment card, status, and detail action


<figure class="figure screenshot"><img src="assets/screenshots/final/html-redbox/fig-12-student-14-assignment-list-redbox.png" alt="Fig. 12 — 과제 카드의 제출 상태와 상세 이동"><figcaption>Fig. 12 — 과제 카드의 제출 상태와 상세 이동</figcaption></figure>

## Fig. 13 — submission body, attachment area, and current feedback


<figure class="figure screenshot"><img src="assets/screenshots/final/html-redbox/fig-13-student-15-assignment-detail-redbox.png" alt="Fig. 13 — 과제 제출 본문, 첨부 영역, 피드백"><figcaption>Fig. 13 — 과제 제출 본문, 첨부 영역, 피드백</figcaption></figure>

## Fig. 14 — grade and feedback summary card


<figure class="figure screenshot"><img src="assets/screenshots/final/html-redbox/fig-14-student-16-grade-feedback-redbox.png" alt="Fig. 14 — 성적과 피드백 요약 카드"><figcaption>Fig. 14 — 성적과 피드백 요약 카드</figcaption></figure>

## Fig. 15 — learning progress input and save action


<figure class="figure screenshot"><img src="assets/screenshots/final/html-redbox/fig-15-student-17-learning-progress-redbox.png" alt="Fig. 15 — 학습 진도 입력과 저장 동작"><figcaption>Fig. 15 — 학습 진도 입력과 저장 동작</figcaption></figure>

## Fig. 16 — Q&A form and thread status


<figure class="figure screenshot"><img src="assets/screenshots/final/html-redbox/fig-16-student-18-qna-redbox.png" alt="Fig. 16 — Q&amp;A 작성 폼과 thread 상태"><figcaption>Fig. 16 — Q&amp;A 작성 폼과 thread 상태</figcaption></figure>

## Fig. 17 / Fig. 20 — attendance eligibility card and semester matrix


<figure class="figure screenshot"><img src="assets/screenshots/final/html-redbox/fig-17-fig-20-student-07-attendance-before-check-redbox.png" alt="Fig. 17 / Fig. 20 — 출석 가능 여부 카드와 학기 출석표"><figcaption>Fig. 17 / Fig. 20 — 출석 가능 여부 카드와 학기 출석표</figcaption></figure>

## Fig. 18 — eligible summary and evidence card


<figure class="figure screenshot"><img src="assets/screenshots/final/html-redbox/fig-18-student-08-eligibility-result-redbox.png" alt="Fig. 18 — 출석 가능 판정 결과와 근거 카드"><figcaption>Fig. 18 — 출석 가능 판정 결과와 근거 카드</figcaption></figure>

## Fig. 19 — bundle check-in result card


<figure class="figure screenshot"><img src="assets/screenshots/final/html-redbox/fig-19-student-09-check-in-result-redbox.png" alt="Fig. 19 — 묶음 출석 체크인 결과 카드"><figcaption>Fig. 19 — 묶음 출석 체크인 결과 카드</figcaption></figure>

## Fig. 21 — exam list card status and policy


<figure class="figure screenshot"><img src="assets/screenshots/final/html-redbox/fig-21-student-10-exam-list-redbox.png" alt="Fig. 21 — 학생 시험 목록의 상태와 정책"><figcaption>Fig. 21 — 학생 시험 목록의 상태와 정책</figcaption></figure>

## Fig. 22 — question prompt, options, countdown


<figure class="figure screenshot"><img src="assets/screenshots/final/html-redbox/fig-22-student-11-exam-taking-redbox.png" alt="Fig. 22 — 시험 응시 화면의 문항·선택지·타이머"><figcaption>Fig. 22 — 시험 응시 화면의 문항·선택지·타이머</figcaption></figure>

## Fig. 23 — selected option and save state


<figure class="figure screenshot"><img src="assets/screenshots/final/html-redbox/fig-23-student-12-exam-answer-selected-redbox.png" alt="Fig. 23 — 선택한 답안과 저장 상태"><figcaption>Fig. 23 — 선택한 답안과 저장 상태</figcaption></figure>

## Fig. 24 — missing-answer warning or submit guard state


<figure class="figure screenshot"><img src="assets/screenshots/final/html-redbox/fig-24-student-19-exam-missing-answer-warning-redbox.png" alt="Fig. 24 — 미응답 문항 제출 방지 안내"><figcaption>Fig. 24 — 미응답 문항 제출 방지 안내</figcaption></figure>

## Fig. 25 — submission completion status


<figure class="figure screenshot"><img src="assets/screenshots/final/html-redbox/fig-25-student-13-exam-submit-result-redbox.png" alt="Fig. 25 — 시험 제출 완료 결과"><figcaption>Fig. 25 — 시험 제출 완료 결과</figcaption></figure>

## Fig. P2 — professor profile summary


<figure class="figure screenshot"><img src="assets/screenshots/final/html-redbox/fig-p2-professor-02-profile-redbox.png" alt="Fig. P2 — 교수 프로필 요약"><figcaption>Fig. P2 — 교수 프로필 요약</figcaption></figure>

## Fig. 26 — professor course header and action tabs


<figure class="figure screenshot"><img src="assets/screenshots/final/html-redbox/fig-26-professor-03-course-home-redbox.png" alt="Fig. 26 — 교수 강의 홈과 운영 탭"><figcaption>Fig. 26 — 교수 강의 홈과 운영 탭</figcaption></figure>

## Fig. 27 — material upload/create controls


<figure class="figure screenshot"><img src="assets/screenshots/final/html-redbox/fig-27-professor-04-learning-content-manage-redbox.png" alt="Fig. 27 — 교수 학습자료 업로드·생성 controls"><figcaption>Fig. 27 — 교수 학습자료 업로드·생성 controls</figcaption></figure>

## Fig. 28 — professor notice list


<figure class="figure screenshot"><img src="assets/screenshots/final/html-redbox/fig-28-professor-05-notices-redbox.png" alt="Fig. 28 — 교수 공지 목록"><figcaption>Fig. 28 — 교수 공지 목록</figcaption></figure>

## Fig. 29 — notice form and submit action


<figure class="figure screenshot"><img src="assets/screenshots/final/html-redbox/fig-29-professor-06-course-manage-notice-form-redbox.png" alt="Fig. 29 — 교수 공지 작성 폼과 저장 동작"><figcaption>Fig. 29 — 교수 공지 작성 폼과 저장 동작</figcaption></figure>

## Fig. 30 — assignment creation/list management area


<figure class="figure screenshot"><img src="assets/screenshots/final/html-redbox/fig-30-professor-17-assignment-create-redbox.png" alt="Fig. 30 — 과제 생성과 과제 목록 관리 영역"><figcaption>Fig. 30 — 과제 생성과 과제 목록 관리 영역</figcaption></figure>

## Fig. 31 — submission roster and selected student detail


<figure class="figure screenshot"><img src="assets/screenshots/final/html-redbox/fig-31-professor-18-submission-review-redbox.png" alt="Fig. 31 — 제출자 목록과 선택 학생 제출 상세"><figcaption>Fig. 31 — 제출자 목록과 선택 학생 제출 상세</figcaption></figure>

## Fig. 32 — score/status/feedback grading controls


<figure class="figure screenshot"><img src="assets/screenshots/final/html-redbox/fig-32-professor-19-assignment-grading-redbox.png" alt="Fig. 32 — 점수·상태·피드백 채점 controls"><figcaption>Fig. 32 — 점수·상태·피드백 채점 controls</figcaption></figure>

## Fig. 33 — student grade rows and average percent


<figure class="figure screenshot"><img src="assets/screenshots/final/html-redbox/fig-33-professor-20-grade-overview-redbox.png" alt="Fig. 33 — 학생별 성적 행과 평균 비율"><figcaption>Fig. 33 — 학생별 성적 행과 평균 비율</figcaption></figure>

## Fig. 34 — student-by-material learning progress table


<figure class="figure screenshot"><img src="assets/screenshots/final/html-redbox/fig-34-professor-21-learning-progress-redbox.png" alt="Fig. 34 — 학습자료별 학생 진도 표"><figcaption>Fig. 34 — 학습자료별 학생 진도 표</figcaption></figure>

## Fig. 35 — answer textarea, close checkbox, and save action


<figure class="figure screenshot"><img src="assets/screenshots/final/html-redbox/fig-35-professor-22-qna-answer-redbox.png" alt="Fig. 35 — Q&amp;A 답변 입력, 종료 여부, 저장 동작"><figcaption>Fig. 35 — Q&amp;A 답변 입력, 종료 여부, 저장 동작</figcaption></figure>

## Fig. 36 — exam draft/list management card


<figure class="figure screenshot"><img src="assets/screenshots/final/html-redbox/fig-36-professor-07-exam-manage-redbox.png" alt="Fig. 36 — 시험 초안과 목록 관리 카드"><figcaption>Fig. 36 — 시험 초안과 목록 관리 카드</figcaption></figure>

## Fig. 37 — exam policy and question list


<figure class="figure screenshot"><img src="assets/screenshots/final/html-redbox/fig-37-professor-08-exam-detail-redbox.png" alt="Fig. 37 — 시험 정책과 문항 목록"><figcaption>Fig. 37 — 시험 정책과 문항 목록</figcaption></figure>

## Fig. 38 — exam publish status result


<figure class="figure screenshot"><img src="assets/screenshots/final/html-redbox/fig-38-professor-16-exam-publish-result-redbox.png" alt="Fig. 38 — 시험 게시 후 상태 결과"><figcaption>Fig. 38 — 시험 게시 후 상태 결과</figcaption></figure>

## Fig. 39 — exam close result status


<figure class="figure screenshot"><img src="assets/screenshots/final/html-redbox/fig-39-professor-15-exam-close-result-redbox.png" alt="Fig. 39 — 시험 종료 후 상태 결과"><figcaption>Fig. 39 — 시험 종료 후 상태 결과</figcaption></figure>

## Fig. 40 — weekly attendance timeline rows


<figure class="figure screenshot"><img src="assets/screenshots/final/html-redbox/fig-40-professor-09-attendance-timeline-redbox.png" alt="Fig. 40 — 주차별 출석 timeline"><figcaption>Fig. 40 — 주차별 출석 timeline</figcaption></figure>

## Fig. 41 — attendance start modal mode options


<figure class="figure screenshot"><img src="assets/screenshots/final/html-redbox/fig-41-professor-23-attendance-start-modal-redbox.png" alt="Fig. 41 — 출석 시작 modal의 운영 모드 선택"><figcaption>Fig. 41 — 출석 시작 modal의 운영 모드 선택</figcaption></figure>

## Fig. 42 — smart attendance timer and close button


<figure class="figure screenshot"><img src="assets/screenshots/final/html-redbox/fig-42-professor-11-attendance-timer-redbox.png" alt="Fig. 42 — 스마트 출석 timer와 종료 버튼"><figcaption>Fig. 42 — 스마트 출석 timer와 종료 버튼</figcaption></figure>

## Fig. 43 — student status table and reason inputs


<figure class="figure screenshot"><img src="assets/screenshots/final/html-redbox/fig-43-professor-12-attendance-roster-redbox.png" alt="Fig. 43 — 학생 출석 상태 표와 사유 입력"><figcaption>Fig. 43 — 학생 출석 상태 표와 사유 입력</figcaption></figure>

## Fig. 44 — slot-specific roster controls


<figure class="figure screenshot"><img src="assets/screenshots/final/html-redbox/fig-44-professor-13-attendance-slot-roster-redbox.png" alt="Fig. 44 — 차시별 출석 roster controls"><figcaption>Fig. 44 — 차시별 출석 roster controls</figcaption></figure>

## Fig. 45 — save success and updated status row


<figure class="figure screenshot"><img src="assets/screenshots/final/html-redbox/fig-45-professor-14-attendance-edit-save-result-redbox.png" alt="Fig. 45 — 출석 저장 성공과 갱신된 상태 행"><figcaption>Fig. 45 — 출석 저장 성공과 갱신된 상태 행</figcaption></figure>

## Fig. 46 — student stats table and CSV buttons


<figure class="figure screenshot"><img src="assets/screenshots/final/html-redbox/fig-46-professor-10-attendance-student-stats-redbox.png" alt="Fig. 46 — 학생별 출석 통계 표와 CSV 버튼"><figcaption>Fig. 46 — 학생별 출석 통계 표와 CSV 버튼</figcaption></figure>

## Fig. 47 — immutable attendance audit history list


<figure class="figure screenshot"><img src="assets/screenshots/final/html-redbox/fig-47-professor-24-attendance-history-redbox.png" alt="Fig. 47 — 변경 불가능한 출석 감사 이력"><figcaption>Fig. 47 — 변경 불가능한 출석 감사 이력</figcaption></figure>

## Fig. 49 / Fig. 50 / Fig. 51 — classroom/AP mapping, station list, threshold controls


<figure class="figure screenshot"><img src="assets/screenshots/final/html-redbox/fig-49-fig-50-fig-51-admin-02-classrooms-networks-redbox.png" alt="Fig. 49 / Fig. 50 / Fig. 51 — 강의실·AP 매핑, 관측 단말, 임계값 관리"><figcaption>Fig. 49 / Fig. 50 / Fig. 51 — 강의실·AP 매핑, 관측 단말, 임계값 관리</figcaption></figure>

## Fig. 52 — demo source label and overlay controls


<figure class="figure screenshot"><img src="assets/screenshots/final/html-redbox/fig-52-admin-03-presence-demo-control-redbox.png" alt="Fig. 52 — 재실성 demo source와 overlay controls"><figcaption>Fig. 52 — 재실성 demo source와 overlay controls</figcaption></figure>

## Fig. 53 — applied overlay station state


<figure class="figure screenshot"><img src="assets/screenshots/final/html-redbox/fig-53-admin-04-presence-demo-applied-redbox.png" alt="Fig. 53 — 적용된 demo overlay 단말 상태"><figcaption>Fig. 53 — 적용된 demo overlay 단말 상태</figcaption></figure>

## Fig. 54 — reset result and restored baseline


<figure class="figure screenshot"><img src="assets/screenshots/final/html-redbox/fig-54-admin-05-presence-demo-reset-result-redbox.png" alt="Fig. 54 — demo 초기화 결과와 기준 상태 복원"><figcaption>Fig. 54 — demo 초기화 결과와 기준 상태 복원</figcaption></figure>

## Fig. 55 — real/demo snapshot separation labels


<figure class="figure screenshot"><img src="assets/screenshots/final/html-redbox/fig-55-admin-06-real-vs-demo-snapshots-redbox.png" alt="Fig. 55 — real snapshot과 demo snapshot 구분"><figcaption>Fig. 55 — real snapshot과 demo snapshot 구분</figcaption></figure>

## Fig. 56 — OpenWrt router registration/token N/A

현재 Front main에는 전용 router registration/token UI가 없다. 이 기능은 Backend AP registry endpoints, DB `access_points/access_point_interfaces`, Service OpenWrt collector script로 근거를 대체하며, 운영 UI는 향후 과제로 분리한다.

# E. ERD 전체/부분 갤러리

## ERD-1 — Full Smart Class PostgreSQL ERD

- 구성: 세로 1쪽 전체 overview
- 강조 대상: LMS + presence/attendance + assessment + assignment + object-storage domains
- 포함 범위: 전체 34개 schema table과 54개 FK link

<figure class="figure diagram full-erd"><img src="assets/diagrams/final/html-redbox/erd-1-full-smart-class-erd-redbox.png" alt="ERD-1 portrait overview"><figcaption>ERD-1 portrait overview</figcaption></figure>

## ERD-2 — User / auth / registered-device ERD

- 강조 대상: users.id relationships to sessions/devices
- 포함 테이블/노드: users, refresh_sessions, registered_devices

<figure class="figure diagram"><img src="assets/diagrams/final/html-redbox/erd-2-user-auth-device-redbox.png" alt="ERD-2"><figcaption>ERD-2</figcaption></figure>

<figure class="figure diagram"><img src="assets/diagrams/final/html-redbox/erd-2-user-auth-device-redbox.png" alt="ERD-2"><figcaption>ERD-2</figcaption></figure>

## ERD-3 — Course / enrollment / notice / material ERD

- 강조 대상: course ownership/enrollment and attachment relations
- 포함 테이블/노드: courses, course_enrollments, course_schedules, notices, learning_items, learning_item_attachments, notice_attachments

<figure class="figure diagram"><img src="assets/diagrams/final/html-redbox/erd-3-course-enrollment-notice-material-redbox.png" alt="ERD-3"><figcaption>ERD-3</figcaption></figure>

<figure class="figure diagram"><img src="assets/diagrams/final/html-redbox/erd-3-course-enrollment-notice-material-redbox.png" alt="ERD-3"><figcaption>ERD-3</figcaption></figure>

## ERD-4 — Device / classroom / AP / presence ERD

- 강조 대상: classroom network mapping and AP registry evidence
- 포함 테이블/노드: classrooms, classroom_networks, access_points, access_point_interfaces, registered_devices, presence_eligibility_logs

<figure class="figure diagram"><img src="assets/diagrams/final/html-redbox/erd-4-device-classroom-ap-presence-redbox.png" alt="ERD-4"><figcaption>ERD-4</figcaption></figure>

<figure class="figure diagram"><img src="assets/diagrams/final/html-redbox/erd-4-device-classroom-ap-presence-redbox.png" alt="ERD-4"><figcaption>ERD-4</figcaption></figure>

## ERD-5 — Attendance session / record / audit ERD

- 강조 대상: bundle parent, slot fan-out, record/audit history
- 포함 테이블/노드: attendance_sessions, attendance_session_slots, attendance_records, attendance_status_audit_logs, users, courses, classrooms

<figure class="figure diagram"><img src="assets/diagrams/final/html-redbox/erd-5-attendance-session-record-audit-redbox.png" alt="ERD-5"><figcaption>ERD-5</figcaption></figure>

<figure class="figure diagram"><img src="assets/diagrams/final/html-redbox/erd-5-attendance-session-record-audit-redbox.png" alt="ERD-5"><figcaption>ERD-5</figcaption></figure>

## ERD-6 — Exam / question / submission / answer ERD

- 강조 대상: exam-question-option and submission-answer consistency
- 포함 테이블/노드: exams, exam_questions, exam_question_options, exam_submissions, exam_submission_answers, exam_question_attachments, exam_answer_attachments

<figure class="figure diagram"><img src="assets/diagrams/final/html-redbox/erd-6-exam-question-submission-answer-redbox.png" alt="ERD-6"><figcaption>ERD-6</figcaption></figure>

<figure class="figure diagram"><img src="assets/diagrams/final/html-redbox/erd-6-exam-question-submission-answer-redbox.png" alt="ERD-6"><figcaption>ERD-6</figcaption></figure>

## ERD-7 — Selected LMS / assignment / Q&A / progress ERD

- 강조 대상: grading fields, Q&A threads/posts, progress ownership
- 포함 테이블/노드: assignments, assignment_submissions, assignment_submission_attachments, course_qna_threads, course_qna_posts, learning_progress, learning_items, users, courses

<figure class="figure diagram"><img src="assets/diagrams/final/html-redbox/erd-7-selected-lms-assignment-qna-progress-redbox.png" alt="ERD-7"><figcaption>ERD-7</figcaption></figure>

<figure class="figure diagram"><img src="assets/diagrams/final/html-redbox/erd-7-selected-lms-assignment-qna-progress-redbox.png" alt="ERD-7"><figcaption>ERD-7</figcaption></figure>

## ERD-8 — Service / ops metadata ERD and N/A boundary

- 강조 대상: report exports, object deletion outbox, Service runtime N/A boundary
- 포함 테이블/노드: report_exports, object_deletion_jobs, learning_item_attachments, notice_attachments, assignment_submission_attachments, Service runtime: N/A PostgreSQL entity

<figure class="figure diagram"><img src="assets/diagrams/final/html-redbox/erd-8-service-ops-metadata-redbox.png" alt="ERD-8"><figcaption>ERD-8</figcaption></figure>

<figure class="figure diagram"><img src="assets/diagrams/final/html-redbox/erd-8-service-ops-metadata-redbox.png" alt="ERD-8"><figcaption>ERD-8</figcaption></figure>

# F. API request/response 예시

# C.3 대표 request/response 예시

아래 JSON 응답의 datetime 값은 API 직렬화 형식을 보여주기 위해 ISO 8601 offset 예시를 사용한다.

## C.3.1 인증 로그인

**Request**

```http
POST /api/auth/login
Content-Type: application/json

{
  "login_id": "20201239",
  "password": "devpass123"
}
```

**Response**

```json
{
  "success": true,
  "data": {
    "access_token": "<jwt>",
    "token_type": "bearer",
    "expires_at": "2026-05-22T02:30:00+09:00",
    "user": {
      "id": 1,
      "login_id": "20201239",
      "role": "student",
      "name": "Demo Student"
    },
    "route_access": {
      "dashboard": true,
      "student_courses": true
    },
    "refresh_expires_at": "2026-05-29T02:00:00+09:00"
  },
  "message": "ok",
  "meta": {
    "refresh_cookie_name": "smart_class_refresh",
    "access_cookie_name": "smart_class_access",
    "legacy_dev_token_enabled": false
  },
  "access_token": "<jwt>",
  "user": {
    "id": 1,
    "login_id": "20201239",
    "role": "student",
    "name": "Demo Student"
  }
}
```

근거: `Backend/app/main.py:920`, `Backend/tests/test_presence_admin_and_auth.py:590`.

## C.3.2 출석 eligibility

**Request**

```http
POST /api/attendance/eligibility
Authorization: Bearer <student-access-token>
Content-Type: application/json

{
  "student_id": "20201239",
  "course_code": "CSE116"
}
```

**Response**

```json
{
  "success": true,
  "data": {
    "eligible": true,
    "reason_code": "OK",
    "matched_device_mac": "AA:BB:CC:DD:EE:FF",
    "observed_at": "2026-05-22T00:49:00+09:00",
    "snapshot_age_seconds": 4,
    "evidence": {
      "source": "demo-overlay",
      "ap_id": "b101-ap-1",
      "signal_dbm": -51,
      "threshold_dbm": -65
    }
  },
  "message": "ok",
  "meta": {}
}
```

근거: `Backend/app/main.py:2030`, `PresenceService/app/main.py:88`, `Backend/tests/test_presence_admin_and_auth.py:906`.

## C.3.3 교수 출석 CSV export

**Request**

```http
POST /api/professors/PRF002/courses/CSE116/attendance/report-exports
Authorization: Bearer <professor-access-token>
Content-Type: application/json

{
  "export_type": "attendance_summary_csv"
}
```

**Response**

```json
{
  "success": true,
  "data": {
    "id": 42,
    "original_filename": "attendance-summary-CSE116-20260522004900.csv",
    "mime_type": "text/csv; charset=utf-8",
    "file_size_bytes": 1234,
    "uploaded_at": "2026-05-22T00:49:00+09:00",
    "storage_provider": "local",
    "bucket_name": "smart-class",
    "export_type": "attendance_csv",
    "course_code": "CSE116",
    "status": "ready",
    "generated_at": "2026-05-22T00:49:00+09:00"
  },
  "message": "ok",
  "meta": {}
}
```

근거: `Backend/app/main.py:2093`, `:2106`, `:2117`, weekly Backend commit `36e8524`, Front commit `73f5e09`.

## C.3.4 학생 시험 시작 및 답안 저장

### 시험 시작

**Request**

```http
POST /api/students/20201239/courses/CSE116/exams/1/start
Authorization: Bearer <student-access-token>
```

**Response**

```json
{
  "success": true,
  "data": {
    "submission_id": 1001,
    "attempt_no": 1,
    "status": "in_progress",
    "started_at": "2026-05-22T02:00:00+09:00",
    "expires_at": "2026-05-22T02:30:00+09:00",
    "idempotent": false
  },
  "message": "ok",
  "meta": {}
}
```

### 답안 저장

**Request**

```http
PUT /api/students/20201239/courses/CSE116/exams/1/submissions/1001/answers/10
Authorization: Bearer <student-access-token>
Content-Type: application/json

{
  "selected_option_id": 44
}
```

**Response**

```json
{
  "success": true,
  "data": {
    "submission_id": 1001,
    "question_id": 10,
    "selected_option_id": 44,
    "answer_text": null,
    "answered_at": "2026-05-22T02:03:00+09:00"
  },
  "message": "ok",
  "meta": {}
}
```

근거: `Backend/app/main.py:1494`, `:1708`, `:1712`, `Backend/tests/test_exam_contract_alignment.py:261`, `Front/tests/e2e/exam-workflow.spec.ts:244`.

## C.3.5 selected LMS: Q&A / learning progress / grade feedback

### Q&A 질문 등록

**Request**

```http
POST /api/students/20201239/courses/CSE116/qna
Authorization: Bearer <student-access-token>
Content-Type: application/json

{
  "title": "과제 제출 형식 문의",
  "body": "첨부파일 형식 제한이 있나요?"
}
```

**Response**

```json
{
  "success": true,
  "data": {
    "id": 15,
    "student_id": "20201239",
    "student_name": "Demo Student",
    "title": "과제 제출 형식 문의",
    "body": "첨부파일 형식 제한이 있나요?",
    "status": "open",
    "created_at": "2026-05-22T02:04:00+09:00",
    "updated_at": "2026-05-22T02:04:00+09:00",
    "posts": [
      {
        "id": 31,
        "author_id": "20201239",
        "author_name": "Demo Student",
        "author_role": "student",
        "body": "첨부파일 형식 제한이 있나요?",
        "post_type": "question",
        "created_at": "2026-05-22T02:04:00+09:00"
      }
    ]
  },
  "message": "ok",
  "meta": {}
}
```

### 학습 진도 저장

**Request**

```http
PUT /api/students/20201239/courses/CSE116/learning-items/7/progress
Authorization: Bearer <student-access-token>
Content-Type: application/json

{
  "progress_percent": 80
}
```

**Response**

```json
{
  "success": true,
  "data": {
    "learning_item_id": 7,
    "learning_item_title": "1주차 요구사항 분석",
    "title": "1주차 요구사항 분석",
    "kind": "material",
    "student_id": "20201239",
    "student_name": "Demo Student",
    "progress_percent": 80,
    "status": "in_progress",
    "last_viewed_at": "2026-05-22T02:04:00+09:00",
    "completed_at": null,
    "updated_at": "2026-05-22T02:04:00+09:00"
  },
  "message": "ok",
  "meta": {}
}
```

### 성적·피드백 조회

**Request**

```http
GET /api/students/20201239/courses/CSE116/grades
Authorization: Bearer <student-access-token>
```

**Response**

```json
{
  "success": true,
  "data": {
    "course_code": "CSE116",
    "student_id": "20201239",
    "student_name": "Demo Student",
    "overall_percent": 92,
    "items": [
      {
        "type": "assignment",
        "item_type": "assignment",
        "assignment_id": 3,
        "item_id": 3,
        "title": "요구사항 분석 보고서",
        "score": 92,
        "max_score": 100,
        "percent": 92,
        "feedback": "요구사항 분석이 구체적입니다.",
        "grading_status": "published"
      }
    ],
    "assignments": [
      {
        "type": "assignment",
        "item_type": "assignment",
        "assignment_id": 3,
        "item_id": 3,
        "title": "요구사항 분석 보고서",
        "score": 92,
        "percent": 92,
        "max_score": 100,
        "grading_status": "published",
        "feedback": "요구사항 분석이 구체적입니다."
      }
    ],
    "exams": []
  },
  "message": "ok",
  "meta": {}
}
```

근거: `Backend/app/main.py:1282`, `:1315`, `:1384`, `Backend/app/lms_selected.py:143`, `:235`, `:308`, `Backend/tests/test_lms_selected_subset.py:123`, `:172`, `:200`.

## C.3.6 PresenceService collector snapshot ingest

**Request**

```http
POST /collector/aps/b101-ap-1/snapshot
Authorization: Bearer <collector-token>
X-Collector-Nonce: 20260615-b101-001
X-Collector-Timestamp: 2026-06-15T09:00:00Z
Content-Type: application/json

{
  "classroom_id": "B101",
  "interfaces": [
    {
      "interface_id": "wlan0",
      "stations": [
        {"mac": "AA:BB:CC:DD:EE:FF", "signal_dbm": -51, "connected": true}
      ]
    }
  ]
}
```

**Response**

```json
{
  "accepted": true,
  "collector_ap_id": "b101-ap-1",
  "stored_interfaces": 1,
  "stored_stations": 1
}
```

근거: `PresenceService/app/main.py:64`, `PresenceService/tests/test_service.py:296`, `DB/postgres/migrations/016_openwrt_collector_registry.sql`.


# G. 코드 근거 excerpt

## G.1 Front API request wrapper와 인증/세션 API

Source: `Front/src/api.ts:743-955`

```ts
0743: export function resolveBackendHttpBase(configuredUrl = import.meta.env.VITE_BACKEND_URL): string {
0744:   return (configuredUrl ?? '').trim().replace(/\/+$/, '')
0745: }
0746:
0747: type BrowserLocation = Pick<Location, 'protocol' | 'host'>
0748:
0749: export function resolveBackendWebSocketBase(
0750:   configuredUrl = import.meta.env.VITE_BACKEND_URL,
0751:   location: BrowserLocation = window.location,
0752: ): string {
0753:   const explicitBase = resolveBackendHttpBase(configuredUrl)
0754:   if (explicitBase) {
0755:     return explicitBase.replace(/^http:/, 'ws:').replace(/^https:/, 'wss:')
0756:   }
0757:
0758:   const protocol = location.protocol === 'https:' ? 'wss:' : 'ws:'
0759:   return `${protocol}//${location.host}`
0760: }
0761:
0762: export function buildAttendanceWebSocketUrl(
0763:   courseCode: string,
0764:   view: 'student' | 'professor',
0765:   configuredUrl = import.meta.env.VITE_BACKEND_URL,
0766:   location: BrowserLocation = window.location,
0767: ): string {
0768:   const params = new URLSearchParams({
0769:     courseCode,
0770:     view,
0771:   })
0772:   return `${resolveBackendWebSocketBase(configuredUrl, location)}/ws/attendance?${params.toString()}`
0773: }
0774:
0775: const API_BASE = resolveBackendHttpBase()
0776: let authFailureHandler: (() => void) | null = null
0777: let refreshPromise: Promise<LoginResponse> | null = null
0778:
0779: type RequestOptions = {
0780:   allowSessionRefresh?: boolean
0781:   suppressAuthFailureHandler?: boolean
0782: }
0783:
0784: export class ApiRequestError extends Error {
0785:   status: number
0786:   code?: string
0787:   details?: Record<string, unknown> | null
0788:
0789:   constructor(message: string, status: number, code?: string, details?: Record<string, unknown> | null) {
0790:     super(message)
0791:     this.name = 'ApiRequestError'
0792:     this.status = status
0793:     this.code = code
0794:     this.details = details ?? null
0795:   }
0796: }
0797:
0798: export function setAuthFailureHandler(handler: (() => void) | null) {
0799:   authFailureHandler = handler
0800: }
0801:
0802: function shouldTrySessionRefresh(path: string) {
0803:   return !['/api/auth/login', '/api/auth/refresh', '/api/auth/logout', '/api/auth/bootstrap', '/api/auth/me'].includes(path)
0804: }
0805:
0806: function requiresApiEnvelope(path: string) {
0807:   return path.startsWith('/api/')
0808: }
0809:
0810: async function requestInternal<T>(path: string, init?: RequestInit, options: RequestOptions = {}): Promise<T> {
0811:   const headers = new Headers(init?.headers ?? {})
0812:   if (!(init?.body instanceof FormData) && !headers.has('Content-Type')) {
0813:     headers.set('Content-Type', 'application/json')
0814:   }
0815:
0816:   const response = await fetch(`${API_BASE}${path}`, {
0817:     credentials: 'include',
0818:     headers,
0819:     ...init,
0820:   })
0821:
0822:   if (response.status === 401 && options.allowSessionRefresh !== false && shouldTrySessionRefresh(path)) {
0823:     try {
0824:       await refreshAccessToken()
0825:       return requestInternal<T>(path, init, {
0826:         ...options,
0827:         allowSessionRefresh: false,
0828:       })
0829:     } catch {
0830:       // fall through to envelope parsing + auth failure handling below
0831:     }
0832:   }
0833:
0834:   const contentType = response.headers.get('content-type') ?? ''
0835:   const payload = contentType.includes('application/json') ? await response.json() : await response.text()
0836:
0837:   if (response.ok && (response.status === 204 || payload === '')) {
0838:     return undefined as T
0839:   }
0840:
0841:   if (!response.ok) {
0842:     const envelope = payload as ApiErrorEnvelope | undefined
0843:     const code = envelope?.error?.code
0844:     const envelopeDetails = envelope?.error?.details
0845:     const detailMessage =
0846:       typeof payload === 'object' && payload && 'detail' in payload && typeof payload.detail === 'object' && payload.detail
0847:         ? (payload.detail as { message?: string; code?: string }).message ?? null
0848:         : null
0849:     const detailCode =
0850:       typeof payload === 'object' && payload && 'detail' in payload && typeof payload.detail === 'object' && payload.detail
0851:         ? (payload.detail as { message?: string; code?: string }).code ?? null
0852:         : null
0853:     const detailDetails =
0854:       typeof payload === 'object' && payload && 'detail' in payload && typeof payload.detail === 'object' && payload.detail
0855:         ? ((payload.detail as { details?: Record<string, unknown> }).details ?? null)
0856:         : null
0857:     const message =
0858:       typeof payload === 'string'
0859:         ? payload
0860:         : envelope?.error?.message ?? detailMessage ?? payload?.message ?? 'Request failed'
0861:     if (response.status === 401 && !options.suppressAuthFailureHandler) {
0862:       authFailureHandler?.()
0863:     }
0864:     throw new ApiRequestError(message, response.status, code ?? detailCode ?? undefined, envelopeDetails ?? detailDetails ?? null)
0865:   }
0866:
0867:   const successEnvelope = payload as ApiSuccessEnvelope<T> | undefined
0868:   if (
0869:     successEnvelope &&
0870:     typeof successEnvelope === 'object' &&
0871:     successEnvelope.success === true &&
0872:     'data' in successEnvelope
0873:   ) {
0874:     return successEnvelope.data
0875:   }
0876:
0877:   if (requiresApiEnvelope(path)) {
0878:     throw new ApiRequestError('Invalid API response envelope', response.status, 'INVALID_API_RESPONSE_ENVELOPE', {
0879:       path,
0880:     })
0881:   }
0882:
0883:   return payload as T
0884: }
0885:
0886: async function authRequest<T>(path: string, init?: RequestInit): Promise<T> {
0887:   return requestInternal<T>(path, init, {
0888:     allowSessionRefresh: false,
0889:     suppressAuthFailureHandler: true,
0890:   })
0891: }
0892:
0893: async function refreshAccessToken() {
0894:   if (!refreshPromise) {
0895:     refreshPromise = authRequest<LoginResponse>('/api/auth/refresh', {
0896:       method: 'POST',
0897:     })
0898:       .finally(() => {
0899:         refreshPromise = null
0900:       })
0901:   }
0902:
0903:   return refreshPromise
0904: }
0905:
0906: async function request<T>(path: string, init?: RequestInit): Promise<T> {
0907:   return requestInternal<T>(path, init)
0908: }
0909:
0910: function buildApiUrl(path: string) {
0911:   return `${API_BASE}${path}`
0912: }
0913:
0914: function pathSegment(value: string | number) {
0915:   return encodeURIComponent(String(value))
0916: }
0917:
0918: function learningItemFormData(payload: LearningItemCreatePayload) {
0919:   const formData = new FormData()
0920:   formData.append('kind', payload.kind)
0921:   formData.append('title', payload.title)
0922:   if (payload.description != null) formData.append('description', payload.description)
0923:   if (payload.week_label != null) formData.append('week_label', payload.week_label)
0924:   if (payload.format_label != null) formData.append('format_label', payload.format_label)
0925:   if (payload.duration_label != null) formData.append('duration_label', payload.duration_label)
0926:   for (const file of payload.files ?? []) {
0927:     formData.append('files', file)
0928:   }
0929:   return formData
0930: }
0931:
0932: function noticeFormData(payload: { title: string; body: string; course_code?: string | null; files?: File[] }) {
0933:   const formData = new FormData()
0934:   formData.append('title', payload.title)
0935:   formData.append('body', payload.body)
0936:   if (payload.course_code != null) formData.append('course_code', payload.course_code)
0937:   for (const file of payload.files ?? []) {
0938:     formData.append('files', file)
0939:   }
0940:   return formData
0941: }
0942:
0943: export const api = {
0944:   health: () => request<{ status?: string }>('/health'),
0945:   login: (payload: { login_id: string; password: string }) =>
0946:     authRequest<LoginResponse>('/api/auth/login', {
0947:       method: 'POST',
0948:       body: JSON.stringify(payload),
0949:     }),
0950:   bootstrapSession: async () => {
0951:     try {
0952:       return await authRequest<LoginResponse>('/api/auth/bootstrap')
0953:     } catch (error) {
0954:       if (error instanceof ApiRequestError && error.status === 404) {
0955:         return authRequest<LoginResponse>('/api/auth/me')
```

## G.2 Front selected LMS / assignment / exam / attendance API client

Source: `Front/src/api.ts:968-1150`

```ts
0968:     request<StudentAssignmentSummary[]>(`/api/students/${pathSegment(studentId)}/courses/${pathSegment(courseCode)}/assignments`),
0969:   getStudentAssignmentDetail: (studentId: string, courseCode: string, assignmentId: number) =>
0970:     request<StudentAssignmentDetail>(`/api/students/${pathSegment(studentId)}/courses/${pathSegment(courseCode)}/assignments/${pathSegment(assignmentId)}`),
0971:   submitStudentAssignment: (
0972:     studentId: string,
0973:     courseCode: string,
0974:     assignmentId: number,
0975:     payload: {
0976:       submission_text?: string | null
0977:       remove_attachment_ids?: number[]
0978:       files?: File[]
0979:     },
0980:   ) => {
0981:     const formData = new FormData()
0982:     if (payload.submission_text != null) {
0983:       formData.append('submission_text', payload.submission_text)
0984:     }
0985:     for (const attachmentId of payload.remove_attachment_ids ?? []) {
0986:       formData.append('remove_attachment_ids', String(attachmentId))
0987:     }
0988:     for (const file of payload.files ?? []) {
0989:       formData.append('files', file)
0990:     }
0991:     return request<StudentAssignmentDetail>(
0992:       `/api/students/${pathSegment(studentId)}/courses/${pathSegment(courseCode)}/assignments/${pathSegment(assignmentId)}/submission`,
0993:       {
0994:         method: 'POST',
0995:         body: formData,
0996:       },
0997:     )
0998:   },
0999:   buildStudentAssignmentAttachmentUrl: (
1000:     studentId: string,
1001:     courseCode: string,
1002:     assignmentId: number,
1003:     attachmentId: number,
1004:   ) =>
1005:     buildApiUrl(`/api/students/${pathSegment(studentId)}/courses/${pathSegment(courseCode)}/assignments/${pathSegment(assignmentId)}/attachments/${pathSegment(attachmentId)}`),
1006:   listProfessorAssignments: (professorId: string, courseCode: string) =>
1007:     request<ProfessorAssignmentSummary[]>(`/api/professors/${pathSegment(professorId)}/courses/${pathSegment(courseCode)}/assignments`),
1008:   getProfessorAssignmentDetail: (professorId: string, courseCode: string, assignmentId: number) =>
1009:     request<ProfessorAssignmentDetail>(`/api/professors/${pathSegment(professorId)}/courses/${pathSegment(courseCode)}/assignments/${pathSegment(assignmentId)}`),
1010:   createProfessorAssignment: (professorId: string, courseCode: string, payload: ProfessorAssignmentCreatePayload) =>
1011:     request<ProfessorAssignmentDetail>(`/api/professors/${pathSegment(professorId)}/courses/${pathSegment(courseCode)}/assignments`, {
1012:       method: 'POST',
1013:       body: JSON.stringify(payload),
1014:     }),
1015:   gradeProfessorAssignmentSubmission: (
1016:     professorId: string,
1017:     courseCode: string,
1018:     assignmentId: number,
1019:     submissionId: number,
1020:     payload: AssignmentGradePayload,
1021:   ) =>
1022:     request<ProfessorAssignmentDetail | ProfessorAssignmentSubmission>(
1023:       `/api/professors/${pathSegment(professorId)}/courses/${pathSegment(courseCode)}/assignments/${pathSegment(assignmentId)}/submissions/${pathSegment(submissionId)}/grade`,
1024:       {
1025:         method: 'PUT',
1026:         body: JSON.stringify(payload),
1027:       },
1028:     ),
1029:   getStudentGrades: (studentId: string, courseCode: string) =>
1030:     request<StudentCourseGrades>(`/api/students/${pathSegment(studentId)}/courses/${pathSegment(courseCode)}/grades`),
1031:   getProfessorGrades: (professorId: string, courseCode: string) =>
1032:     request<ProfessorCourseGradeSummary[]>(`/api/professors/${pathSegment(professorId)}/courses/${pathSegment(courseCode)}/grades`),
1033:   listStudentQna: (studentId: string, courseCode: string) =>
1034:     request<CourseQnaThread[]>(`/api/students/${pathSegment(studentId)}/courses/${pathSegment(courseCode)}/qna`),
1035:   createStudentQna: (studentId: string, courseCode: string, payload: StudentQnaCreatePayload) =>
1036:     request<CourseQnaThread>(`/api/students/${pathSegment(studentId)}/courses/${pathSegment(courseCode)}/qna`, {
1037:       method: 'POST',
1038:       body: JSON.stringify(payload),
1039:     }),
1040:   listProfessorQna: (professorId: string, courseCode: string) =>
1041:     request<CourseQnaThread[]>(`/api/professors/${pathSegment(professorId)}/courses/${pathSegment(courseCode)}/qna`),
1042:   answerProfessorQna: (professorId: string, courseCode: string, threadId: number, payload: ProfessorQnaAnswerPayload) =>
1043:     request<CourseQnaThread>(`/api/professors/${pathSegment(professorId)}/courses/${pathSegment(courseCode)}/qna/${pathSegment(threadId)}/answer`, {
1044:       method: 'POST',
1045:       body: JSON.stringify(payload),
1046:     }),
1047:   listStudentLearningProgress: (studentId: string, courseCode: string) =>
1048:     request<StudentLearningProgressItem[]>(`/api/students/${pathSegment(studentId)}/courses/${pathSegment(courseCode)}/learning-progress`),
1049:   updateStudentLearningProgress: (
1050:     studentId: string,
1051:     courseCode: string,
1052:     learningItemId: number,
1053:     payload: LearningProgressUpdatePayload,
1054:   ) =>
1055:     request<StudentLearningProgressItem>(
1056:       `/api/students/${pathSegment(studentId)}/courses/${pathSegment(courseCode)}/learning-items/${pathSegment(learningItemId)}/progress`,
1057:       {
1058:         method: 'PUT',
1059:         body: JSON.stringify(payload),
1060:       },
1061:     ),
1062:   listProfessorLearningProgress: (professorId: string, courseCode: string) =>
1063:     request<ProfessorLearningProgressRow[]>(`/api/professors/${pathSegment(professorId)}/courses/${pathSegment(courseCode)}/learning-progress`),
1064:   buildProfessorAssignmentAttachmentUrl: (
1065:     professorId: string,
1066:     courseCode: string,
1067:     assignmentId: number,
1068:     attachmentId: number,
1069:   ) =>
1070:     buildApiUrl(`/api/professors/${pathSegment(professorId)}/courses/${pathSegment(courseCode)}/assignments/${pathSegment(assignmentId)}/attachments/${pathSegment(attachmentId)}`),
1071:   listStudentLearningItems: (studentId: string, courseCode: string) =>
1072:     request<LearningItem[]>(`/api/students/${pathSegment(studentId)}/courses/${pathSegment(courseCode)}/learning-items`),
1073:   listProfessorLearningItems: (professorId: string, courseCode: string) =>
1074:     request<LearningItem[]>(`/api/professors/${pathSegment(professorId)}/courses/${pathSegment(courseCode)}/learning-items`),
1075:   createProfessorLearningItem: (professorId: string, courseCode: string, payload: LearningItemCreatePayload) =>
1076:     request<LearningItem>(`/api/professors/${pathSegment(professorId)}/courses/${pathSegment(courseCode)}/learning-items`, {
1077:       method: 'POST',
1078:       body: learningItemFormData(payload),
1079:     }),
1080:   deleteProfessorLearningItem: (professorId: string, courseCode: string, learningItemId: number) =>
1081:     request<void>(
1082:       `/api/professors/${pathSegment(professorId)}/courses/${pathSegment(courseCode)}/learning-items/${pathSegment(learningItemId)}`,
1083:       {
1084:         method: 'DELETE',
1085:       },
1086:     ),
1087:   buildStudentLearningAttachmentUrl: (studentId: string, courseCode: string, learningItemId: number, attachmentId: number) =>
1088:     buildApiUrl(
1089:       `/api/students/${pathSegment(studentId)}/courses/${pathSegment(courseCode)}/learning-items/${pathSegment(learningItemId)}/attachments/${pathSegment(attachmentId)}`,
1090:     ),
1091:   buildProfessorLearningAttachmentUrl: (professorId: string, courseCode: string, learningItemId: number, attachmentId: number) =>
1092:     buildApiUrl(
1093:       `/api/professors/${pathSegment(professorId)}/courses/${pathSegment(courseCode)}/learning-items/${pathSegment(learningItemId)}/attachments/${pathSegment(attachmentId)}`,
1094:     ),
1095:   listStudentExams: (studentId: string, courseCode: string) =>
1096:     request<StudentExamSummary[]>(`/api/students/${studentId}/courses/${courseCode}/exams`),
1097:   getStudentExamDetail: (studentId: string, courseCode: string, examId: number) =>
1098:     request<StudentExamDetail>(`/api/students/${studentId}/courses/${courseCode}/exams/${examId}`),
1099:   startStudentExam: (studentId: string, courseCode: string, examId: number) =>
1100:     request<ExamSubmissionStart>(`/api/students/${studentId}/courses/${courseCode}/exams/${examId}/start`, {
1101:       method: 'POST',
1102:     }),
1103:   saveStudentExamAnswer: (
1104:     studentId: string,
1105:     courseCode: string,
1106:     examId: number,
1107:     submissionId: number,
1108:     questionId: number,
1109:     payload: StudentExamSaveAnswerPayload,
1110:   ) =>
1111:     request<StudentExamSavedAnswer>(
1112:       `/api/students/${studentId}/courses/${courseCode}/exams/${examId}/submissions/${submissionId}/answers/${questionId}`,
1113:       {
1114:         method: 'PUT',
1115:         body: JSON.stringify(payload),
1116:       },
1117:     ),
1118:   submitStudentExam: (studentId: string, courseCode: string, examId: number, payload: StudentExamSubmitPayload) =>
1119:     request<StudentExamSubmitResult>(`/api/students/${studentId}/courses/${courseCode}/exams/${examId}/submit`, {
1120:       method: 'POST',
1121:       body: JSON.stringify(payload),
1122:     }),
1123:   listProfessorExams: (professorId: string, courseCode: string) =>
1124:     request<ExamSummary[]>(`/api/professors/${professorId}/courses/${courseCode}/exams`),
1125:   getProfessorExamDetail: (professorId: string, courseCode: string, examId: number) =>
1126:     request<ProfessorExamDetail>(`/api/professors/${professorId}/courses/${courseCode}/exams/${examId}`),
1127:   createProfessorExam: (professorId: string, courseCode: string, payload: ProfessorExamCreatePayload) =>
1128:     request<ProfessorExamDetail>(`/api/professors/${professorId}/courses/${courseCode}/exams`, {
1129:       method: 'POST',
1130:       body: JSON.stringify(payload),
1131:     }),
1132:   updateProfessorExam: (professorId: string, courseCode: string, examId: number, payload: ProfessorExamCreatePayload) =>
1133:     request<ProfessorExamDetail>(`/api/professors/${professorId}/courses/${courseCode}/exams/${examId}`, {
1134:       method: 'PUT',
1135:       body: JSON.stringify(payload),
1136:     }),
1137:   deleteProfessorExam: (professorId: string, courseCode: string, examId: number) =>
1138:     request<void>(`/api/professors/${professorId}/courses/${courseCode}/exams/${examId}`, {
1139:       method: 'DELETE',
1140:     }),
1141:   publishProfessorExam: (professorId: string, courseCode: string, examId: number) =>
1142:     request<ProfessorExamDetail>(`/api/professors/${professorId}/courses/${courseCode}/exams/${examId}/publish`, {
1143:       method: 'POST',
1144:     }),
1145:   closeProfessorExam: (professorId: string, courseCode: string, examId: number) =>
1146:     request<ProfessorExamDetail>(`/api/professors/${professorId}/courses/${courseCode}/exams/${examId}/close`, {
1147:       method: 'POST',
1148:     }),
1149:   uploadProfessorExamQuestionAttachment: (
1150:     professorId: string,
```

## G.3 Front route parser와 URL build 규칙

Source: `Front/src/router.ts:1-140`

```ts
0001: export type CourseSection = 'overview' | 'content' | 'notices' | 'assignments' | 'exams' | 'lms' | 'attendance' | 'manage'
0002: export type AttendancePage = 'timeline' | 'timer' | 'roster'
0003:
0004: export type AppRoute =
0005:   | { kind: 'login' }
0006:   | { kind: 'dashboard' }
0007:   | { kind: 'profile' }
0008:   | { kind: 'notice'; noticeId: number }
0009:   | {
0010:       kind: 'course'
0011:       courseCode: string
0012:       section: CourseSection
0013:       attendancePage?: AttendancePage
0014:       sessionId?: number
0015:       projectionKey?: string
0016:       assignmentId?: number
0017:       examId?: number
0018:       examMode?: 'take'
0019:     }
0020:
0021: function cleanPathname(pathname: string) {
0022:   if (!pathname || pathname === '/') return '/'
0023:   return pathname.replace(/\/+$/, '') || '/'
0024: }
0025:
0026: export function parseAppRoute(pathname: string): AppRoute {
0027:   const normalizedPath = cleanPathname(pathname)
0028:
0029:   if (normalizedPath === '/' || normalizedPath === '/dashboard') {
0030:     return { kind: 'dashboard' }
0031:   }
0032:
0033:   if (normalizedPath === '/login') {
0034:     return { kind: 'login' }
0035:   }
0036:
0037:   if (normalizedPath === '/profile') {
0038:     return { kind: 'profile' }
0039:   }
0040:
0041:   const noticeMatch = normalizedPath.match(/^\/notices\/(\d+)$/)
0042:   if (noticeMatch) {
0043:     return { kind: 'notice', noticeId: Number(noticeMatch[1]) }
0044:   }
0045:
0046:   const courseAttendanceBundleMatch = normalizedPath.match(
0047:     /^\/courses\/([^/]+)\/attendance\/sessions\/(\d+)\/(timer|roster)$/,
0048:   )
0049:   if (courseAttendanceBundleMatch) {
0050:     return {
0051:       kind: 'course',
0052:       courseCode: decodeURIComponent(courseAttendanceBundleMatch[1]),
0053:       section: 'attendance',
0054:       sessionId: Number(courseAttendanceBundleMatch[2]),
0055:       attendancePage: courseAttendanceBundleMatch[3] as AttendancePage,
0056:     }
0057:   }
0058:
0059:   const courseAttendanceSlotRosterMatch = normalizedPath.match(
0060:     /^\/courses\/([^/]+)\/attendance\/slots\/([^/]+)\/roster$/,
0061:   )
0062:   if (courseAttendanceSlotRosterMatch) {
0063:     return {
0064:       kind: 'course',
0065:       courseCode: decodeURIComponent(courseAttendanceSlotRosterMatch[1]),
0066:       section: 'attendance',
0067:       projectionKey: decodeURIComponent(courseAttendanceSlotRosterMatch[2]),
0068:       attendancePage: 'roster',
0069:     }
0070:   }
0071:
0072:   const courseAssignmentDetailMatch = normalizedPath.match(/^\/courses\/([^/]+)\/assignments\/(\d+)$/)
0073:   if (courseAssignmentDetailMatch) {
0074:     return {
0075:       kind: 'course',
0076:       courseCode: decodeURIComponent(courseAssignmentDetailMatch[1]),
0077:       section: 'assignments',
0078:       assignmentId: Number(courseAssignmentDetailMatch[2]),
0079:     }
0080:   }
0081:
0082:   const courseExamTakeMatch = normalizedPath.match(/^\/courses\/([^/]+)\/exams\/(\d+)\/take$/)
0083:   if (courseExamTakeMatch) {
0084:     return {
0085:       kind: 'course',
0086:       courseCode: decodeURIComponent(courseExamTakeMatch[1]),
0087:       section: 'exams',
0088:       examId: Number(courseExamTakeMatch[2]),
0089:       examMode: 'take',
0090:     }
0091:   }
0092:
0093:   const courseSectionMatch = normalizedPath.match(/^\/courses\/([^/]+)\/(content|notices|assignments|exams|lms|attendance|manage)$/)
0094:   if (courseSectionMatch) {
0095:     return {
0096:       kind: 'course',
0097:       courseCode: decodeURIComponent(courseSectionMatch[1]),
0098:       section: courseSectionMatch[2] as CourseSection,
0099:       attendancePage: courseSectionMatch[2] === 'attendance' ? 'timeline' : undefined,
0100:     }
0101:   }
0102:
0103:   const courseOverviewMatch = normalizedPath.match(/^\/courses\/([^/]+)$/)
0104:   if (courseOverviewMatch) {
0105:     return {
0106:       kind: 'course',
0107:       courseCode: decodeURIComponent(courseOverviewMatch[1]),
0108:       section: 'overview',
0109:     }
0110:   }
0111:
0112:   return { kind: 'dashboard' }
0113: }
0114:
0115: export function buildAppPath(route: AppRoute) {
0116:   switch (route.kind) {
0117:     case 'login':
0118:       return '/login'
0119:     case 'dashboard':
0120:       return '/dashboard'
0121:     case 'profile':
0122:       return '/profile'
0123:     case 'notice':
0124:       return `/notices/${route.noticeId}`
0125:     case 'course': {
0126:       const basePath = `/courses/${encodeURIComponent(route.courseCode)}`
0127:       if (route.section === 'overview') return basePath
0128:       if (route.section === 'assignments' && route.assignmentId != null) {
0129:         return `${basePath}/assignments/${route.assignmentId}`
0130:       }
0131:       if (route.section === 'exams' && route.examMode === 'take' && route.examId != null) {
0132:         return `${basePath}/exams/${route.examId}/take`
0133:       }
0134:       if (route.section !== 'attendance') return `${basePath}/${route.section}`
0135:       if (route.attendancePage && route.attendancePage !== 'timeline' && route.sessionId) {
0136:         return `${basePath}/attendance/sessions/${route.sessionId}/${route.attendancePage}`
0137:       }
0138:       if (route.attendancePage === 'roster' && route.projectionKey) {
0139:         return `${basePath}/attendance/slots/${encodeURIComponent(route.projectionKey)}/${route.attendancePage}`
0140:       }
```

## G.4 Front 출석 modal/history UI 핵심

Source: `Front/src/App.tsx:4677-4745`

```tsx
4677:                       {attendanceCsvBusyVariant === 'full' ? '전체본 생성 중...' : '전체본 CSV'}
4678:                     </button>
4679:                   </div>
4680:                 }
4681:               >
4682:                 {attendanceStudentStats ? (
4683:                   <div className="attendance-roster-scroll">
4684:                     <table className="attendance-stats-table">
4685:                       <thead>
4686:                         <tr>
4687:                           <th scope="col">학번</th>
4688:                           <th scope="col">이름</th>
4689:                           <th scope="col">출석 차시</th>
4690:                           <th scope="col">지각 차시</th>
4691:                           <th scope="col">결석 차시</th>
4692:                           <th scope="col">공결 차시</th>
4693:                         </tr>
4694:                       </thead>
4695:                       <tbody>
4696:                         {attendanceStudentStats.rows.map((row) => (
4697:                           <tr key={`attendance-stat-${row.student_id}`}>
4698:                             <td>{row.student_id}</td>
4699:                             <td>{row.student_name}</td>
4700:                             <td>{row.present}</td>
4701:                             <td>{row.late}</td>
4702:                             <td>{row.absent}</td>
4703:                             <td>{row.official}</td>
4704:                           </tr>
4705:                         ))}
4706:                       </tbody>
4707:                     </table>
4708:                   </div>
4709:                 ) : (
4710:                   <p className="empty-state">학생별 누계 통계를 불러오는 중입니다.</p>
4711:                 )}
4712:               </SectionCard>
4713:             ) : null}
4714:             {attendanceMessage ? <p className="success-text">{attendanceMessage}</p> : null}
4715:
4716:             {attendanceModalOpen && attendanceModalAnchorSlot ? (
4717:               <div className="attendance-modal-backdrop" role="presentation" onClick={() => setAttendanceModalOpen(false)}>
4718:                 <div className="attendance-modal" role="dialog" aria-modal="true" onClick={(event) => event.stopPropagation()}>
4719:                   <div className="attendance-modal-head">
4720:                     <strong>출석 시작 · {attendanceModalAnchorSlot.session_date}</strong>
4721:                     <button type="button" className="text-button" onClick={() => setAttendanceModalOpen(false)}>닫기</button>
4722:                   </div>
4723:                   <div className="attendance-mode-group">
4724:                     {([
4725:                       ['manual', '일반출석'],
4726:                       ['smart', '스마트출석'],
4727:                       ['canceled', '휴강'],
4728:                     ] as const).map(([mode, label]) => (
4729:                       <button
4730:                         key={mode}
4731:                         type="button"
4732:                         className={`filter-chip${selectedAttendanceMode === mode ? ' active' : ''}`}
4733:                         onClick={() => setSelectedAttendanceMode(mode)}
4734:                       >
4735:                         {label}
4736:                       </button>
4737:                     ))}
4738:                   </div>
4739:                   <div className="attendance-modal-slot-list">
4740:                     {modalDateSlots.map((slot) => (
4741:                       <label key={slot.projection_key} className="attendance-modal-slot-option">
4742:                         <input
4743:                           type="checkbox"
4744:                           checked={selectedBatchProjectionKeys.includes(slot.projection_key)}
4745:                           onChange={() => toggleModalProjectionKey(slot.projection_key)}
```

## G.5 Front selected LMS UI 핵심

Source: `Front/src/App.tsx:5800-5945`

```tsx
5800:                                   <option value="submitted">제출됨</option>
5801:                                   <option value="graded">채점 완료</option>
5802:                                   <option value="returned">반려/재제출</option>
5803:                                 </select>
5804:                               </label>
5805:                             </div>
5806:                             <label>
5807:                               피드백
5808:                               <textarea
5809:                                 rows={4}
5810:                                 value={assignmentGradeDrafts[selectedSubmission.id]?.feedback ?? ''}
5811:                                 onChange={(event) => setAssignmentGradeDrafts((current) => ({
5812:                                   ...current,
5813:                                   [selectedSubmission.id]: {
5814:                                     score: current[selectedSubmission.id]?.score ?? (selectedSubmission.score == null ? '' : String(selectedSubmission.score)),
5815:                                     feedback: event.target.value,
5816:                                     gradingStatus: current[selectedSubmission.id]?.gradingStatus ?? 'graded',
5817:                                   },
5818:                                 }))}
5819:                                 placeholder="학생에게 공개할 피드백을 입력하세요."
5820:                               />
5821:                             </label>
5822:                             <div className="exam-detail-actions">
5823:                               <button type="submit" className="primary-button" disabled={assignmentBusyKey === `grade-${selectedSubmission.id}`}>
5824:                                 {assignmentBusyKey === `grade-${selectedSubmission.id}` ? '저장 중...' : '채점 저장'}
5825:                               </button>
5826:                               <span className="caption-text">
5827:                                 현재 상태: {getGradingStatusLabel(selectedSubmission.grading_status)} · {formatOptionalScore(selectedSubmission.score, '점수 없음')}
5828:                               </span>
5829:                             </div>
5830:                           </form>
5831:                           {selectedSubmission.attachments.length > 0 ? (
5832:                             <div className="assignment-attachment-stack">
5833:                               <strong>첨부 파일</strong>
5834:                               <div className="assignment-attachment-list">
5835:                                 {selectedSubmission.attachments.map((attachment) => (
5836:                                   <a
5837:                                     key={attachment.id}
5838:                                     className="assignment-attachment-chip"
5839:                                     href={api.buildProfessorAssignmentAttachmentUrl(
5840:                                       currentUser!.login_id,
5841:                                       selectedCourse!.course_code,
5842:                                       professorAssignmentDetail.id,
5843:                                       attachment.id,
5844:                                     )}
5845:                                     target="_blank"
5846:                                     rel="noreferrer"
5847:                                   >
5848:                                     <span>{attachment.original_filename}</span>
5849:                                     <small>{formatFileSize(attachment.file_size_bytes)}</small>
5850:                                   </a>
5851:                                 ))}
5852:                               </div>
5853:                             </div>
5854:                           ) : null}
5855:                         </article>
5856:                       ) : null}
5857:                     </div>
5858:                   )}
5859:                 </article>
5860:               </div>
5861:             </SectionCard>
5862:           ) : null}
5863:         </div>
5864:       )
5865:     }
5866:
5867:     if (isStudent) {
5868:       return renderStudentAssignmentSection()
5869:     }
5870:     if (isProfessor) {
5871:       return renderProfessorAssignmentSection()
5872:     }
5873:     return (
5874:       <SectionCard title="과제">
5875:         <p className="empty-state">관리자 계정에서는 과제 화면을 직접 사용할 수 없습니다.</p>
5876:       </SectionCard>
5877:     )
5878:   }
5879:
5880:
5881:   function renderGradeItems(items: GradeBookItem[]) {
5882:     if (items.length === 0) {
5883:       return <p className="empty-state">표시할 성적 항목이 없습니다.</p>
5884:     }
5885:
5886:     return (
5887:       <div className="entity-list">
5888:         {items.map((item) => (
5889:           <article key={getGradeItemKey(item)} className="entity-row entity-row--wide">
5890:             <div>
5891:               <p className="entity-title">{item.title}</p>
5892:               <p className="entity-subtitle">
5893:                 {item.item_type === 'assignment' ? '과제' : item.item_type === 'exam' ? '시험' : item.item_type}
5894:                 {item.grading_status ? ` · ${getGradingStatusLabel(item.grading_status)}` : ''}
5895:                 {item.feedback ? ` · 피드백: ${item.feedback}` : ''}
5896:               </p>
5897:             </div>
5898:             <div className="entity-actions">
5899:               <span className="info-chip">{formatOptionalScore(item.score, '점수 없음')} / {formatOptionalScore(item.max_score, '-')}</span>
5900:               <span className="badge">{formatOptionalPercent(item.percent)}</span>
5901:             </div>
5902:           </article>
5903:         ))}
5904:       </div>
5905:     )
5906:   }
5907:
5908:   function renderQnaThread(thread: CourseQnaThread) {
5909:     const isClosedThread = thread.status === 'closed'
5910:
5911:     return (
5912:       <article key={thread.id} className="exam-list-card exam-list-card--student">
5913:         <div className="exam-list-card-top">
5914:           <div className="exam-card-copy">
5915:             <strong>{thread.title}</strong>
5916:             <p>{thread.body}</p>
5917:             <span className="caption-text">
5918:               {thread.student_name ?? thread.student_id ?? '학생'} · {formatBoardDate(thread.updated_at ?? thread.created_at)}
5919:             </span>
5920:           </div>
5921:           <span className={`status-pill status-pill--${getQnaStatusTone(thread.status)}`}>
5922:             {getQnaStatusLabel(thread.status)}
5923:           </span>
5924:         </div>
5925:         {thread.posts?.length ? (
5926:           <div className="helper-list">
5927:             {thread.posts.map((post) => (
5928:               <div key={post.id} className="helper-row">
5929:                 <strong>{post.post_type === 'answer' ? '답변' : post.post_type === 'question' ? '질문' : '댓글'}</strong>
5930:                 <span>{post.body}</span>
5931:               </div>
5932:             ))}
5933:           </div>
5934:         ) : null}
5935:         {isProfessor ? (
5936:           <div className="stack-form">
5937:             {isClosedThread ? (
5938:               <p className="caption-text">종료된 문의입니다. 추가 답변은 등록할 수 없습니다.</p>
5939:             ) : (
5940:               <>
5941:                 <label>
5942:                   답변 작성
5943:                   <textarea
5944:                     rows={3}
5945:                     value={qnaAnswerDrafts[thread.id] ?? ''}
```

## G.6 Backend 인증/세션/권한 endpoint

Source: `Backend/app/main.py:920-1075`

```py
0920: @app.post("/api/auth/login", response_model=None)
0921: def login(
0922:     payload: AuthLoginRequest,
0923:     db: Session = Depends(get_db),
0924: ) -> dict[str, Any] | JSONResponse:
0925:     try:
0926:         user = authenticate_user(db, payload.login_id, payload.password)
0927:         bundle = create_login_session(db, user)
0928:         auth_payload = build_auth_session_payload(
0929:             db,
0930:             bundle,
0931:             user,
0932:             bundle.access_token,
0933:             bundle.access_expires_at,
0934:         )
0935:         return auth_success_response(
0936:             auth_payload,
0937:             meta={
0938:                 "refresh_cookie_name": settings.refresh_cookie_name,
0939:                 "access_cookie_name": settings.access_cookie_name,
0940:                 "legacy_dev_token_enabled": settings.auth_allow_legacy_dev_tokens,
0941:             },
0942:             compatibility={
0943:                 "access_token": bundle.access_token,
0944:                 "user": auth_payload["user"],
0945:             },
0946:             access_token=bundle.access_token,
0947:             access_expires_at=bundle.access_expires_at,
0948:             refresh_token=bundle.refresh_token,
0949:             refresh_expires_at=bundle.refresh_expires_at,
0950:         )
0951:     except HTTPException as exc:
0952:         detail = exc.detail if isinstance(exc.detail, dict) else {}
0953:         return error_payload(
0954:             exc.status_code,
0955:             detail.get("code", "UNAUTHENTICATED"),
0956:             detail.get("message", "invalid credentials"),
0957:             detail.get("details", {"login_id": payload.login_id}),
0958:         )
0959:
0960:
0961: @app.post("/api/auth/refresh", response_model=None)
0962: def refresh_auth_session(
0963:     request: Request,
0964:     db: Session = Depends(get_db),
0965: ) -> dict[str, Any] | JSONResponse:
0966:     raw_refresh_token = request.cookies.get(settings.refresh_cookie_name)
0967:     if not raw_refresh_token:
0968:         return error_payload(status.HTTP_401_UNAUTHORIZED, "UNAUTHENTICATED", "refresh token is required")
0969:     try:
0970:         bundle = rotate_refresh_session(db, raw_refresh_token)
0971:         return auth_success_response(
0972:             build_auth_session_payload(
0973:                 db,
0974:                 bundle,
0975:                 bundle.user,
0976:                 bundle.access_token,
0977:                 bundle.access_expires_at,
0978:             ),
0979:             meta={"refreshed": True},
0980:             access_token=bundle.access_token,
0981:             access_expires_at=bundle.access_expires_at,
0982:             refresh_token=bundle.refresh_token,
0983:             refresh_expires_at=bundle.refresh_expires_at,
0984:         )
0985:     except HTTPException as exc:
0986:         error_response = error_response_from_exception(exc)
0987:         clear_access_cookie(error_response)
0988:         clear_refresh_cookie(error_response)
0989:         return error_response
0990:
0991:
0992: def _bootstrap_auth_session(
0993:     request: Request,
0994:     db: Session,
0995: ) -> dict[str, Any] | JSONResponse:
0996:     authorization = request.headers.get("Authorization")
0997:     if authorization:
0998:         try:
0999:             identity = verify_access_token(authorization.partition(" ")[2] if " " in authorization else authorization)
1000:             user = get_user_by_login_id(db, identity.login_id)
1001:             access_token = authorization.partition(" ")[2] if " " in authorization else authorization
1002:             return auth_success_response(
1003:                 build_auth_session_payload(db, None, user, access_token, identity.expires_at),
1004:                 meta={
1005:                     "restored_via": "access-token",
1006:                     "legacy_dev_token": identity.legacy_dev_token,
1007:                 },
1008:             )
1009:         except HTTPException as exc:
1010:             detail = exc.detail if isinstance(exc.detail, dict) else {}
1011:             if detail.get("code") not in {"TOKEN_EXPIRED", "UNAUTHENTICATED"}:
1012:                 return error_response_from_exception(exc)
1013:
1014:     raw_access_cookie = request.cookies.get(settings.access_cookie_name)
1015:     if raw_access_cookie:
1016:         try:
1017:             identity = verify_access_token(raw_access_cookie)
1018:             user = get_user_by_login_id(db, identity.login_id)
1019:             return auth_success_response(
1020:                 build_auth_session_payload(db, None, user, raw_access_cookie, identity.expires_at),
1021:                 meta={"restored_via": "access-cookie"},
1022:             )
1023:         except HTTPException as exc:
1024:             detail = exc.detail if isinstance(exc.detail, dict) else {}
1025:             if detail.get("code") not in {"TOKEN_EXPIRED", "UNAUTHENTICATED"}:
1026:                 return error_response_from_exception(exc)
1027:
1028:     raw_refresh_token = request.cookies.get(settings.refresh_cookie_name)
1029:     if not raw_refresh_token:
1030:         return error_payload(status.HTTP_401_UNAUTHORIZED, "UNAUTHENTICATED", "authentication is required")
1031:     try:
1032:         bundle = rotate_refresh_session(db, raw_refresh_token)
1033:         return auth_success_response(
1034:             build_auth_session_payload(
1035:                 db,
1036:                 bundle,
1037:                 bundle.user,
1038:                 bundle.access_token,
1039:                 bundle.access_expires_at,
1040:             ),
1041:             meta={"restored_via": "refresh-cookie"},
1042:             access_token=bundle.access_token,
1043:             access_expires_at=bundle.access_expires_at,
1044:             refresh_token=bundle.refresh_token,
1045:             refresh_expires_at=bundle.refresh_expires_at,
1046:         )
1047:     except HTTPException as exc:
1048:         error_response = error_response_from_exception(exc)
1049:         clear_access_cookie(error_response)
1050:         clear_refresh_cookie(error_response)
1051:         return error_response
1052:
1053:
1054: @app.get("/api/auth/bootstrap", response_model=None)
1055: def bootstrap_auth_session(
1056:     request: Request,
1057:     db: Session = Depends(get_db),
1058: ) -> dict[str, Any] | JSONResponse:
1059:     return _bootstrap_auth_session(request, db)
1060:
1061:
1062: @app.get("/api/auth/me", response_model=None)
1063: def bootstrap_auth_session_alias(
1064:     request: Request,
1065:     db: Session = Depends(get_db),
1066: ) -> dict[str, Any] | JSONResponse:
1067:     return _bootstrap_auth_session(request, db)
1068:
1069:
1070: @app.post("/api/auth/logout")
1071: def logout_auth_session(
1072:     request: Request,
1073:     db: Session = Depends(get_db),
1074: ) -> JSONResponse:
1075:     revoke_refresh_session(db, request.cookies.get(settings.refresh_cookie_name))
```

## G.7 Backend selected LMS/assignment/Q&A/learning endpoints

Source: `Backend/app/main.py:1102-1456`

```py
1102: @app.get("/api/students/{student_id}/courses/{course_code}/assignments", response_model=list[StudentAssignmentSummaryRead])
1103: def get_student_course_assignments(
1104:     student_id: str,
1105:     course_code: str,
1106:     current_user: User = Depends(require_authenticated_user),
1107:     db: Session = Depends(get_db),
1108: ) -> list[StudentAssignmentSummaryRead]:
1109:     student, course = require_student_course_access(student_id, course_code, current_user, db)
1110:     return [
1111:         StudentAssignmentSummaryRead(**assignment)
1112:         for assignment in list_student_assignments(db, student_user_id=student.id, course_id=course.id)
1113:     ]
1114:
1115:
1116: @app.get(
1117:     "/api/students/{student_id}/courses/{course_code}/assignments/{assignment_id}",
1118:     response_model=StudentAssignmentDetailRead,
1119: )
1120: def get_student_course_assignment_detail(
1121:     student_id: str,
1122:     course_code: str,
1123:     assignment_id: int,
1124:     current_user: User = Depends(require_authenticated_user),
1125:     db: Session = Depends(get_db),
1126: ) -> StudentAssignmentDetailRead:
1127:     student, course = require_student_course_access(student_id, course_code, current_user, db)
1128:     return StudentAssignmentDetailRead(
1129:         **get_student_assignment_detail(
1130:             db,
1131:             student_user_id=student.id,
1132:             course_id=course.id,
1133:             assignment_id=assignment_id,
1134:         )
1135:     )
1136:
1137:
1138: @app.post(
1139:     "/api/students/{student_id}/courses/{course_code}/assignments/{assignment_id}/submission",
1140:     response_model=StudentAssignmentDetailRead,
1141: )
1142: def submit_student_course_assignment(
1143:     student_id: str,
1144:     course_code: str,
1145:     assignment_id: int,
1146:     submission_text: str | None = Form(default=None),
1147:     remove_attachment_ids: list[int] = Form(default_factory=list),
1148:     files: list[UploadFile] = File(default_factory=list),
1149:     current_user: User = Depends(require_authenticated_user),
1150:     db: Session = Depends(get_db),
1151: ) -> StudentAssignmentDetailRead:
1152:     student, course = require_student_course_access(student_id, course_code, current_user, db)
1153:     return StudentAssignmentDetailRead(
1154:         **submit_student_assignment(
1155:             db,
1156:             student_user_id=student.id,
1157:             course_id=course.id,
1158:             assignment_id=assignment_id,
1159:             submission_text=submission_text,
1160:             files=files,
1161:             remove_attachment_ids=remove_attachment_ids,
1162:         )
1163:     )
1164:
1165:
1166: @app.get("/api/professors/{professor_id}/courses/{course_code}/assignments", response_model=list[ProfessorAssignmentSummaryRead])
1167: def get_professor_course_assignments(
1168:     professor_id: str,
1169:     course_code: str,
1170:     current_user: User = Depends(require_authenticated_user),
1171:     db: Session = Depends(get_db),
1172: ) -> list[ProfessorAssignmentSummaryRead]:
1173:     _, course = require_professor_course_ownership(professor_id, course_code, current_user, db)
1174:     return [ProfessorAssignmentSummaryRead(**assignment) for assignment in list_professor_assignments(db, course_id=course.id)]
1175:
1176:
1177: @app.post(
1178:     "/api/professors/{professor_id}/courses/{course_code}/assignments",
1179:     response_model=ProfessorAssignmentDetailRead,
1180:     status_code=status.HTTP_201_CREATED,
1181: )
1182: def create_professor_course_assignment(
1183:     professor_id: str,
1184:     course_code: str,
1185:     payload: ProfessorAssignmentCreateRequest,
1186:     current_user: User = Depends(require_authenticated_user),
1187:     db: Session = Depends(get_db),
1188: ) -> ProfessorAssignmentDetailRead:
1189:     _, course = require_professor_course_ownership(professor_id, course_code, current_user, db)
1190:     return ProfessorAssignmentDetailRead(
1191:         **create_professor_assignment(
1192:             db,
1193:             course_id=course.id,
1194:             payload=payload.model_dump(),
1195:         )
1196:     )
1197:
1198:
1199: @app.get(
1200:     "/api/professors/{professor_id}/courses/{course_code}/assignments/{assignment_id}",
1201:     response_model=ProfessorAssignmentDetailRead,
1202: )
1203: def get_professor_course_assignment_detail(
1204:     professor_id: str,
1205:     course_code: str,
1206:     assignment_id: int,
1207:     current_user: User = Depends(require_authenticated_user),
1208:     db: Session = Depends(get_db),
1209: ) -> ProfessorAssignmentDetailRead:
1210:     _, course = require_professor_course_ownership(professor_id, course_code, current_user, db)
1211:     return ProfessorAssignmentDetailRead(
1212:         **get_professor_assignment_detail(
1213:             db,
1214:             course_id=course.id,
1215:             assignment_id=assignment_id,
1216:         )
1217:     )
1218:
1219:
1220: @app.put("/api/professors/{professor_id}/courses/{course_code}/assignments/{assignment_id}/submissions/{submission_id}/grade")
1221: def grade_professor_assignment_submission(
1222:     professor_id: str,
1223:     course_code: str,
1224:     assignment_id: int,
1225:     submission_id: int,
1226:     payload: AssignmentGradeRequest,
1227:     current_user: User = Depends(require_authenticated_user),
1228:     db: Session = Depends(get_db),
1229: ) -> ProfessorAssignmentDetailRead:
1230:     professor, course = require_professor_course_ownership(professor_id, course_code, current_user, db)
1231:     return ProfessorAssignmentDetailRead(**grade_assignment_submission(
1232:         db,
1233:         course_id=course.id,
1234:         assignment_id=assignment_id,
1235:         submission_id=submission_id,
1236:         grader_user_id=professor.id,
1237:         payload=payload.model_dump(),
1238:     ))
1239:
1240:
1241: @app.get("/api/students/{student_id}/courses/{course_code}/assignments/{assignment_id}/attachments/{attachment_id}")
1242: def download_student_assignment_attachment(
1243:     student_id: str,
1244:     course_code: str,
1245:     assignment_id: int,
1246:     attachment_id: int,
1247:     range_header: str | None = Header(default=None, alias="Range"),
1248:     current_user: User = Depends(require_authenticated_user),
1249:     db: Session = Depends(get_db),
1250: ) -> StreamingResponse:
1251:     student, course = require_student_course_access(student_id, course_code, current_user, db)
1252:     download = get_student_assignment_attachment_download(
1253:         db,
1254:         student_user_id=student.id,
1255:         course_id=course.id,
1256:         assignment_id=assignment_id,
1257:         attachment_id=attachment_id,
1258:     )
1259:     return _stream_storage_download(download, range_header)
1260:
1261:
1262: @app.get("/api/professors/{professor_id}/courses/{course_code}/assignments/{assignment_id}/attachments/{attachment_id}")
1263: def download_professor_assignment_attachment(
1264:     professor_id: str,
1265:     course_code: str,
1266:     assignment_id: int,
1267:     attachment_id: int,
1268:     range_header: str | None = Header(default=None, alias="Range"),
1269:     current_user: User = Depends(require_authenticated_user),
1270:     db: Session = Depends(get_db),
1271: ) -> StreamingResponse:
1272:     _, course = require_professor_course_ownership(professor_id, course_code, current_user, db)
1273:     download = get_professor_assignment_attachment_download(
1274:         db,
1275:         course_id=course.id,
1276:         assignment_id=assignment_id,
1277:         attachment_id=attachment_id,
1278:     )
1279:     return _stream_storage_download(download, range_header)
1280:
1281:
1282: @app.get("/api/students/{student_id}/courses/{course_code}/grades")
1283: def get_student_course_grades(
1284:     student_id: str,
1285:     course_code: str,
1286:     current_user: User = Depends(require_authenticated_user),
1287:     db: Session = Depends(get_db),
1288: ) -> dict[str, Any]:
1289:     student, course = require_student_course_access(student_id, course_code, current_user, db)
1290:     return build_student_grades(db, student=student, course=course)
1291:
1292:
1293: @app.get("/api/professors/{professor_id}/courses/{course_code}/grades")
1294: def get_professor_course_grades(
1295:     professor_id: str,
1296:     course_code: str,
1297:     current_user: User = Depends(require_authenticated_user),
1298:     db: Session = Depends(get_db),
1299: ) -> list[dict[str, Any]]:
1300:     _, course = require_professor_course_ownership(professor_id, course_code, current_user, db)
1301:     return build_professor_grades(db, course=course)
1302:
1303:
1304: @app.get("/api/students/{student_id}/courses/{course_code}/qna")
1305: def get_student_course_qna(
1306:     student_id: str,
1307:     course_code: str,
1308:     current_user: User = Depends(require_authenticated_user),
1309:     db: Session = Depends(get_db),
1310: ) -> list[dict[str, Any]]:
1311:     student, course = require_student_course_access(student_id, course_code, current_user, db)
1312:     return list_student_qna_threads(db, course=course, student=student)
1313:
1314:
1315: @app.post("/api/students/{student_id}/courses/{course_code}/qna", status_code=status.HTTP_201_CREATED)
1316: def post_student_course_qna(
1317:     student_id: str,
1318:     course_code: str,
1319:     payload: QnaCreateRequest,
1320:     current_user: User = Depends(require_authenticated_user),
1321:     db: Session = Depends(get_db),
1322: ) -> dict[str, Any]:
1323:     student, course = require_student_course_access(student_id, course_code, current_user, db)
1324:     return create_student_qna_thread(db, course=course, student=student, title=payload.title, body=payload.body)
1325:
1326:
1327: @app.get("/api/professors/{professor_id}/courses/{course_code}/qna")
1328: def get_professor_course_qna(
1329:     professor_id: str,
1330:     course_code: str,
1331:     current_user: User = Depends(require_authenticated_user),
1332:     db: Session = Depends(get_db),
1333: ) -> list[dict[str, Any]]:
1334:     _, course = require_professor_course_ownership(professor_id, course_code, current_user, db)
1335:     return list_professor_qna_threads(db, course=course)
1336:
1337:
1338: @app.post("/api/professors/{professor_id}/courses/{course_code}/qna/{thread_id}/answer", status_code=status.HTTP_201_CREATED)
1339: def post_professor_course_qna_answer(
1340:     professor_id: str,
1341:     course_code: str,
1342:     thread_id: int,
1343:     payload: QnaAnswerRequest,
1344:     current_user: User = Depends(require_authenticated_user),
1345:     db: Session = Depends(get_db),
1346: ) -> dict[str, Any]:
1347:     professor, course = require_professor_course_ownership(professor_id, course_code, current_user, db)
1348:     return answer_qna_thread(db, course=course, professor=professor, thread_id=thread_id, body=payload.body, close=payload.close)
1349:
1350:
1351: @app.get("/api/students/{student_id}/courses/{course_code}/learning-items", response_model=list[LearningItemRead])
1352: def get_student_learning_items(
1353:     student_id: str,
1354:     course_code: str,
1355:     current_user: User = Depends(require_authenticated_user),
1356:     db: Session = Depends(get_db),
1357: ) -> list[LearningItemRead]:
1358:     _, course = require_student_course_access(student_id, course_code, current_user, db)
1359:     return [LearningItemRead(**item) for item in list_learning_items_for_course(db, course=course)]
1360:
1361:
1362: @app.get("/api/professors/{professor_id}/courses/{course_code}/learning-items", response_model=list[LearningItemRead])
1363: def get_professor_learning_items(
1364:     professor_id: str,
1365:     course_code: str,
1366:     current_user: User = Depends(require_authenticated_user),
1367:     db: Session = Depends(get_db),
1368: ) -> list[LearningItemRead]:
1369:     _, course = require_professor_course_ownership(professor_id, course_code, current_user, db)
1370:     return [LearningItemRead(**item) for item in list_learning_items_for_course(db, course=course, include_unpublished=True)]
1371:
1372:
1373: @app.get("/api/students/{student_id}/courses/{course_code}/learning-progress")
1374: def get_student_course_learning_progress(
1375:     student_id: str,
1376:     course_code: str,
1377:     current_user: User = Depends(require_authenticated_user),
1378:     db: Session = Depends(get_db),
1379: ) -> list[dict[str, Any]]:
1380:     student, course = require_student_course_access(student_id, course_code, current_user, db)
1381:     return list_student_learning_progress(db, course=course, student=student)
1382:
1383:
1384: @app.put("/api/students/{student_id}/courses/{course_code}/learning-items/{learning_item_id}/progress")
1385: def put_student_course_learning_progress(
1386:     student_id: str,
1387:     course_code: str,
1388:     learning_item_id: int,
1389:     payload: LearningProgressUpdateRequest,
1390:     current_user: User = Depends(require_authenticated_user),
1391:     db: Session = Depends(get_db),
1392: ) -> dict[str, Any]:
1393:     student, course = require_student_course_access(student_id, course_code, current_user, db)
1394:     return update_student_learning_progress(
1395:         db,
1396:         course=course,
1397:         student=student,
1398:         learning_item_id=learning_item_id,
1399:         progress_percent=payload.progress_percent,
1400:         status=payload.status,
1401:     )
1402:
1403:
1404: @app.get("/api/professors/{professor_id}/courses/{course_code}/learning-progress")
1405: def get_professor_course_learning_progress(
1406:     professor_id: str,
1407:     course_code: str,
1408:     current_user: User = Depends(require_authenticated_user),
1409:     db: Session = Depends(get_db),
1410: ) -> list[dict[str, Any]]:
1411:     _, course = require_professor_course_ownership(professor_id, course_code, current_user, db)
1412:     return build_professor_learning_progress(db, course=course)
1413:
1414:
1415: @app.post("/api/professors/{professor_id}/courses/{course_code}/learning-items", response_model=LearningItemRead, status_code=status.HTTP_201_CREATED)
1416: def add_professor_learning_item(
1417:     professor_id: str,
1418:     course_code: str,
1419:     kind: str = Form("material"),
1420:     title: str = Form(...),
1421:     description: str | None = Form(None),
1422:     files: list[UploadFile] = File(default_factory=list),
1423:     current_user: User = Depends(require_authenticated_user),
1424:     db: Session = Depends(get_db),
1425: ) -> LearningItemRead:
1426:     professor, course = require_professor_course_ownership(professor_id, course_code, current_user, db)
1427:     return LearningItemRead(**create_learning_item(db, course=course, professor=professor, kind=kind, title=title, description=description, files=files))
1428:
1429:
1430: @app.delete("/api/professors/{professor_id}/courses/{course_code}/learning-items/{learning_item_id}", status_code=status.HTTP_204_NO_CONTENT)
1431: def remove_professor_learning_item(
1432:     professor_id: str,
1433:     course_code: str,
1434:     learning_item_id: int,
1435:     current_user: User = Depends(require_authenticated_user),
1436:     db: Session = Depends(get_db),
1437: ) -> Response:
1438:     _, course = require_professor_course_ownership(professor_id, course_code, current_user, db)
1439:     delete_learning_item(db, course_id=course.id, learning_item_id=learning_item_id)
1440:     return Response(status_code=status.HTTP_204_NO_CONTENT)
1441:
1442:
1443: @app.get("/api/students/{student_id}/courses/{course_code}/learning-items/{learning_item_id}/attachments/{attachment_id}")
1444: def download_student_learning_attachment(
1445:     student_id: str,
1446:     course_code: str,
1447:     learning_item_id: int,
1448:     attachment_id: int,
1449:     range_header: str | None = Header(default=None, alias="Range"),
1450:     current_user: User = Depends(require_authenticated_user),
1451:     db: Session = Depends(get_db),
1452: ) -> StreamingResponse:
1453:     _, course = require_student_course_access(student_id, course_code, current_user, db)
1454:     return _stream_storage_download(get_learning_attachment_download(db, course=course, learning_item_id=learning_item_id, attachment_id=attachment_id), range_header)
1455:
1456:
```

## G.8 Backend exam endpoints

Source: `Backend/app/main.py:1469-1715`

```py
1469:
1470:
1471: @app.get("/api/students/{student_id}/courses/{course_code}/exams", response_model=list[StudentExamSummaryRead])
1472: def get_student_course_exams(
1473:     student_id: str,
1474:     course_code: str,
1475:     current_user: User = Depends(require_authenticated_user),
1476:     db: Session = Depends(get_db),
1477: ) -> list[StudentExamSummaryRead]:
1478:     student, course = require_student_course_access(student_id, course_code, current_user, db)
1479:     return [StudentExamSummaryRead(**exam) for exam in list_student_exams(db, student.id, course.id)]
1480:
1481:
1482: @app.get("/api/students/{student_id}/courses/{course_code}/exams/{exam_id}", response_model=StudentExamDetailRead)
1483: def get_student_course_exam_detail(
1484:     student_id: str,
1485:     course_code: str,
1486:     exam_id: int,
1487:     current_user: User = Depends(require_authenticated_user),
1488:     db: Session = Depends(get_db),
1489: ) -> StudentExamDetailRead:
1490:     student, course = require_student_course_access(student_id, course_code, current_user, db)
1491:     return StudentExamDetailRead(**get_student_exam_detail(db, student.id, course.id, exam_id))
1492:
1493:
1494: @app.post("/api/students/{student_id}/courses/{course_code}/exams/{exam_id}/start", response_model=ExamSubmissionStartRead)
1495: def start_student_course_exam(
1496:     student_id: str,
1497:     course_code: str,
1498:     exam_id: int,
1499:     current_user: User = Depends(require_authenticated_user),
1500:     db: Session = Depends(get_db),
1501: ) -> ExamSubmissionStartRead:
1502:     student, course = require_student_course_access(student_id, course_code, current_user, db)
1503:     return ExamSubmissionStartRead(
1504:         **start_student_exam(
1505:             db=db,
1506:             presence_client=presence_client,
1507:             student_id=student_id,
1508:             student_user_id=student.id,
1509:             course_code=course_code,
1510:             course_id=course.id,
1511:             exam_id=exam_id,
1512:         )
1513:     )
1514:
1515:
1516: @app.get("/api/professors/{professor_id}/courses/{course_code}/exams", response_model=list[ExamSummaryRead])
1517: def get_professor_course_exams(
1518:     professor_id: str,
1519:     course_code: str,
1520:     current_user: User = Depends(require_authenticated_user),
1521:     db: Session = Depends(get_db),
1522: ) -> list[ExamSummaryRead]:
1523:     _, course = require_professor_course_ownership(professor_id, course_code, current_user, db)
1524:     return [ExamSummaryRead(**exam) for exam in list_professor_exams(db, course.id)]
1525:
1526:
1527: @app.post(
1528:     "/api/professors/{professor_id}/courses/{course_code}/exams",
1529:     response_model=ProfessorExamDetailRead,
1530:     status_code=status.HTTP_201_CREATED,
1531: )
1532: def create_professor_course_exam(
1533:     professor_id: str,
1534:     course_code: str,
1535:     payload: ProfessorExamCreateRequest,
1536:     current_user: User = Depends(require_authenticated_user),
1537:     db: Session = Depends(get_db),
1538:  ) -> ProfessorExamDetailRead:
1539:     _, course = require_professor_course_ownership(professor_id, course_code, current_user, db)
1540:     return ProfessorExamDetailRead(**create_professor_exam(db=db, course_id=course.id, payload=payload.model_dump()))
1541:
1542:
1543: @app.get(
1544:     "/api/professors/{professor_id}/courses/{course_code}/exams/{exam_id}",
1545:     response_model=ProfessorExamDetailRead,
1546: )
1547: def get_professor_course_exam_detail(
1548:     professor_id: str,
1549:     course_code: str,
1550:     exam_id: int,
1551:     current_user: User = Depends(require_authenticated_user),
1552:     db: Session = Depends(get_db),
1553: ) -> ProfessorExamDetailRead:
1554:     _, course = require_professor_course_ownership(professor_id, course_code, current_user, db)
1555:     return ProfessorExamDetailRead(**get_professor_exam_detail(db=db, course_id=course.id, exam_id=exam_id))
1556:
1557:
1558: @app.put(
1559:     "/api/professors/{professor_id}/courses/{course_code}/exams/{exam_id}",
1560:     response_model=ProfessorExamDetailRead,
1561: )
1562: def update_professor_course_exam(
1563:     professor_id: str,
1564:     course_code: str,
1565:     exam_id: int,
1566:     payload: ProfessorExamCreateRequest,
1567:     current_user: User = Depends(require_authenticated_user),
1568:     db: Session = Depends(get_db),
1569: ) -> ProfessorExamDetailRead:
1570:     _, course = require_professor_course_ownership(professor_id, course_code, current_user, db)
1571:     return ProfessorExamDetailRead(
1572:         **update_professor_exam(
1573:             db=db,
1574:             course_id=course.id,
1575:             exam_id=exam_id,
1576:             payload=payload.model_dump(),
1577:         )
1578:     )
1579:
1580:
1581: @app.delete(
1582:     "/api/professors/{professor_id}/courses/{course_code}/exams/{exam_id}",
1583:     status_code=status.HTTP_204_NO_CONTENT,
1584: )
1585: def delete_professor_course_exam(
1586:     professor_id: str,
1587:     course_code: str,
1588:     exam_id: int,
1589:     current_user: User = Depends(require_authenticated_user),
1590:     db: Session = Depends(get_db),
1591: ) -> Response:
1592:     _, course = require_professor_course_ownership(professor_id, course_code, current_user, db)
1593:     delete_professor_exam(db=db, course_id=course.id, exam_id=exam_id)
1594:     return Response(status_code=status.HTTP_204_NO_CONTENT)
1595:
1596:
1597: @app.post(
1598:     "/api/professors/{professor_id}/courses/{course_code}/exams/{exam_id}/publish",
1599:     response_model=ProfessorExamDetailRead,
1600: )
1601: def publish_professor_course_exam(
1602:     professor_id: str,
1603:     course_code: str,
1604:     exam_id: int,
1605:     current_user: User = Depends(require_authenticated_user),
1606:     db: Session = Depends(get_db),
1607: ) -> ProfessorExamDetailRead:
1608:     _, course = require_professor_course_ownership(professor_id, course_code, current_user, db)
1609:     return ProfessorExamDetailRead(**publish_professor_exam(db=db, course_id=course.id, exam_id=exam_id))
1610:
1611:
1612: @app.post(
1613:     "/api/professors/{professor_id}/courses/{course_code}/exams/{exam_id}/close",
1614:     response_model=ProfessorExamDetailRead,
1615: )
1616: def close_professor_course_exam(
1617:     professor_id: str,
1618:     course_code: str,
1619:     exam_id: int,
1620:     current_user: User = Depends(require_authenticated_user),
1621:     db: Session = Depends(get_db),
1622: ) -> ProfessorExamDetailRead:
1623:     _, course = require_professor_course_ownership(professor_id, course_code, current_user, db)
1624:     return ProfessorExamDetailRead(**close_professor_exam(db=db, course_id=course.id, exam_id=exam_id))
1625:
1626:
1627: @app.post(
1628:     "/api/professors/{professor_id}/courses/{course_code}/exams/{exam_id}/questions/{question_id}/attachments",
1629:     response_model=list[ExamMediaAttachmentRead],
1630:     status_code=status.HTTP_201_CREATED,
1631: )
1632: def upload_professor_exam_question_media(
1633:     professor_id: str,
1634:     course_code: str,
1635:     exam_id: int,
1636:     question_id: int,
1637:     files: list[UploadFile] = File(default_factory=list),
1638:     current_user: User = Depends(require_authenticated_user),
1639:     db: Session = Depends(get_db),
1640: ) -> list[ExamMediaAttachmentRead]:
1641:     _, course = require_professor_course_ownership(professor_id, course_code, current_user, db)
1642:     return [
1643:         ExamMediaAttachmentRead(**item)
1644:         for item in upload_exam_question_attachments(db, course_id=course.id, exam_id=exam_id, question_id=question_id, files=files)
1645:     ]
1646:
1647:
1648: @app.get("/api/students/{student_id}/courses/{course_code}/exams/{exam_id}/questions/{question_id}/attachments/{attachment_id}")
1649: def download_student_exam_question_media(
1650:     student_id: str,
1651:     course_code: str,
1652:     exam_id: int,
1653:     question_id: int,
1654:     attachment_id: int,
1655:     range_header: str | None = Header(default=None, alias="Range"),
1656:     current_user: User = Depends(require_authenticated_user),
1657:     db: Session = Depends(get_db),
1658: ) -> StreamingResponse:
1659:     _, course = require_student_course_access(student_id, course_code, current_user, db)
1660:     return _stream_storage_download(
1661:         get_exam_question_attachment_download(db, course_id=course.id, exam_id=exam_id, question_id=question_id, attachment_id=attachment_id),
1662:         range_header,
1663:     )
1664:
1665:
1666: @app.get("/api/professors/{professor_id}/courses/{course_code}/exams/{exam_id}/questions/{question_id}/attachments/{attachment_id}")
1667: def download_professor_exam_question_media(
1668:     professor_id: str,
1669:     course_code: str,
1670:     exam_id: int,
1671:     question_id: int,
1672:     attachment_id: int,
1673:     range_header: str | None = Header(default=None, alias="Range"),
1674:     current_user: User = Depends(require_authenticated_user),
1675:     db: Session = Depends(get_db),
1676: ) -> StreamingResponse:
1677:     _, course = require_professor_course_ownership(professor_id, course_code, current_user, db)
1678:     return _stream_storage_download(
1679:         get_exam_question_attachment_download(db, course_id=course.id, exam_id=exam_id, question_id=question_id, attachment_id=attachment_id),
1680:         range_header,
1681:     )
1682:
1683:
1684: @app.post(
1685:     "/api/students/{student_id}/courses/{course_code}/exams/{exam_id}/submit",
1686:     response_model=StudentExamSubmitResultRead,
1687: )
1688: def submit_student_course_exam(
1689:     student_id: str,
1690:     course_code: str,
1691:     exam_id: int,
1692:     payload: StudentExamSubmitRequest,
1693:     current_user: User = Depends(require_authenticated_user),
1694:     db: Session = Depends(get_db),
1695: ) -> StudentExamSubmitResultRead:
1696:     student, course = require_student_course_access(student_id, course_code, current_user, db)
1697:     return StudentExamSubmitResultRead(
1698:         **submit_student_exam(
1699:             db=db,
1700:             student_user_id=student.id,
1701:             course_id=course.id,
1702:             exam_id=exam_id,
1703:             payload=payload.model_dump(),
1704:         )
1705:     )
1706:
1707:
1708: @app.put(
1709:     "/api/students/{student_id}/courses/{course_code}/exams/{exam_id}/submissions/{submission_id}/answers/{question_id}",
1710:     response_model=StudentExamSaveAnswerRead,
1711: )
1712: def save_student_course_exam_answer(
1713:     student_id: str,
1714:     course_code: str,
1715:     exam_id: int,
```

## G.9 Backend attendance endpoints + WebSocket

Source: `Backend/app/main.py:2030-2367`

```py
2030: @app.post(
2031:     "/api/attendance/eligibility",
2032:     response_model=AttendanceEligibilityResponse,
2033: )
2034: def attendance_eligibility(
2035:     payload: AttendanceEligibilityRequest,
2036:     current_user: User = Depends(require_authenticated_user),
2037:     db: Session = Depends(get_db),
2038: ) -> AttendanceEligibilityResponse:
2039:     require_student_self(payload.student_id, current_user)
2040:     result = check_attendance_eligibility(
2041:         db=db,
2042:         presence_client=presence_client,
2043:         student_id=payload.student_id,
2044:         course_id=payload.course_code,
2045:         classroom_id=None,
2046:         purpose="attendance",
2047:     )
2048:     return AttendanceEligibilityResponse(**result)
2049:
2050:
2051: @app.get("/api/professors/{professor_id}/courses/{course_code}/attendance/timeline")
2052: def professor_attendance_timeline(
2053:     professor_id: str,
2054:     course_code: str,
2055:     current_user: User = Depends(require_authenticated_user),
2056:     db: Session = Depends(get_db),
2057: ) -> dict[str, Any]:
2058:     require_professor_course_ownership(professor_id, course_code, current_user, db)
2059:     expired_events = expire_stale_attendance_sessions(db, course_code)
2060:     _release_db_connection(db)
2061:     _publish_expired_attendance_events_sync(expired_events)
2062:     return build_attendance_timeline(db, professor_id, course_code)
2063:
2064:
2065: @app.get("/api/professors/{professor_id}/courses/{course_code}/attendance/report")
2066: def professor_attendance_report(
2067:     professor_id: str,
2068:     course_code: str,
2069:     current_user: User = Depends(require_authenticated_user),
2070:     db: Session = Depends(get_db),
2071: ) -> dict[str, Any]:
2072:     require_professor_course_ownership(professor_id, course_code, current_user, db)
2073:     expired_events = expire_stale_attendance_sessions(db, course_code)
2074:     _release_db_connection(db)
2075:     _publish_expired_attendance_events_sync(expired_events)
2076:     return build_attendance_report(db, professor_id, course_code)
2077:
2078:
2079: @app.get("/api/professors/{professor_id}/courses/{course_code}/attendance/student-stats")
2080: def professor_attendance_student_stats(
2081:     professor_id: str,
2082:     course_code: str,
2083:     current_user: User = Depends(require_authenticated_user),
2084:     db: Session = Depends(get_db),
2085: ) -> dict[str, Any]:
2086:     require_professor_course_ownership(professor_id, course_code, current_user, db)
2087:     expired_events = expire_stale_attendance_sessions(db, course_code)
2088:     _release_db_connection(db)
2089:     _publish_expired_attendance_events_sync(expired_events)
2090:     return build_professor_student_attendance_stats(db, professor_id, course_code)
2091:
2092:
2093: @app.post("/api/professors/{professor_id}/courses/{course_code}/attendance/report-exports", response_model=ReportExportRead, status_code=status.HTTP_201_CREATED)
2094: def create_professor_attendance_report_export(
2095:     professor_id: str,
2096:     course_code: str,
2097:     payload: AttendanceReportExportCreate | None = None,
2098:     current_user: User = Depends(require_authenticated_user),
2099:     db: Session = Depends(get_db),
2100: ) -> ReportExportRead:
2101:     require_professor_course_ownership(professor_id, course_code, current_user, db)
2102:     export_type = payload.export_type if payload is not None else "attendance_summary_csv"
2103:     return ReportExportRead(**create_attendance_csv_export(db, professor_id=professor_id, course_code=course_code, export_type=export_type))
2104:
2105:
2106: @app.get("/api/professors/{professor_id}/courses/{course_code}/attendance/report-exports", response_model=list[ReportExportRead])
2107: def list_professor_attendance_report_exports(
2108:     professor_id: str,
2109:     course_code: str,
2110:     current_user: User = Depends(require_authenticated_user),
2111:     db: Session = Depends(get_db),
2112: ) -> list[ReportExportRead]:
2113:     require_professor_course_ownership(professor_id, course_code, current_user, db)
2114:     return [ReportExportRead(**item) for item in list_attendance_csv_exports(db, professor_id=professor_id, course_code=course_code)]
2115:
2116:
2117: @app.get("/api/professors/{professor_id}/courses/{course_code}/attendance/report-exports/{export_id}/download")
2118: def download_professor_attendance_report_export(
2119:     professor_id: str,
2120:     course_code: str,
2121:     export_id: int,
2122:     range_header: str | None = Header(default=None, alias="Range"),
2123:     current_user: User = Depends(require_authenticated_user),
2124:     db: Session = Depends(get_db),
2125: ) -> StreamingResponse:
2126:     require_professor_course_ownership(professor_id, course_code, current_user, db)
2127:     return _stream_storage_download(get_report_export_download(db, professor_id=professor_id, course_code=course_code, export_id=export_id), range_header)
2128:
2129:
2130: @app.post("/api/professors/{professor_id}/courses/{course_code}/attendance/sessions/batch")
2131: def professor_open_attendance_sessions_batch(
2132:     professor_id: str,
2133:     course_code: str,
2134:     payload: AttendanceSessionBatchRequest,
2135:     current_user: User = Depends(require_authenticated_user),
2136:     db: Session = Depends(get_db),
2137: ) -> dict[str, Any]:
2138:     require_professor_course_ownership(professor_id, course_code, current_user, db)
2139:     result = open_attendance_sessions_batch(
2140:         db,
2141:         professor_id,
2142:         course_code,
2143:         projection_keys=payload.projection_keys,
2144:         mode=payload.mode,
2145:     )
2146:     _release_db_connection(db)
2147:     _publish_attendance_sync(
2148:         course_code,
2149:         attendance_event_payload(
2150:             event_type="attendance.session.batch_applied",
2151:             course_code=course_code,
2152:             projection_keys=result["changed_projection_keys"],
2153:             session_ids=result["changed_session_ids"],
2154:             changed_payload={"results": result["results"], "mode": payload.mode},
2155:         ),
2156:     )
2157:     return result
2158:
2159:
2160: @app.post("/api/professors/{professor_id}/attendance/sessions/{session_id}/close")
2161: def professor_close_attendance(
2162:     professor_id: str,
2163:     session_id: int,
2164:     current_user: User = Depends(require_authenticated_user),
2165:     db: Session = Depends(get_db),
2166: ) -> dict[str, Any]:
2167:     require_professor_self(professor_id, current_user)
2168:     result = close_attendance_session(db, professor_id, session_id)
2169:     if "course_code" in result:
2170:         _release_db_connection(db)
2171:         _publish_attendance_sync(
2172:             result["course_code"],
2173:             attendance_event_payload(
2174:                 event_type="attendance.session.closed",
2175:                 course_code=result["course_code"],
2176:                 projection_keys=result.get("projection_keys", [result["projection_key"]]),
2177:                 session_ids=[result["session_id"]],
2178:                 version=result["version"],
2179:             ),
2180:         )
2181:     return result
2182:
2183:
2184: @app.get("/api/professors/{professor_id}/attendance/sessions/{session_id}/roster")
2185: def professor_attendance_roster(
2186:     professor_id: str,
2187:     session_id: int,
2188:     current_user: User = Depends(require_authenticated_user),
2189:     db: Session = Depends(get_db),
2190: ) -> dict[str, Any]:
2191:     require_professor_self(professor_id, current_user)
2192:     return get_attendance_session_roster(db, professor_id, session_id)
2193:
2194:
2195: @app.get("/api/professors/{professor_id}/courses/{course_code}/attendance/slot-roster")
2196: def professor_attendance_slot_roster(
2197:     professor_id: str,
2198:     course_code: str,
2199:     projection_key: str = Query(...),
2200:     current_user: User = Depends(require_authenticated_user),
2201:     db: Session = Depends(get_db),
2202: ) -> dict[str, Any]:
2203:     require_professor_course_ownership(professor_id, course_code, current_user, db)
2204:     return get_attendance_slot_roster_preview(db, professor_id, course_code, projection_key)
2205:
2206:
2207: @app.patch("/api/professors/{professor_id}/attendance/sessions/{session_id}/students/{student_id}")
2208: def professor_update_attendance_record(
2209:     professor_id: str,
2210:     session_id: int,
2211:     student_id: str,
2212:     payload: AttendanceRecordUpdateRequest,
2213:     current_user: User = Depends(require_authenticated_user),
2214:     db: Session = Depends(get_db),
2215: ) -> dict[str, Any]:
2216:     require_professor_self(professor_id, current_user)
2217:     result = update_attendance_session_record(
2218:         db,
2219:         professor_id,
2220:         session_id,
2221:         student_id,
2222:         payload.status,
2223:         payload.reason,
2224:         payload.projection_key,
2225:     )
2226:     if result.get("changed", True):
2227:         _release_db_connection(db)
2228:         _publish_attendance_sync(
2229:             result["course_code"],
2230:             attendance_event_payload(
2231:                 event_type="attendance.record.updated",
2232:                 course_code=result["course_code"],
2233:                 projection_keys=result.get("projection_keys", [result["projection_key"]]),
2234:                 session_ids=[result["session_id"]],
2235:                 version=result["version"],
2236:                 changed_payload={
2237:                     "student_id": result["student_id"],
2238:                     "new_status": result["new_status"],
2239:                     "projection_keys": result.get("projection_keys", []),
2240:                 },
2241:             ),
2242:         )
2243:     return result
2244:
2245:
2246: @app.get("/api/professors/{professor_id}/courses/{course_code}/attendance/students/{student_id}/history")
2247: def professor_attendance_student_history(
2248:     professor_id: str,
2249:     course_code: str,
2250:     student_id: str,
2251:     current_user: User = Depends(require_authenticated_user),
2252:     db: Session = Depends(get_db),
2253: ) -> dict[str, Any]:
2254:     require_professor_course_ownership(professor_id, course_code, current_user, db)
2255:     return list_attendance_history(db, professor_id, course_code, student_id)
2256:
2257:
2258: @app.get("/api/students/{student_id}/courses/{course_code}/attendance/active-sessions")
2259: def student_active_attendance_sessions(
2260:     student_id: str,
2261:     course_code: str,
2262:     current_user: User = Depends(require_authenticated_user),
2263:     db: Session = Depends(get_db),
2264: ) -> dict[str, Any]:
2265:     require_student_course_access(student_id, course_code, current_user, db)
2266:     expired_events = expire_stale_attendance_sessions(db, course_code)
2267:     _release_db_connection(db)
2268:     _publish_expired_attendance_events_sync(expired_events)
2269:     return list_student_active_attendance_sessions(db, presence_client, student_id, course_code)
2270:
2271:
2272: @app.get("/api/students/{student_id}/courses/{course_code}/attendance/semester-matrix")
2273: def student_attendance_semester_matrix(
2274:     student_id: str,
2275:     course_code: str,
2276:     current_user: User = Depends(require_authenticated_user),
2277:     db: Session = Depends(get_db),
2278: ) -> dict[str, Any]:
2279:     require_student_course_access(student_id, course_code, current_user, db)
2280:     expired_events = expire_stale_attendance_sessions(db, course_code)
2281:     _release_db_connection(db)
2282:     _publish_expired_attendance_events_sync(expired_events)
2283:     return build_student_attendance_semester_matrix(db, student_id, course_code)
2284:
2285:
2286: @app.post("/api/students/{student_id}/attendance/sessions/{session_id}/check-in")
2287: def student_attendance_check_in_endpoint(
2288:     student_id: str,
2289:     session_id: int,
2290:     current_user: User = Depends(require_authenticated_user),
2291:     db: Session = Depends(get_db),
2292: ) -> dict[str, Any]:
2293:     require_student_self(student_id, current_user)
2294:     result = student_attendance_check_in(db, presence_client, student_id, session_id)
2295:     _release_db_connection(db)
2296:     if result.get("changed_count", 0) > 0:
2297:         _publish_attendance_sync(
2298:             result["course_code"],
2299:             attendance_event_payload(
2300:                 event_type="attendance.student.checked_in",
2301:                 course_code=result["course_code"],
2302:                 projection_keys=result.get("projection_keys", [result["projection_key"]]),
2303:                 session_ids=[result["session_id"]],
2304:                 version=result["version"],
2305:                 changed_payload={
2306:                     "student_id": result["student_id"],
2307:                     "status": result["status"],
2308:                     "idempotent": result["idempotent"],
2309:                     "changed_count": result.get("changed_count"),
2310:                     "already_present_count": result.get("already_present_count"),
2311:                     "rejected_count": result.get("rejected_count"),
2312:                     "projection_keys": result.get("projection_keys", []),
2313:                 },
2314:             ),
2315:         )
2316:     return result
2317:
2318:
2319: @app.websocket("/ws/attendance")
2320: async def attendance_websocket(
2321:     websocket: WebSocket,
2322:     token: str | None = Query(default=None),
2323:     courseCode: str = Query(...),
2324:     view: str = Query(default="professor"),
2325: ) -> None:
2326:     await websocket.accept()
2327:     try:
2328:         login_id, user_role, expired_events, bootstrap_data = await anyio.to_thread.run_sync(
2329:             lambda: _build_attendance_websocket_bootstrap(
2330:                 token=token,
2331:                 raw_access_cookie=websocket.cookies.get(settings.access_cookie_name),
2332:                 course_code=courseCode,
2333:                 view=view,
2334:             )
2335:         )
2336:         attendance_broker.register(
2337:             courseCode,
2338:             websocket,
2339:             {"login_id": login_id, "role": user_role, "view": view, "course_code": courseCode},
2340:         )
2341:         await websocket.send_json(
2342:             attendance_event_payload(
2343:                 event_type="attendance.bootstrap",
2344:                 course_code=courseCode,
2345:                 changed_payload={"view": view, "data": bootstrap_data},
2346:             )
2347:         )
2348:         for event in expired_events:
2349:             await attendance_broker.publish(
2350:                 courseCode,
2351:                 attendance_event_payload(
2352:                     event_type=f"attendance.{event['event_type']}",
2353:                     course_code=courseCode,
2354:                     projection_keys=event["projection_keys"],
2355:                     changed_payload=event,
2356:                     session_ids=[event["session_id"]],
2357:                     version=event["version"],
2358:                 ),
2359:             )
2360:         while True:
2361:             await websocket.receive_text()
2362:     except HTTPException:
2363:         await websocket.close(code=1008)
2364:     except WebSocketDisconnect:
2365:         pass
2366:     finally:
2367:         attendance_broker.disconnect(courseCode, websocket)
```

## G.10 Backend attendance bundle open/check-in core

Source: `Backend/app/attendance.py:718-850`

```py
0718: def open_attendance_sessions_batch(
0719:     db: Session,
0720:     professor_id: str,
0721:     course_code: str,
0722:     *,
0723:     projection_keys: list[str],
0724:     mode: Literal["manual", "smart", "canceled"],
0725: ) -> dict[str, Any]:
0726:     if mode not in SESSION_MODES:
0727:         raise attendance_api_error(400, "INVALID_SESSION_MODE", "invalid attendance session mode", {"mode": mode})
0728:     professor, course = get_owned_course(db, professor_id, course_code)
0729:     slot_map = _projection_slot_lookup(db, course, professor)
0730:     now = _utcnow()
0731:     deduped_projection_keys = list(dict.fromkeys(projection_keys))
0732:     if mode == "smart":
0733:         requested_key_set = set(deduped_projection_keys)
0734:         for requested_projection_key in list(deduped_projection_keys):
0735:             active_manual_session = db.scalar(
0736:                 select(AttendanceSession)
0737:                 .outerjoin(AttendanceSessionSlot, AttendanceSessionSlot.attendance_session_id == AttendanceSession.id)
0738:                 .where(
0739:                     AttendanceSession.status == "active",
0740:                     AttendanceSession.mode == "manual",
0741:                     or_(
0742:                         AttendanceSession.projection_key == requested_projection_key,
0743:                         AttendanceSessionSlot.projection_key == requested_projection_key,
0744:                     ),
0745:                 )
0746:                 .order_by(desc(AttendanceSession.opened_at), desc(AttendanceSession.id))
0747:             )
0748:             if active_manual_session is None:
0749:                 continue
0750:             for assignment in _session_assignments_for_one(db, active_manual_session):
0751:                 if assignment.projection_key not in requested_key_set:
0752:                     deduped_projection_keys.append(assignment.projection_key)
0753:                     requested_key_set.add(assignment.projection_key)
0754:     results: list[dict[str, Any]] = []
0755:     valid_assignments: list[SessionSlotAssignment] = []
0756:     target_session_date: date | None = None
0757:     previous_sessions: dict[str, AttendanceSession | None] = {}
0758:     replaced_manual_sessions: dict[int, AttendanceSession] = {}
0759:
0760:     for order, projection_key in enumerate(deduped_projection_keys):
0761:         slot = slot_map.get(projection_key)
0762:         if slot is None:
0763:             results.append(
0764:                 {
0765:                     "projection_key": projection_key,
0766:                     "success": False,
0767:                     "code": "SESSION_SLOT_INVALID",
0768:                     "message": "projection key is not a valid slot for the course",
0769:                     "session_id": None,
0770:                     "resulting_slot_state": "unchecked",
0771:                 }
0772:             )
0773:             continue
0774:         if target_session_date is None:
0775:             target_session_date = slot.session_date
0776:         elif slot.session_date != target_session_date:
0777:             results.append(
0778:                 {
0779:                     "projection_key": projection_key,
0780:                     "success": False,
0781:                     "code": "SESSION_SLOT_INVALID",
0782:                     "message": "batch attendance operations must stay within the same date",
0783:                     "session_id": None,
0784:                     "resulting_slot_state": "unchecked",
0785:                 }
0786:             )
0787:             continue
0788:
0789:         manual_session_to_replace: AttendanceSession | None = None
0790:         active_existing = db.scalar(
0791:             select(AttendanceSession)
0792:             .outerjoin(AttendanceSessionSlot, AttendanceSessionSlot.attendance_session_id == AttendanceSession.id)
0793:             .where(
0794:                 AttendanceSession.status == "active",
0795:                 or_(
0796:                     AttendanceSession.projection_key == projection_key,
0797:                     AttendanceSessionSlot.projection_key == projection_key,
0798:                 ),
0799:             )
0800:             .order_by(desc(AttendanceSession.opened_at), desc(AttendanceSession.id))
0801:         )
0802:         if active_existing is not None:
0803:             if mode == "smart" and active_existing.mode == "manual":
0804:                 manual_session_to_replace = active_existing
0805:             else:
0806:                 results.append(
0807:                     {
0808:                         "projection_key": projection_key,
0809:                         "success": False,
0810:                         "code": "SESSION_ALREADY_OPEN",
0811:                         "message": "an active session already exists for the projection key",
0812:                         "session_id": active_existing.id,
0813:                         "resulting_slot_state": _slot_state(active_existing),
0814:                     }
0815:                 )
0816:                 continue
0817:
0818:         classroom_id = db.scalar(select(Classroom.id).where(Classroom.classroom_code == slot.classroom_code))
0819:         if classroom_id is None:
0820:             results.append(
0821:                 {
0822:                     "projection_key": projection_key,
0823:                     "success": False,
0824:                     "code": "SESSION_SLOT_INVALID",
0825:                     "message": "projection slot classroom is missing",
0826:                     "session_id": None,
0827:                     "resulting_slot_state": "unchecked",
0828:                 }
0829:             )
0830:             continue
0831:
0832:         valid_assignments.append(
0833:             SessionSlotAssignment(
0834:                 attendance_session_id=0,
0835:                 projection_key=projection_key,
0836:                 classroom_id=classroom_id,
0837:                 session_date=slot.session_date,
0838:                 slot_start_at=slot.slot_start_at,
0839:                 slot_end_at=slot.slot_end_at,
0840:                 slot_order=order,
0841:             )
0842:         )
0843:         if manual_session_to_replace is not None:
0844:             replaced_manual_sessions[manual_session_to_replace.id] = manual_session_to_replace
0845:         previous_sessions[projection_key] = _latest_session_for_projection(db, projection_key)
0846:
0847:     if valid_assignments:
0848:         for replaced_session in replaced_manual_sessions.values():
0849:             replaced_session.status = "closed"
0850:             replaced_session.closed_at = now
```

## G.11 Backend student check-in with presence gate

Source: `Backend/app/attendance.py:1607-1815`

```py
1607: def _presence_eligibility_for_assignment(
1608:     db: Session,
1609:     presence_client: PresenceClient,
1610:     student: User,
1611:     course: Course,
1612:     assignment: SessionSlotAssignment,
1613:     registered_devices: list[dict[str, str]],
1614:     persist_log: bool = False,
1615:     release_connection_before_check: bool = True,
1616: ) -> dict[str, Any]:
1617:     classroom = db.scalar(select(Classroom).where(Classroom.id == assignment.classroom_id))
1618:     student_login_id = student.student_id or ""
1619:     course_code = course.course_code
1620:     if not registered_devices:
1621:         result = {
1622:             "eligible": False,
1623:             "reason_code": "DEVICE_NOT_REGISTERED",
1624:             "matched_device_mac": None,
1625:             "observed_at": None,
1626:             "snapshot_age_seconds": None,
1627:             "evidence": {},
1628:         }
1629:         if persist_log:
1630:             _persist_attendance_presence_log(db, student=student, course=course, assignment=assignment, result=result)
1631:         return result
1632:     resolved_classroom_code = classroom.classroom_code if classroom else ""
1633:     classroom_networks = [
1634:         {
1635:             "apId": network.ap_id,
1636:             "ssid": network.ssid,
1637:             "signalThresholdDbm": network.signal_threshold_dbm,
1638:         }
1639:         for network in db.scalars(select(ClassroomNetwork).where(ClassroomNetwork.classroom_id == assignment.classroom_id))
1640:     ]
1641:     if release_connection_before_check:
1642:         # The active-session listing path is read-only. Return its DB
1643:         # connection before waiting on PresenceService so dashboard/student
1644:         # polling cannot exhaust the backend pool during AP outages.
1645:         db.rollback()
1646:     try:
1647:         payload = presence_client.check_eligibility(
1648:             student_id=student_login_id,
1649:             course_id=course_code,
1650:             classroom_id=resolved_classroom_code,
1651:             purpose="attendance",
1652:             classroom_networks=classroom_networks,
1653:             registered_devices=registered_devices,
1654:         )
1655:     except HTTPException as exc:
1656:         if not is_presence_dependency_unavailable(exc):
1657:             raise
1658:         result = presence_dependency_unavailable_result(exc, classroom_id=resolved_classroom_code)
1659:         if persist_log:
1660:             _persist_attendance_presence_log(db, student=student, course=course, assignment=assignment, result=result)
1661:         return result
1662:     result = {
1663:         "eligible": bool(payload.get("eligible")),
1664:         "reason_code": payload.get("reasonCode", "UNKNOWN"),
1665:         "matched_device_mac": payload.get("matchedDeviceMac"),
1666:         "observed_at": payload.get("observedAt"),
1667:         "snapshot_age_seconds": payload.get("snapshotAgeSeconds"),
1668:         "evidence": payload.get("evidence", {}),
1669:     }
1670:     if persist_log:
1671:         _persist_attendance_presence_log(db, student=student, course=course, assignment=assignment, result=result)
1672:     return result
1673:
1674:
1675:
1676: def list_student_active_attendance_sessions(
1677:     db: Session,
1678:     presence_client: PresenceClient,
1679:     student_id: str,
1680:     course_code: str,
1681: ) -> dict[str, Any]:
1682:     student = get_student_user(db, student_id)
1683:     course = get_course_by_code(db, course_code)
1684:     ensure_student_enrolled(db, student.id, course.id, student_id, course_code)
1685:     expire_stale_attendance_sessions(db, course_code)
1686:     professor = db.scalar(select(User).where(User.id == course.professor_user_id)) or User(name="담당 교수", role="professor", password="", professor_id="")
1687:     slot_map = _projection_slot_lookup(db, course, professor)
1688:     sessions = db.scalars(
1689:         select(AttendanceSession)
1690:         .where(
1691:             AttendanceSession.course_id == course.id,
1692:             AttendanceSession.status == "active",
1693:             AttendanceSession.mode == "smart",
1694:         )
1695:         .order_by(AttendanceSession.session_date.asc(), AttendanceSession.slot_start_at.asc(), AttendanceSession.id.asc())
1696:     ).all()
1697:     assignments_by_session = _session_slot_assignments(db, sessions)
1698:     registered_devices = _registered_devices_payload(db, student)
1699:     serialized_sessions = []
1700:     for session in sessions:
1701:         assignments = assignments_by_session.get(session.id, [_fallback_session_assignment(session)])
1702:         eligibilities = [
1703:             {
1704:                 "projection_key": assignment.projection_key,
1705:                 "eligibility": _presence_eligibility_for_assignment(
1706:                     db,
1707:                     presence_client,
1708:                     student,
1709:                     course,
1710:                     assignment,
1711:                     registered_devices,
1712:                 ),
1713:             }
1714:             for assignment in assignments
1715:         ]
1716:         changed_or_present = [item for item in eligibilities if item["eligibility"]["eligible"]]
1717:         anchor_slot = slot_map.get(session.projection_key)
1718:         serialized_sessions.append(
1719:             {
1720:                 "session_id": session.id,
1721:                 "projection_key": session.projection_key,
1722:                 "projection_keys": [assignment.projection_key for assignment in assignments],
1723:                 "included_slots": [_serialize_assignment(slot_map, assignment) for assignment in assignments],
1724:                 "display_label": anchor_slot.display_label if anchor_slot else session.projection_key,
1725:                 "session_date": _serialize_date(session.session_date),
1726:                 "slot_start_at": _serialize_time(session.slot_start_at),
1727:                 "slot_end_at": _serialize_time(session.slot_end_at),
1728:                 "expires_at": _serialize_dt(session.expires_at),
1729:                 "can_check_in": bool(changed_or_present),
1730:                 "eligibility": {
1731:                     "eligible_slot_count": len(changed_or_present),
1732:                     "rejected_slot_count": len(eligibilities) - len(changed_or_present),
1733:                     "per_slot": eligibilities,
1734:                 },
1735:                 "version": session.latest_version,
1736:             }
1737:         )
1738:     return {
1739:         "course_code": course.course_code,
1740:         "student_id": student_id,
1741:         "sessions": serialized_sessions,
1742:     }
1743:
1744:
1745:
1746: def student_attendance_check_in(db: Session, presence_client: PresenceClient, student_id: str, session_id: int) -> dict[str, Any]:
1747:     student = get_student_user(db, student_id)
1748:     session = db.scalar(select(AttendanceSession).where(AttendanceSession.id == session_id))
1749:     if session is None:
1750:         raise attendance_api_error(404, "ATTENDANCE_SESSION_NOT_FOUND", "attendance session not found", {"session_id": session_id})
1751:     course = db.scalar(select(Course).where(Course.id == session.course_id))
1752:     if course is None:
1753:         raise attendance_api_error(404, "COURSE_NOT_FOUND", "course not found")
1754:     ensure_student_enrolled(db, student.id, course.id, student_id, course.course_code)
1755:     expire_stale_attendance_sessions(db, course.course_code)
1756:     db.refresh(session)
1757:     if session.mode != "smart" or session.status != "active":
1758:         raise attendance_api_error(409, "SESSION_NOT_OPEN", "smart attendance session is not open", {"session_id": session_id})
1759:
1760:     assignments = _session_assignments_for_one(db, session)
1761:     registered_devices = _registered_devices_payload(db, student)
1762:     now = _utcnow()
1763:     pending_audits: list[AttendanceStatusAuditLog] = []
1764:     changed_projection_keys: list[str] = []
1765:     already_present_count = 0
1766:     rejected_count = 0
1767:     per_slot_results: list[dict[str, Any]] = []
1768:     eligibility_results: list[tuple[SessionSlotAssignment, dict[str, Any]]] = []
1769:
1770:     for assignment in assignments:
1771:         eligibility = _presence_eligibility_for_assignment(
1772:             db,
1773:             presence_client,
1774:             student,
1775:             course,
1776:             assignment,
1777:             registered_devices,
1778:             persist_log=False,
1779:             release_connection_before_check=True,
1780:         )
1781:         eligibility_results.append((assignment, eligibility))
1782:
1783:     for assignment, eligibility in eligibility_results:
1784:         _persist_attendance_presence_log(db, student=student, course=course, assignment=assignment, result=eligibility)
1785:         if not eligibility["eligible"]:
1786:             rejected_count += 1
1787:             per_slot_results.append(
1788:                 {
1789:                     "projection_key": assignment.projection_key,
1790:                     "result": "rejected",
1791:                     "reason_code": eligibility["reason_code"],
1792:                     "eligibility": eligibility,
1793:                 }
1794:             )
1795:             continue
1796:
1797:         record = db.scalar(
1798:             select(AttendanceRecord).where(
1799:                 AttendanceRecord.attendance_session_id == session.id,
1800:                 AttendanceRecord.projection_key == assignment.projection_key,
1801:                 AttendanceRecord.student_user_id == student.id,
1802:             )
1803:         )
1804:         if record is not None and record.final_status == "present":
1805:             already_present_count += 1
1806:             per_slot_results.append(
1807:                 {
1808:                     "projection_key": assignment.projection_key,
1809:                     "result": "already-present",
1810:                     "reason_code": "OK",
1811:                     "eligibility": eligibility,
1812:                 }
1813:             )
1814:             continue
1815:
```

## G.12 Backend exam start/submit/answer service

Source: `Backend/app/services.py:1378-1605`

```py
1378: def start_student_exam(
1379:     *,
1380:     db: Session,
1381:     presence_client: PresenceClient,
1382:     student_id: str,
1383:     student_user_id: int,
1384:     course_code: str,
1385:     course_id: int,
1386:     exam_id: int,
1387: ) -> dict:
1388:     student_visible_statuses = ("published", "open", "closed")
1389:
1390:     exam = db.scalar(
1391:         select(Exam).where(
1392:             Exam.id == exam_id,
1393:             Exam.course_id == course_id,
1394:             Exam.status.in_(student_visible_statuses),
1395:         )
1396:     )
1397:     if exam is None:
1398:         raise HTTPException(
1399:             status_code=404,
1400:             detail={
1401:                 "code": "EXAM_NOT_FOUND",
1402:                 "message": "exam not found",
1403:                 "details": {"exam_id": exam_id},
1404:             },
1405:         )
1406:
1407:     existing = db.scalar(
1408:         select(ExamSubmission).where(
1409:             ExamSubmission.exam_id == exam.id,
1410:             ExamSubmission.student_user_id == student_user_id,
1411:             ExamSubmission.status == "in_progress",
1412:         )
1413:     )
1414:     if existing is not None:
1415:         return {
1416:             "submission_id": existing.id,
1417:             "attempt_no": existing.attempt_no,
1418:             "status": existing.status,
1419:             "started_at": existing.started_at,
1420:             "expires_at": existing.expires_at,
1421:             "idempotent": True,
1422:         }
1423:
1424:     now = datetime.now(UTC)
1425:     if exam.status not in {"published", "open"} or now < exam.starts_at or now >= exam.ends_at:
1426:         raise HTTPException(
1427:             status_code=409,
1428:             detail={
1429:                 "code": "EXAM_NOT_OPEN",
1430:                 "message": "exam is not open",
1431:                 "details": {"exam_id": exam.id, "status": exam.status},
1432:             },
1433:         )
1434:
1435:     if not exam.late_entry_allowed and now > exam.starts_at:
1436:         raise HTTPException(
1437:             status_code=409,
1438:             detail={
1439:                 "code": "EXAM_LATE_ENTRY_NOT_ALLOWED",
1440:                 "message": "late entry is not allowed for this exam",
1441:                 "details": {"exam_id": exam.id},
1442:             },
1443:         )
1444:
1445:     attempts_used = db.scalar(
1446:         select(func.count(ExamSubmission.id)).where(
1447:             ExamSubmission.exam_id == exam.id,
1448:             ExamSubmission.student_user_id == student_user_id,
1449:         )
1450:     ) or 0
1451:     if int(attempts_used) >= exam.max_attempts:
1452:         raise HTTPException(
1453:             status_code=409,
1454:             detail={
1455:                 "code": "EXAM_ATTEMPT_LIMIT_REACHED",
1456:                 "message": "exam attempt limit reached",
1457:                 "details": {"exam_id": exam.id, "attempts_used": int(attempts_used), "max_attempts": exam.max_attempts},
1458:             },
1459:         )
1460:
1461:     if exam.requires_presence:
1462:         eligibility = check_attendance_eligibility(
1463:             db=db,
1464:             presence_client=presence_client,
1465:             student_id=student_id,
1466:             course_id=course_code,
1467:             classroom_id=None,
1468:             purpose="exam",
1469:         )
1470:         if not eligibility["eligible"]:
1471:             raise HTTPException(
1472:                 status_code=403,
1473:                 detail={
1474:                     "code": "PRESENCE_INELIGIBLE",
1475:                     "message": "presence eligibility is required for this exam",
1476:                     "details": {
1477:                         "exam_id": exam.id,
1478:                         "reason_code": eligibility["reason_code"],
1479:                         "evidence": eligibility.get("evidence", {}),
1480:                     },
1481:                 },
1482:             )
1483:
1484:     expires_at = min(now + timedelta(minutes=exam.duration_minutes), exam.ends_at)
1485:     effective_seconds = max(0.0, (expires_at - now).total_seconds())
1486:     effective_time_limit_minutes = max(1, math.ceil(effective_seconds / 60)) if effective_seconds > 0 else 1
1487:     submission = ExamSubmission(
1488:         exam_id=exam.id,
1489:         student_user_id=student_user_id,
1490:         attempt_no=int(attempts_used) + 1,
1491:         status="in_progress",
1492:         started_at=now,
1493:         expires_at=expires_at,
1494:         time_limit_snapshot_minutes=effective_time_limit_minutes,
1495:     )
1496:     db.add(submission)
1497:     db.commit()
1498:     db.refresh(submission)
1499:     return {
1500:         "submission_id": submission.id,
1501:         "attempt_no": submission.attempt_no,
1502:         "status": submission.status,
1503:         "started_at": submission.started_at,
1504:         "expires_at": submission.expires_at,
1505:         "idempotent": False,
1506:     }
1507:
1508:
1509: def submit_student_exam(
1510:     *,
1511:     db: Session,
1512:     student_user_id: int,
1513:     course_id: int,
1514:     exam_id: int,
1515:     payload: dict,
1516: ) -> dict:
1517:     student_visible_statuses = ("published", "open", "closed")
1518:     exam = db.scalar(
1519:         select(Exam).where(
1520:             Exam.id == exam_id,
1521:             Exam.course_id == course_id,
1522:             Exam.status.in_(student_visible_statuses),
1523:         )
1524:     )
1525:     if exam is None:
1526:         raise HTTPException(
1527:             status_code=404,
1528:             detail={
1529:                 "code": "EXAM_NOT_FOUND",
1530:                 "message": "exam not found",
1531:                 "details": {"exam_id": exam_id},
1532:             },
1533:         )
1534:
1535:     submission = db.scalar(
1536:         select(ExamSubmission).where(
1537:             ExamSubmission.exam_id == exam.id,
1538:             ExamSubmission.student_user_id == student_user_id,
1539:             ExamSubmission.status == "in_progress",
1540:         )
1541:     )
1542:     if submission is None:
1543:         raise HTTPException(
1544:             status_code=404,
1545:             detail={
1546:                 "code": "EXAM_SUBMISSION_NOT_FOUND",
1547:                 "message": "active exam submission not found",
1548:                 "details": {"exam_id": exam.id},
1549:             },
1550:         )
1551:
1552:     answers = payload.get("answers") or []
1553:     answer_by_question = {answer["question_id"]: answer for answer in answers}
1554:     now = datetime.now(UTC)
1555:     if submission.expires_at is not None and now > submission.expires_at and not exam.auto_submit_enabled:
1556:         raise HTTPException(
1557:             status_code=409,
1558:             detail={
1559:                 "code": "EXAM_SUBMISSION_ALREADY_FINALIZED",
1560:                 "message": "submission can no longer be finalized manually",
1561:                 "details": {"submission_id": submission.id, "status": submission.status},
1562:             },
1563:         )
1564:
1565:     result = _finalize_exam_submission(
1566:         db=db,
1567:         exam=exam,
1568:         submission=submission,
1569:         final_status="auto_submitted" if submission.expires_at is not None and now > submission.expires_at else "submitted",
1570:         reject_missing_required=not (submission.expires_at is not None and now > submission.expires_at),
1571:         payload_answers=answer_by_question,
1572:     )
1573:     db.commit()
1574:     db.refresh(submission)
1575:     return result
1576:
1577:
1578: def save_student_exam_answer(
1579:     *,
1580:     db: Session,
1581:     student_user_id: int,
1582:     course_id: int,
1583:     exam_id: int,
1584:     submission_id: int,
1585:     question_id: int,
1586:     payload: dict,
1587: ) -> dict:
1588:     student_visible_statuses = ("published", "open", "closed")
1589:     exam = db.scalar(
1590:         select(Exam).where(
1591:             Exam.id == exam_id,
1592:             Exam.course_id == course_id,
1593:             Exam.status.in_(student_visible_statuses),
1594:         )
1595:     )
1596:     if exam is None:
1597:         raise HTTPException(
1598:             status_code=404,
1599:             detail={
1600:                 "code": "EXAM_NOT_FOUND",
1601:                 "message": "exam not found",
1602:                 "details": {"exam_id": exam_id},
1603:             },
1604:         )
1605:
```

## G.13 Backend attendance CSV export service

Source: `Backend/app/services.py:2007-2115`

```py
2007: def _attendance_csv_content(headers: list[str], rows: list[list[str | int]]) -> bytes:
2008:     buffer = StringIO()
2009:     buffer.write("\ufeff")
2010:     writer = csv.writer(buffer)
2011:     writer.writerow(headers)
2012:     writer.writerows(rows)
2013:     return buffer.getvalue().encode("utf-8")
2014:
2015:
2016: def create_attendance_csv_export(db: Session, *, professor_id: str, course_code: str, export_type: str = "attendance_summary_csv") -> dict:
2017:     professor = db.scalar(select(User).where(User.professor_id == professor_id, User.role == "professor"))
2018:     course = db.scalar(select(Course).where(Course.course_code == course_code, Course.professor_user_id == getattr(professor, "id", None)))
2019:     if professor is None or course is None:
2020:         raise HTTPException(
2021:             status_code=404,
2022:             detail={"code": "COURSE_NOT_FOUND", "message": "course not found", "details": {"course_code": course_code}},
2023:         )
2024:     variant = ATTENDANCE_CSV_EXPORT_TYPES.get(export_type)
2025:     if variant is None:
2026:         raise HTTPException(
2027:             status_code=400,
2028:             detail={
2029:                 "code": "INVALID_REPORT_EXPORT_TYPE",
2030:                 "message": "invalid attendance report export type",
2031:                 "details": {"export_type": export_type},
2032:             },
2033:         )
2034:     generated_at = datetime.now(UTC)
2035:     csv_table = build_professor_attendance_csv_table(db, professor_id, course_code, variant=variant)
2036:     filename = f"attendance-{variant}-{course_code}-{generated_at.strftime('%Y%m%d%H%M%S')}.csv"
2037:     written = _store_bytes_object(
2038:         content=_attendance_csv_content(csv_table["headers"], csv_table["rows"]),
2039:         filename=filename,
2040:         mime_type="text/csv; charset=utf-8",
2041:         prefix=f"reports/attendance/{course_code}/{generated_at:%Y/%m}",
2042:     )
2043:     report = ReportExport(
2044:         course_id=course.id,
2045:         requested_by_user_id=professor.id,
2046:         report_domain="attendance",
2047:         export_format="csv",
2048:         status="ready",
2049:         generated_at=generated_at,
2050:         **written,
2051:     )
2052:     db.add(report)
2053:     db.commit()
2054:     db.refresh(report)
2055:     return _report_export_payload(report, course.course_code)
2056:
2057:
2058: def _report_export_payload(report: ReportExport, course_code: str) -> dict:
2059:     return {
2060:         "id": report.id,
2061:         "original_filename": report.original_filename,
2062:         "mime_type": report.mime_type,
2063:         "file_size_bytes": report.file_size_bytes,
2064:         "uploaded_at": report.created_at,
2065:         "storage_provider": report.storage_provider,
2066:         "bucket_name": report.bucket_name,
2067:         "export_type": f"{report.report_domain}_{report.export_format}",
2068:         "course_code": course_code,
2069:         "status": report.status,
2070:         "generated_at": report.generated_at,
2071:     }
2072:
2073:
2074: def list_attendance_csv_exports(db: Session, *, professor_id: str, course_code: str) -> list[dict]:
2075:     professor = db.scalar(select(User).where(User.professor_id == professor_id, User.role == "professor"))
2076:     course = db.scalar(select(Course).where(Course.course_code == course_code, Course.professor_user_id == getattr(professor, "id", None)))
2077:     if professor is None or course is None:
2078:         raise HTTPException(
2079:             status_code=404,
2080:             detail={"code": "COURSE_NOT_FOUND", "message": "course not found", "details": {"course_code": course_code}},
2081:         )
2082:     reports = list(
2083:         db.scalars(
2084:             select(ReportExport)
2085:             .where(ReportExport.course_id == course.id, ReportExport.report_domain == "attendance")
2086:             .order_by(ReportExport.created_at.desc(), ReportExport.id.desc())
2087:         )
2088:     )
2089:     return [_report_export_payload(report, course.course_code) for report in reports]
2090:
2091:
2092: def get_report_export_download(db: Session, *, professor_id: str, course_code: str, export_id: int) -> ObjectDownload:
2093:     professor = db.scalar(select(User).where(User.professor_id == professor_id, User.role == "professor"))
2094:     course = db.scalar(select(Course).where(Course.course_code == course_code, Course.professor_user_id == getattr(professor, "id", None)))
2095:     if professor is None or course is None:
2096:         raise HTTPException(
2097:             status_code=404,
2098:             detail={"code": "COURSE_NOT_FOUND", "message": "course not found", "details": {"course_code": course_code}},
2099:         )
2100:     report = db.scalar(select(ReportExport).where(ReportExport.id == export_id, ReportExport.course_id == course.id))
2101:     if report is None:
2102:         raise HTTPException(
2103:             status_code=404,
2104:             detail={"code": "REPORT_EXPORT_NOT_FOUND", "message": "report export not found", "details": {"export_id": export_id}},
2105:         )
2106:     return ObjectDownload(
2107:         storage_key=report.storage_key,
2108:         filename=report.original_filename,
2109:         media_type=report.mime_type,
2110:         file_size_bytes=report.file_size_bytes,
2111:         storage_provider=report.storage_provider,
2112:         bucket_name=report.bucket_name,
2113:     )
2114:
2115:
```

## G.14 PresenceService HTTP endpoints

Source: `PresenceService/app/main.py:36-129`

```py
0036:     @app.get("/health", response_model=HealthResponse)
0037:     def health() -> HealthResponse:
0038:         service = get_presence_service()
0039:         return HealthResponse(
0040:             status="ok",
0041:             redisConnected=service.cache.ping(),
0042:             snapshotTtlSeconds=settings.snapshot_ttl_seconds,
0043:         )
0044:
0045:     @app.get("/snapshots/classrooms/{classroom_id}", response_model=SnapshotEnvelope)
0046:     def get_snapshot(classroom_id: str) -> SnapshotEnvelope:
0047:         service = get_presence_service()
0048:         try:
0049:             snapshot, cache_hit = service.get_or_refresh_snapshot(classroom_id)
0050:         except KeyError as exc:
0051:             raise HTTPException(status_code=404, detail="CLASSROOM_NOT_MAPPED") from exc
0052:         return SnapshotEnvelope(cacheHit=cache_hit, snapshot=snapshot)
0053:
0054:
0055:
0056:     @app.get("/collector/aps/health")
0057:     def collector_health() -> dict:
0058:         service = get_presence_service()
0059:         try:
0060:             return service.collector_health()
0061:         except RegistryUnavailableError as exc:
0062:             raise registry_unavailable(exc) from exc
0063:
0064:     @app.post("/collector/aps/{collector_ap_id}/snapshot", response_model=CollectorIngestResponse)
0065:     def ingest_collector_snapshot(
0066:         collector_ap_id: str,
0067:         payload: dict[str, Any] = Body(...),
0068:         authorization: str | None = Header(default=None, alias="Authorization"),
0069:         x_collector_nonce: str | None = Header(default=None, alias="X-Collector-Nonce"),
0070:         x_collector_timestamp: str | None = Header(default=None, alias="X-Collector-Timestamp"),
0071:     ) -> CollectorIngestResponse:
0072:         service = get_presence_service()
0073:         try:
0074:             return service.ingest_collector_snapshot(
0075:                 collector_ap_id=collector_ap_id,
0076:                 authorization=authorization,
0077:                 request=CollectorSnapshotRequest.model_validate(payload),
0078:                 nonce=x_collector_nonce,
0079:                 timestamp_header=x_collector_timestamp,
0080:             )
0081:         except PermissionError as exc:
0082:             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"code": str(exc), "message": "collector authentication failed"}) from exc
0083:         except RegistryUnavailableError as exc:
0084:             raise registry_unavailable(exc) from exc
0085:         except ValueError as exc:
0086:             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"code": str(exc), "message": "collector snapshot rejected"}) from exc
0087:
0088:     @app.post("/eligibility/check", response_model=EligibilityResponse)
0089:     def check_eligibility(payload: dict[str, Any] = Body(...)) -> EligibilityResponse:
0090:         service = get_presence_service()
0091:         try:
0092:             return service.evaluate_eligibility(EligibilityRequest.model_validate(payload))
0093:         except RegistryUnavailableError as exc:
0094:             raise registry_unavailable(exc) from exc
0095:         except ValueError as exc:
0096:             raise HTTPException(status_code=400, detail=str(exc)) from exc
0097:         except LookupError as exc:
0098:             raise HTTPException(status_code=404, detail=str(exc)) from exc
0099:
0100:     @app.get("/admin/dummy/classrooms/{classroom_id}/snapshot", response_model=AdminSnapshotEnvelope)
0101:     def get_admin_snapshot(classroom_id: str, refresh: bool = False, source: str = "auto") -> AdminSnapshotEnvelope:
0102:         service = get_presence_service()
0103:         try:
0104:             return service.get_admin_snapshot(classroom_id, force_refresh=refresh, source=source)
0105:         except RegistryUnavailableError as exc:
0106:             raise registry_unavailable(exc) from exc
0107:         except KeyError as exc:
0108:             raise HTTPException(status_code=404, detail="CLASSROOM_NOT_MAPPED") from exc
0109:         except ValueError as exc:
0110:             raise HTTPException(status_code=400, detail=str(exc)) from exc
0111:
0112:     @app.post("/admin/dummy/classrooms/{classroom_id}/overlay", response_model=AdminSnapshotEnvelope)
0113:     def apply_admin_overlay(classroom_id: str, payload: dict[str, Any] = Body(...)) -> AdminSnapshotEnvelope:
0114:         service = get_presence_service()
0115:         try:
0116:             return service.apply_overlay(classroom_id, DummyOverlayMutationRequest.model_validate(payload))
0117:         except KeyError as exc:
0118:             raise HTTPException(status_code=404, detail="CLASSROOM_NOT_MAPPED") from exc
0119:         except ValueError as exc:
0120:             raise HTTPException(status_code=400, detail=str(exc)) from exc
0121:         except TimeoutError as exc:
0122:             raise HTTPException(status_code=409, detail=str(exc)) from exc
0123:
0124:     @app.post("/admin/dummy/classrooms/{classroom_id}/overlay/reset", response_model=AdminSnapshotEnvelope)
0125:     def reset_admin_overlay(classroom_id: str) -> AdminSnapshotEnvelope:
0126:         service = get_presence_service()
0127:         try:
0128:             return service.reset_overlay(classroom_id)
0129:         except KeyError as exc:
```

## G.15 PresenceService collector/cache/eligibility core

Source: `PresenceService/app/service.py:86-170`

```py
0086:     def ingest_collector_snapshot(
0087:         self,
0088:         *,
0089:         collector_ap_id: str,
0090:         authorization: str | None,
0091:         request: CollectorSnapshotRequest,
0092:         nonce: str | None,
0093:         timestamp_header: str | None,
0094:     ) -> CollectorIngestResponse:
0095:         if request.collector_ap_id != collector_ap_id:
0096:             raise ValueError("COLLECTOR_AP_ID_MISMATCH")
0097:         registry = self._registry()
0098:         if registry is None:
0099:             raise RuntimeError("COLLECTOR_REGISTRY_UNAVAILABLE")
0100:         ap = registry.get_access_point(collector_ap_id)
0101:         if ap is None or ap.status != "active":
0102:             raise PermissionError("COLLECTOR_AP_UNKNOWN")
0103:         if not ap.token_hash or ap.token_revoked_at:
0104:             raise PermissionError("COLLECTOR_TOKEN_REVOKED")
0105:         token = self._bearer_token(authorization)
0106:         if self._hash_ap_token(token) != ap.token_hash:
0107:             raise PermissionError("COLLECTOR_TOKEN_INVALID")
0108:
0109:         timestamp = request.observed_at
0110:         if timestamp_header:
0111:             try:
0112:                 timestamp = datetime.fromisoformat(timestamp_header.replace("Z", "+00:00"))
0113:             except ValueError as exc:
0114:                 raise ValueError("COLLECTOR_TIMESTAMP_INVALID") from exc
0115:         if timestamp.tzinfo is None:
0116:             timestamp = timestamp.replace(tzinfo=UTC)
0117:         age = abs((datetime.now(UTC) - timestamp.astimezone(UTC)).total_seconds())
0118:         if age > self.collector_timestamp_window_seconds:
0119:             raise ValueError("COLLECTOR_TIMESTAMP_STALE")
0120:
0121:         if nonce and not self.cache.remember_collector_nonce(collector_ap_id, nonce, self.collector_timestamp_window_seconds):
0122:             raise ValueError("COLLECTOR_NONCE_REPLAY")
0123:
0124:         iface_registry = {interface.interface_id: interface for interface in ap.interfaces}
0125:         accepted_interfaces = []
0126:         for interface in request.interfaces:
0127:             registry_interface = iface_registry.get(interface.interface_id)
0128:             if registry_interface is None:
0129:                 continue
0130:             if request.diagnostic_classroom_id and request.diagnostic_classroom_id != registry_interface.classroom_id:
0131:                 raise ValueError("COLLECTOR_CLASSROOM_MISMATCH")
0132:             accepted_interfaces.append(
0133:                 {
0134:                     "interfaceId": registry_interface.interface_id,
0135:                     "classroomId": registry_interface.classroom_id,
0136:                     "apId": registry_interface.classroom_network_ap_id,
0137:                     "ssid": interface.ssid or registry_interface.ssid,
0138:                     "bssid": interface.bssid or registry_interface.bssid,
0139:                     "stations": [station.model_dump(mode="json", by_alias=True) for station in interface.stations],
0140:                 }
0141:             )
0142:         if not accepted_interfaces:
0143:             raise ValueError("COLLECTOR_INTERFACE_NOT_MAPPED")
0144:
0145:         payload = {
0146:             "collectorApId": collector_ap_id,
0147:             "observedAt": request.observed_at.astimezone(UTC).isoformat(),
0148:             "interfaces": accepted_interfaces,
0149:         }
0150:         self.cache.set_collector_snapshot(collector_ap_id, payload, self.collector_offline_after_seconds)
0151:         return CollectorIngestResponse(
0152:             accepted=True,
0153:             collectorApId=collector_ap_id,
0154:             acceptedInterfaceCount=len(accepted_interfaces),
0155:             stationCount=sum(len(interface["stations"]) for interface in accepted_interfaces),
0156:             observedAt=request.observed_at,
0157:         )
0158:
0159:     def _collector_snapshot_for_classroom(
0160:         self,
0161:         classroom_id: str,
0162:         *,
0163:         allow_stale_registry: bool = False,
0164:     ) -> tuple[ClassroomSnapshot | None, bool] | None:
0165:         registry = self._registry(allow_stale=allow_stale_registry)
0166:         if registry is None:
0167:             return None
0168:         mappings = registry.classroom_mappings(classroom_id)
0169:         if not mappings:
0170:             return None
```

## G.16 PresenceService eligibility evaluation

Source: `PresenceService/app/service.py:548-640`

```py
0548:     def evaluate_eligibility(self, request: EligibilityRequest) -> EligibilityResponse:
0549:         if not request.registered_devices:
0550:             raise ValueError("DEVICE_NOT_REGISTERED")
0551:
0552:         collector_snapshot = self._collector_snapshot_for_classroom(request.classroom_id)
0553:         if collector_snapshot is not None:
0554:             snapshot, cache_hit = collector_snapshot
0555:             if snapshot is None:
0556:                 return self._ap_offline_response(request)
0557:         else:
0558:             try:
0559:                 snapshot, cache_hit = self.get_or_refresh_snapshot(request.classroom_id)
0560:             except KeyError as exc:
0561:                 raise LookupError("CLASSROOM_NOT_MAPPED") from exc
0562:
0563:         matched_station: StationObservation | None = None
0564:         matched_ap_ids: list[str] = []
0565:         matched_threshold: int | None = None
0566:         saw_matching_device = False
0567:         strongest_seen_station: StationObservation | None = None
0568:         strongest_seen_ap_id: str | None = None
0569:         device_macs = {normalize_mac(device.mac_address) for device in request.registered_devices}
0570:         threshold_by_ap = {
0571:             network.ap_id: self.resolve_signal_threshold(network)
0572:             for network in request.classroom_networks
0573:         }
0574:
0575:         for ap in snapshot.aps:
0576:             for station in ap.stations:
0577:                 if station.mac_address not in device_macs:
0578:                     continue
0579:                 saw_matching_device = True
0580:                 if strongest_seen_station is None or station.signal_dbm > strongest_seen_station.signal_dbm:
0581:                     strongest_seen_station = station
0582:                     strongest_seen_ap_id = ap.ap_id
0583:                 threshold = threshold_by_ap.get(ap.ap_id, -65)
0584:                 if station.associated and station.signal_dbm >= threshold:
0585:                     matched_station = station
0586:                     matched_ap_ids.append(ap.ap_id)
0587:                     matched_threshold = threshold
0588:                     break
0589:             if matched_station:
0590:                 break
0591:
0592:         age_seconds = max(0, int((datetime.now(UTC) - snapshot.observed_at).total_seconds()))
0593:
0594:         if matched_station is None and not saw_matching_device:
0595:             return EligibilityResponse(
0596:                 eligible=False,
0597:                 reasonCode="DEVICE_NOT_PRESENT",
0598:                 matchedDeviceMac=None,
0599:                 observedAt=snapshot.observed_at,
0600:                 snapshotAgeSeconds=age_seconds,
0601:                 evidence=EligibilityEvidence(
0602:                     classroomId=request.classroom_id,
0603:                     matchedApIds=[],
0604:                     stationCount=sum(len(ap.stations) for ap in snapshot.aps),
0605:                     signalDbm=None,
0606:                     signalThresholdDbm=None,
0607:                     associated=None,
0608:                     authenticated=None,
0609:                     authorized=None,
0610:                     cacheHit=cache_hit,
0611:                 ),
0612:             )
0613:
0614:         if matched_station is None:
0615:             fallback_threshold = threshold_by_ap.get(strongest_seen_ap_id, -65 if strongest_seen_ap_id else None)
0616:             return EligibilityResponse(
0617:                 eligible=False,
0618:                 reasonCode="NETWORK_NOT_ELIGIBLE",
0619:                 matchedDeviceMac=strongest_seen_station.mac_address if strongest_seen_station else None,
0620:                 observedAt=snapshot.observed_at,
0621:                 snapshotAgeSeconds=age_seconds,
0622:                 evidence=EligibilityEvidence(
0623:                     classroomId=request.classroom_id,
0624:                     matchedApIds=[strongest_seen_ap_id] if strongest_seen_ap_id else [],
0625:                     stationCount=sum(len(ap.stations) for ap in snapshot.aps),
0626:                     signalDbm=strongest_seen_station.signal_dbm if strongest_seen_station else None,
0627:                     signalThresholdDbm=fallback_threshold,
0628:                     associated=strongest_seen_station.associated if strongest_seen_station else None,
0629:                     authenticated=strongest_seen_station.authenticated if strongest_seen_station else None,
0630:                     authorized=strongest_seen_station.authorized if strongest_seen_station else None,
0631:                     cacheHit=cache_hit,
0632:                 ),
0633:             )
0634:
0635:         return EligibilityResponse(
0636:             eligible=True,
0637:             reasonCode="OK",
0638:             matchedDeviceMac=matched_station.mac_address,
0639:             observedAt=snapshot.observed_at,
0640:             snapshotAgeSeconds=age_seconds,
```

# H. DB schema excerpt

## H.1 users/classrooms/courses/enrollments/schedules/notices

Source: `DB/postgres/init/001_schema.sql:1-59`

```sql
0001: CREATE TABLE IF NOT EXISTS users (
0002:     id BIGSERIAL PRIMARY KEY,
0003:     student_id VARCHAR(32) UNIQUE,
0004:     professor_id VARCHAR(32) UNIQUE,
0005:     admin_id VARCHAR(32) UNIQUE,
0006:     name VARCHAR(120) NOT NULL,
0007:     role VARCHAR(20) NOT NULL CHECK (role IN ('student', 'professor', 'admin')),
0008:     password VARCHAR(120) NOT NULL,
0009:     created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
0010:     updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
0011: );
0012:
0013: CREATE TABLE IF NOT EXISTS classrooms (
0014:     id BIGSERIAL PRIMARY KEY,
0015:     classroom_code VARCHAR(32) NOT NULL UNIQUE,
0016:     name VARCHAR(120) NOT NULL,
0017:     building VARCHAR(120),
0018:     floor_label VARCHAR(32),
0019:     created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
0020:     updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
0021: );
0022:
0023: CREATE TABLE IF NOT EXISTS courses (
0024:     id BIGSERIAL PRIMARY KEY,
0025:     course_code VARCHAR(32) NOT NULL UNIQUE,
0026:     title VARCHAR(200) NOT NULL,
0027:     professor_user_id BIGINT REFERENCES users(id),
0028:     created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
0029:     updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
0030: );
0031:
0032: CREATE TABLE IF NOT EXISTS course_enrollments (
0033:     id BIGSERIAL PRIMARY KEY,
0034:     course_id BIGINT NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
0035:     student_user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
0036:     status VARCHAR(20) NOT NULL DEFAULT 'active',
0037:     created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
0038:     UNIQUE (course_id, student_user_id)
0039: );
0040:
0041: CREATE TABLE IF NOT EXISTS course_schedules (
0042:     id BIGSERIAL PRIMARY KEY,
0043:     course_id BIGINT NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
0044:     classroom_id BIGINT NOT NULL REFERENCES classrooms(id) ON DELETE CASCADE,
0045:     day_of_week SMALLINT NOT NULL CHECK (day_of_week BETWEEN 0 AND 6),
0046:     starts_at TIME NOT NULL,
0047:     ends_at TIME NOT NULL,
0048:     created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
0049: );
0050:
0051: CREATE TABLE IF NOT EXISTS notices (
0052:     id BIGSERIAL PRIMARY KEY,
0053:     course_id BIGINT REFERENCES courses(id) ON DELETE CASCADE,
0054:     author_user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
0055:     title VARCHAR(200) NOT NULL,
0056:     body TEXT NOT NULL,
0057:     created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
0058: );
0059:
```

## H.2 classroom networks / devices / presence logs / refresh sessions

Source: `DB/postgres/init/001_schema.sql:60-115`

```sql
0060: CREATE TABLE IF NOT EXISTS classroom_networks (
0061:     id BIGSERIAL PRIMARY KEY,
0062:     classroom_id BIGINT NOT NULL REFERENCES classrooms(id) ON DELETE CASCADE,
0063:     ap_id VARCHAR(64) NOT NULL,
0064:     ssid VARCHAR(120) NOT NULL,
0065:     gateway_host VARCHAR(120),
0066:     signal_threshold_dbm INTEGER,
0067:     collection_mode VARCHAR(40) NOT NULL DEFAULT 'openwrt-ssh',
0068:     created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
0069:     UNIQUE (classroom_id, ap_id)
0070: );
0071:
0072: CREATE TABLE IF NOT EXISTS registered_devices (
0073:     id BIGSERIAL PRIMARY KEY,
0074:     user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
0075:     label VARCHAR(120),
0076:     mac_address VARCHAR(17) NOT NULL UNIQUE,
0077:     status VARCHAR(20) NOT NULL DEFAULT 'active',
0078:     created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
0079:     updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
0080: );
0081:
0082: CREATE INDEX IF NOT EXISTS idx_registered_devices_user_id
0083:     ON registered_devices (user_id);
0084:
0085: CREATE TABLE IF NOT EXISTS presence_eligibility_logs (
0086:     id BIGSERIAL PRIMARY KEY,
0087:     student_user_id BIGINT REFERENCES users(id),
0088:     course_id BIGINT REFERENCES courses(id),
0089:     classroom_id BIGINT REFERENCES classrooms(id),
0090:     purpose VARCHAR(20) NOT NULL,
0091:     eligible BOOLEAN NOT NULL,
0092:     reason_code VARCHAR(64) NOT NULL,
0093:     matched_device_mac VARCHAR(17),
0094:     evidence JSONB NOT NULL DEFAULT '{}'::jsonb,
0095:     observed_at TIMESTAMPTZ,
0096:     snapshot_age_seconds INTEGER,
0097:     created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
0098: );
0099:
0100: CREATE TABLE IF NOT EXISTS refresh_sessions (
0101:     id BIGSERIAL PRIMARY KEY,
0102:     session_key VARCHAR(128) NOT NULL UNIQUE,
0103:     user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
0104:     current_token_hash VARCHAR(64) NOT NULL,
0105:     expires_at TIMESTAMPTZ NOT NULL,
0106:     revoked_at TIMESTAMPTZ,
0107:     replay_detected_at TIMESTAMPTZ,
0108:     last_rotated_at TIMESTAMPTZ,
0109:     created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
0110:     updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
0111: );
0112:
0113: CREATE INDEX IF NOT EXISTS idx_refresh_sessions_user_id
0114:     ON refresh_sessions (user_id);
0115:
```

## H.3 attendance sessions / slots / records / audit / AP registry

Source: `DB/postgres/init/001_schema.sql:116-223`

```sql
0116: CREATE TABLE IF NOT EXISTS attendance_sessions (
0117:     id BIGSERIAL PRIMARY KEY,
0118:     projection_key VARCHAR(255) NOT NULL,
0119:     course_id BIGINT NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
0120:     classroom_id BIGINT NOT NULL REFERENCES classrooms(id) ON DELETE CASCADE,
0121:     session_date DATE NOT NULL,
0122:     slot_start_at TIME NOT NULL,
0123:     slot_end_at TIME NOT NULL,
0124:     mode VARCHAR(16) NOT NULL CHECK (mode IN ('manual', 'smart', 'canceled')),
0125:     status VARCHAR(16) NOT NULL CHECK (status IN ('active', 'closed', 'expired', 'canceled')),
0126:     opened_by_user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
0127:     opened_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
0128:     closed_at TIMESTAMPTZ,
0129:     expires_at TIMESTAMPTZ,
0130:     latest_version INTEGER NOT NULL DEFAULT 0,
0131:     created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
0132:     updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
0133: );
0134:
0135: CREATE TABLE IF NOT EXISTS attendance_session_slots (
0136:     id BIGSERIAL PRIMARY KEY,
0137:     attendance_session_id BIGINT NOT NULL REFERENCES attendance_sessions(id) ON DELETE CASCADE,
0138:     projection_key VARCHAR(255) NOT NULL,
0139:     classroom_id BIGINT NOT NULL REFERENCES classrooms(id) ON DELETE CASCADE,
0140:     session_date DATE NOT NULL,
0141:     slot_start_at TIME NOT NULL,
0142:     slot_end_at TIME NOT NULL,
0143:     slot_order INTEGER NOT NULL,
0144:     created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
0145:     UNIQUE (attendance_session_id, projection_key)
0146: );
0147:
0148: CREATE TABLE IF NOT EXISTS attendance_records (
0149:     id BIGSERIAL PRIMARY KEY,
0150:     attendance_session_id BIGINT NOT NULL REFERENCES attendance_sessions(id) ON DELETE CASCADE,
0151:     projection_key VARCHAR(255) NOT NULL,
0152:     student_user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
0153:     final_status VARCHAR(16) NOT NULL CHECK (final_status IN ('present', 'absent', 'late', 'official', 'sick')),
0154:     attendance_reason VARCHAR(500),
0155:     finalized_by_user_id BIGINT REFERENCES users(id) ON DELETE SET NULL,
0156:     finalized_at TIMESTAMPTZ,
0157:     created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
0158:     updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
0159:     UNIQUE (attendance_session_id, projection_key, student_user_id)
0160: );
0161:
0162: CREATE TABLE IF NOT EXISTS attendance_status_audit_logs (
0163:     id BIGSERIAL PRIMARY KEY,
0164:     attendance_session_id BIGINT NOT NULL REFERENCES attendance_sessions(id) ON DELETE CASCADE,
0165:     projection_key VARCHAR(255) NOT NULL,
0166:     student_user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
0167:     actor_user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
0168:     actor_role VARCHAR(16) NOT NULL,
0169:     change_source VARCHAR(32) NOT NULL,
0170:     previous_status VARCHAR(16),
0171:     new_status VARCHAR(16),
0172:     reason VARCHAR(500),
0173:     changed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
0174:     version INTEGER NOT NULL
0175: );
0176:
0177: CREATE INDEX IF NOT EXISTS idx_attendance_session_slots_session_order
0178:     ON attendance_session_slots (attendance_session_id, slot_order);
0179:
0180: CREATE INDEX IF NOT EXISTS idx_attendance_session_slots_projection
0181:     ON attendance_session_slots (projection_key);
0182:
0183: CREATE INDEX IF NOT EXISTS idx_attendance_sessions_course_date
0184:     ON attendance_sessions (course_id, session_date);
0185:
0186: CREATE INDEX IF NOT EXISTS idx_attendance_records_student_session_projection
0187:     ON attendance_records (student_user_id, attendance_session_id, projection_key);
0188:
0189: CREATE INDEX IF NOT EXISTS idx_attendance_status_audit_logs_student_changed_at
0190:     ON attendance_status_audit_logs (student_user_id, changed_at DESC);
0191:
0192: CREATE INDEX IF NOT EXISTS idx_attendance_status_audit_logs_session_projection
0193:     ON attendance_status_audit_logs (attendance_session_id, projection_key, changed_at DESC);
0194:
0195: CREATE TABLE IF NOT EXISTS access_points (
0196:     id BIGSERIAL PRIMARY KEY,
0197:     collector_ap_id VARCHAR(64) NOT NULL UNIQUE,
0198:     label VARCHAR(120) NOT NULL,
0199:     management_ip VARCHAR(64),
0200:     tailnet_ip VARCHAR(64),
0201:     status VARCHAR(20) NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'inactive')),
0202:     token_hash VARCHAR(128),
0203:     token_version INTEGER NOT NULL DEFAULT 0,
0204:     token_revoked_at TIMESTAMPTZ,
0205:     last_rotated_at TIMESTAMPTZ,
0206:     created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
0207:     updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
0208: );
0209:
0210: CREATE TABLE IF NOT EXISTS access_point_interfaces (
0211:     id BIGSERIAL PRIMARY KEY,
0212:     access_point_id BIGINT NOT NULL REFERENCES access_points(id) ON DELETE CASCADE,
0213:     interface_id VARCHAR(64) NOT NULL,
0214:     bssid VARCHAR(32),
0215:     ssid VARCHAR(120),
0216:     classroom_network_id BIGINT NOT NULL REFERENCES classroom_networks(id) ON DELETE CASCADE,
0217:     created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
0218:     UNIQUE (access_point_id, interface_id),
0219:     UNIQUE (classroom_network_id)
0220: );
0221:
0222: CREATE INDEX IF NOT EXISTS idx_access_point_interfaces_network_id
0223:     ON access_point_interfaces (classroom_network_id);
```

## H.4 exam schema

Source: `DB/postgres/init/013_exam_schema.sql:1-140`

```sql
0001: -- Exam domain schema
0002: -- Each attempt expires at:
0003: -- min(started_at + time_limit_snapshot_minutes, exams.ends_at)
0004: -- Exam ownership is derived from courses.professor_user_id.
0005:
0006: CREATE TABLE IF NOT EXISTS exams (
0007:     id BIGSERIAL PRIMARY KEY,
0008:     course_id BIGINT NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
0009:     title VARCHAR(200) NOT NULL,
0010:     description TEXT,
0011:     exam_type VARCHAR(20) NOT NULL DEFAULT 'quiz'
0012:         CHECK (exam_type IN ('quiz', 'midterm', 'final', 'practice', 'custom')),
0013:     status VARCHAR(20) NOT NULL DEFAULT 'draft'
0014:         CHECK (status IN ('draft', 'published', 'open', 'closed', 'archived')),
0015:     starts_at TIMESTAMPTZ NOT NULL,
0016:     ends_at TIMESTAMPTZ NOT NULL,
0017:     duration_minutes INTEGER NOT NULL CHECK (duration_minutes > 0),
0018:     requires_presence BOOLEAN NOT NULL DEFAULT TRUE,
0019:     late_entry_allowed BOOLEAN NOT NULL DEFAULT TRUE,
0020:     auto_submit_enabled BOOLEAN NOT NULL DEFAULT TRUE,
0021:     shuffle_questions BOOLEAN NOT NULL DEFAULT FALSE,
0022:     shuffle_options BOOLEAN NOT NULL DEFAULT FALSE,
0023:     max_attempts INTEGER NOT NULL DEFAULT 1 CHECK (max_attempts > 0),
0024:     created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
0025:     updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
0026:     CHECK (ends_at > starts_at)
0027: );
0028:
0029: COMMENT ON TABLE exams IS 'Exam master records bound to a course. Ownership is derived from the course owner.';
0030: COMMENT ON COLUMN exams.duration_minutes IS 'Per-student time budget in minutes before the global ends_at cap is applied.';
0031: COMMENT ON COLUMN exams.late_entry_allowed IS 'When false, students may not start after starts_at.';
0032: COMMENT ON COLUMN exams.auto_submit_enabled IS 'When true, in-progress attempts should be auto-submitted at expires_at.';
0033:
0034: CREATE INDEX IF NOT EXISTS idx_exams_course_status_starts_at
0035:     ON exams (course_id, status, starts_at);
0036:
0037: CREATE TABLE IF NOT EXISTS exam_questions (
0038:     id BIGSERIAL PRIMARY KEY,
0039:     exam_id BIGINT NOT NULL REFERENCES exams(id) ON DELETE CASCADE,
0040:     question_order INTEGER NOT NULL CHECK (question_order > 0),
0041:     question_type VARCHAR(30) NOT NULL
0042:         CHECK (question_type IN ('multiple_choice', 'true_false')),
0043:     prompt TEXT NOT NULL,
0044:     points NUMERIC(6,2) NOT NULL DEFAULT 1.00 CHECK (points >= 0),
0045:     correct_answer_text TEXT,
0046:     explanation TEXT,
0047:     is_required BOOLEAN NOT NULL DEFAULT TRUE,
0048:     created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
0049:     updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
0050:     UNIQUE (exam_id, question_order),
0051:     UNIQUE (id, exam_id)
0052: );
0053:
0054: COMMENT ON TABLE exam_questions IS 'Questions that belong to an exam.';
0055: COMMENT ON COLUMN exam_questions.correct_answer_text IS 'Canonical answer text for auto-gradable question types.';
0056:
0057: CREATE INDEX IF NOT EXISTS idx_exam_questions_exam_order
0058:     ON exam_questions (exam_id, question_order);
0059:
0060: CREATE TABLE IF NOT EXISTS exam_question_options (
0061:     id BIGSERIAL PRIMARY KEY,
0062:     question_id BIGINT NOT NULL REFERENCES exam_questions(id) ON DELETE CASCADE,
0063:     option_order INTEGER NOT NULL CHECK (option_order > 0),
0064:     option_text TEXT NOT NULL,
0065:     is_correct BOOLEAN NOT NULL DEFAULT FALSE,
0066:     created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
0067:     UNIQUE (question_id, option_order),
0068:     UNIQUE (id, question_id)
0069: );
0070:
0071: COMMENT ON TABLE exam_question_options IS 'Answer choices for multiple-choice and true-false questions.';
0072:
0073: CREATE INDEX IF NOT EXISTS idx_exam_question_options_question_order
0074:     ON exam_question_options (question_id, option_order);
0075:
0076: CREATE UNIQUE INDEX IF NOT EXISTS uniq_exam_question_options_one_correct
0077:     ON exam_question_options (question_id)
0078:     WHERE is_correct;
0079:
0080: CREATE TABLE IF NOT EXISTS exam_submissions (
0081:     id BIGSERIAL PRIMARY KEY,
0082:     exam_id BIGINT NOT NULL REFERENCES exams(id) ON DELETE CASCADE,
0083:     student_user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
0084:     attempt_no INTEGER NOT NULL DEFAULT 1 CHECK (attempt_no > 0),
0085:     status VARCHAR(20) NOT NULL DEFAULT 'in_progress'
0086:         CHECK (status IN ('in_progress', 'submitted', 'auto_submitted', 'graded', 'expired')),
0087:     started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
0088:     submitted_at TIMESTAMPTZ,
0089:     expires_at TIMESTAMPTZ NOT NULL,
0090:     time_limit_snapshot_minutes INTEGER NOT NULL CHECK (time_limit_snapshot_minutes > 0),
0091:     score NUMERIC(8,2) CHECK (score >= 0),
0092:     created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
0093:     updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
0094:     UNIQUE (exam_id, student_user_id, attempt_no),
0095:     UNIQUE (id, exam_id),
0096:     CHECK (submitted_at IS NULL OR submitted_at >= started_at),
0097:     CHECK (expires_at >= started_at)
0098: );
0099:
0100: COMMENT ON TABLE exam_submissions IS 'One student attempt for one exam.';
0101: COMMENT ON COLUMN exam_submissions.expires_at IS 'Application-computed personal deadline capped by the exam ends_at.';
0102: COMMENT ON COLUMN exam_submissions.time_limit_snapshot_minutes IS 'Duration copied at attempt start so later exam edits do not rewrite past attempts.';
0103:
0104: CREATE INDEX IF NOT EXISTS idx_exam_submissions_exam_student
0105:     ON exam_submissions (exam_id, student_user_id);
0106:
0107: CREATE INDEX IF NOT EXISTS idx_exam_submissions_student_status
0108:     ON exam_submissions (student_user_id, status);
0109:
0110: CREATE UNIQUE INDEX IF NOT EXISTS uniq_exam_submissions_one_in_progress
0111:     ON exam_submissions (exam_id, student_user_id)
0112:     WHERE status = 'in_progress';
0113:
0114: CREATE TABLE IF NOT EXISTS exam_submission_answers (
0115:     id BIGSERIAL PRIMARY KEY,
0116:     exam_id BIGINT NOT NULL REFERENCES exams(id) ON DELETE CASCADE,
0117:     submission_id BIGINT NOT NULL,
0118:     question_id BIGINT NOT NULL,
0119:     selected_option_id BIGINT,
0120:     answer_text TEXT,
0121:     is_correct BOOLEAN,
0122:     awarded_score NUMERIC(8,2) CHECK (awarded_score >= 0),
0123:     answered_at TIMESTAMPTZ,
0124:     created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
0125:     updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
0126:     UNIQUE (submission_id, question_id),
0127:     CONSTRAINT fk_exam_submission_answers_submission_exam
0128:         FOREIGN KEY (submission_id, exam_id)
0129:         REFERENCES exam_submissions(id, exam_id)
0130:         ON DELETE CASCADE,
0131:     CONSTRAINT fk_exam_submission_answers_question_exam
0132:         FOREIGN KEY (question_id, exam_id)
0133:         REFERENCES exam_questions(id, exam_id)
0134:         ON DELETE CASCADE,
0135:     CONSTRAINT fk_exam_submission_answers_option_question
0136:         FOREIGN KEY (selected_option_id, question_id)
0137:         REFERENCES exam_question_options(id, question_id)
0138:         ON DELETE SET NULL
0139: );
0140:
```

## H.5 assignment schema

Source: `DB/postgres/init/014_assignment_schema.sql:1-55`

```sql
0001: -- Assignment domain schema
0002: -- One mutable submission row per assignment and student.
0003: -- Files are stored on the backend local filesystem and only metadata is stored here.
0004:
0005: CREATE TABLE IF NOT EXISTS assignments (
0006:     id BIGSERIAL PRIMARY KEY,
0007:     course_id BIGINT NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
0008:     title VARCHAR(200) NOT NULL,
0009:     description TEXT,
0010:     opens_at TIMESTAMPTZ NOT NULL,
0011:     due_at TIMESTAMPTZ NOT NULL,
0012:     created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
0013:     updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
0014:     CHECK (due_at > opens_at)
0015: );
0016:
0017: COMMENT ON TABLE assignments IS 'Course assignment master records.';
0018:
0019: CREATE INDEX IF NOT EXISTS idx_assignments_course_due_at
0020:     ON assignments (course_id, due_at DESC);
0021:
0022: CREATE TABLE IF NOT EXISTS assignment_submissions (
0023:     id BIGSERIAL PRIMARY KEY,
0024:     assignment_id BIGINT NOT NULL REFERENCES assignments(id) ON DELETE CASCADE,
0025:     student_user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
0026:     submission_text TEXT,
0027:     submitted_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
0028:     updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
0029:     UNIQUE (assignment_id, student_user_id)
0030: );
0031:
0032: COMMENT ON TABLE assignment_submissions IS 'Latest submission per assignment and student.';
0033:
0034: CREATE INDEX IF NOT EXISTS idx_assignment_submissions_assignment_student
0035:     ON assignment_submissions (assignment_id, student_user_id);
0036:
0037: CREATE INDEX IF NOT EXISTS idx_assignment_submissions_student_submitted_at
0038:     ON assignment_submissions (student_user_id, submitted_at DESC);
0039:
0040: CREATE TABLE IF NOT EXISTS assignment_submission_attachments (
0041:     id BIGSERIAL PRIMARY KEY,
0042:     submission_id BIGINT NOT NULL REFERENCES assignment_submissions(id) ON DELETE CASCADE,
0043:     original_filename VARCHAR(255) NOT NULL,
0044:     stored_filename VARCHAR(255) NOT NULL,
0045:     mime_type VARCHAR(120),
0046:     file_size_bytes INTEGER NOT NULL CHECK (file_size_bytes >= 0),
0047:     storage_key VARCHAR(500) NOT NULL,
0048:     created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
0049: );
0050:
0051: COMMENT ON TABLE assignment_submission_attachments IS 'Attachment metadata for assignment submissions.';
0052: COMMENT ON COLUMN assignment_submission_attachments.storage_key IS 'Internal backend storage path or key, not a public URL.';
0053:
0054: CREATE INDEX IF NOT EXISTS idx_assignment_submission_attachments_submission
0055:     ON assignment_submission_attachments (submission_id, created_at ASC);
```

## H.6 object storage / report export / deletion jobs

Source: `DB/postgres/init/015_object_storage_schema.sql:49-205`

```sql
0049: CREATE TABLE IF NOT EXISTS learning_items (
0050:     id BIGSERIAL PRIMARY KEY,
0051:     course_id BIGINT NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
0052:     created_by_user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
0053:     title VARCHAR(200) NOT NULL,
0054:     description TEXT,
0055:     item_type VARCHAR(20) NOT NULL DEFAULT 'file'
0056:         CHECK (item_type IN ('document', 'video', 'file', 'link')),
0057:     external_url TEXT,
0058:     sort_order INTEGER NOT NULL DEFAULT 0,
0059:     is_published BOOLEAN NOT NULL DEFAULT FALSE,
0060:     created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
0061:     updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
0062:     CHECK ((item_type = 'link' AND external_url IS NOT NULL) OR (item_type <> 'link'))
0063: );
0064:
0065: COMMENT ON TABLE learning_items IS 'Persisted course learning materials owned by Backend; Front no longer treats learning content as local-only state.';
0066: COMMENT ON COLUMN learning_items.external_url IS 'Optional external link for link-type learning items; uploaded files use learning_item_attachments.';
0067:
0068: CREATE INDEX IF NOT EXISTS idx_learning_items_course_published_sort
0069:     ON learning_items (course_id, is_published, sort_order, created_at DESC);
0070:
0071: CREATE TABLE IF NOT EXISTS learning_item_attachments (
0072:     id BIGSERIAL PRIMARY KEY,
0073:     learning_item_id BIGINT NOT NULL REFERENCES learning_items(id) ON DELETE CASCADE,
0074:     original_filename VARCHAR(255) NOT NULL,
0075:     stored_filename VARCHAR(255) NOT NULL,
0076:     mime_type VARCHAR(120),
0077:     file_size_bytes BIGINT NOT NULL CHECK (file_size_bytes >= 0),
0078:     storage_provider VARCHAR(20) NOT NULL DEFAULT 's3' CHECK (storage_provider IN ('local', 's3')),
0079:     bucket_name VARCHAR(120) NOT NULL DEFAULT 'smart-class' CHECK (bucket_name <> ''),
0080:     storage_key VARCHAR(700) NOT NULL CHECK (storage_key <> '' AND storage_key !~* '^https?://'),
0081:     checksum_sha256 VARCHAR(64) CHECK (checksum_sha256 IS NULL OR checksum_sha256 ~ '^[0-9a-f]{64}$'),
0082:     created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
0083: );
0084:
0085: COMMENT ON TABLE learning_item_attachments IS 'Object metadata for course learning materials and lecture videos.';
0086: COMMENT ON COLUMN learning_item_attachments.storage_key IS 'Internal object key, for example learning/{course_code}/{item_id}/{uuid}_{filename}.';
0087:
0088: CREATE INDEX IF NOT EXISTS idx_learning_item_attachments_item
0089:     ON learning_item_attachments (learning_item_id, created_at ASC);
0090:
0091: CREATE TABLE IF NOT EXISTS notice_attachments (
0092:     id BIGSERIAL PRIMARY KEY,
0093:     notice_id BIGINT NOT NULL REFERENCES notices(id) ON DELETE CASCADE,
0094:     original_filename VARCHAR(255) NOT NULL,
0095:     stored_filename VARCHAR(255) NOT NULL,
0096:     mime_type VARCHAR(120),
0097:     file_size_bytes BIGINT NOT NULL CHECK (file_size_bytes >= 0),
0098:     storage_provider VARCHAR(20) NOT NULL DEFAULT 's3' CHECK (storage_provider IN ('local', 's3')),
0099:     bucket_name VARCHAR(120) NOT NULL DEFAULT 'smart-class' CHECK (bucket_name <> ''),
0100:     storage_key VARCHAR(700) NOT NULL CHECK (storage_key <> '' AND storage_key !~* '^https?://'),
0101:     checksum_sha256 VARCHAR(64) CHECK (checksum_sha256 IS NULL OR checksum_sha256 ~ '^[0-9a-f]{64}$'),
0102:     created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
0103: );
0104:
0105: COMMENT ON TABLE notice_attachments IS 'Object metadata for course or global notice attachments.';
0106: COMMENT ON COLUMN notice_attachments.storage_key IS 'Internal object key, for example notices/{notice_id}/{uuid}_{filename}.';
0107:
0108: CREATE INDEX IF NOT EXISTS idx_notice_attachments_notice
0109:     ON notice_attachments (notice_id, created_at ASC);
0110:
0111: CREATE TABLE IF NOT EXISTS exam_question_attachments (
0112:     id BIGSERIAL PRIMARY KEY,
0113:     question_id BIGINT NOT NULL REFERENCES exam_questions(id) ON DELETE CASCADE,
0114:     attachment_role VARCHAR(20) NOT NULL DEFAULT 'prompt'
0115:         CHECK (attachment_role IN ('prompt', 'explanation')),
0116:     original_filename VARCHAR(255) NOT NULL,
0117:     stored_filename VARCHAR(255) NOT NULL,
0118:     mime_type VARCHAR(120),
0119:     file_size_bytes BIGINT NOT NULL CHECK (file_size_bytes >= 0),
0120:     storage_provider VARCHAR(20) NOT NULL DEFAULT 's3' CHECK (storage_provider IN ('local', 's3')),
0121:     bucket_name VARCHAR(120) NOT NULL DEFAULT 'smart-class' CHECK (bucket_name <> ''),
0122:     storage_key VARCHAR(700) NOT NULL CHECK (storage_key <> '' AND storage_key !~* '^https?://'),
0123:     checksum_sha256 VARCHAR(64) CHECK (checksum_sha256 IS NULL OR checksum_sha256 ~ '^[0-9a-f]{64}$'),
0124:     created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
0125: );
0126:
0127: COMMENT ON TABLE exam_question_attachments IS 'Object metadata for professor-authored exam question or explanation media.';
0128: COMMENT ON COLUMN exam_question_attachments.storage_key IS 'Internal object key, for example exams/{exam_id}/questions/{question_id}/{uuid}_{filename}.';
0129:
0130: CREATE INDEX IF NOT EXISTS idx_exam_question_attachments_question
0131:     ON exam_question_attachments (question_id, created_at ASC);
0132:
0133: CREATE TABLE IF NOT EXISTS exam_answer_attachments (
0134:     id BIGSERIAL PRIMARY KEY,
0135:     answer_id BIGINT NOT NULL REFERENCES exam_submission_answers(id) ON DELETE CASCADE,
0136:     original_filename VARCHAR(255) NOT NULL,
0137:     stored_filename VARCHAR(255) NOT NULL,
0138:     mime_type VARCHAR(120),
0139:     file_size_bytes BIGINT NOT NULL CHECK (file_size_bytes >= 0),
0140:     storage_provider VARCHAR(20) NOT NULL DEFAULT 's3' CHECK (storage_provider IN ('local', 's3')),
0141:     bucket_name VARCHAR(120) NOT NULL DEFAULT 'smart-class' CHECK (bucket_name <> ''),
0142:     storage_key VARCHAR(700) NOT NULL CHECK (storage_key <> '' AND storage_key !~* '^https?://'),
0143:     checksum_sha256 VARCHAR(64) CHECK (checksum_sha256 IS NULL OR checksum_sha256 ~ '^[0-9a-f]{64}$'),
0144:     created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
0145: );
0146:
0147: COMMENT ON TABLE exam_answer_attachments IS 'Future-compatible object metadata for student exam answer files; first-pass objective exams do not require file-answer UI.';
0148: COMMENT ON COLUMN exam_answer_attachments.storage_key IS 'Internal object key, for example exams/{exam_id}/submissions/{submission_id}/answers/{answer_id}/{uuid}_{filename}.';
0149:
0150: CREATE INDEX IF NOT EXISTS idx_exam_answer_attachments_answer
0151:     ON exam_answer_attachments (answer_id, created_at ASC);
0152:
0153: CREATE TABLE IF NOT EXISTS report_exports (
0154:     id BIGSERIAL PRIMARY KEY,
0155:     course_id BIGINT REFERENCES courses(id) ON DELETE SET NULL,
0156:     requested_by_user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
0157:     report_domain VARCHAR(20) NOT NULL DEFAULT 'attendance'
0158:         CHECK (report_domain IN ('attendance', 'grade', 'assignment', 'exam')),
0159:     export_format VARCHAR(20) NOT NULL DEFAULT 'csv'
0160:         CHECK (export_format IN ('csv', 'pdf')),
0161:     original_filename VARCHAR(255) NOT NULL,
0162:     stored_filename VARCHAR(255) NOT NULL,
0163:     mime_type VARCHAR(120),
0164:     file_size_bytes BIGINT NOT NULL CHECK (file_size_bytes >= 0),
0165:     storage_provider VARCHAR(20) NOT NULL DEFAULT 's3' CHECK (storage_provider IN ('local', 's3')),
0166:     bucket_name VARCHAR(120) NOT NULL DEFAULT 'smart-class' CHECK (bucket_name <> ''),
0167:     storage_key VARCHAR(700) NOT NULL CHECK (storage_key <> '' AND storage_key !~* '^https?://'),
0168:     checksum_sha256 VARCHAR(64) CHECK (checksum_sha256 IS NULL OR checksum_sha256 ~ '^[0-9a-f]{64}$'),
0169:     status VARCHAR(20) NOT NULL DEFAULT 'ready'
0170:         CHECK (status IN ('pending', 'ready', 'failed', 'deleted')),
0171:     generated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
0172:     created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
0173: );
0174:
0175: COMMENT ON TABLE report_exports IS 'Metadata for generated report files; first pass stores attendance CSV exports only, other domains are future-compatible.';
0176: COMMENT ON COLUMN report_exports.storage_key IS 'Internal object key, for example reports/{domain}/{course_code}/{yyyy}/{mm}/{uuid}_{filename}.';
0177:
0178: CREATE INDEX IF NOT EXISTS idx_report_exports_course_domain_created
0179:     ON report_exports (course_id, report_domain, created_at DESC);
0180:
0181: CREATE TABLE IF NOT EXISTS object_deletion_jobs (
0182:     id BIGSERIAL PRIMARY KEY,
0183:     storage_provider VARCHAR(20) NOT NULL CHECK (storage_provider IN ('local', 's3')),
0184:     bucket_name VARCHAR(120) NOT NULL CHECK (bucket_name <> ''),
0185:     storage_key VARCHAR(700) NOT NULL CHECK (storage_key <> '' AND storage_key !~* '^https?://'),
0186:     owner_domain VARCHAR(80) NOT NULL,
0187:     owner_id BIGINT,
0188:     reason VARCHAR(80) NOT NULL DEFAULT 'metadata_deleted',
0189:     status VARCHAR(20) NOT NULL DEFAULT 'pending'
0190:         CHECK (status IN ('pending', 'processing', 'completed', 'failed')),
0191:     attempt_count INTEGER NOT NULL DEFAULT 0 CHECK (attempt_count >= 0),
0192:     last_error TEXT,
0193:     created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
0194:     completed_at TIMESTAMPTZ,
0195:     CHECK ((status = 'completed' AND completed_at IS NOT NULL) OR (status <> 'completed'))
0196: );
0197:
0198: COMMENT ON TABLE object_deletion_jobs IS 'Durable outbox for DB-driven immediate object deletion after metadata delete/replace.';
0199: COMMENT ON COLUMN object_deletion_jobs.owner_domain IS 'Domain/table context that owned the deleted object metadata.';
0200: COMMENT ON COLUMN object_deletion_jobs.owner_id IS 'Owning domain row id captured from the deleted metadata row when available.';
0201:
0202: CREATE INDEX IF NOT EXISTS idx_object_deletion_jobs_status_created
0203:     ON object_deletion_jobs (status, created_at ASC);
0204:
0205: CREATE INDEX IF NOT EXISTS idx_object_deletion_jobs_object_active
```

## H.7 selected LMS Q&A / learning progress

Source: `DB/postgres/init/016_selected_lms_subset.sql:84-150`

```sql
0084: CREATE TABLE IF NOT EXISTS course_qna_threads (
0085:     id BIGSERIAL PRIMARY KEY,
0086:     course_id BIGINT NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
0087:     student_user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
0088:     title VARCHAR(200) NOT NULL,
0089:     body TEXT NOT NULL,
0090:     status VARCHAR(20) NOT NULL DEFAULT 'open'
0091:         CHECK (status IN ('open', 'answered', 'closed')),
0092:     created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
0093:     updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
0094:     CHECK (btrim(title) <> ''),
0095:     CHECK (btrim(body) <> '')
0096: );
0097:
0098: COMMENT ON TABLE course_qna_threads IS 'Student-authored course Q&A/inquiry threads for the selected LMS subset.';
0099: COMMENT ON COLUMN course_qna_threads.status IS 'Thread state visible to students and professors: open, answered, or closed.';
0100:
0101: CREATE INDEX IF NOT EXISTS idx_course_qna_threads_course_status_updated
0102:     ON course_qna_threads (course_id, status, updated_at DESC);
0103:
0104: CREATE INDEX IF NOT EXISTS idx_course_qna_threads_student_updated
0105:     ON course_qna_threads (student_user_id, updated_at DESC);
0106:
0107: CREATE TABLE IF NOT EXISTS course_qna_posts (
0108:     id BIGSERIAL PRIMARY KEY,
0109:     thread_id BIGINT NOT NULL REFERENCES course_qna_threads(id) ON DELETE CASCADE,
0110:     author_user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
0111:     body TEXT NOT NULL,
0112:     post_type VARCHAR(20) NOT NULL DEFAULT 'comment'
0113:         CHECK (post_type IN ('question', 'answer', 'comment')),
0114:     created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
0115:     CHECK (btrim(body) <> '')
0116: );
0117:
0118: COMMENT ON TABLE course_qna_posts IS 'Posts inside a course Q&A thread: initial question, professor answer, or comments.';
0119: COMMENT ON COLUMN course_qna_posts.post_type IS 'Q&A post type: question, answer, or comment.';
0120:
0121: CREATE INDEX IF NOT EXISTS idx_course_qna_posts_thread_created
0122:     ON course_qna_posts (thread_id, created_at ASC);
0123:
0124: CREATE INDEX IF NOT EXISTS idx_course_qna_posts_author_created
0125:     ON course_qna_posts (author_user_id, created_at DESC);
0126:
0127: CREATE TABLE IF NOT EXISTS learning_progress (
0128:     id BIGSERIAL PRIMARY KEY,
0129:     learning_item_id BIGINT NOT NULL REFERENCES learning_items(id) ON DELETE CASCADE,
0130:     student_user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
0131:     progress_percent NUMERIC(5,2) NOT NULL DEFAULT 0.00
0132:         CHECK (progress_percent >= 0 AND progress_percent <= 100),
0133:     status VARCHAR(20) NOT NULL DEFAULT 'not_started'
0134:         CHECK (status IN ('not_started', 'in_progress', 'completed')),
0135:     last_viewed_at TIMESTAMPTZ,
0136:     completed_at TIMESTAMPTZ,
0137:     updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
0138:     UNIQUE (learning_item_id, student_user_id),
0139:     CHECK (status <> 'completed' OR progress_percent = 100.00)
0140: );
0141:
0142: COMMENT ON TABLE learning_progress IS 'Per-student learning material progress snapshot for selected LMS progress APIs.';
0143: COMMENT ON COLUMN learning_progress.progress_percent IS 'Progress percentage from 0 through 100.';
0144: COMMENT ON COLUMN learning_progress.status IS 'Learning progress state: not_started, in_progress, or completed.';
0145:
0146: CREATE INDEX IF NOT EXISTS idx_learning_progress_student_status
0147:     ON learning_progress (student_user_id, status, updated_at DESC);
0148:
0149: CREATE INDEX IF NOT EXISTS idx_learning_progress_item_status
0150:     ON learning_progress (learning_item_id, status, updated_at DESC);
```

## H.8 OpenWrt collector registry migration

Source: `DB/postgres/migrations/016_openwrt_collector_registry.sql:1-70`

```sql
0001: CREATE TABLE IF NOT EXISTS access_points (
0002:     id BIGSERIAL PRIMARY KEY,
0003:     collector_ap_id VARCHAR(64) NOT NULL UNIQUE,
0004:     label VARCHAR(120) NOT NULL,
0005:     management_ip VARCHAR(64),
0006:     tailnet_ip VARCHAR(64),
0007:     status VARCHAR(20) NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'inactive')),
0008:     token_hash VARCHAR(128),
0009:     token_version INTEGER NOT NULL DEFAULT 0,
0010:     token_revoked_at TIMESTAMPTZ,
0011:     last_rotated_at TIMESTAMPTZ,
0012:     created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
0013:     updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
0014: );
0015:
0016: CREATE TABLE IF NOT EXISTS access_point_interfaces (
0017:     id BIGSERIAL PRIMARY KEY,
0018:     access_point_id BIGINT NOT NULL REFERENCES access_points(id) ON DELETE CASCADE,
0019:     interface_id VARCHAR(64) NOT NULL,
0020:     bssid VARCHAR(32),
0021:     ssid VARCHAR(120),
0022:     classroom_network_id BIGINT NOT NULL REFERENCES classroom_networks(id) ON DELETE CASCADE,
0023:     created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
0024:     UNIQUE (access_point_id, interface_id),
0025:     UNIQUE (classroom_network_id)
0026: );
0027:
0028: CREATE INDEX IF NOT EXISTS idx_access_point_interfaces_network_id
0029:     ON access_point_interfaces (classroom_network_id);
0030:
0031: UPDATE classroom_networks
0032: SET collection_mode = 'openwrt-push',
0033:     ssid = 'SmartClass-Demo',
0034:     gateway_host = CASE
0035:         WHEN ap_id LIKE 'phy0-%' OR ap_id LIKE 'phy1-%' THEN '192.168.97.1'
0036:         WHEN ap_id LIKE 'phy4-%' OR ap_id LIKE 'phy5-%' THEN '192.168.97.2'
0037:         WHEN ap_id LIKE 'phy7-%' OR ap_id LIKE 'phy8-%' THEN '192.168.97.3'
0038:         ELSE gateway_host
0039:     END
0040: WHERE ap_id IN ('phy0-ap0','phy1-ap0','phy4-ap0','phy5-ap0','phy7-ap0','phy8-ap0');
0041:
0042: INSERT INTO access_points (collector_ap_id, label, management_ip, tailnet_ip, status)
0043: VALUES
0044:     ('openwrt-a', 'Demo AP A / B101', '192.168.97.1', '100.78.116.89', 'active'),
0045:     ('openwrt-b', 'Demo AP B / B102', '192.168.97.2', '100.86.49.51', 'active'),
0046:     ('openwrt-c', 'Demo AP C / C201', '192.168.97.3', '100.99.237.79', 'active')
0047: ON CONFLICT (collector_ap_id) DO UPDATE
0048: SET label = EXCLUDED.label,
0049:     management_ip = EXCLUDED.management_ip,
0050:     tailnet_ip = EXCLUDED.tailnet_ip,
0051:     status = EXCLUDED.status,
0052:     updated_at = NOW();
0053:
0054: DELETE FROM access_point_interfaces api
0055: USING access_points ap
0056: WHERE api.access_point_id = ap.id
0057:   AND ap.collector_ap_id IN ('openwrt-a', 'openwrt-b', 'openwrt-c')
0058:   AND api.interface_id <> 'phy1-ap0';
0059:
0060: INSERT INTO access_point_interfaces (access_point_id, interface_id, ssid, classroom_network_id)
0061: SELECT ap.id, mapping.interface_id, cn.ssid, cn.id
0062: FROM (VALUES
0063:     ('openwrt-a', 'phy1-ap0', 'phy1-ap0'),
0064:     ('openwrt-b', 'phy1-ap0', 'phy4-ap0'),
0065:     ('openwrt-c', 'phy1-ap0', 'phy7-ap0')
0066: ) AS mapping(collector_ap_id, interface_id, classroom_ap_id)
0067: JOIN access_points ap ON ap.collector_ap_id = mapping.collector_ap_id
0068: JOIN classroom_networks cn ON cn.ap_id = mapping.classroom_ap_id
0069: ON CONFLICT (access_point_id, interface_id) DO UPDATE
0070: SET ssid = EXCLUDED.ssid,
```

# I. 검증 및 품질 게이트 근거

## I.1 실행/검증 명령

```text
git -C docs diff --check
completion-marker audit: unresolved placeholder and missing-evidence phrase scan
asset reference audit: screenshot checklist + diagram inventory
API request/response pair count audit
two-file report/appendix alignment audit
```

## I.2 현재 산출물 수량

- Screenshot PNG: 52
- 화면 근거 이미지: 52
- ERD SVG: 16
- ERD set: ERD-1 full + ERD-2~ERD-8 partial/N/A boundary

## I.3 최종 품질 원칙

- 완료 주장에는 화면, API/코드, DB/ERD, 테스트/실행 근거 중 가능한 근거를 함께 둔다.
- 운영 배포, 장기 현장 검증, SIS 연동, 네이티브 모바일 앱은 한계/후속 과제로만 표현한다.
- 보고서와 부록은 외부 보조 산출물 없이도 읽히는 형태를 유지한다.
