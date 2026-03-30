from copy import deepcopy
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt


ROOT = Path("/Users/kimhyeonseok/CodeStorage/smart-class/docs/08-slide-decks/weekly-progress")
BASE = ROOT / "published" / "w3.pptx"
OUT = ROOT / "published" / "w4.pptx"

NAVY = RGBColor(0x1E, 0x3A, 0x5F)
BLUE = RGBColor(0x2C, 0x5E, 0x96)
SKY = RGBColor(0xEA, 0xF2, 0xFB)
GRAY = RGBColor(0xEE, 0xF2, 0xF7)
LINE = RGBColor(0xC6, 0xD3, 0xE3)
TEXT = RGBColor(0x1B, 0x2A, 0x38)
MUTED = RGBColor(0x64, 0x74, 0x8B)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)


def set_text_frame(text_frame, text, font_size=14, bold=False, color=TEXT):
    text_frame.clear()
    lines = text.split("\n")
    for idx, line in enumerate(lines):
        p = text_frame.paragraphs[0] if idx == 0 else text_frame.add_paragraph()
        p.text = line
        p.font.name = "Pretendard"
        p.font.size = Pt(font_size)
        p.font.bold = bold
        p.font.color.rgb = color
        p.space_after = Pt(0)
        p.line_spacing = 1.1


def add_top_title(slide, title, page_no):
    line = slide.shapes.add_shape(
        MSO_AUTO_SHAPE_TYPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.22)
    )
    line.fill.solid()
    line.fill.fore_color.rgb = NAVY
    line.line.color.rgb = NAVY

    accent = slide.shapes.add_shape(
        MSO_AUTO_SHAPE_TYPE.RECTANGLE, Inches(0.24), Inches(0.72), Inches(0.03), Inches(0.34)
    )
    accent.fill.solid()
    accent.fill.fore_color.rgb = NAVY
    accent.line.color.rgb = NAVY

    title_box = slide.shapes.add_textbox(Inches(0.38), Inches(0.58), Inches(4.8), Inches(0.4))
    set_text_frame(title_box.text_frame, title, font_size=21, bold=True, color=TEXT)

    page_box = slide.shapes.add_textbox(Inches(12.82), Inches(7.04), Inches(0.22), Inches(0.18))
    tf = page_box.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    p.text = str(page_no)
    p.alignment = PP_ALIGN.RIGHT
    p.font.name = "Pretendard"
    p.font.size = Pt(9)
    p.font.color.rgb = MUTED


def add_card(slide, x, y, w, h, title, body, fill_rgb):
    box = slide.shapes.add_shape(
        MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h)
    )
    box.fill.solid()
    box.fill.fore_color.rgb = fill_rgb
    box.line.color.rgb = LINE
    box.line.width = Pt(1)

    title_box = slide.shapes.add_textbox(Inches(x + 0.16), Inches(y + 0.14), Inches(w - 0.32), Inches(0.24))
    set_text_frame(title_box.text_frame, title, font_size=14, bold=True, color=NAVY)

    body_box = slide.shapes.add_textbox(Inches(x + 0.16), Inches(y + 0.46), Inches(w - 0.32), Inches(h - 0.58))
    set_text_frame(body_box.text_frame, body, font_size=11.5, color=TEXT)
    body_box.text_frame.vertical_anchor = MSO_ANCHOR.TOP


def add_bullets(slide, x, y, w, h, items, font_size=17):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.clear()
    for idx, item in enumerate(items):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.text = item
        p.level = 0
        p.bullet = True
        p.font.name = "Pretendard Variable"
        p.font.size = Pt(font_size)
        p.font.color.rgb = TEXT
        p.space_after = Pt(8)
        p.line_spacing = 1.12


def clone_thanks_to_end(prs):
    sldIdLst = prs.slides._sldIdLst
    thanks = sldIdLst[17]
    sldIdLst.remove(thanks)
    sldIdLst.append(thanks)


def update_thanks_page_number(prs):
    thanks = prs.slides[-1]
    for shape in thanks.shapes:
        if getattr(shape, "has_text_frame", False) and shape.text.strip() == "18":
            shape.text = "21"
            for paragraph in shape.text_frame.paragraphs:
                for run in paragraph.runs:
                    run.font.name = "Pretendard"
            break


def update_cover_date(prs):
    cover = prs.slides[0]
    meta = cover.shapes[1]
    meta.text = meta.text.replace("03월 30일", "04월 06일")


def add_incremental_slides(prs):
    layout = prs.slide_layouts[6]

    slide = prs.slides.add_slide(layout)
    add_top_title(slide, "W4 추가 진행사항", 18)
    add_bullets(
        slide,
        0.82,
        1.32,
        6.9,
        4.7,
        [
            "docs 저장소를 기준으로 로드맵, 리스크, 오픈 질문이 현재 상태에 맞게 정리되었습니다.",
            "CodexKit이 워크스페이스 부트스트랩, docs seed, 브랜치 규약을 묶는 운영 패키지로 정리되었습니다.",
            "발표 자료도 일회성 산출물이 아니라 Git으로 관리되는 주간 자산으로 전환하기 시작했습니다.",
        ],
        font_size=17,
    )
    add_card(slide, 8.02, 1.42, 4.0, 0.98, "문서", "source of truth 정착", SKY)
    add_card(slide, 8.02, 2.72, 4.0, 0.98, "운영", "CodexKit 기반 작업 흐름 정리", GRAY)
    add_card(slide, 8.02, 4.02, 4.0, 0.98, "발표", "PPTX + manifest + notes 관리 시작", SKY)
    add_card(slide, 8.02, 5.32, 4.0, 0.74, "의미", "제안서에서 진행 보고 체계로 전환", GRAY)

    slide = prs.slides.add_slide(layout)
    add_top_title(slide, "W4 저장소별 구현 현황", 19)
    add_card(slide, 0.82, 1.35, 2.25, 2.02, "Front", "로그인 / 프로필 / 강의 화면 구조 재정리", SKY)
    add_card(slide, 3.18, 1.35, 2.25, 2.02, "Backend", "eligibility 및 attendance read-model spine 확보", GRAY)
    add_card(slide, 5.54, 1.35, 2.25, 2.02, "PresenceService", "OpenWrt형 더미 수집 서비스 제공", SKY)
    add_card(slide, 7.90, 1.35, 2.25, 2.02, "DB", "CSV 기반 attendance slice 데모 데이터 시드", GRAY)
    add_card(slide, 10.26, 1.35, 2.25, 2.02, "docs", "요구사항 / 상태 / 슬라이드 운영 설계 갱신", SKY)
    add_card(slide, 2.0, 4.05, 4.15, 1.48, "현재 단계", "Phase 1: 로그인, 단말 관리, eligibility, Docker 기본 동작 확보\nPhase 2: 강의 목록 / 공지 / 관리자 조회 뼈대 진행", GRAY)
    add_card(slide, 6.6, 4.05, 4.6, 1.48, "다음 연결 포인트", "Front-Backend-PresenceService-DB 사이를 실제 출석 흐름으로 연결하고 검증하는 단계로 이동", SKY)
    note_box = slide.shapes.add_textbox(Inches(0.9), Inches(6.0), Inches(11.7), Inches(0.42))
    set_text_frame(note_box.text_frame, "핵심은 기능 수 증가보다 서비스 경계와 실행 가능한 첫 slice를 확보한 것입니다.", font_size=16, color=TEXT)

    slide = prs.slides.add_slide(layout)
    add_top_title(slide, "W4 리스크와 다음 액션", 20)
    add_card(
        slide,
        0.82,
        1.38,
        5.7,
        4.75,
        "현재 리스크",
        "• OpenWrt / 게이트웨이 환경에서 필요한 단말 정보를 안정적으로 수집할 수 있는지 검증 필요\n"
        "• 랜덤 MAC 활성화 시 등록 단말 매칭 실패 가능\n"
        "• Redis snapshot 캐시 만료 구간에 수집 부하 집중 가능\n"
        "• 시험 접근 제어 범위를 성급히 넓히면 운영 복잡도 급증",
        GRAY,
    )
    add_card(
        slide,
        6.72,
        1.38,
        5.8,
        4.75,
        "다음 액션",
        "• Front / Backend / PresenceService / DB의 첫 slice를 실제 흐름으로 연결\n"
        "• 단말 등록과 eligibility 경로를 우선 검증\n"
        "• OpenWrt 수집 가능 정보와 랜덤 MAC 영향을 실제 환경에서 확인\n"
        "• 주간 발표는 최신 published deck 기준으로 증분 편집 유지",
        SKY,
    )
    note_box = slide.shapes.add_textbox(Inches(0.9), Inches(6.08), Inches(11.5), Inches(0.36))
    set_text_frame(note_box.text_frame, "이번 W4에서는 기존 발표를 유지한 채, 현재 저장소 변경사항만 뒤에 덧붙이는 방식으로 업데이트합니다.", font_size=15, color=TEXT)


def main():
    prs = Presentation(BASE)
    update_cover_date(prs)
    add_incremental_slides(prs)
    clone_thanks_to_end(prs)
    update_thanks_page_number(prs)
    prs.save(OUT)
    print(f"saved {OUT}")


if __name__ == "__main__":
    main()
