"""AI 데일리 보고서 HTML 템플릿.

톤앤매너는 기존 Global News Intelligence(2026-news-agent/generate_site.py)와 맞춘다:
회청색 바탕·카드, 고딕 단일 서체(Pretendard), 굵은 헤드라인, 5단 보드, 사례 카드(case),
빨간 소제목 필드, 색 점·게이지, 아카이브 목록(log-row).
"""
import datetime as dt
from html import escape as _e

WD = ["월", "화", "수", "목", "금", "토", "일"]

# 검증 등급 → 라벨 / 색 / 게이지 단계 (GNI 추세 게이지와 같은 방식)
GRADE_LABEL = {"primary": "1차 출처 확인", "multi": "복수 매체 교차", "single": "단일 출처"}
GRADE_ICON = {"primary": "✅", "multi": "☑️", "single": "⚠️"}
GRADE_COLOR = {"primary": "#3F7A5D", "multi": "#2C5C87", "single": "#B43B2E"}
GRADE_STEPS = {"primary": 4, "multi": 3, "single": 1}

# 오늘의 AI 보드 컬럼 (GNI '오늘의 세계' 보드와 같은 구조)
BOARD_COLORS = {
    "핵심": "#12151C", "key": "#A6790F", "korea": "#2C5C87", "social": "#5A6270", "calendar": "#B43B2E",
}
DISCLAIMER = "AI 데일리 · Claude 자동 취재·분석 브리핑 · 판단 전 원문 확인 요망 · 투자 판단의 근거가 아님"


def e(s):
    return _e(str(s if s is not None else ""))


def pretty_date(d):
    try:
        x = dt.date.fromisoformat(d)
        return f"{x.year}년 {x.month}월 {x.day}일 {WD[x.weekday()]}요일"
    except Exception:
        return d


def compact_date(d):
    try:
        x = dt.date.fromisoformat(d)
        return f"{x.month}.{x.day} ({WD[x.weekday()]})"
    except Exception:
        return d


CSS = """
:root{
  --paper:#E7EBEE; --card:#F6F8F9;
  --ink:#12151C; --ink-soft:#4B515C; --rule:#C6CCD3; --red:#B43B2E;
}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--paper);color:var(--ink);
  font-family:"Pretendard",-apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo","Malgun Gothic",sans-serif;
  font-size:19px;line-height:1.65;word-break:keep-all;-webkit-font-smoothing:antialiased}
a{color:inherit}
.wrap{padding:0 5vw}
.back{display:inline-block;margin:26px 0 6px;font-size:16px;color:var(--ink-soft);
  text-decoration:none;border-bottom:1px solid var(--rule)}
.back:hover{border-color:var(--ink);color:var(--ink)}
.headline{font-weight:800;font-size:clamp(32px,5vw,52px);letter-spacing:-.01em;margin:10px 0 6px;line-height:1.25}
.metarow{display:flex;gap:20px;flex-wrap:wrap;margin:14px 0 30px;font-size:16px;color:var(--ink-soft)}
.metarow .m{display:flex;align-items:center;gap:7px}
.dot{width:9px;height:9px;border-radius:50%;flex:none;display:inline-block}

.board{margin:0 0 40px}
.board-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:1px;background:var(--rule);border:1px solid var(--rule)}
.board-col{background:var(--card);padding:18px 18px 20px}
.board-col h3{font-size:14px;letter-spacing:.06em;color:var(--ink-soft);margin-bottom:12px;
  display:flex;align-items:center;gap:7px;font-weight:700}
.board-col ul{list-style:none}
.board-col li{display:flex;gap:8px;padding:8px 0;border-top:1px solid var(--rule);font-size:15.5px;line-height:1.5}
.board-col li:first-child{border-top:none}
.board-col li i{width:6px;height:6px;border-radius:50%;flex:none;margin-top:7px}
.board-col li small{display:block;color:var(--ink-soft);font-size:13px}
.board-col .empty{color:var(--ink-soft);font-size:14px}
@media (max-width:1100px){.board-grid{grid-template-columns:repeat(2,1fr)}}
@media (max-width:600px){.board-grid{grid-template-columns:1fr}}

.section-title{font-weight:800;font-size:23px;margin:36px 0 14px;display:flex;align-items:baseline;gap:12px}
.section-title small{font-size:15px;font-weight:500;color:var(--ink-soft)}

.case{background:var(--card);border:1px solid var(--rule);margin-bottom:24px}
.case.top{border-top:4px solid var(--ink)}
.case-head{padding:20px 22px;border-bottom:1px solid var(--rule);
  display:flex;align-items:flex-start;justify-content:space-between;gap:16px;flex-wrap:wrap}
.case-id{font-size:13px;color:var(--ink-soft);letter-spacing:.05em;margin-bottom:8px}
.case-title{font-weight:800;font-size:24px;line-height:1.4;max-width:860px}
.case.top .case-title{font-size:clamp(26px,3vw,34px)}
.lead{font-size:17.5px;color:var(--ink);line-height:1.6;margin-top:10px;max-width:900px;font-weight:500}
.velocity{flex:none;display:flex;flex-direction:column;align-items:flex-end;gap:6px}
.velocity .label{font-size:14px;font-weight:700;letter-spacing:.03em}
.gauge{display:flex;gap:3px}
.gauge i{width:18px;height:6px;border-radius:1px;background:var(--rule)}

.media{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,1fr);border-bottom:1px solid var(--rule)}
.media.solo{grid-template-columns:1fr}
.media figure{border-right:1px solid var(--rule);background:#fff}
.media.solo figure{border-right:none}
.media img{display:block;width:100%;height:auto}
.media.solo img{max-height:460px;object-fit:cover}
.media figcaption{font-size:13px;color:var(--ink-soft);padding:8px 14px;border-top:1px solid var(--rule)}
@media (max-width:820px){.media{grid-template-columns:1fr}.media figure{border-right:none;border-bottom:1px solid var(--rule)}}

.chart{padding:18px 22px}
.chart h4{font-size:13px;letter-spacing:.04em;color:var(--red);margin-bottom:12px;font-weight:700}
.chart h4 small{color:var(--ink-soft);font-weight:500;margin-left:4px}
.bar{display:grid;grid-template-columns:110px 1fr 64px;gap:10px;align-items:center;font-size:15px;padding:5px 0}
.bar .track{background:#E1E6EA;height:12px}
.bar .fill{height:12px;background:#9AA6B2}
.bar .fill.hi{background:#2C5C87}
.bar b{text-align:right}
.chart .src-note{font-size:13px;color:var(--ink-soft);margin-top:10px}

.fields{display:grid;grid-template-columns:repeat(2,1fr)}
.field{padding:18px 22px;border-right:1px solid var(--rule);border-bottom:1px solid var(--rule)}
.field:nth-child(2n){border-right:none}
.field.wide{grid-column:1 / -1;border-right:none}
.field b{display:block;font-size:13px;letter-spacing:.04em;color:var(--red);margin-bottom:7px;font-weight:700}
.field p{font-size:17px;color:var(--ink-soft);line-height:1.6}
.field p + p{margin-top:10px}
@media (max-width:640px){.fields{grid-template-columns:1fr}.field{border-right:none}}

.sources{padding:14px 22px;display:flex;gap:12px;flex-wrap:wrap;align-items:center}
.sources .lbl{font-size:13px;letter-spacing:.04em;color:var(--ink-soft)}
.src{font-size:15px;text-decoration:none;border-bottom:1px solid var(--rule)}
.src:hover{border-color:var(--ink)}
.src small{color:var(--ink-soft);margin-left:3px}

.list-card{background:var(--card);border:1px solid var(--rule);margin-bottom:24px}
.list-row{display:grid;grid-template-columns:auto 1fr auto;gap:14px;align-items:baseline;padding:14px 22px;border-top:1px solid var(--rule);font-size:17px}
.list-row:first-child{border-top:none}
.list-row .tag{font-size:13px;font-weight:700;white-space:nowrap}
.list-row .links{font-size:14px;color:var(--ink-soft);white-space:nowrap}
.list-row .links a{text-decoration:none;border-bottom:1px solid var(--rule);margin-left:8px}
@media (max-width:640px){.list-row{grid-template-columns:1fr}.list-row .links{white-space:normal}}

.editorial{background:var(--card);border:1px solid var(--rule);border-left:4px solid var(--red);padding:22px 24px;margin-bottom:24px}
.editorial .k{font-size:13px;letter-spacing:.06em;color:var(--red);font-weight:700}
.editorial h3{font-weight:800;font-size:24px;margin:6px 0 10px;line-height:1.4}
.editorial p{font-size:17.5px;color:var(--ink-soft);line-height:1.7}

.foot{padding:24px 0 60px;font-size:13px;color:var(--ink-soft);line-height:1.8;border-top:1px solid var(--rule);margin-top:20px}

.log-row{display:grid;grid-template-columns:140px 1fr auto;gap:20px;align-items:center;
  padding:24px 0;border-top:1px solid var(--rule);text-decoration:none}
.log-row:last-child{border-bottom:1px solid var(--rule)}
.rdate{font-weight:700;font-size:19px;white-space:nowrap}
.rteaser{font-size:18px;color:var(--ink-soft);display:-webkit-box;-webkit-line-clamp:1;
  -webkit-box-orient:vertical;overflow:hidden}
.rarrow{font-size:15px;color:var(--ink-soft)}
.log-row:hover .rteaser{color:var(--ink)}
@media (max-width:600px){.log-row{grid-template-columns:1fr}.rarrow{display:none}}
"""


def page(title, body):
    return (f'<!DOCTYPE html>\n<html lang="ko">\n<head>\n<meta charset="UTF-8">\n'
            f'<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            f'<title>{e(title)}</title>\n<style>{CSS}</style>\n</head>\n<body>\n<div class="wrap">\n'
            f'{body}\n</div>\n</body>\n</html>\n')


# ── 컴포넌트 ─────────────────────────────────────────────────────────

def velocity(grade):
    color, steps = GRADE_COLOR[grade], GRADE_STEPS[grade]
    gauge = "".join(f'<i style="background:{color}"></i>' if i < steps else "<i></i>" for i in range(4))
    return (f'<div class="velocity"><div class="label" style="color:{color}">'
            f'{GRADE_ICON[grade]} {GRADE_LABEL[grade]}</div><div class="gauge">{gauge}</div></div>')


def chart_html(c):
    if not c:
        return ""
    mx = max(b["value"] for b in c["bars"]) or 1
    rows = []
    for b in c["bars"]:
        v = b["value"]
        val = (f"{v:,.2f}".rstrip("0").rstrip(".")) if isinstance(v, float) else f"{v:,}"
        pct = max(1.5, v / mx * 100)
        rows.append(f'<div class="bar"><span>{e(b["label"])}</span><div class="track">'
                    f'<div class="fill{" hi" if b.get("highlight") else ""}" style="width:{pct:.1f}%"></div></div>'
                    f'<b>{val}</b></div>')
    return (f'<div class="chart"><h4>{e(c["title"])}<small>단위: {e(c["unit"])}</small></h4>{"".join(rows)}'
            f'<div class="src-note">자료: {e(c["source"])}</div></div>')


def media_html(a):
    img = a.get("image_url")
    chart = chart_html(a.get("chart"))
    if not img and not chart:
        return ""
    fig = ""
    if img:
        cap = e(a.get("image_caption") or "대표 이미지")
        fig = (f'<figure><img src="{e(img)}" alt="{cap}" loading="lazy">'
               f'<figcaption>{cap} · 출처 {e(a.get("image_credit", ""))}</figcaption></figure>')
    solo = " solo" if not (img and chart) else ""
    return f'<div class="media{solo}">{fig}{chart}</div>'


def sources_html(sources):
    links = "".join(
        f'<a class="src" href="{e(s["url"])}" target="_blank" rel="noopener">{e(s["name"])}'
        f'{"<small>(" + e(s["date"]) + ")</small>" if s.get("date") else ""}</a>' for s in sources)
    return f'<div class="sources"><span class="lbl">출처</span>{links}</div>'


def fields_html(pairs, body=None):
    cells = []
    for label, val in pairs:
        if val:
            cells.append(f'<div class="field"><b>{label}</b><p>{e(val)}</p></div>')
    if body:
        ps = "".join(f"<p>{e(p)}</p>" for p in body)
        cells.append(f'<div class="field wide"><b>자세히</b>{ps}</div>')
    # 홀수 칸이면 마지막 일반 칸을 넓게
    plain = [i for i, c in enumerate(cells) if 'class="field"' in c]
    if len(plain) % 2 == 1:
        i = plain[-1]
        cells[i] = cells[i].replace('class="field"', 'class="field wide"', 1)
    return f'<div class="fields">{"".join(cells)}</div>' if cells else ""


def case_html(a, case_id, top=False, deep=False):
    if deep:
        pairs = [("무엇인가", a.get("what")), ("핵심 수치", a.get("numbers")),
                 ("경쟁 구도", a.get("competition")), ("반응", a.get("reaction")),
                 ("써볼 수 있나", a.get("availability")), ("왜 중요한가", a.get("why"))]
    else:
        pairs = [("왜 중요한가", a.get("why"))]
    return (f'<div class="case{" top" if top else ""}">'
            f'<div class="case-head"><div><div class="case-id">{e(case_id)} · {e(a["category"])}</div>'
            f'<div class="case-title">{e(a["headline"])}</div><div class="lead">{e(a["lead"])}</div></div>'
            f'{velocity(a["grade"])}</div>'
            f'{media_html(a)}{fields_html(pairs, a.get("body"))}{sources_html(a["sources"])}</div>')


def board_html(issue):
    def col(title, color, items):
        if items:
            lis = "".join(f'<li><i style="background:{color}"></i><span>{t}</span></li>' for t in items)
        else:
            lis = '<li class="empty">이번 호에는 없음</li>'
        return (f'<div class="board-col"><h3><span class="dot" style="background:{color}"></span>{title}</h3>'
                f'<ul>{lis}</ul></div>')
    cols = [
        col("오늘의 핵심", BOARD_COLORS["핵심"], [e(p) for p in issue["key_points"]]),
        col("주요소스 새 항목", BOARD_COLORS["key"],
            [e(s["headline"]) for s in issue["key_sources"]]),
        col("한국 AI", BOARD_COLORS["korea"], [e(a["headline"]) for a in issue["korea"]]),
        col("X · LinkedIn에서", BOARD_COLORS["social"],
            [f'<b>{e(s["who"])}</b> {e(s["text"])}<small>{e(s.get("date", ""))} · '
             f'<a href="{e(s["url"])}" target="_blank" rel="noopener">원문</a></small>' for s in issue["social"]]),
        col("주목할 일정", BOARD_COLORS["calendar"],
            [f'<b>{e(c["when"])}</b> {e(c["what"])}' for c in issue["calendar"]]),
    ]
    return f'<div class="board"><div class="board-grid">{"".join(cols)}</div></div>'


def all_articles(issue):
    arts = [issue["top_story"], *issue["key_sources"], *issue["korea"]]
    for s in issue["sections"]:
        arts += s.get("articles", [])
    return arts


# ── 페이지 ───────────────────────────────────────────────────────────

def report_page(issue, site_url):
    d = issue["date"]
    cid = f'AID·{d.replace("-", "")}'
    arts = all_articles(issue)
    primary_n = sum(1 for a in arts if a["grade"] == "primary")
    meta = (f'<div class="m"><span class="dot" style="background:{GRADE_COLOR["primary"]}"></span>1차 출처 확인 {primary_n}건</div>'
            f'<div class="m"><span class="dot" style="background:{BOARD_COLORS["key"]}"></span>주요소스 새 항목 {len(issue["key_sources"])}건</div>'
            f'<div class="m">기사 {len(arts)}건 · 단신 {len(issue["briefs"])}건 수록</div>'
            f'<div class="m">{pretty_date(d)} · 대상 {e(issue["period"])}</div>')
    out = [f'<a class="back" href="index.html">&larr; 전체 아카이브로</a>',
           f'<div class="headline">{e(d)} — 오늘의 AI</div>',
           f'<div class="metarow">{meta}</div>',
           board_html(issue),
           '<div class="section-title">1면 톱</div>',
           case_html(issue["top_story"], f"{cid}·TOP", top=True)]
    if issue["key_sources"]:
        out.append('<div class="section-title">주요소스 심층 리포트<small>주요소스 새 항목에서 출발해 원문 추적</small></div>')
        out += [case_html(s, f'{cid}·KS{i + 1:02d}', deep=True) for i, s in enumerate(issue["key_sources"])]
    n = 0
    for sec in issue["sections"]:
        if not sec.get("articles"):
            continue
        out.append(f'<div class="section-title">{e(sec["name"])}</div>')
        for a in sec["articles"]:
            n += 1
            out.append(case_html(a, f"{cid}·{n:02d}"))
    if issue["korea"]:
        out.append('<div class="section-title">한국 AI</div>')
        out += [case_html(a, f"{cid}·KR{i + 1:02d}") for i, a in enumerate(issue["korea"])]
    if issue["briefs"]:
        rows = "".join(
            f'<div class="list-row"><span class="tag" style="color:{GRADE_COLOR[b["grade"]]}">{GRADE_ICON[b["grade"]]}</span>'
            f'<span>{e(b["text"])}</span><span class="links">'
            + "".join(f'<a href="{e(s["url"])}" target="_blank" rel="noopener">{e(s["name"])}</a>' for s in b["sources"])
            + "</span></div>" for b in issue["briefs"])
        out.append(f'<div class="section-title">단신</div><div class="list-card">{rows}</div>')
    ed = issue["editorial"]
    out.append(f'<div class="section-title">해설</div><div class="editorial"><div class="k">오늘의 흐름</div>'
               f'<h3>{e(ed["title"])}</h3><p>{e(ed["body"])}</p></div>')
    notes = "".join(f"<br>· {e(x)}" for x in issue.get("notes") or [])
    out.append(f'<div class="foot">검증 등급 — ✅ 1차 출처(공식 발표·공시·문서) · ☑️ 복수 매체 교차 확인 · ⚠️ 단일 출처·협상 중 보도<br>'
               f'취재 범위 — {e(issue["coverage"])} · 주요소스 {e(issue["key_sources_checked"])}곳 확인{notes}<br>'
               f'이미지는 기업 공식 페이지의 대표 이미지만 원본 주소로 싣고 출처를 표기합니다. 차트는 공개 수치로 직접 작성했습니다.<br>'
               f'{DISCLAIMER}</div>')
    return page(f"{d} — AI 데일리", "\n".join(out))


def index_page(issues, site_url):
    rows = "".join(
        f'<a class="log-row" href="{e(i["date"])}.html"><div class="rdate">{compact_date(i["date"])}</div>'
        f'<div class="rteaser">{e(i["top_story"]["headline"])}</div><div class="rarrow">열기 →</div></a>'
        for i in issues) or '<div class="rteaser" style="padding:24px 0">아직 발행된 호가 없습니다.</div>'
    body = (f'<div class="headline" style="margin-top:60px">AI DAILY INTELLIGENCE</div>'
            f'<div class="metarow"><div class="m">매일 아침 전세계 AI 생태계 브리핑</div>'
            f'<div class="m"><a href="latest.html">최신 호 바로가기 →</a></div></div>'
            f'<div style="margin:24px 0 90px">{rows}</div>')
    return page("AI DAILY INTELLIGENCE — 아카이브", body)
