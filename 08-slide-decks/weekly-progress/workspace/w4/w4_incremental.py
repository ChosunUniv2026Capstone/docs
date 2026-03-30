import subprocess
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt


WORKSPACE = Path("/Users/kimhyeonseok/CodeStorage/smart-class")
ROOT = WORKSPACE / "docs" / "08-slide-decks" / "weekly-progress"
BASE = ROOT / "published" / "w3.pptx"
OUT = ROOT / "published" / "w4.pptx"
EMPTY_TREE = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"

NAVY = RGBColor(0x1E, 0x3A, 0x5F)
SKY = RGBColor(0xEA, 0xF2, 0xFB)
GRAY = RGBColor(0xEE, 0xF2, 0xF7)
LINE = RGBColor(0xC6, 0xD3, 0xE3)
TEXT = RGBColor(0x1B, 0x2A, 0x38)
MUTED = RGBColor(0x64, 0x74, 0x8B)

REPOS = ["docs", "CodexKit", "Front", "Backend", "PresenceService", "DB"]


def git(repo, *args):
    return subprocess.check_output(
        ["git", "-C", str(WORKSPACE / repo), *args],
        text=True,
    ).strip()


def resolve_base(repo):
    tags = [t for t in git(repo, "tag", "--merged", "HEAD", "--sort=creatordate").splitlines() if t]
    result = subprocess.run(
        ["git", "-C", str(WORKSPACE / repo), "describe", "--tags", "--exact-match", "HEAD"],
        text=True,
        capture_output=True,
    )
    head_tag = result.stdout.strip() if result.returncode == 0 else ""

    if not tags:
        return {"mode": "empty", "ref": EMPTY_TREE, "label": "empty repo"}
    if head_tag and len(tags) >= 2 and tags[-1] == head_tag:
        return {"mode": "tag", "ref": tags[-2], "label": f"tag:{tags[-2]}"}
    return {"mode": "tag", "ref": tags[-1], "label": f"tag:{tags[-1]}"}


def diff_files(repo, base):
    if base["mode"] == "empty":
        out = git(repo, "diff", "--name-only", EMPTY_TREE, "HEAD")
    else:
        out = git(repo, "diff", "--name-only", f"{base['ref']}..HEAD")
    return [line for line in out.splitlines() if line]


def diff_shortstat(repo, base):
    if base["mode"] == "empty":
        return git(repo, "diff", "--shortstat", EMPTY_TREE, "HEAD")
    return git(repo, "diff", "--shortstat", f"{base['ref']}..HEAD")


def commit_subjects(repo, base):
    if base["mode"] == "empty":
        out = git(repo, "log", "--format=%s", "--reverse")
    else:
        out = git(repo, "log", "--format=%s", "--reverse", f"{base['ref']}..HEAD")
    return [line for line in out.splitlines() if line]


def commit_bodies(repo, base):
    if base["mode"] == "empty":
        out = git(repo, "log", "--format=%s%n%b<<END>>", "--reverse")
    else:
        out = git(repo, "log", "--format=%s%n%b<<END>>", "--reverse", f"{base['ref']}..HEAD")
    return [chunk.strip() for chunk in out.split("<<END>>") if chunk.strip()]


def repo_info(repo):
    base = resolve_base(repo)
    return {
        "repo": repo,
        "base": base,
        "files": diff_files(repo, base),
        "shortstat": diff_shortstat(repo, base),
        "subjects": commit_subjects(repo, base),
        "commits": commit_bodies(repo, base),
    }


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
        p.line_spacing = 1.08


def add_top_title(slide, title):
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

    title_box = slide.shapes.add_textbox(Inches(0.38), Inches(0.58), Inches(6.2), Inches(0.4))
    set_text_frame(title_box.text_frame, title, font_size=20, bold=True, color=TEXT)


def add_card(slide, x, y, w, h, title, body, fill_rgb=SKY):
    box = slide.shapes.add_shape(
        MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h)
    )
    box.fill.solid()
    box.fill.fore_color.rgb = fill_rgb
    box.line.color.rgb = LINE
    box.line.width = Pt(1)

    title_box = slide.shapes.add_textbox(Inches(x + 0.14), Inches(y + 0.12), Inches(w - 0.28), Inches(0.22))
    set_text_frame(title_box.text_frame, title, font_size=12.8, bold=True, color=NAVY)

    body_box = slide.shapes.add_textbox(Inches(x + 0.14), Inches(y + 0.4), Inches(w - 0.28), Inches(h - 0.5))
    set_text_frame(body_box.text_frame, body, font_size=10.8, color=TEXT)
    body_box.text_frame.vertical_anchor = MSO_ANCHOR.TOP


def add_bullet_card(slide, x, y, w, h, title, items, fill_rgb=GRAY):
    add_card(slide, x, y, w, h, title, "", fill_rgb=fill_rgb)
    body_box = slide.shapes.add_textbox(Inches(x + 0.14), Inches(y + 0.4), Inches(w - 0.28), Inches(h - 0.5))
    tf = body_box.text_frame
    tf.clear()
    for idx, item in enumerate(items):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.text = item
        p.level = 0
        p.bullet = True
        p.font.name = "Pretendard"
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT
        p.space_after = Pt(4)
        p.line_spacing = 1.04


def add_slide_at(prs, index):
    layout = prs.slide_layouts[6]
    prs.slides.add_slide(layout)
    sld_id_lst = prs.slides._sldIdLst
    new_id = sld_id_lst[-1]
    sld_id_lst.remove(new_id)
    sld_id_lst.insert(index, new_id)
    return prs.slides[index]


def move_thanks_to_end(prs):
    thanks_idx = None
    for idx, slide in enumerate(prs.slides):
        texts = [sh.text.strip() for sh in slide.shapes if getattr(sh, "has_text_frame", False) and sh.text.strip()]
        if "감사합니다." in texts:
            thanks_idx = idx
            break
    if thanks_idx is None:
        return
    sld_id_lst = prs.slides._sldIdLst
    thanks = sld_id_lst[thanks_idx]
    sld_id_lst.remove(thanks)
    sld_id_lst.append(thanks)


def renumber_pages(prs):
    for slide_index, slide in enumerate(prs.slides, start=1):
        for shape in slide.shapes:
            if not getattr(shape, "has_text_frame", False):
                continue
            txt = shape.text.strip()
            if txt.isdigit() and shape.left > 15000000 and shape.top > 9000000:
                shape.text = str(slide_index)
                for paragraph in shape.text_frame.paragraphs:
                    paragraph.alignment = PP_ALIGN.RIGHT
                    for run in paragraph.runs:
                        run.font.name = "Pretendard"
                        run.font.size = Pt(9)
                        run.font.color.rgb = MUTED


def update_cover_date(prs):
    cover = prs.slides[0]
    meta = cover.shapes[1]
    meta.text = meta.text.replace("03월 30일", "04월 06일")


def pick_commit(info, keyword):
    for subject in reversed(info["subjects"]):
        if keyword.lower() in subject.lower():
            return subject
    return info["subjects"][-1] if info["subjects"] else "(commit 없음)"


def feature_data(infos):
    docs = infos["docs"]
    kit = infos["CodexKit"]
    front = infos["Front"]
    backend = infos["Backend"]
    presence = infos["PresenceService"]
    db = infos["DB"]

    return {
        "ops": {
            "title": "운영 기반 기능",
            "commits": [
                pick_commit(docs, "source of truth"),
                pick_commit(kit, "bootstrap"),
                pick_commit(kit, "branch"),
            ],
            "features": [
                "docs 저장소를 source of truth로 고정하고 요구사항·아키텍처·상태 문서 체계를 정리",
                "CodexKit으로 workspace bootstrap, docs seed, 로컬 runtime 템플릿 제공",
                "브랜치 규약과 repo template이 split-repo 구조에 맞게 통일",
            ],
            "files": [
                "docs/07-status/*",
                "CodexKit/install/bootstrap_workspace.sh",
                "CodexKit/workspace-seed/docs/*",
            ],
            "base": f"{docs['base']['label']} / {kit['base']['label']}",
        },
        "lms": {
            "title": "LMS 기본 기능",
            "commits": [
                pick_commit(front, "login"),
                pick_commit(backend, "attendance"),
            ],
            "features": [
                "역할 기반 로그인, 프로필 단말 관리, 대시보드 강의 카드, 강의 상세 화면 구성",
                "학생·교수 강의 조회, 공지 API, 관리자 조회 API, 출석 eligibility read endpoint 구현",
                "프론트와 백엔드가 같은 LMS 기본 정보 구조를 공유하도록 첫 vertical slice 확보",
            ],
            "files": [
                "Front/src/App.tsx",
                "Front/src/api.ts",
                "Backend/app/main.py",
                "Backend/app/services.py",
            ],
            "base": f"{front['base']['label']} / {backend['base']['label']}",
        },
        "presence": {
            "title": "재실성 출석 기능",
            "commits": [
                pick_commit(presence, "OpenWrt"),
                pick_commit(db, "attendance slice"),
                pick_commit(backend, "attendance"),
            ],
            "features": [
                "OpenWrt 형태를 닮은 dummy snapshot 수집과 Redis-backed 캐시 서비스 구현",
                "백엔드에서 PresenceService eligibility 결과를 사용하도록 서비스 경계 유지",
                "사용자·강의·강의실·AP·등록 단말 데이터를 seed로 넣어 출석 판정 검증 기반 확보",
            ],
            "files": [
                "PresenceService/app/service.py",
                "PresenceService/app/dummy_openwrt.py",
                "DB/postgres/init/001_schema.sql",
                "DB/postgres/seed/registered_devices.csv",
            ],
            "base": f"{presence['base']['label']} / {db['base']['label']}",
        },
        "qa": {
            "title": "개발·검증 지원 기능",
            "commits": [
                pick_commit(kit, "runtime"),
                pick_commit(docs, "runtime"),
                pick_commit(db, "attendance slice"),
            ],
            "features": [
                "로컬 runtime topology와 Docker 기반 개발 경로를 문서/seed에 반영",
                "DB seed, Presence dummy data, Backend/Frontend 실행 흐름을 한 워크스페이스에서 검증 가능",
                "주간 발표 자료도 이후에는 이전 tag부터 현재까지의 diff와 commit 메시지를 기준으로 생성 가능",
            ],
            "files": [
                "docs/04-architecture/local-runtime-topology.md",
                "CodexKit/docker-compose.yml",
                "DB/postgres/seed/*",
            ],
            "base": f"{docs['base']['label']} / {kit['base']['label']} / {db['base']['label']}",
        },
    }


def feature_slide(slide, title, feature, stat_left, stat_right):
    add_top_title(slide, title)
    add_bullet_card(slide, 0.82, 1.36, 5.5, 4.95, "구현된 기능", feature["features"], fill_rgb=GRAY)
    add_bullet_card(slide, 6.58, 1.36, 5.85, 2.3, "근거 commit", feature["commits"], fill_rgb=SKY)
    add_card(slide, 6.58, 3.92, 5.85, 1.12, "기준 범위", feature["base"], fill_rgb=GRAY)
    add_card(slide, 6.58, 5.3, 2.8, 1.02, "관련 파일", "\n".join(feature["files"][:2]), fill_rgb=SKY)
    add_card(slide, 9.63, 5.3, 2.8, 1.02, "관련 파일", "\n".join(feature["files"][2:]), fill_rgb=SKY)
    add_card(slide, 0.82, 6.48, 5.65, 0.52, "Diff 요약", stat_left, fill_rgb=SKY)
    add_card(slide, 6.58, 6.48, 5.85, 0.52, "Diff 요약", stat_right, fill_rgb=SKY)


def main():
    infos = {repo: repo_info(repo) for repo in REPOS}
    features = feature_data(infos)

    prs = Presentation(BASE)
    update_cover_date(prs)

    slide = add_slide_at(prs, 4)
    feature_slide(
        slide,
        "팀 소개 및 진행사항 - 운영 기반 기능",
        features["ops"],
        infos["docs"]["shortstat"] or "docs diff 없음",
        infos["CodexKit"]["shortstat"] or "CodexKit diff 없음",
    )

    slide = add_slide_at(prs, 12)
    feature_slide(
        slide,
        "구현 기능 - LMS 기본 기능",
        features["lms"],
        infos["Front"]["shortstat"] or "Front diff 없음",
        infos["Backend"]["shortstat"] or "Backend diff 없음",
    )

    slide = add_slide_at(prs, 15)
    feature_slide(
        slide,
        "구현 기능 - 재실성 출석 기능",
        features["presence"],
        infos["PresenceService"]["shortstat"] or "PresenceService diff 없음",
        infos["DB"]["shortstat"] or "DB diff 없음",
    )

    slide = add_slide_at(prs, 19)
    feature_slide(
        slide,
        "개발 계획 보강 - 개발·검증 지원 기능",
        features["qa"],
        infos["docs"]["shortstat"] or "docs diff 없음",
        infos["CodexKit"]["shortstat"] or "CodexKit diff 없음",
    )

    move_thanks_to_end(prs)
    renumber_pages(prs)
    prs.save(OUT)
    print(f"saved {OUT}")


if __name__ == "__main__":
    main()
