const pptxgen = require("pptxgenjs");
const {
  warnIfSlideHasOverlaps,
  warnIfSlideElementsOutOfBounds,
} = require("./pptxgenjs_helpers/layout");
const { safeOuterShadow } = require("./pptxgenjs_helpers/util");

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
pptx.author = "Codex";
pptx.company = "Smart Class";
pptx.subject = "Weekly project progress";
pptx.title = "스마트 클래스 서비스 W4 진행 업데이트";
pptx.lang = "ko-KR";
pptx.theme = {
  headFontFace: "Pretendard Variable",
  bodyFontFace: "Pretendard Variable",
  lang: "ko-KR",
};

const COLORS = {
  navy: "1E3A5F",
  navyDeep: "18304F",
  blue: "2C5E96",
  sky: "EAF2FB",
  line: "C6D3E3",
  text: "1B2A38",
  muted: "64748B",
  white: "FFFFFF",
  green: "2E8B57",
  amber: "D97706",
  red: "C0392B",
  gray: "EEF2F7",
};

function addPageNo(slide, n) {
  slide.addText(String(n), {
    x: 12.75,
    y: 7.05,
    w: 0.35,
    h: 0.18,
    fontFace: "Pretendard Variable",
    fontSize: 9,
    color: COLORS.muted,
    align: "right",
    margin: 0,
  });
}

function addHeader(slide, title, page) {
  slide.background = { color: COLORS.white };
  slide.addShape(pptx.ShapeType.rect, {
    x: 0,
    y: 0,
    w: 13.333,
    h: 0.32,
    line: { color: COLORS.navy, transparency: 100 },
    fill: { color: COLORS.navy },
  });
  slide.addShape(pptx.ShapeType.line, {
    x: 0.25,
    y: 0.72,
    w: 0,
    h: 0.38,
    line: { color: COLORS.navy, width: 1.8 },
  });
  slide.addText(title, {
    x: 0.38,
    y: 0.62,
    w: 4.8,
    h: 0.35,
    fontFace: "Pretendard Variable",
    fontSize: 21,
    bold: true,
    color: COLORS.text,
    margin: 0,
  });
  addPageNo(slide, page);
}

function addBulletList(slide, items, opts = {}) {
  const x = opts.x ?? 0.8;
  const y = opts.y ?? 1.55;
  const w = opts.w ?? 5.6;
  const h = opts.h ?? 4.8;
  const fontSize = opts.fontSize ?? 18;
  const runs = [];
  items.forEach((item) => {
    runs.push({
      text: item,
      options: {
        breakLine: true,
        bullet: { indent: fontSize * 0.9 },
      },
    });
  });
  slide.addText(runs, {
    x,
    y,
    w,
    h,
    margin: 0.03,
    fontFace: "Pretendard Variable",
    fontSize,
    color: COLORS.text,
    breakLine: false,
    paraSpaceAfterPt: 10,
    valign: "top",
  });
}

function addCard(slide, x, y, w, h, title, body, fill = COLORS.white) {
  slide.addShape(pptx.ShapeType.roundRect, {
    x,
    y,
    w,
    h,
    rectRadius: 0.08,
    line: { color: COLORS.line, width: 1 },
    fill: { color: fill },
    shadow: safeOuterShadow("355070", 0.12, 45, 1.5, 1),
  });
  slide.addText(title, {
    x: x + 0.2,
    y: y + 0.18,
    w: w - 0.4,
    h: 0.25,
    fontFace: "Pretendard Variable",
    fontSize: 15,
    bold: true,
    color: COLORS.navy,
    margin: 0,
  });
  slide.addText(body, {
    x: x + 0.2,
    y: y + 0.52,
    w: w - 0.4,
    h: h - 0.68,
    fontFace: "Pretendard Variable",
    fontSize: 11.5,
    color: COLORS.text,
    margin: 0,
    valign: "top",
  });
}

function finalize(slide) {
  warnIfSlideHasOverlaps(slide, pptx, { muteContainment: true });
  warnIfSlideElementsOutOfBounds(slide, pptx);
}

// Slide 1: Cover
{
  const slide = pptx.addSlide();
  slide.background = { color: COLORS.navy };
  slide.addShape(pptx.ShapeType.line, {
    x: 11.4,
    y: 0.32,
    w: 1.45,
    h: 0,
    line: { color: "8FA8C7", width: 1.2 },
  });
  slide.addShape(pptx.ShapeType.line, {
    x: 10.5,
    y: 6.75,
    w: 2.2,
    h: 0,
    line: { color: "8FA8C7", width: 1.2 },
  });
  slide.addText("Wi-Fi 기반 위치 판별과 디바이스 인증을 결합한", {
    x: 0.6,
    y: 1.45,
    w: 7.2,
    h: 0.36,
    fontFace: "Pretendard Variable",
    fontSize: 19,
    color: COLORS.white,
    margin: 0,
  });
  slide.addText("스마트 클래스 서비스", {
    x: 0.6,
    y: 1.95,
    w: 6.4,
    h: 0.45,
    fontFace: "Pretendard Variable",
    fontSize: 27,
    bold: true,
    color: COLORS.white,
    margin: 0,
  });
  slide.addText("W4 진행 업데이트", {
    x: 0.6,
    y: 2.45,
    w: 4.4,
    h: 0.42,
    fontFace: "Pretendard Variable",
    fontSize: 23,
    bold: true,
    color: "C8DAEF",
    margin: 0,
  });
  slide.addText("조선대학교 차세대 사이버캠퍼스 프로토타입\n기준 시점: 2026-03-30\n초점: 현재 저장소 변경사항과 다음 단계 정리", {
    x: 0.62,
    y: 4.82,
    w: 4.8,
    h: 1.1,
    fontFace: "Pretendard Variable",
    fontSize: 11.5,
    color: "D6E2F0",
    margin: 0,
    breakLine: true,
  });
  slide.addText("1", {
    x: 12.85,
    y: 7.05,
    w: 0.2,
    h: 0.18,
    fontFace: "Pretendard Variable",
    fontSize: 9,
    color: "D6E2F0",
    align: "right",
    margin: 0,
  });
}

// Slide 2: Agenda
{
  const slide = pptx.addSlide();
  addHeader(slide, "목차", 2);
  slide.addShape(pptx.ShapeType.rect, {
    x: 0.8,
    y: 1.35,
    w: 2.3,
    h: 5.05,
    line: { color: COLORS.navy, transparency: 100 },
    fill: { color: COLORS.navy },
  });
  slide.addText(
    [
      { text: "01\n", options: { bold: true, fontSize: 18, color: COLORS.white } },
      { text: "이번 주 핵심 변화", options: { breakLine: true, color: COLORS.white } },
      { text: "\n02\n", options: { bold: true, fontSize: 18, color: COLORS.white } },
      { text: "저장소별 구현 진행", options: { breakLine: true, color: COLORS.white } },
      { text: "\n03\n", options: { bold: true, fontSize: 18, color: COLORS.white } },
      { text: "현재 단계와 아키텍처", options: { breakLine: true, color: COLORS.white } },
      { text: "\n04\n", options: { bold: true, fontSize: 18, color: COLORS.white } },
      { text: "리스크와 다음 액션", options: { color: COLORS.white } },
    ],
    {
      x: 1.1,
      y: 1.8,
      w: 1.7,
      h: 4.8,
      fontFace: "Pretendard Variable",
      fontSize: 15,
      margin: 0,
      valign: "mid",
      color: COLORS.white,
      breakLine: false,
    }
  );
  addBulletList(
    slide,
    [
      "문서 기준 source of truth와 저장소 분리 구조가 실제 작업 흐름으로 고정되었습니다.",
      "Front, Backend, PresenceService, DB에 각자 첫 번째 구현 뼈대가 생겼습니다.",
      "이번 W4는 제안서가 아니라 현재 구현 상태를 설명하는 주간 업데이트용 덱입니다.",
    ],
    { x: 3.5, y: 1.65, w: 8.5, h: 3.9, fontSize: 17 }
  );
  addCard(
    slide,
    3.55,
    5.35,
    4.05,
    1.0,
    "이번 주 포인트",
    "기능 범위보다 구현 경계와 실행 가능 구조를 먼저 고정했습니다.",
    COLORS.sky
  );
  addCard(
    slide,
    7.85,
    5.35,
    4.05,
    1.0,
    "발표 방향",
    "‘왜 필요한가’보다 ‘지금 어디까지 만들었는가’ 중심으로 재구성했습니다.",
    COLORS.gray
  );
  finalize(slide);
}

// Slide 3: Highlights
{
  const slide = pptx.addSlide();
  addHeader(slide, "이번 주 핵심 변화", 3);
  addBulletList(
    slide,
    [
      "docs 저장소를 중심으로 요구사항·로드맵·리스크·오픈질문이 현재 기준으로 정리되었습니다.",
      "CodexKit이 워크스페이스 부트스트랩, docs seed, 브랜치 규약을 묶는 운영 패키지로 자리 잡았습니다.",
      "프론트·백엔드·재실성 서비스·DB에 각각 첫 번째 실행 가능한 slice가 생겼습니다.",
      "주간 진행 발표를 계속 고도화할 수 있도록 PPTX와 manifest를 Git으로 관리하는 방향을 확정했습니다.",
    ],
    { x: 0.9, y: 1.35, w: 7.15, h: 4.9, fontSize: 18 }
  );
  addCard(slide, 8.35, 1.45, 4.15, 1.1, "문서", "로드맵 / 리스크 / 운영 규칙 정리", COLORS.sky);
  addCard(slide, 8.35, 2.85, 4.15, 1.1, "구현", "서비스별 첫 번째 뼈대 확보", COLORS.gray);
  addCard(slide, 8.35, 4.25, 4.15, 1.1, "발표", "주간 덱 증분 편집 체계 정의", COLORS.sky);
  addCard(slide, 8.35, 5.65, 4.15, 0.7, "상태 판단", "제안 단계 -> 구현 진행 보고 단계로 전환", "F4F8FC");
  finalize(slide);
}

// Slide 4: Repo progress
{
  const slide = pptx.addSlide();
  addHeader(slide, "저장소별 구현 진행", 4);
  const rows = [
    [
      { text: "저장소", options: { bold: true, color: COLORS.white } },
      { text: "이번 상태", options: { bold: true, color: COLORS.white } },
      { text: "판단", options: { bold: true, color: COLORS.white } },
    ],
    ["docs", "로드맵·리스크·오픈질문·슬라이드 운영 설계 정리", "기준 문서 정착"],
    ["CodexKit", "워크스페이스 부트스트랩 / docs seed / 브랜치 규약 반영", "운영 기반 확보"],
    ["Front", "로그인·프로필·강의 페이지 재구성", "UI 뼈대 진행 중"],
    ["Backend", "출석 eligibility 및 read-model spine 구축", "도메인 뼈대 진행 중"],
    ["PresenceService", "OpenWrt형 더미 수집 서비스 제공", "연동 기반 확보"],
    ["DB", "CSV 기반 데모 데이터와 attendance slice 시드", "데이터 기반 확보"],
  ];
  slide.addTable(rows, {
    x: 0.7,
    y: 1.45,
    w: 12,
    h: 4.8,
    border: { type: "solid", color: COLORS.line, pt: 1 },
    fill: COLORS.white,
    color: COLORS.text,
    fontFace: "Pretendard Variable",
    fontSize: 13,
    margin: 0.08,
    rowH: 0.52,
    colW: [1.75, 7.75, 2.5],
    autoFit: false,
    valign: "mid",
    fillHeader: COLORS.navy,
  });
  addCard(
    slide,
    0.8,
    6.35,
    12.0,
    0.62,
    "해석",
    "각 저장소가 서로 다른 책임을 가진 상태로 첫 구현 조각을 확보했습니다. 다음 주부터는 slice 간 연결과 검증의 비중이 커집니다.",
    "F8FBFE"
  );
  finalize(slide);
}

// Slide 5: Phase status
{
  const slide = pptx.addSlide();
  addHeader(slide, "현재 단계와 범위", 5);
  addCard(slide, 0.8, 1.4, 3.85, 3.65, "Phase 1", "로그인, 단말 관리, eligibility, Docker 실행의 기본 동작 확보", COLORS.sky);
  addCard(slide, 4.75, 1.4, 3.85, 3.65, "Phase 2", "강의 목록 / 공지 / 관리자 조회의 1차 뼈대 구현", COLORS.gray);
  addCard(slide, 8.7, 1.4, 3.85, 3.65, "Phase 3+", "강의자료 / 동영상 / 과제 / 퀴즈 / 성적은 계획 수립 완료, 아직 미착수", COLORS.sky);
  slide.addShape(pptx.ShapeType.line, {
    x: 1.7,
    y: 5.45,
    w: 9.9,
    h: 0,
    line: { color: COLORS.navy, width: 1.5, beginArrowType: "none", endArrowType: "triangle" },
  });
  slide.addText("기본 동작 확보", {
    x: 1.0,
    y: 5.62,
    w: 2.0,
    h: 0.25,
    fontFace: "Pretendard Variable",
    fontSize: 12,
    color: COLORS.muted,
    margin: 0,
  });
  slide.addText("조회 중심 뼈대 확장", {
    x: 4.75,
    y: 5.62,
    w: 2.3,
    h: 0.25,
    fontFace: "Pretendard Variable",
    fontSize: 12,
    color: COLORS.muted,
    margin: 0,
  });
  slide.addText("콘텐츠·평가 기능 연결", {
    x: 8.55,
    y: 5.62,
    w: 2.6,
    h: 0.25,
    fontFace: "Pretendard Variable",
    fontSize: 12,
    color: COLORS.muted,
    margin: 0,
  });
  finalize(slide);
}

// Slide 6: Architecture now
{
  const slide = pptx.addSlide();
  addHeader(slide, "현재 아키텍처 진행 포인트", 6);
  addCard(slide, 0.85, 1.55, 2.35, 2.2, "Front", "학생/교수/관리자 UI\n로그인·프로필·강의 화면", COLORS.sky);
  addCard(slide, 3.4, 1.55, 2.35, 2.2, "Backend", "LMS 도메인 + eligibility\nread model spine", COLORS.gray);
  addCard(slide, 5.95, 1.55, 2.35, 2.2, "PresenceService", "OpenWrt형 단말 연결 정보 수집\n재실성 보조", COLORS.sky);
  addCard(slide, 8.5, 1.55, 2.35, 2.2, "DB", "attendance slice demo data\nCSV 기반 초기값", COLORS.gray);
  addCard(slide, 11.05, 1.55, 1.45, 2.2, "docs", "요구사항/규약/상태", COLORS.sky);
  slide.addShape(pptx.ShapeType.chevron, { x: 3.03, y: 2.35, w: 0.22, h: 0.35, line: { color: COLORS.navy, transparency: 100 }, fill: { color: COLORS.navy } });
  slide.addShape(pptx.ShapeType.chevron, { x: 5.58, y: 2.35, w: 0.22, h: 0.35, line: { color: COLORS.navy, transparency: 100 }, fill: { color: COLORS.navy } });
  slide.addShape(pptx.ShapeType.chevron, { x: 8.13, y: 2.35, w: 0.22, h: 0.35, line: { color: COLORS.navy, transparency: 100 }, fill: { color: COLORS.navy } });
  slide.addShape(pptx.ShapeType.chevron, { x: 10.68, y: 2.35, w: 0.22, h: 0.35, line: { color: COLORS.navy, transparency: 100 }, fill: { color: COLORS.navy } });
  addBulletList(
    slide,
    [
      "핵심은 서비스별 책임을 먼저 분리하고, eligibility와 attendance 흐름을 연결 가능한 상태로 만드는 것입니다.",
      "docs와 CodexKit이 구현보다 먼저 경계를 고정해 주기 때문에 이후 기능 확장 시 서비스 혼선을 줄일 수 있습니다.",
    ],
    { x: 0.9, y: 4.35, w: 11.9, h: 2.1, fontSize: 16 }
  );
  finalize(slide);
}

// Slide 7: Operating improvements
{
  const slide = pptx.addSlide();
  addHeader(slide, "문서 및 운영 개선", 7);
  addCard(slide, 0.85, 1.45, 4.0, 2.0, "docs", "source of truth 역할 정착\n로드맵·리스크·오픈질문이 현재 기준으로 갱신됨", COLORS.sky);
  addCard(slide, 4.95, 1.45, 4.0, 2.0, "CodexKit", "workspace bootstrap, docs seed, 브랜치 규약을 하나의 운영 패키지로 정리", COLORS.gray);
  addCard(slide, 9.05, 1.45, 3.45, 2.0, "slides workflow", "PPTX + manifest + notes를 Git으로 관리하는 주간 덱 운영 방향 합의", COLORS.sky);
  slide.addText("의미", {
    x: 0.9,
    y: 4.0,
    w: 1.0,
    h: 0.28,
    fontFace: "Pretendard Variable",
    fontSize: 16,
    bold: true,
    color: COLORS.navy,
    margin: 0,
  });
  addBulletList(
    slide,
    [
      "문서가 구현보다 한 발 앞서면서, 기능 추가 시 어떤 저장소에서 무엇을 해야 하는지가 더 명확해졌습니다.",
      "발표 자료도 일회성 산출물이 아니라 점진적으로 고도화되는 프로젝트 자산으로 전환합니다.",
    ],
    { x: 0.9, y: 4.4, w: 11.7, h: 1.8, fontSize: 17 }
  );
  finalize(slide);
}

// Slide 8: Risks and open questions
{
  const slide = pptx.addSlide();
  addHeader(slide, "리스크와 오픈 질문", 8);
  addCard(slide, 0.85, 1.4, 5.95, 4.9, "주요 리스크", "• OpenWrt / 게이트웨이 환경에서 필요한 단말 정보를 안정적으로 수집할 수 있는지 검증 필요\n• 랜덤 MAC 활성화 시 등록 단말 매칭 실패 가능\n• Redis snapshot 캐시 만료 구간에 수집 부하 집중 위험\n• 시험 접근 제어 범위를 너무 빠르게 넓히면 운영 복잡도 급증", COLORS.gray);
  addCard(slide, 6.95, 1.4, 5.55, 4.9, "오픈 질문", "• 시험 접근 제어에 재실성 조건을 어디까지 적용할 것인가\n• 실제 교내 Wi-Fi 환경에서 사용할 수 있는 식별자 범위는 어디까지인가\n• 수강신청과 관리자 기능의 MVP 우선순위는 어떻게 정할 것인가\n• OpenWrt 수집 실패 시 fail-close 정책을 어느 수준까지 둘 것인가", COLORS.sky);
  finalize(slide);
}

// Slide 9: Next actions
{
  const slide = pptx.addSlide();
  addHeader(slide, "다음 주 액션", 9);
  addCard(slide, 0.85, 1.45, 3.85, 3.7, "개발", "Front / Backend / PresenceService / DB의 첫 slice를 실제 흐름으로 연결합니다.\n\n출석 eligibility와 단말 등록 경로를 우선 검증합니다.", COLORS.sky);
  addCard(slide, 4.9, 1.45, 3.85, 3.7, "문서", "로드맵과 리스크를 구현 결과에 맞춰 계속 갱신합니다.\n\n발표 자료는 manifest 기반 주간 증분 편집으로 전환합니다.", COLORS.gray);
  addCard(slide, 8.95, 1.45, 3.55, 3.7, "검증", "OpenWrt 수집 가능 정보와 랜덤 MAC 영향을 실제 환경에서 확인합니다.\n\nDocker 로컬 런타임을 연결 검증 단위로 삼습니다.", COLORS.sky);
  slide.addText("요약", {
    x: 0.95,
    y: 5.65,
    w: 0.9,
    h: 0.22,
    fontFace: "Pretendard Variable",
    fontSize: 16,
    bold: true,
    color: COLORS.navy,
    margin: 0,
  });
  slide.addText("이번 W4는 ‘무엇을 만들 것인가’보다 ‘지금 어떤 구조와 구현 조각이 확보되었는가’를 보여주는 업데이트 덱입니다.", {
    x: 0.95,
    y: 6.02,
    w: 11.7,
    h: 0.4,
    fontFace: "Pretendard Variable",
    fontSize: 17,
    color: COLORS.text,
    margin: 0,
  });
  finalize(slide);
}

(async () => {
  const out = "../../published/w4.pptx";
  await pptx.writeFile({ fileName: out });
  console.log(`Wrote ${out}`);
})().catch((err) => {
  console.error(err);
  process.exit(1);
});
