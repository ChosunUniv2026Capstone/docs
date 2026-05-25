---
title: HWP 최종보고서 생성 플레이북
type: report-playbook
status: active
updated: 2026-05-25
owners:
  - team
related:
  - [[/08-reports/00-index.md]]
  - [[/08-reports/01-report-template.md]]
  - [[/08-reports/99-combined-report.md]]
  - [[/08-reports/99-combined-report-appendix.md]]
  - [[/03-conventions/conv-final-report-writing.md]]
source:
  - [[/08-reports/99-combined-report.md]]
  - [[/08-reports/99-combined-report-appendix.md]]
---

# HWP 최종보고서 생성 플레이북

이 문서는 Smart Class 최종보고서를 HTML/PDF 검토본과 편집 가능한 HWP 파일로 다시 생성하기 위한 실행 절차와 검증 기준이다. 다음 보고서 작성자는 이 문서를 기준으로 본문 보고서와 부록 두 산출물을 같은 형식으로 재생성한다.

최종 독자가 열어야 하는 문서 산출물은 다음 두 파일이다.

1. `docs/08-reports/99-combined-report.md` - 보고서 본문
2. `docs/08-reports/99-combined-report-appendix.md` - 부록

다른 보고서 조각, 과거 부록, architecture/status/convention 문서는 작성 근거로만 사용한다. 최종 보고서와 부록만으로 프로젝트 목표, 설계, 구현, 화면 흐름, 코드, DB/ERD, 검증, 한계를 이해할 수 있어야 한다.

# 1. 산출물 구조

최종 생성 산출물은 두 갈래로 관리한다.

| 구분 | 목적 | 출력 위치 |
|---|---|---|
| HTML/PDF 검토본 | 브라우저 기반 레이아웃, PDF 페이지 이미지, 화면/ERD 크기 검증 | `output/revised-main-report` |
| 편집 가능 HWP | 제출용 한글 문서, 표/그림/쪽번호/제목 구조 검증 | `output/rhwp-editable` |

HTML/PDF는 HWP 생성 전 레이아웃 기준점이다. HWP는 별도 렌더링 특성이 있으므로 PDF가 정상이어도 HWP 렌더와 HWP 내부 속성 검증을 다시 수행한다.

# 2. 본문 작성 기준

보고서 본문은 최종보고서 문체로 작성한다. AI가 설명하는 듯한 표현, 작업 지시문, 파일 경로 나열 중심 문장은 줄이고 실제 제출 보고서에 들어갈 설명으로 구성한다.

본문에서는 다음 원칙을 유지한다.

- 구현 성과와 한계를 분리한다.
- 완료 주장은 화면, API, 코드, DB, 테스트 증거와 연결한다.
- 코드 전문을 길게 붙이지 않고, 꼭 필요한 핵심 로직만 짧게 인용한다.
- 화면/ERD asset 경로명보다 그림이 설명하는 기능, 강조 대상, 포함 범위를 설명한다.
- `redbox SVG`, `raw SVG` 같은 내부 asset 표현은 본문 설명 문장에 직접 노출하지 않는다.
- 보고서와 부록이 서로 보완하되, 둘 중 하나만 열어도 큰 흐름이 이해되도록 한다.

# 3. 페이지 구성

HWP 본문은 다음 페이지 흐름을 기준으로 만든다.

| 페이지 | 내용 | 규칙 |
|---|---|---|
| 1쪽 | 표지 | 산학프로젝트 보고서 제목, 과목/분반, 담당교수, 작성일자, GitHub/Docs/시연 링크, 팀원 표를 배치한다. |
| 2쪽 | 목차 자리 | 목차는 사용자가 HWP에서 직접 삽입하거나 편집한다. 자동 목차가 아니라 빈 목차 페이지를 유지한다. |
| 3쪽 이후 | 본문 | 실제 보고서 내용을 시작한다. |

제목 구조는 Markdown 제목 수준을 HWP 문단 스타일로 반영한다.

- 1수준 제목은 새 페이지에서 시작한다.
- 2수준 이하 제목은 같은 장 안에서 이어지되, HWP 스타일 수준을 잃지 않게 한다.
- 제목 번호는 장/절 번호 체계를 따른다. 전체 문단 번호처럼 `162. 9. 부록` 형태가 되지 않도록 변환 결과를 확인한다.
- 본문에서 강제로 쪽을 넘겨야 하는 경우는 장 시작, 큰 ERD, 표지/목차 분리에 한정한다.

# 4. 표 규칙

표는 반드시 HWP 표 개체로 들어가야 한다. 단순 텍스트, 이미지, 줄맞춤 문단으로 대체하지 않는다.

HWP 표 개체 속성은 다음과 같이 맞춘다.

| 항목 | 값 |
|---|---|
| 글자처럼 취급 | 끔 |
| 본문과의 배치 | 자리차지 |
| 표 여러 쪽 지원 | 쪽 경계에서 셀 단위 나눔 |
| 제목 행 반복 | 켬 |
| 겹침 허용 | 끔 |

긴 표는 여러 표로 억지로 나누지 않는다. `코드 1/2`, `코드 2/2`처럼 나누어 둔 표기는 하나의 표로 합친다. 페이지를 넘어가더라도 표 개체 자체가 유지되게 하고, 헤더 반복과 셀 단위 나눔으로 처리한다.

# 5. 코드블록 규칙

코드블록은 1x1 HWP 표로 넣는다. 일반 문단이나 이미지로 넣지 않는다.

코드 인용은 다음 기준을 따른다.

- 본문은 핵심 로직 위주로 짧게 인용한다.
- 긴 코드 전문은 부록으로 보내거나 생략하고, 파일 경로와 역할 설명으로 대체한다.
- 코드 표는 가능한 한 하나의 1x1 표로 유지한다.
- 코드 표 안의 글자 크기는 본문보다 작게 두되, 읽을 수 없는 수준으로 줄이지 않는다.

# 6. 그림과 화면 캡처 규칙

그림은 페이지 폭과 높이를 넘지 않게 제한한다. HWP에서 그림이 페이지 밖으로 밀리거나 너무 작아지면 실패로 본다.

화면 캡처는 다음 기준으로 넣는다.

- 가로형 화면은 본문 폭 안에서 읽히는 크기로 배치한다.
- 세로 길이가 가로 길이보다 큰 이미지는 필요한 설명 대상 주변만 포함하도록 크롭한다.
- 강조 대상이 있는 이미지는 그림 설명에서 무엇을 확인해야 하는지 적는다.
- 내부 asset 파일명이나 `redbox`라는 표현을 본문 설명에 그대로 쓰지 않는다.
- 그림이 너무 작아 기능을 판별할 수 없으면 크기 제한값을 조정하고 PDF/HWP 렌더를 다시 확인한다.

# 7. ERD와 DB 설명 규칙

전체 ERD는 세로 한 페이지에 들어가는 개요형 그림으로 유지한다. 전체 테이블을 한 그림에 모두 넣으면 세부 컬럼 가독성이 낮으므로, 본문/부록은 다음 구조를 함께 사용한다.

1. 전체 테이블 목록 표
   - 실제 테이블 이름
   - 한국어 역할 설명
2. 전체 ERD 한 페이지 개요
   - 도메인 경계와 주요 관계를 빠르게 확인하기 위한 그림
3. 주요 테이블 상세 ERD
   - 약 15개 핵심 테이블을 Mermaid ERD 기반 이미지로 생성해 포함
   - 테이블명뿐 아니라 주요 컬럼과 관계를 확인할 수 있어야 함

ERD 설명은 asset 경로 나열보다 다음 정보를 우선한다.

- 강조 대상 도메인
- 포함 테이블/노드
- 해당 그림으로 확인할 수 있는 설계 의도

# 8. 실행 절차

실행은 repository 루트 `smart-class`에서 수행한다.

1. HTML/PDF 검토본 생성

```powershell
node .omx\kordoc-runtime\scripts\build-revised-main-report.mjs
```

2. HWP 보정 도구 빌드

```powershell
Push-Location .omx\rhwp-tools
cargo build --release
Pop-Location
```

3. 편집 가능 HWP 생성

```powershell
node .omx\kordoc-runtime\scripts\build-editable-hwp.cjs
```

주요 스크립트 역할은 다음과 같다.

| 파일 | 역할 |
|---|---|
| `.omx/kordoc-runtime/scripts/build-revised-main-report.mjs` | Markdown 본문/부록을 HTML, PDF, QA 이미지로 렌더링한다. 화면 캡처, ERD, Mermaid/diagram 산출물 크기와 배치를 조정한다. |
| `.omx/kordoc-runtime/scripts/build-editable-hwp.cjs` | HTML/PDF 기준 내용을 편집 가능한 HWP로 재구성한다. 표지, 목차 자리, 제목, 표, 코드블록, 그림, 쪽번호를 생성한다. |
| `.omx/rhwp-tools/src/main.rs` | 생성된 HWP의 표 속성과 쪽번호를 rhwp로 후처리한다. |

# 9. 검증 체크리스트

검증은 생성 명령이 끝났다는 사실만으로 완료하지 않는다. 아래 항목이 모두 통과해야 한다.

| 검증 항목 | 확인 방법 |
|---|---|
| Markdown 원본 | `99-combined-report.md`, `99-combined-report-appendix.md`가 최종 내용 기준인지 확인 |
| HTML/PDF 생성 | `output/revised-main-report` 산출물과 QA JSON 확인 |
| PDF 페이지 이미지 | `output/revised-main-report/qa/pdf-pages`, `output/revised-main-report/qa/appendix-pages`를 페이지 단위로 확인 |
| HWP 생성 | `output/rhwp-editable`에 본문/부록 HWP가 생성되었는지 확인 |
| HWP 표 속성 | build summary와 rhwp patch log에서 표 개체 속성 보정이 실행되었는지 확인 |
| 쪽번호 | HWP 하단 중앙 쪽번호가 활성화되었는지 page-number verify JSON과 렌더 이미지로 확인 |
| 제목 수준 | 1/2/3수준 제목이 HWP에서 제목 수준으로 보이는지 확인 |
| 페이지 바꿈 | 1수준 제목은 새 페이지, 불필요한 빈 페이지나 흐름을 끊는 페이지 바꿈은 없는지 확인 |
| 그림 크기 | 화면 캡처와 ERD가 페이지 밖으로 넘치지 않고, 너무 작아지지 않았는지 확인 |
| 표 페이지 나눔 | 긴 표가 셀 단위로 넘어가며 헤더가 유지되는지 확인 |
| 코드블록 | 코드가 1x1 표로 들어가며 여러 표로 불필요하게 쪼개지지 않았는지 확인 |

# 10. PR 전 문서 검증

보고서 생성 플레이북이나 보고서 원본을 변경한 뒤 PR을 올리기 전에는 다음 검증을 수행한다.

```powershell
git -C docs diff --check
node --check .omx\kordoc-runtime\scripts\build-revised-main-report.mjs
node --check .omx\kordoc-runtime\scripts\build-editable-hwp.cjs
Push-Location .omx\rhwp-tools
cargo build --release
Pop-Location
```

필요하면 실제 산출물 생성 명령까지 다시 실행한다.

```powershell
node .omx\kordoc-runtime\scripts\build-revised-main-report.mjs
node .omx\kordoc-runtime\scripts\build-editable-hwp.cjs
```

# 11. 문제 해결

| 증상 | 처리 |
|---|---|
| HWP 파일 쓰기 실패 | HWP 파일이 열려 있을 수 있으므로 닫고 다시 실행한다. 필요하면 timestamp가 붙은 대체 파일명으로 생성한다. |
| 표가 문단처럼 밀림 | rhwp 후처리가 실행되었는지 확인하고, 표 속성 patch를 다시 적용한다. |
| 표가 페이지에서 깨짐 | 글자처럼 취급이 꺼졌는지, 쪽 경계에서 셀 단위 나눔이 적용되었는지 확인한다. |
| 그림이 너무 작음 | 이미지 제한값을 조정하되, PDF/HWP 렌더에서 페이지 밖으로 넘치지 않는지 다시 확인한다. |
| 세로형 캡처가 페이지를 넘침 | 원본 전체를 넣지 말고 설명 대상 주변으로 크롭한다. |
| 제목 번호가 이상함 | Markdown 제목 numbering과 HWP 변환 numbering을 다시 확인한다. 전역 문단 번호처럼 누적되면 실패다. |
| 목차가 목차 개체가 아님 | 목차 페이지는 자리만 유지한다. 최종 제출 전 HWP에서 사용자가 직접 목차를 삽입하거나 편집한다. |

# 12. 유지보수 규칙

다음 항목이 바뀌면 이 플레이북을 함께 갱신한다.

- 최종 보고서 source of truth 파일명
- HTML/PDF 또는 HWP 생성 스크립트 경로
- HWP 표 속성 후처리 방식
- 쪽번호 생성 방식
- 화면 캡처/ERD 생성 방식
- PR 전 필수 검증 명령

플레이북과 스크립트가 서로 다르면 스크립트가 현재 실행 기준이고, 플레이북은 즉시 수정 대상이다.
