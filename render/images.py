"""기업 공식 페이지에서 대표 이미지(og:image) 주소를 찾는다.

- 허용된 공식 도메인의 페이지만 조회한다(보도사진·언론사 이미지 사용 방지).
- 이미지는 저장소에 복사하지 않고 원본 주소를 그대로 쓴다(출처 표기는 템플릿이 자동).
- 실패하면 None을 돌려주고 빌드는 계속한다(사진만 빠짐).
"""
import html
import re
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

import requests

UA = "Mozilla/5.0 (compatible; ai-daily-briefing/1.0; +https://github.com/)"
TIMEOUT = 15

# 공식 블로그·뉴스룸·제품 페이지 도메인 (하위 도메인 포함)
OFFICIAL_DOMAINS = [
    "openai.com", "chatgpt.com", "anthropic.com", "claude.com", "blog.google", "deepmind.google",
    "ai.google.dev", "research.google", "about.fb.com", "ai.meta.com", "blogs.microsoft.com",
    "news.microsoft.com", "microsoft.ai", "nvidia.com", "nvidianews.nvidia.com", "aws.amazon.com",
    "aboutamazon.com", "apple.com", "x.ai", "mistral.ai", "huggingface.co", "github.blog",
    "thinkingmachines.ai", "deepseek.com", "qwenlm.github.io", "alibabacloud.com", "cohere.com",
    "perplexity.ai", "samsung.com", "news.samsung.com", "lgresearch.ai", "lgcorp.com",
    "kakaocorp.com", "navercorp.com", "clova.ai", "sktelecom.com", "news.sktelecom.com",
    "upstage.ai", "kt.com", "msit.go.kr", "korea.kr",
]


def is_official(url):
    host = (urlparse(url).hostname or "").lower()
    return any(host == d or host.endswith("." + d) for d in OFFICIAL_DOMAINS)


class _MetaParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.found = {}

    def handle_starttag(self, tag, attrs):
        if tag != "meta":
            return
        a = dict(attrs)
        key = (a.get("property") or a.get("name") or "").lower()
        if key in ("og:image", "og:image:url", "og:image:secure_url", "twitter:image") and a.get("content"):
            self.found.setdefault(key, a["content"])


def find_image(page_url, session=None):
    """공식 페이지의 대표 이미지 URL. 허용 도메인이 아니거나 실패하면 None."""
    if not page_url or not is_official(page_url):
        if page_url:
            print(f"[WARN] 이미지: 공식 도메인 아님, 건너뜀 {page_url}")
        return None
    s = session or requests.Session()
    try:
        r = s.get(page_url, headers={"User-Agent": UA}, timeout=TIMEOUT)
        r.raise_for_status()
        p = _MetaParser()
        p.feed(r.text[:400_000])
        img = None
        for k in ("og:image:secure_url", "og:image", "og:image:url", "twitter:image"):
            if p.found.get(k):
                img = html.unescape(p.found[k]).strip()
                break
        if not img:
            print(f"[WARN] 이미지: og:image 없음 {page_url}")
            return None
        img = urljoin(page_url, img)
        # 실제 이미지인지 확인
        h = s.get(img, headers={"User-Agent": UA}, timeout=TIMEOUT, stream=True)
        ctype = h.headers.get("Content-Type", "")
        h.close()
        if h.status_code != 200 or not ctype.startswith("image/"):
            print(f"[WARN] 이미지: 응답 이상({h.status_code}, {ctype}) {img}")
            return None
        return img
    except Exception as e:  # 네트워크 오류는 사진만 빼고 계속
        print(f"[WARN] 이미지: {page_url} → {e}")
        return None


def resolve_issue_images(issue):
    """이슈 안 모든 article의 image_page → image_url 채우기. 찾은 개수를 반환."""
    s = requests.Session()
    found = 0
    arts = [issue["top_story"], *issue["sketchlab"], *issue["korea"]]
    for sec in issue["sections"]:
        arts.extend(sec.get("articles", []))
    cache = {}
    for a in arts:
        page = a.get("image_page")
        if not page:
            continue
        if page not in cache:
            cache[page] = find_image(page, s)
        if cache[page]:
            a["image_url"] = cache[page]
            a["image_credit"] = re.sub(r"^www\.", "", urlparse(page).hostname or "")
            found += 1
    return found
