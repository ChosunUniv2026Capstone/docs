---
title: 차세대 사이버캠퍼스 Smart Class 최종보고서
type: final-report
status: draft
updated: 2026-05-22
owners:
  - team
related:
  - [[/08-reports/99-combined-report.md]]
  - [[/08-reports/01-report-template.md]]
  - [[/08-reports/90-appendix/05-evidence-ledger.md]]
source:
  - [[/03-conventions/conv-final-report-writing.md]]
  - [[/08-reports/90-appendix/01-source-map.md]]
  - [[/08-reports/90-appendix/02-screenshot-checklist.md]]
  - [[/08-reports/90-appendix/03-api-endpoint-inventory.md]]
  - [[/08-reports/90-appendix/04-diagram-inventory.md]]
  - [[/08-reports/90-appendix/05-evidence-ledger.md]]
---

# 차세대 사이버캠퍼스 Smart Class 최종보고서

## 보고서 정보

| 항목 | 내용 |
|---|---|
| 보고서 종류 | 최종보고서 |
| 기준 시각 | 2026-05-22T02:14:43.202751+09:00 (KST) |
| 이번 주 변경사항 기간 | 2026-05-18 09:00 KST ~ 2026-05-22 02:14:43 KST |
| 기준 브랜치 | 모든 구현 레포의 `main`; docs는 작성 브랜치와 완료 근거를 분리 |
| 제출본 원천 | `docs/08-reports/40-final/final-report-draft.md` |
| 통합 검토본 | `docs/08-reports/99-combined-report.md` |
| 핵심 증거 | `docs/08-reports/90-appendix/05-evidence-ledger.md` |

## 초록

본 프로젝트는 조선대학교 사이버캠퍼스의 핵심 LMS 기능을 웹 기반 프로토타입으로 재구성하고, Wi-Fi 기반 재실성 판별과 등록 단말 인증을 결합하여 출석과 시험 접근의 신뢰성을 높이는 Smart Class 시스템을 구현한 것이다. 시스템은 `Front`, `Backend`, `PresenceService`, `DB`, `Service`로 책임을 분리한다. Front는 학생·교수·서비스관리자 UI를 제공하고, Backend는 인증·LMS·출석·시험 도메인 판단을 수행하며, PresenceService는 강의실 AP snapshot, 등록 단말 매칭, RSSI threshold 기반 eligibility 근거를 제공한다. DB는 사용자, 강의, 단말, 출석, 시험, 과제, Q&A, 학습진도, 운영 메타데이터를 저장하고, Service repo는 Docker Compose/Nginx 기반 로컬·이미지 실행 구조와 release manifest를 관리한다.

완성도 평가는 기능별 종합 증거 매트릭스를 기준으로 수행했다. 인증/세션, 역할별 UI, 강의·공지·선택 LMS read model, 출석 workflow, 객관식 시험 workflow, PresenceService eligibility, DB schema/ERD는 로컬 MVP 수준의 구현 근거를 갖는다. 반면 실운영/상용 배포, 장기 교내 Wi-Fi 현장 검증, 학사시스템 정식 연동, 네이티브 모바일 앱은 본 최종보고서의 완료 성과가 아니라 한계와 향후 과제로 분리했다.

## 목차

1. 이번 주 진행사항 및 전체 완성도 자체평가
   1. 이번 주 main 기준 변경사항
   2. 전체 완성도 자체평가
   3. 기능별 종합 증거 매트릭스 요약
2. 서론
   1. 연구 배경
   2. 필요성
   3. 목적과 범위
3. 관련 연구 및 기술
   1. 기존 LMS 및 출석 관리 방식
   2. 위치·단말 기반 인증 기술
   3. 차별성 분석
4. 시스템 설계
   1. 전체 구조
   2. 핵심 알고리즘
   3. DB 설계와 ERD
   4. UML/흐름 다이어그램
5. 구현
   1. 사용 기술과 개발 환경
   2. 서비스별 구현
   3. 코드 구조와 주요 구현 포인트
6. 실험 및 결과
   1. 테스트 방법
   2. 기능 검증 결과
   3. 성능 평가와 운영 검증 경계
   4. 한계점
7. 결론
   1. 성과
   2. 문제 해결 과정
   3. 개선 방향
8. 참고문헌
9. 부록

# 1. 이번 주 진행사항 및 전체 완성도 자체평가

## 1.1 이번 주 main 기준 변경사항

이번 주 기준 기간은 2026-05-18 09:00 KST부터 2026-05-22 02:14:43 KST까지다. 모든 구현 완료 주장은 각 레포의 `main` 또는 `origin/main` 기준으로 확인했다.

| Repo | 기준 커밋 | 이번 주 main 반영 내용 | 보고서 반영 방식 |
|---|---|---|---|
| Front | `418ae29` | `smart-class-front-v0.6.0` release, 교수 출석 CSV 다운로드 UI | 출석/교수 기능, 화면 근거, 기능 검증에 반영 |
| Backend | `f06169e` | `v0.6.0` release, 교수 출석 CSV export, slow attendance bootstrap 중 realtime socket/DB pool starvation 완화 | 출석 workflow, CSV export, 성능/문제 해결 과정에 반영 |
| PresenceService | `bffda67` | 기간 내 신규 main commit 없음 | 기존 eligibility/collector/demo overlay 구현 근거 유지 |
| DB | `621d712` | 기간 내 신규 main commit 없음 | 기존 schema/seed/ERD 근거 유지 |
| Service | `c36a432` | `v0.4.1` release, attendance CSV demo manifest pin | Service runtime/manifest/CI-CD 근거에 반영 |
| docs | `cef3c2f` + 작성 브랜치 변경 | attendance CSV export scope, 최종보고서 작성 규약/부록 보강 | docs 작성 지시는 completion proof와 분리 |
| CodexKit | `a5a68c1` | 기간 내 신규 main commit 없음 | runtime 소유권은 Service로 이전된 상태로 설명 |
| DocsQuartz | `90d012b` | 기간 내 신규 main commit 없음 | 보고서 배포/문서 사이트 보조 레포로만 취급 |

## 1.2 전체 완성도 자체평가

| 영역 | 자체평가 | 근거 | 남은 보강 |
|---|---|---|---|
| Front | 로컬 MVP 완료 | 역할별 화면, 출석/시험/selected LMS e2e 근거, 기존 37개 화면 캡처와 redbox 주석 | 최종 제출 직전 동일 runtime/seed 기준 전체 재촬영 여부 검토 |
| Backend | 로컬 MVP 완료 | 인증, LMS, 출석, 시험, API envelope, CSV export pytest 근거 | 최종 제출 직전 전체 pytest 로그 재수집 |
| PresenceService | 로컬 MVP 완료 | eligibility, cache, demo overlay, collector push/registry 테스트 | 실제 OpenWrt 장기 현장 검증 |
| DB | 로컬 MVP 완료 | init/migration SQL, seed, ERD-1~ERD-8 산출물 | 실제 DB migration 실행 로그 보강 |
| Service / CI-CD | 부분 완료 | compose/nginx/manifest/test 근거, release commit | workflow-run/demo server provenance 없이는 실배포 완료로 표현하지 않음 |
| 문서 / 보고서 | 부분 완료 | 최종보고서 본문, 부록, 증거 원장 정비 | 제출 전 캡션/참고문헌/테스트 로그 최종 검수 |

## 1.3 기능별 종합 증거 매트릭스 요약

상세 표는 부록 E `최종보고서 증거 원장`에 둔다. 본문에서는 평가자가 완료도와 한계를 빠르게 확인할 수 있도록 요약한다.

| 기능 영역 | 완료도 | 핵심 증거 | 한계 / 후속 과제 |
|---|---|---|---|
| 인증 / 세션 | 로컬 MVP 완료 | Backend login/refresh/bootstrap/logout, refresh session DB, auth-routing e2e | 운영 SSO/학사 인증 연동 |
| 역할별 Front UI | 로컬 MVP 완료 | 학생/교수/관리자 화면 캡처 및 redbox, route/e2e 근거 | OpenWrt router registration/token은 N/A로 API/DB/Service 근거 대체 |
| 강의 / 공지 / selected LMS | 로컬 MVP 완료 | assignments/grades/qna/learning-progress API와 DB schema/test | 전체 기능 화면 캡처 보강 |
| 출석 workflow | 로컬 MVP 완료 | bundle attendance session, roster, audit, CSV export, websocket tests | 장기 현장 검증 |
| 객관식 시험 workflow | 로컬 MVP 완료 | exam create/publish/take/answer/submit API와 e2e | 서술형/파일형/대규모 부정행위 대응 |
| PresenceService | 로컬 MVP 완료 | collector, cache, eligibility, demo overlay tests | dummy overlay와 real OpenWrt 검증 분리 |
| DB schema / ERD | 로컬 MVP 완료 | ERD-1~ERD-8, schema/init/migration files | migration 실행 로그 보강 |
| Service / CI-CD | 부분 완료 | compose, nginx, manifest, Service tests | workflow-run/server provenance 보강 |

# 2. 서론

## 2.1 연구 배경

대학 LMS는 강의 공지, 학습자료, 과제, 시험, 출석, 성적 확인을 담당하는 핵심 학사 플랫폼이다. 그러나 기존 LMS의 출석과 시험 접근 제어는 실제 수업 참여 여부와 느슨하게 연결되는 경우가 많다. 단순 로그인이나 버튼 클릭만으로는 학생이 강의실에 있는지, 등록된 단말을 사용 중인지, 해당 수업 시간과 강의실 조건을 만족하는지 확인하기 어렵다.

Smart Class는 기존 LMS 기능을 웹 기반으로 재구성하면서 출석과 시험 접근에 재실성 근거를 결합한다. 프로젝트는 강의실 네트워크에서 관측되는 단말 정보, 학생의 사전 등록 단말, 수강 정보, 수업 시간표, 교수의 출석 세션 상태를 함께 사용한다.

## 2.2 필요성

첫째, 대리출석과 원격 출석 시도를 줄이려면 사용자의 계정뿐 아니라 물리 단말과 강의실 네트워크 관측 근거가 필요하다. 둘째, 교수자는 출석 세션을 열고 닫으며 학생별 출석 상태를 실시간으로 확인·수정할 수 있어야 한다. 셋째, 사후 이의 제기나 운영 장애 대응을 위해 출석 판정 사유와 변경 이력이 추적 가능해야 한다. 넷째, 시험 접근에서도 출석과 동일한 재실성 근거를 활용하면 시험 응시 조건을 더 명확히 만들 수 있다.

## 2.3 목적과 범위

본 프로젝트의 목적은 학생·교수·서비스관리자 세 역할을 지원하는 웹 기반 LMS 프로토타입을 구현하고, 등록 단말과 강의실 Wi-Fi 관측 정보를 결합한 재실성 기반 출석/시험 접근 제어를 로컬 테스트베드에서 검증하는 것이다.

완료 성과로 다루는 범위는 로컬/테스트베드 MVP다. 실운영/상용 배포 완료, 장기 교내 Wi-Fi 현장 검증 완료, 학사시스템 정식 연동, 네이티브 모바일 앱 구현은 본 최종보고서의 완료 성과가 아니라 한계와 개선 방향으로 분리한다.

# 3. 관련 연구 및 기술

## 3.1 기존 LMS 및 출석 관리 방식

일반 LMS는 강의자료, 공지, 과제, 시험, 성적, 출석 기능을 제공한다. 그러나 출석은 교수 수기 입력, 학생 버튼 클릭, QR 인증, 위치 인증 등으로 운영되는 경우가 많고, 각 방식은 편의성과 신뢰성 사이의 trade-off를 가진다. 버튼 클릭 방식은 구현이 쉽지만 대리출석에 취약하고, QR 방식은 단기 인증에는 유용하지만 QR 공유와 시간 제한 관리가 필요하다. GPS는 실내 강의실 단위 정확도와 개인정보 문제가 있다.

## 3.2 위치·단말 기반 인증 기술

Wi-Fi 기반 재실성 판별은 학생 단말이 특정 강의실 AP 또는 네트워크에서 관측되는지를 활용한다. 본 프로젝트는 OpenWrt collector 또는 demo overlay snapshot을 PresenceService가 읽고, 등록 단말 MAC, AP online 상태, RSSI threshold, snapshot freshness를 함께 판정한다. 단말 기반 인증은 랜덤 MAC, 단말 변경 정책, 개인정보 저장 정책을 함께 고려해야 하므로 운영 정책이 필요하다.

## 3.3 차별성 분석

Smart Class의 차별점은 LMS 기능과 재실성 판정을 별도 서비스 경계로 결합한 데 있다. Front는 판정 결과를 보여주고, Backend는 수강/시간표/세션/권한을 결합해 최종 도메인 판단을 수행하며, PresenceService는 네트워크/단말 근거를 제공한다. 이 분리는 네트워크 수집 실패와 학사 도메인 판단을 분리하고, dummy overlay와 real collector snapshot을 혼동하지 않게 한다.

# 4. 시스템 설계

## 4.1 전체 구조

시스템은 `Front`, `Backend`, `PresenceService`, `DB`, `Service`로 구성된다. Nginx는 단일 origin에서 `/`, `/api/`, `/ws/`, `/health`를 라우팅한다. Front는 React/Vite 기반 UI이며, Backend는 FastAPI 기반 LMS/API 서버다. PresenceService는 FastAPI 기반 재실성 판정 보조 서비스이며 Redis snapshot cache와 demo overlay를 사용한다. DB는 PostgreSQL schema와 seed를 소유하고, Service repo는 Docker Compose, nginx 설정, image mode, release manifest, demo deploy wrapper를 소유한다.

## 4.2 핵심 알고리즘

출석 eligibility 판정은 다음 순서로 수행된다.

1. 학생/교수/관리자 인증과 역할 권한을 확인한다.
2. Backend가 수강 여부, 강의 시간표, 강의실, 출석 세션 상태를 확인한다.
3. Backend가 PresenceService에 `purpose`를 포함한 eligibility 요청을 보낸다.
4. PresenceService는 classroom snapshot을 읽고, AP online 상태, 등록 단말 MAC, RSSI threshold, snapshot freshness를 평가한다.
5. Backend는 PresenceService 결과와 도메인 조건을 결합해 출석/시험 접근을 허용하거나 거부한다.
6. 판정 로그와 출석 record/audit log를 저장하고, 필요한 경우 WebSocket으로 roster/timeline 상태를 갱신한다.

## 4.3 DB 설계와 ERD

DB는 사용자/강의/수강, 강의실/AP/단말, 출석 세션/기록/audit, 시험/문항/제출/답안, 과제/학습자료/Q&A/학습진도, object storage metadata, report export metadata를 포함한다. 전체 ERD와 부분 ERD는 부록 D의 ERD-1~ERD-8에 생성했다.

| ERD | 설명 | redbox 주석 |
|---|---|---|
| ERD-1 | 전체 Smart Class PostgreSQL ERD | `assets/diagrams/final/annotated/erd-1-full-smart-class-erd-redbox.svg` |
| ERD-2 | user/auth/device | `assets/diagrams/final/annotated/erd-2-user-auth-device-redbox.svg` |
| ERD-3 | course/enrollment/notice/material | `assets/diagrams/final/annotated/erd-3-course-enrollment-notice-material-redbox.svg` |
| ERD-4 | device/classroom/AP/presence | `assets/diagrams/final/annotated/erd-4-device-classroom-ap-presence-redbox.svg` |
| ERD-5 | attendance/session/record/audit | `assets/diagrams/final/annotated/erd-5-attendance-session-record-audit-redbox.svg` |
| ERD-6 | exam/question/submission/answer | `assets/diagrams/final/annotated/erd-6-exam-question-submission-answer-redbox.svg` |
| ERD-7 | selected LMS/assignment/Q&A/progress | `assets/diagrams/final/annotated/erd-7-selected-lms-assignment-qna-progress-redbox.svg` |
| ERD-8 | service/ops metadata와 N/A 경계 | `assets/diagrams/final/annotated/erd-8-service-ops-metadata-redbox.svg` |

## 4.4 UML/흐름 다이어그램

본문 다이어그램은 로그인/세션 복구, 출석 eligibility, 출석 세션 운영, Backend API 흐름, Presence snapshot/cache, CI pipeline을 포함한다. 각 다이어그램은 부록 D에서 위치와 목적을 추적한다.

# 5. 구현

## 5.1 사용 기술과 개발 환경

| 계층 | 기술 |
|---|---|
| Front | React, Vite, TypeScript, Playwright e2e |
| Backend | FastAPI, SQLAlchemy, pytest, WebSocket |
| PresenceService | FastAPI, Redis snapshot cache, pytest |
| DB | PostgreSQL, SQL init/migration, seed data |
| Service | Docker Compose, Nginx, GHCR image mode, release manifest |
| 문서 | Markdown, Mermaid, 보고서 부록/증거 원장 |

## 5.2 서비스별 구현

### 5.2.1 Front

Front는 학생, 교수, 서비스관리자 역할별 UI를 제공한다. 학생은 강의 목록, 공지, 학습자료, 과제, 성적/피드백, Q&A, 출석, 시험, 단말 등록을 사용한다. 교수는 담당 강의, 공지, 학습자료/과제, 시험 생성/게시/종료, 출석 timeline/roster/manual update, CSV export를 사용한다. 서비스관리자는 사용자/강의실/AP 매핑, threshold, presence snapshot, demo overlay를 관리한다.

### 5.2.2 Backend

Backend는 인증, API envelope, RBAC, LMS domain API, 출석/시험 도메인 판단, WebSocket publish를 담당한다. 출석에서는 bundle attendance session parent와 slot membership을 분리하고, self check-in과 professor manual update 모두 audit log를 남긴다. 시험에서는 객관식/참거짓 중심 MVP를 제공하고, 시험 시작/답안 저장/제출/교수 게시·종료 workflow를 구현한다.

### 5.2.3 PresenceService

PresenceService는 classroom snapshot, collector push, Redis cache, demo overlay, eligibility check를 담당한다. AP online 여부, 등록 단말 매칭, signal threshold, snapshot freshness를 reason code와 함께 반환한다. demo overlay는 실제 collector snapshot과 분리하여 로컬 시연 가능성과 운영 검증을 혼동하지 않게 한다.

### 5.2.4 DB

DB는 LMS/출석/시험/선택 LMS subset/운영 metadata를 schema와 seed로 관리한다. 출석 모델은 bundle parent, slot membership, slot별 records, append-only audit log를 가진다. 시험 모델은 exam, question, option, submission, answer 관계를 가진다. 선택 LMS subset은 assignment grading, Q&A, learning progress를 포함한다.

### 5.2.5 Service / CI-CD

Service repo는 runtime orchestration owner다. source build와 image mode compose, nginx routing, release manifest, demo deploy wrapper를 제공한다. 다만 최종보고서에서는 workflow-run 및 실제 demo server provenance가 부족한 부분을 실배포 완료가 아니라 부분 완료/후속 검증으로 표현한다.

## 5.3 코드 구조와 주요 구현 포인트

- 인증/세션: `Backend/app/main.py`의 login/refresh/bootstrap/logout과 `refresh_sessions` DB 모델로 cookie-backed session restore와 replay rejection을 다룬다.
- 출석 workflow: `Backend/app/attendance.py`와 `Backend/app/main.py` attendance endpoints가 timeline, batch open, roster, check-in, close, CSV export, WebSocket event를 처리한다.
- 시험 workflow: Backend exam endpoints와 Front exam route가 시험 목록, 응시, 답안 저장, 제출, 교수 관리 상태를 연결한다.
- PresenceService: `PresenceService/app/service.py`와 `app/main.py`가 snapshot/cache/overlay/collector/eligibility를 분리한다.
- DB: `DB/postgres/init/*.sql`과 `migrations/*.sql`이 schema source-of-truth이며, 보고서 ERD는 이 파일들을 기준으로 작성했다.

# 6. 실험 및 결과

## 6.1 테스트 방법

검증은 repo `main` 기준 테스트와 보고서 산출물 검증을 분리한다.

| 영역 | 대표 검증 |
|---|---|
| Front | `npm --prefix Front run lint`, `npm --prefix Front run build`, Playwright e2e (`auth-routing`, `exam-workflow`, `selected-lms-subset`) |
| Backend | `PYTHONPATH=. pytest -q`, `test_presence_admin_and_auth.py`, `test_lms_selected_subset.py`, `test_attendance_realtime.py`, `test_exam_contract_alignment.py` |
| PresenceService | `PYTHONPATH=. pytest -q`, `test_service.py`, `test_registry.py` |
| DB | SQL schema review, object storage trigger SQL, Backend/Presence tests를 통한 간접 계약 검증 |
| Service | release manifest contract tests, workspace release readiness tests |
| 보고서 | 부록 B-D/E, redbox asset 존재, ERD 산출물 존재, `git -C docs diff --check` |

## 6.2 기능 검증 결과

기능 검증 결과는 인증/세션, 역할별 UI, 강의/공지/선택 LMS, 출석, 시험, PresenceService, DB, Service/CI-CD로 나누어 부록 E에 정리했다. 완료도는 `완료`보다 보수적인 `로컬 MVP 완료` 또는 `부분 완료`를 사용했다. 이는 실운영 배포와 장기 현장 검증이 아직 분리된 한계이기 때문이다.

## 6.3 성능 평가와 운영 검증 경계

정량 부하 테스트는 아직 별도 benchmark로 수행하지 않았다. 대신 이번 주 Backend main에는 slow attendance bootstrap 중 realtime socket 연결성과 DB pool starvation을 완화하는 변경이 반영되었다. PresenceService는 Redis snapshot cache를 사용해 매 요청마다 OpenWrt 장비를 직접 조회하지 않도록 설계했다. 따라서 현재 성능 평가는 구조적 개선과 회귀 테스트 중심이며, 실제 강의실 다수 AP/다수 학생 부하 평가는 후속 과제다.

## 6.4 한계점

- OpenWrt 실제 장비 장기 현장 검증은 완료되지 않았다.
- Service image/manifest 검증은 있으나 workflow-run/demo server provenance가 부족하다.
- 학사시스템 정식 연동과 운영 인증 체계 연계는 후속 과제다.
- 네이티브 모바일 앱은 구현 범위가 아니다.
- 기존 화면 원본은 2026-04-12 캡처이므로 최종 제출 전 Service runtime 기준 재촬영 여부를 결정해야 한다.

# 7. 결론

## 7.1 성과

본 프로젝트는 LMS 핵심 기능과 재실성 기반 출석/시험 접근 제어를 하나의 웹 프로토타입으로 통합했다. 인증/세션, 역할별 UI, 강의/공지/read model, 출석 세션, 객관식 시험, PresenceService eligibility, DB schema/ERD, Service runtime 구조가 각각 근거와 함께 문서화되었다. 특히 출석 workflow는 단순 버튼 클릭이 아니라 수강, 시간표, 강의실, 등록 단말, AP snapshot, 교수 출석 세션을 결합하는 구조로 설계·구현되었다.

## 7.2 문제 해결 과정

초기 문제는 “로그인한 학생이 실제 강의실에 있는가”를 LMS가 판단하기 어렵다는 점이었다. 이를 해결하기 위해 네트워크 관측과 학사 도메인 판단을 분리했다. PresenceService는 단말/네트워크 근거를 제공하고, Backend는 수강/시간표/세션/권한을 결합해 최종 판정을 수행한다. 이후 bundle attendance session, slot fan-out record, append-only audit log, WebSocket update, CSV export로 교수 운영 흐름을 보강했다.

## 7.3 개선 방향

향후에는 실제 OpenWrt AP 장기 현장 테스트, 랜덤 MAC/개인정보 정책, 운영 배포와 관측 로그, 학사시스템 연동 가능성, 대규모 부하 테스트, selected-LMS 화면 캡처 보강을 진행해야 한다. 이 항목들은 본 보고서에서 완료 성과가 아니라 후속 과제로 분리한다.

# 8. 참고문헌

## 8.1 프로젝트 내부 문서

1. `docs/00-overview/project-summary.md`, 프로젝트 개요.
2. `docs/01-requirements/req-attendance-presence.md`, 출석/재실성 요구사항.
3. `docs/04-architecture/service-map.md`, 서비스 맵.
4. `docs/04-architecture/data-model-overview.md`, 데이터 모델 개요.
5. `docs/04-architecture/attendance-workflow-architecture.md`, 출석 workflow 아키텍처.
6. `docs/04-architecture/exam-workflow-api.md`, 시험 workflow API.
7. `docs/07-status/implementation-roadmap.md`, 구현 현황 및 검증 caveat.
8. `docs/08-reports/90-appendix/05-evidence-ledger.md`, 최종보고서 증거 원장.

## 8.2 기술 문서

1. FastAPI Documentation, API server and OpenAPI framework reference.
2. React Documentation, component-based UI reference.
3. Vite Documentation, frontend build tool reference.
4. PostgreSQL Documentation, relational database and SQL reference.
5. Redis Documentation, in-memory cache reference.
6. Docker Compose Documentation, multi-container local runtime reference.
7. Nginx Documentation, reverse proxy and WebSocket routing reference.
8. OpenWrt Documentation, router/AP platform reference.

## 8.3 코드 및 테스트 출처

- `Front/src/App.tsx`, `Front/src/api.ts`, `Front/src/router.ts`, `Front/tests/e2e/*.spec.ts`
- `Backend/app/main.py`, `Backend/app/attendance.py`, `Backend/app/services.py`, `Backend/tests/*.py`
- `PresenceService/app/main.py`, `PresenceService/app/service.py`, `PresenceService/tests/*.py`
- `DB/postgres/init/*.sql`, `DB/postgres/migrations/*.sql`, `DB/postgres/tests/*.sql`
- `Service/compose*.yml`, `Service/nginx/local.conf`, `Service/tests/*.py`, `Service/.github/workflows/*.yml`

# 9. 부록

- 부록 A: `docs/08-reports/90-appendix/01-source-map.md`
- 부록 B: `docs/08-reports/90-appendix/02-screenshot-checklist.md`
- 부록 C: `docs/08-reports/90-appendix/03-api-endpoint-inventory.md`
- 부록 D: `docs/08-reports/90-appendix/04-diagram-inventory.md`
- 부록 E: `docs/08-reports/90-appendix/05-evidence-ledger.md`
