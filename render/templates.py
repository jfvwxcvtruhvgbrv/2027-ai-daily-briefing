"""일간지형 보고서·메일 HTML 템플릿.

메일 호환을 위해 레이아웃은 표(table)와 인라인 스타일만 쓴다.
같은 컴포넌트를 보고서(Pages)와 메일에서 함께 쓴다.
"""
from html import escape as e

GRADE = {
    "primary": ("✅", "1차 출처"),
    "multi": ("☑️", "복수 매체"),
    "single": ("⚠️", "단일 출처"),
}
INK, PAPER, RED, NAVY, MUTED, RULE = "#1a1a1a", "#fffdf8", "#9b1c1c", "#1f3a5f", "#666666", "#d6d1c4"
SERIF = "Georgia,'Nanum Myeongjo','Batang',serif"
SANS = "'Apple SD Gothic Neo','Malgun Gothic','Noto Sans KR',sans-serif"
DISCLAIMER = "본 보고서는 Claude가 자동으로 취재·작성한 요약으로 원문 확인을 권장하며, 투자 판단의 근거가 아닙니다."


def grade_tag(g):
    icon, label = GRADE[g]
    return f"{icon} {label}"


def sources_line(sources, size=11.5):
    links = " · ".join(
        f'<a href="{e(s["url"])}" style="color:{NAVY};">{e(s["name"])}{" (" + e(s["date"]) + ")" if s.get("date") else ""}</a>'
        for s in sources)
    return f'<div style="font-size:{size}px;color:{MUTED};line-height:1.7;margin-top:6px;">근거: {links}</div>'


def image_block(a, width=648):
    if not a.get("image_url"):
        return ""
    cap = e(a.get("image_caption") or "대표 이미지")
    credit = e(a.get("image_credit", ""))
    return (f'<img src="{e(a["image_url"])}" alt="{cap}" width="{width}" '
            f'style="width:100%;max-width:{width}px;height:auto;display:block;border:1px solid {RULE};">'
            f'<div style="font-size:11px;color:#777;margin:4px 0 10px;">이미지: {cap} (출처 {credit})</div>')


def chart_block(c):
    if not c:
        return ""
    mx = max(b["value"] for b in c["bars"]) or 1
    rows = []
    for b in c["bars"]:
        pct = max(2, round(b["value"] / mx * 100))
        color = NAVY if b.get("highlight") else "#9aa6b2"
        val = f'{b["value"]:,}'.rstrip("0").rstrip(".") if isinstance(b["value"], float) else f'{b["value"]:,}'
        rows.append(
            f'<tr><td width="96" style="padding:5px 6px 5px 0;font-size:12px;color:#555;">{e(b["label"])}</td>'
            f'<td><table role="presentation" cellpadding="0" cellspacing="0" width="{pct}%"><tr>'
            f'<td bgcolor="{color}" style="background:{color};height:16px;font-size:0;line-height:0;">&nbsp;</td>'
            f'</tr></table></td><td width="56" align="right" style="font-size:12px;font-weight:700;">{val}</td></tr>')
    return (f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" bgcolor="#f7f5ef" '
            f'style="background:#f7f5ef;border:1px solid #e2ddd0;margin:6px 0 12px;">'
            f'<tr><td style="padding:10px 14px 2px;font-size:13px;font-weight:700;">{e(c["title"])} '
            f'<span style="font-weight:400;color:#777;">(단위: {e(c["unit"])})</span></td></tr>'
            f'<tr><td style="padding:4px 14px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0">'
            f'{"".join(rows)}</table></td></tr>'
            f'<tr><td style="padding:2px 14px 10px;font-size:11px;color:#777;">자료: {e(c["source"])}</td></tr></table>')


def why_block(text):
    return (f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin:10px 0 4px;"><tr>'
            f'<td width="3" bgcolor="#b45309" style="background:#b45309;font-size:0;">&nbsp;</td>'
            f'<td bgcolor="#fbf3e4" style="background:#fbf3e4;padding:8px 12px;font-size:13.5px;line-height:1.7;">'
            f'<b>💡 왜 중요한가</b> — {e(text)}</td></tr></table>')


def section_title(name):
    return (f'<div style="border-top:2px solid {INK};padding-top:8px;margin-top:22px;font-size:13px;'
            f'font-weight:700;color:{RED};letter-spacing:.1em;">{e(name)}</div>')


def paragraphs(paras):
    return "".join(f'<p style="margin:0 0 10px;">{e(p)}</p>' for p in paras or [])


def article_full(a, kicker=None, size=21):
    k = kicker or a["category"]
    return (f'<div style="padding:14px 0 12px;border-bottom:1px solid {RULE};">'
            f'<div style="font-size:12px;color:{RED};font-weight:700;">{e(k)} · {grade_tag(a["grade"])}</div>'
            f'<div style="font-family:{SERIF};font-size:{size}px;font-weight:700;line-height:1.35;margin:5px 0 8px;">{e(a["headline"])}</div>'
            f'{image_block(a)}'
            f'<div style="font-size:15px;line-height:1.75;color:#333;font-weight:600;margin-bottom:10px;">{e(a["lead"])}</div>'
            f'{chart_block(a.get("chart"))}'
            f'<div style="font-size:14.5px;line-height:1.85;">{paragraphs(a.get("body"))}</div>'
            f'{why_block(a["why"])}{sources_line(a["sources"])}</div>')


def sketchlab_item(s):
    parts = [("무엇인가", s.get("what")), ("핵심 수치", s.get("numbers")), ("경쟁 구도", s.get("competition")),
             ("반응", s.get("reaction")), ("써볼 수 있나", s.get("availability"))]
    body = "".join(f'<p style="margin:0 0 8px;"><b>{t}.</b> {e(v)}</p>' for t, v in parts if v)
    body += paragraphs(s.get("body"))
    return (f'<div style="padding:14px 0 12px;border-bottom:1px solid {RULE};">'
            f'<div style="font-size:12px;color:{NAVY};font-weight:700;">#{s["no"]} · {e(s["tags"])} · {grade_tag(s["grade"])}</div>'
            f'<div style="font-family:{SERIF};font-size:21px;font-weight:700;line-height:1.35;margin:5px 0 8px;">{e(s["headline"])}</div>'
            f'{image_block(s)}'
            f'<div style="font-size:15px;line-height:1.75;color:#333;font-weight:600;margin-bottom:10px;">{e(s["lead"])}</div>'
            f'{chart_block(s.get("chart"))}'
            f'<div style="font-size:14.5px;line-height:1.85;">{body}</div>'
            f'{why_block(s["why"])}{sources_line(s["sources"])}</div>')


def masthead(issue, label="GLOBAL AI DAILY"):
    return (f'<tr><td style="padding:20px 26px 10px;border-bottom:3px double {INK};text-align:center;">'
            f'<div style="font-size:11px;letter-spacing:.3em;color:{MUTED};">{e(label)}</div>'
            f'<div style="font-family:{SERIF};font-size:38px;font-weight:700;letter-spacing:-1px;margin:4px 0 2px;">AI 데일리</div>'
            f'<table role="presentation" width="100%" style="font-size:12px;color:#444;margin-top:6px;"><tr>'
            f'<td align="left">{e(issue["date"])} ({e(issue["weekday"])})</td>'
            f'<td align="right">대상 기간: {e(issue["period"])}</td></tr></table></td></tr>'
            f'<tr><td bgcolor="#f4f1e8" style="padding:8px 26px;background:#f4f1e8;font-size:12px;color:#444;border-bottom:1px solid {RULE};">'
            f'<b>검증 등급</b> &nbsp; ✅ 1차 출처(공식 발표·공시·문서) · ☑️ 복수 매체 교차 확인 · ⚠️ 단일 출처·협상 중 보도</td></tr>')


def key_points(issue):
    lis = "".join(f"<li>{e(p)}</li>" for p in issue["key_points"])
    return (f'<tr><td style="padding:16px 26px 6px;"><div style="font-size:13px;font-weight:700;color:{RED};letter-spacing:.1em;">오늘의 핵심</div>'
            f'<ol style="margin:6px 0 0;padding-left:20px;font-size:14.5px;line-height:1.8;">{lis}</ol></td></tr>')


def shell(title, inner, body_bg="#ece9e2"):
    return (f'<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width, initial-scale=1"><title>{e(title)}</title></head>'
            f'<body style="margin:0;padding:0;background:{body_bg};font-family:{SANS};color:{INK};">'
            f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" bgcolor="{body_bg}" style="background:{body_bg};">'
            f'<tr><td align="center" style="padding:18px 10px;">'
            f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" bgcolor="{PAPER}" '
            f'style="max-width:700px;background:{PAPER};border:1px solid {RULE};">{inner}</table>'
            f'</td></tr></table></body></html>')


def report_page(issue, site_url):
    rows = [masthead(issue), key_points(issue)]
    body = [section_title("1면 톱"), article_full(issue["top_story"], kicker=f'1면 톱 · {issue["top_story"]["category"]}', size=27)]
    if issue["sketchlab"]:
        body.append(f'<div bgcolor="{NAVY}" style="background:{NAVY};color:#fff;padding:8px 12px;font-size:14px;font-weight:700;margin-top:22px;">'
                    f'SketchLab 심층 리포트 <span style="font-weight:400;font-size:12px;">KAIST SketchLab Daily AI 새 항목을 출발점으로 원문 추적</span></div>')
        body += [sketchlab_item(s) for s in issue["sketchlab"]]
    for sec in issue["sections"]:
        if sec.get("articles"):
            body.append(section_title(sec["name"]))
            body += [article_full(a) for a in sec["articles"]]
    if issue["korea"]:
        body.append(section_title("한국 AI"))
        body += [article_full(a) for a in issue["korea"]]
    if issue["briefs"]:
        lis = "".join(
            f'<li>{e(b["text"])} {GRADE[b["grade"]][0]} '
            + " ".join(f'<a href="{e(s["url"])}" style="color:{NAVY};font-size:11px;">{e(s["name"])}</a>' for s in b["sources"])
            + "</li>" for b in issue["briefs"])
        body.append(section_title("단신") + f'<ul style="margin:8px 0 0;padding-left:18px;font-size:13.5px;line-height:1.85;">{lis}</ul>')
    social = issue["social"]
    lis = "".join(
        f'<li><b>{e(s["who"])}</b> — {e(s["text"])}{" (" + e(s["date"]) + ")" if s.get("date") else ""} '
        f'{GRADE.get(s.get("grade", "single"), GRADE["single"])[0]} <a href="{e(s["url"])}" style="color:{NAVY};font-size:11px;">원문</a></li>'
        for s in social) or f'<li style="color:#777;">이번 기간에 출처를 확인할 수 있는 화제 포스트가 없어 싣지 않음</li>'
    body.append(section_title("X · LinkedIn에서") + f'<ul style="margin:8px 0 0;padding-left:18px;font-size:13.5px;line-height:1.85;">{lis}</ul>')
    ed = issue["editorial"]
    body.append(f'<div style="border:1px solid {INK};padding:14px 16px;background:#f7f5ef;margin-top:22px;">'
                f'<div style="font-size:12px;font-weight:700;color:{RED};letter-spacing:.1em;">해설 · 오늘의 흐름</div>'
                f'<div style="font-family:{SERIF};font-size:18px;font-weight:700;margin:5px 0 8px;">{e(ed["title"])}</div>'
                f'<div style="font-size:14px;line-height:1.85;">{e(ed["body"])}</div></div>')
    if issue["calendar"]:
        trs = "".join(
            f'<tr><td width="84" style="padding:6px 0;color:{RED};font-weight:700;vertical-align:top;">{e(c["when"])}</td>'
            f'<td style="padding:6px 0;">{e(c["what"])}{" " + GRADE[c["grade"]][0] if c.get("grade") in GRADE else ""}</td></tr>'
            for c in issue["calendar"])
        body.append(section_title("주목할 일정") + f'<table role="presentation" width="100%" style="font-size:13.5px;line-height:1.6;margin-top:6px;">{trs}</table>')
    notes = "".join(f"<br>· {e(n)}" for n in issue.get("notes") or [])
    body.append(f'<div style="border-top:3px double {INK};padding-top:10px;margin-top:24px;font-size:11.5px;color:{MUTED};line-height:1.75;">'
                f'<b>이번 호 취재 범위</b> — {e(issue["coverage"])}<br>'
                f'<b>SketchLab 마지막 처리 번호: #{issue["sketchlab_last"]}</b>{notes}<br>'
                f'이미지는 기업 공식 페이지의 대표 이미지만 원본 주소로 싣고 출처를 표기합니다. 차트는 공개 수치로 직접 작성했습니다.<br>'
                f'{DISCLAIMER}<br><a href="{e(site_url)}" style="color:{NAVY};">지난 호 모아보기</a></div>')
    rows.append(f'<tr><td style="padding:0 26px 22px;">{"".join(body)}</td></tr>')
    return shell(f'AI 데일리 — {issue["date"]} ({issue["weekday"]})', "".join(rows))


def index_page(issues, site_url):
    items = "".join(
        f'<tr><td style="padding:10px 0;border-bottom:1px solid {RULE};">'
        f'<a href="{e(i["date"])}.html" style="color:{INK};text-decoration:none;">'
        f'<div style="font-size:12px;color:{RED};font-weight:700;">{e(i["date"])} ({e(i["weekday"])})</div>'
        f'<div style="font-family:{SERIF};font-size:18px;font-weight:700;margin-top:3px;">{e(i["top_story"]["headline"])}</div>'
        f'<div style="font-size:13px;color:#555;margin-top:3px;">{e(i["tagline"])}</div></a></td></tr>'
        for i in issues)
    inner = (f'<tr><td style="padding:20px 26px 10px;border-bottom:3px double {INK};text-align:center;">'
             f'<div style="font-size:11px;letter-spacing:.3em;color:{MUTED};">GLOBAL AI DAILY</div>'
             f'<div style="font-family:{SERIF};font-size:38px;font-weight:700;">AI 데일리</div>'
             f'<div style="font-size:13px;color:#444;">지난 호 모아보기 · 총 {len(issues)}호</div></td></tr>'
             f'<tr><td style="padding:6px 26px 22px;"><table role="presentation" width="100%">{items}</table>'
             f'<div style="font-size:11.5px;color:{MUTED};margin-top:14px;">{DISCLAIMER}</div></td></tr>')
    return shell("AI 데일리 — 지난 호", inner)


def email_html(issue, report_url):
    """메일 본문: 핵심 3줄 + 1면 톱(사진·차트) + 섹션별 헤드라인 + 보고서 링크."""
    t = issue["top_story"]
    heads = []
    groups = []
    if issue["sketchlab"]:
        groups.append(("SketchLab 심층", issue["sketchlab"]))
    groups += [(s["name"], s["articles"]) for s in issue["sections"] if s.get("articles")]
    if issue["korea"]:
        groups.append(("한국 AI", issue["korea"]))
    for name, arts in groups:
        lis = "".join(
            f'<li style="margin-bottom:6px;"><b>{e(a["headline"])}</b> {GRADE[a["grade"]][0]}<br>'
            f'<span style="color:#555;">{e(a["lead"])}</span></li>' for a in arts)
        heads.append(f'<div style="font-size:12.5px;font-weight:700;color:{RED};margin-top:16px;">{e(name)}</div>'
                     f'<ul style="margin:6px 0 0;padding-left:18px;font-size:13.5px;line-height:1.65;">{lis}</ul>')
    button = (f'<table role="presentation" cellpadding="0" cellspacing="0" style="margin:20px auto 6px;"><tr>'
              f'<td bgcolor="{NAVY}" style="background:{NAVY};border-radius:4px;">'
              f'<a href="{e(report_url)}" style="display:inline-block;padding:12px 26px;color:#ffffff;font-size:15px;'
              f'font-weight:700;text-decoration:none;">전체 보고서 읽기 (사진·차트·심층 리포트) →</a></td></tr></table>')
    top = (f'<div style="font-size:12px;color:{RED};font-weight:700;">1면 톱 · {e(t["category"])} · {grade_tag(t["grade"])}</div>'
           f'<div style="font-family:{SERIF};font-size:24px;font-weight:700;line-height:1.3;margin:5px 0 8px;">{e(t["headline"])}</div>'
           f'{image_block(t)}<div style="font-size:14.5px;line-height:1.75;">{e(t["lead"])}</div>'
           f'{chart_block(t.get("chart"))}{why_block(t["why"])}{sources_line(t["sources"])}')
    inner = (masthead(issue) + key_points(issue)
             + f'<tr><td style="padding:10px 26px 4px;"><div style="border-top:2px solid {INK};padding-top:12px;">{top}</div></td></tr>'
             + f'<tr><td style="padding:4px 26px 0;">{button}{"".join(heads)}{button}</td></tr>'
             + f'<tr><td style="padding:14px 26px 22px;font-size:11.5px;color:{MUTED};line-height:1.7;">{DISCLAIMER}</td></tr>')
    return shell(f'[AI 브리핑] {issue["date"]}', inner)


def email_text(issue, report_url):
    lines = [f'[AI 브리핑] {issue["date"]} ({issue["weekday"]}) — {issue["tagline"]}', "", "오늘의 핵심"]
    lines += [f"{i}. {p}" for i, p in enumerate(issue["key_points"], 1)]
    lines += ["", f'1면 톱: {issue["top_story"]["headline"]}', issue["top_story"]["lead"], "",
              f"전체 보고서: {report_url}", "", DISCLAIMER]
    return "\n".join(lines)
