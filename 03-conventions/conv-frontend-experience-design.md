---
title: 프론트엔드 경험 디자인 규약
type: convention
status: active
updated: 2026-03-30
owners:
  - frontend-team
applies_to:
  - frontend
related:
  - [[/01-requirements/req-student-features.md]]
  - [[/01-requirements/req-professor-features.md]]
  - [[/01-requirements/req-admin-features.md]]
  - [[/03-conventions/conv-auth-and-session.md]]
  - [[/03-conventions/conv-api-response.md]]
  - [[/02-decisions/adr-0004-attendance-authorization-flow.md]]
source:
  - https://developers.openai.com/blog/designing-delightful-frontends-with-gpt-5-4
  - [[/superpowers/specs/2026-03-30-front-delight-redesign-design.md]]
---

# 목적

`Front` 의 UI 작업이 임시 MVP 미감으로 되돌아가지 않도록, 화면 구조와 시각 판단 기준을 고정한다.

# 핵심 원칙

- 로그인 화면만 서사적 연출을 허용한다.
- 로그인 이후 앱 화면은 utility copy 와 작업 중심 구조를 기본값으로 한다.
- 학생 / 교수 / 관리자 화면은 같은 거대한 컴포넌트에 계속 누적하지 말고 역할별 surface 로 분리한다.
- 카드가 없어도 의미가 유지되면 카드가 아니다.
- dashboard-card mosaic 를 만들지 않는다.
- routine product UI 뒤에 장식용 gradient, 두꺼운 border, 과한 shadow 를 기본값으로 두지 않는다.
- 색상은 하나의 주요 accent 와 명확한 neutral hierarchy 를 사용한다.
- eligibility 결과는 사람용 설명, reason code, evidence 순으로 보여준다.
- 프론트는 backend / presence 의 판정 결과를 소비하며 business rule 을 재구현하지 않는다.

# 화면 구성 규칙

## 로그인

- 첫 화면은 제품 정체성과 진입 행동을 설명하는 단일 진입면으로 구성한다.
- 첫 화면의 기본 구성은 다음 순서를 따른다.
  1. 제품 식별
  2. 한 줄 핵심 메시지
  3. 짧은 보조 설명
  4. 로그인 폼
  5. 필요 최소한의 seed 계정 안내
- 로그인 화면에서만 분위기용 배경, 큰 타이포, 장면 연출을 허용한다.

## 로그인 이후 앱

- 앱 기본 구조는 `navigation + primary workspace + secondary context` 를 따른다.
- 학생 / 교수 / 관리자 화면은 marketing hero 대신 현재 할 수 있는 작업과 상태를 우선 배치한다.
- 상단 또는 측면 공통 shell 은 계정, 상태, 내비게이션을 안정적으로 제공해야 한다.
- 패널은 정보 구획을 돕는 수준까지만 사용하고, 의미 없는 박스 나열을 금지한다.

# 타이포그래피 / 토큰 규칙

- CSS token 을 먼저 정의하고 컴포넌트에서 직접 색상을 하드코딩하지 않는다.
- 최소 token 범위:
  - `background`
  - `surface`
  - `surface-strong`
  - `text`
  - `text-muted`
  - `accent`
  - `success`
  - `warning`
  - `danger`
- 타이포 역할은 최소 다음을 구분한다.
  - `display`
  - `heading`
  - `body`
  - `meta`
- radius, spacing, border intensity 도 scale 로 관리한다.

# 카피 규칙

- 앱 화면에서는 marketing copy 대신 utility copy 를 사용한다.
- 제목은 사용자가 있는 위치나 할 수 있는 행동을 설명해야 한다.
- 섹션은 한 가지 책임만 가진다.
- 출석 / 시험 결과는 사람이 바로 이해할 수 있는 한국어 문장을 먼저 보여준다.
- raw reason code 와 evidence 는 기술 확인용 보조 정보로 유지한다.

# 상태 / 결과 표현 규칙

- 성공, 주의, 실패 상태는 색과 문구가 동시에 구분되어야 한다.
- 상태 컴포넌트는 다음 순서를 따른다.
  1. 상태 제목
  2. 짧은 설명
  3. reason code
  4. evidence
- evidence 는 기본 요약보다 한 단계 낮은 시각 우선순위를 가져야 한다.

# 구현 워크플로 규칙

- 프론트 구현 전 아래 문서를 먼저 확인한다.
  - `../docs/01-requirements/req-student-features.md`
  - `../docs/01-requirements/req-professor-features.md`
  - `../docs/01-requirements/req-admin-features.md`
  - `../docs/03-conventions/conv-auth-and-session.md`
  - `../docs/03-conventions/conv-api-response.md`
- 큰 UI 변경 전에는 design token, shell 구조, 역할별 surface 경계를 먼저 정한다.
- 기능 추가나 리디자인은 TDD 순서를 따른다. 특히 view model, navigation, presenter 같은 순수 로직 seam 을 먼저 테스트로 잠근다.
- 큰 프론트 작업은 `Front/.codex/prompts/frontend-delight-redesign.md` 또는 이에 준하는 prompt 를 먼저 사용한다.

# 검증 체크리스트

## 자동 검증

- `npm run test:unit`
- `npm run lint`
- `npm run build`

## 수동 검증

- 로그인 화면 데스크톱
- 로그인 화면 모바일 폭
- 학생: 대시보드, 프로필, 기기 등록/삭제, 강의 상세, eligibility 결과
- 교수: 대시보드, 강의 상세, 공지 작성
- 관리자: 운영 화면, 강의실 / AP 정보 확인

## 시각 검증 질문

- 이 화면은 box 나열보다 workspace 처럼 보이는가
- accent color 가 적게, 그러나 분명하게 쓰였는가
- 첫 시선에 primary region 이 명확한가
- 삭제해도 되는 border / shadow / panel 이 남아 있지 않은가
- 모바일에서 텍스트와 터치 영역이 무너지지 않는가
