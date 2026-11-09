"""이슈 JSON 검증. 필수 항목이 빠지면 ValueError로 빌드를 멈춘다(조용한 실패 방지)."""
import re

GRADES = {"primary", "multi", "single"}
TOP_KEYS = ["date", "weekday", "period", "tagline", "key_points", "top_story", "sketchlab",
            "sections", "korea", "briefs", "social", "editorial", "calendar", "coverage", "sketchlab_last"]
ARTICLE_KEYS = ["category", "grade", "headline", "lead", "why", "sources"]


def _err(path, msg):
    raise ValueError(f"[{path}] {msg}")


def _check_sources(path, sources):
    if not isinstance(sources, list) or not sources:
        _err(path, "sources는 1개 이상 필요")
    for i, s in enumerate(sources):
        if not s.get("name") or not str(s.get("url", "")).startswith("http"):
            _err(f"{path}.sources[{i}]", "name과 http(s) url 필요")


def _check_chart(path, chart):
    if chart is None:
        return
    for k in ("title", "unit", "source", "bars"):
        if k not in chart:
            _err(path, f"chart.{k} 누락")
    if not chart["bars"]:
        _err(path, "chart.bars 비어 있음")
    for i, b in enumerate(chart["bars"]):
        if "label" not in b or not isinstance(b.get("value"), (int, float)):
            _err(f"{path}.chart.bars[{i}]", "label과 숫자 value 필요")


def check_article(path, a):
    for k in ARTICLE_KEYS:
        if not a.get(k):
            _err(path, f"{k} 누락")
    if a["grade"] not in GRADES:
        _err(path, f"grade는 {sorted(GRADES)} 중 하나 (현재 {a['grade']!r})")
    if "body" in a and not isinstance(a["body"], list):
        _err(path, "body는 단락 배열")
    if a.get("image_page") and not str(a["image_page"]).startswith("http"):
        _err(path, "image_page는 http(s) URL")
    _check_sources(path, a["sources"])
    _check_chart(path, a.get("chart"))


def validate(issue, filename=None):
    for k in TOP_KEYS:
        if k not in issue:
            _err("issue", f"최상위 {k} 누락")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", issue["date"]):
        _err("issue", "date 형식은 YYYY-MM-DD")
    if filename and not filename.startswith(issue["date"]):
        _err("issue", f"파일명({filename})과 date({issue['date']}) 불일치")
    if len(issue["key_points"]) != 3:
        _err("issue", "key_points는 3개")
    check_article("top_story", issue["top_story"])
    for i, s in enumerate(issue["sketchlab"]):
        check_article(f"sketchlab[{i}]", s)
        if not isinstance(s.get("no"), int):
            _err(f"sketchlab[{i}]", "no(정수) 필요")
    if not issue["sections"]:
        _err("issue", "sections가 비어 있음")
    total = 0
    for i, sec in enumerate(issue["sections"]):
        if not sec.get("name"):
            _err(f"sections[{i}]", "name 누락")
        for j, a in enumerate(sec.get("articles", [])):
            check_article(f"sections[{i}].articles[{j}]", a)
            total += 1
    for i, a in enumerate(issue["korea"]):
        check_article(f"korea[{i}]", a)
    for i, b in enumerate(issue["briefs"]):
        if not b.get("text") or b.get("grade") not in GRADES:
            _err(f"briefs[{i}]", "text와 grade 필요")
        _check_sources(f"briefs[{i}]", b.get("sources"))
    for i, s in enumerate(issue["social"]):
        if not s.get("who") or not s.get("text") or not str(s.get("url", "")).startswith("http"):
            _err(f"social[{i}]", "who, text, url 필요 (확인된 포스트만)")
    if not issue["editorial"].get("title") or not issue["editorial"].get("body"):
        _err("editorial", "title과 body 필요")
    if total + len(issue["korea"]) + 1 < 3:
        _err("issue", "기사가 너무 적음(1면 포함 3건 미만)")
    return issue
