---
title: Redbox 캡처 품질 게이트
type: report-appendix
status: active
updated: 2026-06-01
owners:
  - team
related:
  - [[/03-conventions/conv-final-report-writing.md]]
---

# Redbox 캡처 품질 게이트

최종보고서의 화면 근거 이미지는 SVG 후처리 합성이 아니라 HTML 레벨에서 redbox를 삽입한 뒤 PNG로 캡처한다.

# 생성 방식

1. 실제 서비스 화면은 캡처 직전에 대상 DOM 요소에 redbox와 라벨을 삽입한다.
2. 기존 PNG나 ERD SVG처럼 HTML 화면이 아닌 자료는 원본 이미지를 HTML `<img>`로 배치하고 redbox / 라벨을 absolute positioned HTML 요소로 올린다.
3. 브라우저 screenshot 결과를 `docs/08-reports/assets/**/html-redbox/*.png`에 저장한다.

# 검증 방식

- redbox 좌표가 이미지 캔버스 안에 있는지 확인한다.
- 최종 PNG의 예상 redbox 상/하/좌/우 경계에서 red pixel sampling을 수행한다.
- 라벨은 DOM 기준으로 `scrollWidth <= clientWidth`, `scrollHeight <= clientHeight`를 만족해야 한다.
- 과거 고정 라벨 상자 `360x40`에서 넘쳤던 라벨도 별도 기록해 다음 작성 때 같은 문제가 반복되지 않게 한다.

# 산출물

- `output/full-report-2026-06-01/qa/html-redbox-assets.json`
- `output/full-report-2026-06-01/qa/html-redbox-assets.md`
