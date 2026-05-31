---
title: 한국어 stop-slop 문체 규칙
type: report-appendix
status: active
updated: 2026-06-01
owners:
  - team
related:
  - [[/03-conventions/conv-final-report-writing.md]]
source:
  - https://github.com/hardikpandya/stop-slop
---

# 한국어 stop-slop 문체 규칙

`hardikpandya/stop-slop`은 AI 문체의 흔한 문구, 구조, 리듬을 줄이는 규칙이다. Smart Class 보고서에는 영어 문구 목록을 그대로 적용하지 않고 한국어 보고서에서 반복되는 표현을 기준으로 바꿔 적용한다.

# 차단 규칙

- `ChatGPT`, `AI가 작성`, `인공지능이 작성`, `AI 어시스턴트`처럼 작성 주체를 노출하는 문구는 제출용 본문에 남기지 않는다.
- `Here's the thing`, `Let that sink in`, `Moving forward` 같은 영어 stop-slop 문구가 남아 있으면 실패로 처리한다.
- `본 보고서에서는`, `본 장에서는`, `살펴보고자 한다`처럼 내용을 예고만 하는 문장은 실제 주장이나 근거로 바꾼다.

# 경고 규칙

- `이를 통해 ... 기대할 수 있다`는 원인과 결과가 구체적일 때만 둔다.
- `사용자 편의성 향상`, `효율성 강화`, `체계적인 관리`는 구체 화면, API, 테스트, 수치 중 하나로 바꾼다.
- `확인할 수 있다`, `볼 수 있다`가 반복되면 직접 서술로 줄인다.
- 수동형 문장은 행위자가 분명할 때 행위자와 동작을 앞에 둔다.

# 산출물

- `output/full-report-2026-06-01/qa/korean-stop-slop.json`
- `output/full-report-2026-06-01/qa/korean-stop-slop.md`
