from aiohttp import web

import json

from services import UserServices


async def websocket_registration(request):

    ws = web.WebSocketResponse()
    await ws.prepare(request)
    async for msg in ws:
        data = json.loads(msg.data)
        response = UserServices().save(data)
        await ws.send_json(response)


async def websocket_login(request):

    ws = web.WebSocketResponse()
    await ws.prepare(request)
    async for msg in ws:
        data = json.loads(msg.data)
        response = UserServices().check(data)
        await ws.send_json(response)