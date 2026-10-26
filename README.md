# 古川 格のポートフォリオ

佐賀で HAGAKURE PROGRAMMING塾を運営している古川 格の紹介ページです。末尾に、[Scroll](https://hagakurepgm.net/blog/) へ itaru の名前で公開している記事を、各記事の OGP で添えています。

記事データは `data/posts.json` です。Scroll の一覧を読み直してからページを作ります。

```bash
python3 scripts/fetch_posts.py
python3 scripts/build_page.py
python3 -m http.server 8765 --directory public
```

GitHub Actions の `Update Scroll posts` が、毎日 6:00 JST に同じ取得と再生成を行い、差分があれば main へコミットしてから Cloudflare へ出します。main への push でも `Deploy` が公開します。どちらもリポジトリシークレット `CLOUDFLARE_API_TOKEN` と `CLOUDFLARE_ACCOUNT_ID` を使います。

手元から出すときは、依存を入れたあとです。

```bash
uv sync
uv run pywrangler deploy
```

`/` は `public/index.html`、`/health` は Python Worker が `{"ok": true}` を返します。
