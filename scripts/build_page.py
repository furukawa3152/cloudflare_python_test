"""data/posts.json からポートフォリオの HTML を生成する。"""

import html
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTS_PATH = ROOT / "data" / "posts.json"
FETCHED_PATH = ROOT / "data" / "fetched_on.txt"
OUT_PATH = ROOT / "public" / "index.html"

WORKS = [
    {
        "num": "01",
        "title": "HAGAKURE PROGRAMMING塾",
        "text": "佐賀でITやAIを学びたい仲間とコミュニティを運営しています。\nぜひお気軽に参加ください。",
        "href": "https://hagakurepgm.net/",
        "label": "塾のサイト",
    },
    {
        "num": "02",
        "title": "Scroll",
        "text": "参加者が自分の学びを置く、ハードルの低い技術ブログです。2025年に公開しました。アウトプットを、自分の学びに閉じず、みんなの学びにしたかった場所です。",
        "href": "https://hagakurepgm.net/blog/",
        "label": "ブログを見る",
    },
    {
        "num": "03",
        "title": "Brew Journal",
        "text": "日々のコーヒー抽出と豆の購入履歴を残すアプリケーションです。AWS+v0で作成しています。",
        "href": "https://coffee-notebook-app.vercel.app/",
        "label": "アプリを開く",
    },
    {
        "num": "04",
        "title": "SAGA IT COMMUNITY DAY",
        "text": "県内のITコミュニティが集まるイベントです。\n参加コミュニティとして、\nまた運営メンバーの一人として関わっています。",
        "href": "https://furukawa3152.github.io/saga-it-community-day2027/",
        "label": "イベントを見る",
    },
]

def card(post: dict, hidden: bool = False) -> str:
    title = html.escape(" ".join(post["title"].split()))
    image = html.escape(post["image"], quote=True)
    url = html.escape(post["url"], quote=True)
    date = html.escape(post["date"])
    klass = "note later" if hidden else "note"
    return f"""
        <a class="{klass}" href="{url}">
          <img src="{image}" alt="">
          <time datetime="{date}">{date}</time>
          <strong>{title}</strong>
        </a>"""


def work(item: dict) -> str:
    return f"""
      <a class="row proj" href="{html.escape(item["href"], quote=True)}">
        <span class="num">{item["num"]}</span>
        <div>
          <h3>{html.escape(item["title"])}</h3>
          <span class="tags">{html.escape(item["label"])}</span>
        </div>
        <p>{html.escape(item["text"]).replace("\n", "<br>")}</p>
      </a>"""


def fetched_sentence() -> str:
    if not FETCHED_PATH.exists():
        return ""
    year, month, day = FETCHED_PATH.read_text().strip().split("-")
    return f"{int(year)}年{int(month)}月{int(day)}日に更新"


def main() -> None:
    posts = json.loads(POSTS_PATH.read_text())
    by_year: dict[str, list] = defaultdict(list)
    for post in posts:
        by_year[post["date"][:4]].append(post)

    visible = 5
    seen = 0
    note_sections = []
    for year in sorted(by_year, reverse=True):
        year_hidden = seen >= visible
        cards = []
        for post in by_year[year]:
            cards.append(card(post, seen >= visible))
            seen += 1
        year_class = " later-year" if year_hidden else ""
        note_sections.append(
            f"""
      <h3 class="year{year_class}">{html.escape(year)}<span>{len(by_year[year])}本</span></h3>
      <div class="notes">{"".join(cards)}
      </div>"""
        )
    hidden_count = max(0, len(posts) - visible)
    more_notes = ""
    if hidden_count:
        more_notes = f"""
      <input class="more-notes-toggle" id="more-notes" type="checkbox">
      <label class="more-notes" for="more-notes"><span class="shut">ほか{hidden_count}本</span><span class="open">閉じる</span></label>"""

    page = f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>ITARU FURUKAWA — Portfolio</title>
  <meta name="description" content="古川 格のポートフォリオ。医療の現場から、Python・AI・コミュニティを通じて、日々の課題を形にする。">
  <meta property="og:description" content="日常の気づきを、変化のきっかけに。ITの力で、「ちょっと面白く」">
  <meta property="og:type" content="website">
  <meta property="og:image" content="https://itaruweb.com/images/web/og.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="ITの力で、「ちょっと面白く」">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="https://itaruweb.com/images/web/og.jpg">
  <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' fill='%23171917'/%3E%3Ctext x='32' y='44' text-anchor='middle' font-size='32' fill='%23d9f18d' font-family='serif'%3E格%3C/text%3E%3C/svg%3E">
  <style>
    :root {{
      --bg: #171917;
      --ink: #f1f0e8;
      --muted: #a6aaa1;
      --accent: #d9f18d;
    }}
    * {{ box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; scroll-padding-top: 30px; }}
    body {{
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font-family: Arial, "Helvetica Neue", "Hiragino Kaku Gothic ProN", Meiryo, sans-serif;
      line-break: strict;
      word-break: auto-phrase;
    }}
    a {{ color: inherit; text-decoration: none; }}
    a:focus-visible {{ outline: 2px solid var(--accent); outline-offset: 8px; }}
    img {{ max-width: 100%; display: block; }}
    header {{
      padding: 28px 4%;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      border-bottom: 1px solid #ffffff25;
    }}
    .brand {{ font-size: 17px; font-weight: 700; letter-spacing: -0.6px; white-space: nowrap; }}
    .brand span {{ color: var(--accent); }}
    nav {{ display: flex; flex-wrap: wrap; justify-content: flex-end; gap: 30px; font-size: 11px; letter-spacing: 1px; }}
    nav a:hover {{ color: var(--accent); }}
    .edition {{ font: 10px monospace; color: var(--muted); }}
    .hero {{
      position: relative;
      margin: 24px 24px 0;
      min-height: 720px;
      height: calc(100svh - 115px);
      max-height: 1050px;
      isolation: isolate;
      overflow: hidden;
    }}
    .photo {{
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      object-fit: cover;
      object-position: center;
      z-index: -3;
      filter: brightness(0.68);
    }}
    .hero::before {{
      content: "";
      position: absolute;
      inset: 0;
      background:
        linear-gradient(90deg, #0007, transparent 80%),
        linear-gradient(0deg, #111c, transparent 60%);
      z-index: -1;
    }}
    .eyebrow {{
      position: absolute;
      top: 35px;
      left: 3%;
      font: 10px monospace;
      letter-spacing: 1.7px;
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .dot {{
      width: 6px;
      height: 6px;
      background: var(--accent);
      display: inline-block;
      border-radius: 50%;
    }}
    .side {{
      position: absolute;
      right: 30px;
      top: 38px;
      font: 10px monospace;
      letter-spacing: 2px;
      writing-mode: vertical-rl;
    }}
    .hero-main {{ padding: 128px 3% 150px; }}
    h1 {{
      font-size: clamp(75px, 10.6vw, 160px);
      letter-spacing: -0.075em;
      line-height: 0.88;
      font-weight: 500;
      margin: 0;
    }}
    h1 em {{
      font-style: normal;
      color: var(--accent);
    }}
    .intro {{
      margin: 30px 0 0 5px;
      font-size: 15px;
      font-weight: 500;
      letter-spacing: 0.12em;
      line-height: 2;
    }}
    .hero-bottom {{
      position: absolute;
      bottom: 34px;
      left: 3%;
      right: 3%;
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
    }}
    .person {{ font-size: 12px; line-height: 1.9; }}
    .person strong {{ display: block; font-size: 20px; letter-spacing: 3px; font-weight: 400; }}
    .person small {{ color: #c5c5bb; font: 10px monospace; letter-spacing: 1.6px; }}
    .explore {{ display: flex; gap: 36px; align-items: center; font-size: 11px; letter-spacing: 1px; }}
    .circle {{
      width: 56px;
      height: 56px;
      border: 1px solid #ffffff80;
      border-radius: 50%;
      display: grid;
      place-items: center;
      font-size: 22px;
      transition: 0.2s;
    }}
    .explore:hover .circle {{ background: var(--accent); border-color: var(--accent); color: #171917; }}
    .strip {{
      padding: 22px 4%;
      display: flex;
      justify-content: space-between;
      gap: 16px;
      font: 10px monospace;
      color: var(--muted);
      letter-spacing: 1px;
      border-bottom: 1px solid #ffffff25;
    }}
    .section {{ padding: 95px 6%; }}
    .about {{ display: grid; grid-template-columns: 1fr 2fr; gap: 50px; }}
    .label {{ font: 10px monospace; letter-spacing: 1.7px; color: var(--accent); }}
    h2 {{
      font-weight: 400;
      font-size: clamp(26px, 3.1vw, 44px);
      line-height: 1.65;
      letter-spacing: 0.03em;
      margin: 0 0 24px;
    }}
    .copy {{ font-size: 13px; color: var(--muted); line-height: 2.2; max-width: 650px; margin: 0 0 1.2em; }}
    .work {{ padding-top: 0; }}
    .work-head {{ display: flex; align-items: center; justify-content: space-between; margin-bottom: 30px; }}
    .work-head h2 {{ font-family: Georgia, serif; font-size: 43px; letter-spacing: -1.5px; margin: 0; }}
    .work-list {{ border-top: 1px solid #ffffff40; }}
    .row {{
      display: grid;
      grid-template-columns: 70px 1.2fr 1fr;
      gap: 24px;
      border-bottom: 1px solid #ffffff30;
      padding: 32px 0;
    }}
    .num {{ font: 11px monospace; color: var(--muted); padding-top: 8px; }}
    .row h3 {{ font-size: 25px; font-weight: 400; margin: 0 0 13px; letter-spacing: -0.7px; }}
    .tags {{ font: 9px monospace; letter-spacing: 1px; color: var(--accent); }}
    .row p {{ font-size: 12px; color: var(--muted); line-height: 2; margin: 0; }}
    .proj:hover h3 {{ color: var(--accent); }}
    .likes {{
      list-style: none;
      margin: 10px 0 18px;
      padding: 0;
      font-size: 14px;
      line-height: 1.9;
    }}
    .prints {{
      margin-top: 48px;
      max-width: 720px;
    }}
    .mount {{
      margin: 0;
      background: #f7f5f0;
      color: #171917;
      padding: 12px;
    }}
    .mount img {{ width: 100%; }}
    .credit {{
      margin: 12px 0 0;
      text-align: right;
      font: 10px monospace;
      letter-spacing: 1px;
      color: var(--muted);
    }}
    .plate {{
      min-height: 68vh;
      height: auto;
      max-height: none;
      display: flex;
      align-items: flex-end;
    }}
    .plate .hero-main {{ padding: 18vh 6% 56px; }}
    .plate blockquote {{
      margin: 0;
      max-width: 11em;
      font-size: clamp(28px, 3.4vw, 44px);
      font-weight: 400;
      line-height: 1.65;
      letter-spacing: 0.04em;
    }}
    .plate .keep {{ white-space: nowrap; }}
    .year {{
      display: flex;
      gap: 10px;
      align-items: baseline;
      margin: 36px 0 14px;
      font-size: 22px;
      font-weight: 400;
    }}
    .year span {{ color: var(--muted); font: 11px monospace; }}
    .notes {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; }}
    .note {{ display: flex; flex-direction: column; gap: 6px; min-width: 0; }}
    .note img {{ width: 100%; aspect-ratio: 1.7 / 1; object-fit: cover; }}
    .note time {{ color: var(--muted); font: 10px monospace; }}
    .note strong {{ font-size: 14px; font-weight: 500; line-height: 1.5; }}
    .more-notes-toggle,
    .more-notes {{ display: none; }}
    .more-notes .open {{ display: none; }}
    .foot {{ margin: 28px 0 0; color: var(--muted); font-size: 12px; }}
    .closing {{
      background: #d9f18d;
      color: #1c2416;
      padding: 55px 6%;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 30px;
    }}
    .closing h2 {{
      font-size: clamp(30px, 4vw, 57px);
      letter-spacing: -2px;
      line-height: 1.1;
      margin: 12px 0 0;
    }}
    .closing .label {{ color: #3f4b2e; }}
    .community {{ border-bottom: 1px solid #1c2416; padding: 14px 0; font-size: 11px; }}
    .mail {{
      display: inline-block;
      margin-top: 8px;
      font-size: clamp(22px, 3vw, 36px);
      letter-spacing: -0.03em;
      border-bottom: 1px solid #ffffff40;
      padding-bottom: 8px;
    }}
    .mail:hover {{ color: var(--accent); border-color: var(--accent); }}
    footer {{
      padding: 27px 4%;
      font: 10px monospace;
      display: flex;
      justify-content: space-between;
      gap: 12px;
      color: var(--muted);
    }}
    @media (min-width: 1600px) {{
      .hero-main {{ padding-top: 170px; }}
      .plate .hero-main {{ padding-top: 18vh; }}
    }}
    @media (max-width: 800px) {{
      .notes {{ grid-template-columns: 1fr 1fr; }}
    }}
    @media (max-width: 700px) {{
      header {{ padding: 23px 6%; flex-wrap: wrap; }}
      .edition {{ display: none; }}
      nav {{ width: 100%; justify-content: flex-start; gap: 18px; font-size: 9px; }}
      .hero {{ margin: 12px 12px 0; min-height: 660px; height: calc(100svh - 90px); }}
      .hero-main {{ padding: 150px 6% 170px; }}
      h1 {{ font-size: clamp(62px, 14vw, 98px); }}
      .eyebrow {{ left: 6%; font-size: 8px; letter-spacing: 1px; }}
      .side {{ right: 16px; font-size: 8px; }}
      .intro {{ font-size: 12px; letter-spacing: 0.03em; margin-top: 28px; }}
      .hero-bottom {{ left: 6%; right: 6%; bottom: 26px; }}
      .person strong {{ font-size: 18px; }}
      .explore {{ gap: 12px; font-size: 9px; }}
      .circle {{ width: 40px; height: 40px; }}
      .strip {{ font-size: 8px; gap: 20px; padding: 20px 6%; }}
      .strip span:last-child {{ display: none; }}
      .section {{ padding: 65px 7%; }}
      .about {{ grid-template-columns: 1fr; gap: 25px; }}
      .work {{ padding-top: 0; }}
      .row {{ grid-template-columns: 25px 1fr; gap: 15px; }}
      .row p {{ grid-column: 2; }}
      .row h3 {{ font-size: 23px; }}
      .work-head h2 {{ font-size: 36px; }}
      .plate .hero-main {{ padding: 16vh 7% 40px; }}
      .closing {{ padding: 40px 7%; align-items: flex-start; flex-direction: column; }}
      .closing h2 {{ letter-spacing: -1px; }}
      footer {{ font-size: 8px; padding: 24px 7%; }}
      #notes .note.later,
      #notes .year.later-year {{ display: none; }}
      .more-notes-toggle {{
        display: block;
        position: absolute;
        width: 1px;
        height: 1px;
        overflow: hidden;
        clip: rect(0 0 0 0);
      }}
      .more-notes {{
        display: inline-block;
        margin-top: 22px;
        color: var(--muted);
        font-size: 12px;
        letter-spacing: 0.04em;
        border-bottom: 1px solid #ffffff40;
        padding-bottom: 4px;
      }}
      #notes:has(#more-notes:checked) .note.later {{ display: flex; }}
      #notes:has(#more-notes:checked) .year.later-year {{ display: flex; }}
      #notes:has(#more-notes:checked) .more-notes .shut {{ display: none; }}
      #notes:has(#more-notes:checked) .more-notes .open {{ display: inline; }}
    }}
    @media (max-width: 520px) {{
      .notes {{ grid-template-columns: 1fr; }}
    }}
    @media (prefers-reduced-motion: reduce) {{
      html {{ scroll-behavior: auto; }}
      .circle {{ transition: none; }}
    }}
  </style>
</head>
<body id="top">
  <header>
    <a class="brand" href="#top">ITARU FURUKAWA<span>•</span></a>
    <nav aria-label="メインナビゲーション">
      <a href="#about">ABOUT</a>
      <a href="#work">FOCUS</a>
      <a href="#community">COMMUNITY ↗</a>
      <a href="#notes">NOTES</a>
      <a href="#contact">CONTACT</a>
    </nav>
    <span class="edition">PERSONAL PORTFOLIO / 2026</span>
  </header>
  <main>
    <section class="hero" aria-labelledby="hero-title">
      <img class="photo" src="images/web/hero.jpg" alt="木漏れ日が円弧状の石畳に落とす光と影">
      <div class="eyebrow"><span class="dot"></span> HEALTHCARE · TECHNOLOGY · COMMUNITY</div>
      <span class="side">BASED IN SAGA, JAPAN</span>
      <div class="hero-main">
        <h1 id="hero-title">Make it<br><em>interesting.</em></h1>
        <p class="intro">日常の気づきを、変化のきっかけに。<br>ITの力で、「ちょっと面白く」</p>
      </div>
      <div class="hero-bottom">
        <div class="person"><strong>古川 格</strong><small>ITARU FURUKAWA</small></div>
        <a class="explore" href="#about">EXPLORE MY WORLD <span class="circle" aria-hidden="true">↓</span></a>
      </div>
    </section>
    <div class="strip">
      <span>01 — IDEAS INTO EVERYDAY PRACTICE</span>
      <span>PYTHON / AI / HEALTHCARE DX</span>
      <span>SCROLL TO DISCOVER ↓</span>
    </div>
    <section id="about" class="section about">
      <div class="label">01 / ABOUT ME</div>
      <div>
        <h2>現場で見つけて、つくって、<br>日々の仕事を少しずつ変える。</h2>
        <p class="copy">医療の現場で、院内DXと業務改善に取り組んでいます。<br>PythonやAIを使い、目の前の課題を、実際に使える仕組みへ。<br>「HAGAKURE PROGRAMMING塾」を仲間と運営し、学び、試し、共有する場を育てています。</p>
      </div>
    </section>
    <section class="section" id="profile">
      <div class="about">
        <div class="label">PROFILE</div>
        <div>
          <h2>なんでも面白くしたい人。</h2>
          <p class="copy">40歳手前で、県の講座をきっかけに Python にハマりました。佐賀県が生んだ伝説のプログラマー育成カリキュラム、「SAGA Smart Samurai ゼロから始めるプログラミング塾」の1期生です。</p>
          <p class="label">LIKE</p>
          <ul class="likes">
            <li>guitar</li>
            <li>coffee</li>
            <li>camera</li>
            <li>python</li>
            <li>サウナ</li>
            <li>嫁と双子の娘</li>
          </ul>
          <p class="copy">HTML と CSS の練習も兼ねて、このサイトを作っています。</p>
        </div>
      </div>
      <div class="prints">
        <figure class="mount">
          <img src="images/web/cameras.jpg" alt="窓辺の机に置いた二台のNikon">
        </figure>
        <p class="credit">All Photo with Rollei35</p>
      </div>
    </section>
    <section class="hero plate" aria-label="佐賀で仲間を増やしていきたい">
      <img class="photo" src="images/web/path.jpg" alt="木の枝がトンネルになった道">
      <div class="hero-main">
        <blockquote>佐賀で、プログラミングと<span class="keep">AIによる</span>業務自動化を実践する仲間を増やしていきたい。</blockquote>
      </div>
    </section>
    <section id="work" class="section work">
      <div class="work-head">
        <h2>Areas of focus.</h2>
        <span class="label">02 / WHAT I DO</span>
      </div>
      <div class="work-list">
        <article class="row">
          <span class="num">01</span>
          <div>
            <h3>Healthcare DX</h3>
            <span class="tags">WORKFLOW / DATA / AUTOMATION</span>
          </div>
          <p>医療現場の業務を見つめ、部署を越えて改善する。<br>データの共有と日々の作業の自動化に取り組む。</p>
        </article>
        <article class="row">
          <span class="num">02</span>
          <div>
            <h3>Build with Python &amp; AI</h3>
            <span class="tags">PYTHON / LOCAL AI / WEB APPS</span>
          </div>
          <p>小さくつくって、使いながら磨いていく。<br>音声の文字起こしから、業務を支えるアプリまで。</p>
        </article>
        <article class="row">
          <span class="num">03</span>
          <div>
            <h3>Learning, together.</h3>
            <span class="tags">HAGAKURE / COMMUNITY / SAGA</span>
          </div>
          <p>ひとりの学びを、みんなの次の一歩に。<br>プログラミングと生成AIを、もっと身近なものにする。</p>
        </article>
      </div>
    </section>
    <section class="section" id="works">
      <p class="label">WORK</p>
      <h2>作ったものなど</h2>
      <p class="copy">コミュニティの運営と、そのまわりで公開しているものです。</p>
      <div class="work-list">
        {"".join(work(item) for item in WORKS)}
      </div>
    </section>
    <section class="section" id="notes">
      <p class="label">NOTES</p>
      <h2>Scrollに書いた記事</h2>
      <p class="copy">{fetched_sentence()}</p>
      {"".join(note_sections)}
      {more_notes}
      <p class="foot">記事の本文は Scroll 側にあります。</p>
    </section>
    <section class="section" id="contact">
      <p class="label">CONTACT</p>
      <h2>問い合わせ</h2>
      <p class="copy">仕事のこと、コミュニティのこと、メールでどうぞ。</p>
      <a class="mail" href="mailto:info@itaruweb.com">info@itaruweb.com</a>
    </section>
    <section class="closing" id="community">
      <div>
        <span class="label">03 / COMMUNITY</span>
        <h2>Stay curious. Keep building.</h2>
      </div>
      <a class="community" href="https://hagakurepgm.net/" target="_blank" rel="noopener noreferrer">HAGAKURE PROGRAMMING塾 ↗</a>
    </section>
  </main>
  <footer>
    <span>© 2026 ITARU FURUKAWA</span>
    <span>SAGA, JAPAN · MADE OF SMALL STEPS.</span>
  </footer>
</body>
</html>
"""
    OUT_PATH.write_text(page)
    print(f"wrote {OUT_PATH} ({len(posts)} posts)")


if __name__ == "__main__":
    main()
