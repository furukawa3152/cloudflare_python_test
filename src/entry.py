from urllib.parse import urlparse

from workers import Response, WorkerEntrypoint


class Default(WorkerEntrypoint):
    async def fetch(self, request):
        path = urlparse(request.url).path
        if path == "/health":
            return Response(
                '{"ok": true}',
                headers={"content-type": "application/json; charset=utf-8"},
            )
        return await self.env.ASSETS.fetch(request)
