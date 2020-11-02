from aiohttp import web

import json

from services import UserServices


async def websocket_show(request):

    ws = web.WebSocketResponse()
    await ws.prepare(request)
    async for msg in ws:
        data = json.loads(msg.data)
        response = UserServices().save(data)
        await ws.send_json(response)