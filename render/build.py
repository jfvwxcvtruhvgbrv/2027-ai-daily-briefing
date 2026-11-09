"""issues/*.json → site/(날짜별 보고서, index.html) + out/email-<date>.html

사용:
  python -m render.build                       # 전체 사이트 빌드
  python -m render.build --email 2026-11-09    # 해당 호 메일 HTML·제목도 생성
  python -m render.build --issues examples --no-images   # 로컬 테스트
"""
import argparse
import json
import os
import sys
from pathlib import Path

from . import templates
from .validate import validate


def site_url():
    if os.environ.get("SITE_URL"):
        return os.environ["SITE_URL"].rstrip("/") + "/"
    repo = os.environ.get("GITHUB_REPOSITORY", "owner/repo")
    owner, name = repo.split("/", 1)
    return f"https://{owner.lower()}.github.io/{name}/"


def load_issues(folder):
    issues = []
    for p in sorted(Path(folder).glob("*.json")):
        with open(p, encoding="utf-8") as f:
            data = json.load(f)
        try:
            validate(data, p.name.replace("sample-", ""))
        except ValueError as ex:
            print(f"[ERROR] {p}: {ex}", file=sys.stderr)
            raise
        issues.append(data)
    issues.sort(key=lambda i: i["date"], reverse=True)
    return issues


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--issues", default="issues")
    ap.add_argument("--site", default="site")
    ap.add_argument("--out", default="out")
    ap.add_argument("--email", help="메일을 만들 호의 날짜(YYYY-MM-DD)")
    ap.add_argument("--no-images", action="store_true", help="이미지 조회 생략(로컬 테스트)")
    a = ap.parse_args(argv)

    issues = load_issues(a.issues)
    url = site_url()
    site, out = Path(a.site), Path(a.out)
    site.mkdir(parents=True, exist_ok=True)
    out.mkdir(parents=True, exist_ok=True)

    if not a.no_images:
        from .images import resolve_issue_images
        # 최근 7개 호만 이미지 재조회(오래된 호는 이미지 없이도 무방)
        for i in issues[:7]:
            n = resolve_issue_images(i)
            print(f"[INFO] {i['date']}: 이미지 {n}개 확보")

    for i in issues:
        (site / f"{i['date']}.html").write_text(templates.report_page(i, url), encoding="utf-8")
    (site / "index.html").write_text(templates.index_page(issues, url), encoding="utf-8")
    (site / ".nojekyll").write_text("", encoding="utf-8")
    print(f"[INFO] 보고서 {len(issues)}호 생성 → {site}/  (사이트 {url})")

    if a.email:
        match = [i for i in issues if i["date"] == a.email]
        if not match:
            print(f"[ERROR] {a.email} 호가 없습니다", file=sys.stderr)
            return 1
        i = match[0]
        report_url = f"{url}{i['date']}.html"
        (out / f"email-{i['date']}.html").write_text(templates.email_html(i, report_url), encoding="utf-8")
        (out / f"email-{i['date']}.txt").write_text(templates.email_text(i, report_url), encoding="utf-8")
        (out / f"subject-{i['date']}.txt").write_text(
            f"[AI 브리핑] {i['date']} ({i['weekday']}) — {i['tagline']}", encoding="utf-8")
        print(f"[INFO] 메일 생성 → {out}/email-{i['date']}.html")
    return 0


if __name__ == "__main__":
    sys.exit(main())
