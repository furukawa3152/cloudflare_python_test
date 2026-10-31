"""Scroll の一覧から itaru の記事を取り、data/posts.json を更新する。"""

import json
import re
import subprocess
from datetime import datetime
from html import unescape
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
POSTS_PATH = ROOT / "data" / "posts.json"
FETCHED_PATH = ROOT / "data" / "fetched_on.txt"
INDEX = "https://hagakurepgm.net/blog/"
AUTHOR = "itaru @hagakurepgm"
MAX_PAGES = 30


def fetch(url: str) -> str:
    result = subprocess.run(
        ["curl", "-fsSL", "--max-time", "30", "-A", "itaru-portfolio-fetch", url],
        check=True,
        capture_output=True,
    )
    return result.stdout.decode("utf-8", "replace")


def clean(text: str) -> str:
    return unescape(re.sub(r"\s+", " ", text).strip())


def articles(page: str) -> list[dict]:
    found = []
    for part in page.split('<article class="article">')[1:]:
        block = part.split("</article>", 1)[0]
        # 通常は /blog/。/tags/数字/ で公開された記事もある。
        url_m = re.search(
            r'href="(https://hagakurepgm.net/(?:blog/[^"#?]+|tags/\d+/))"',
            block,
        )
        title_m = re.search(r'<h3 class="article_title">(.*?)</h3>', block, re.S)
        author_m = re.search(
            r'<div class="article_contributor">.*?<p>(.*?)</p>', block, re.S
        )
        if not (url_m and title_m and author_m):
            continue
        url = url_m.group(1)
        if not url.endswith("/"):
            url += "/"
        found.append(
            {
                "url": url,
                "title": clean(title_m.group(1)),
                "author": clean(author_m.group(1)),
            }
        )
    return found


def next_page(page: str) -> str | None:
    match = re.search(r'<a class="page-next" href="([^"]+)"', page)
    if not match:
        return None
    href = match.group(1)
    if href.startswith("?"):
        return INDEX + href
    return href


def meta(page: str, prop: str) -> str:
    patterns = (
        rf'<meta[^>]+property="{prop}"[^>]+content="([^"]*)"',
        rf'<meta[^>]+content="([^"]*)"[^>]+property="{prop}"',
    )
    for pattern in patterns:
        match = re.search(pattern, page)
        if match:
            return clean(match.group(1))
    return ""


def post_from_page(url: str, page: str) -> dict:
    date_m = re.search(r'<time datetime="(\d{4}-\d{2}-\d{2})"', page)
    title = meta(page, "og:title")
    image = meta(page, "og:image")
    if not (date_m and title and image):
        raise RuntimeError(f"OGP が足りません: {url}")
    return {
        "title": title,
        "description": meta(page, "og:description"),
        "image": image,
        "url": url,
        "date": date_m.group(1),
        "site_name": meta(page, "og:site_name") or "HAGAKUREのブログサイト Scroll",
    }


def itaru_urls() -> list[str]:
    url = INDEX
    seen: set[str] = set()
    ordered: list[str] = []
    for _ in range(MAX_PAGES):
        page = fetch(url)
        for article in articles(page):
            if article["author"] != AUTHOR or article["url"] in seen:
                continue
            seen.add(article["url"])
            ordered.append(article["url"])
        url = next_page(page)
        if not url:
            return ordered
    raise RuntimeError(f"一覧が {MAX_PAGES} ページを超えました")


def load_old() -> list[dict]:
    if not POSTS_PATH.exists():
        return []
    return json.loads(POSTS_PATH.read_text())


def main() -> None:
    urls = itaru_urls()
    if not urls:
        raise RuntimeError("itaru の記事が 0 件です。一覧の取得に失敗した可能性があるので、ファイルは書きません。")
    posts = [post_from_page(url, fetch(url)) for url in urls]
    posts.sort(key=lambda post: post["date"], reverse=True)
    old = load_old()
    if posts == old:
        print(f"unchanged ({len(posts)} posts)")
        return
    old_urls = {post["url"] for post in old}
    new_urls = {post["url"] for post in posts}
    POSTS_PATH.write_text(json.dumps(posts, ensure_ascii=False, indent=2) + "\n")
    FETCHED_PATH.write_text(
        datetime.now(ZoneInfo("Asia/Tokyo")).strftime("%Y-%m-%d") + "\n"
    )
    added = [post["title"] for post in posts if post["url"] not in old_urls]
    removed = [post["title"] for post in old if post["url"] not in new_urls]
    print(f"wrote {POSTS_PATH} ({len(posts)} posts)")
    for title in added:
        print(f"  + {title}")
    for title in removed:
        print(f"  - {title}")


if __name__ == "__main__":
    main()
