from urllib.parse import urlparse
from workers import Response


async def on_fetch(request, env):
    path = urlparse(request.url).path
    if path == "/health":
        return Response(
            '{"ok": true}',
            headers={"content-type": "application/json; charset=utf-8"},
        )
    return await env.ASSETS.fetch(request)
