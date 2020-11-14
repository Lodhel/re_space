from aiohttp import web

import json

from services import UserServices, ItemService


async def websocket_registration(request):

    ws = web.WebSocketResponse()
    request.app['channels'].append(ws)
    await ws.prepare(request)
    async for msg in ws:
        data = json.loads(msg.data)
        response = UserServices().save(data)
        await ws.send_json(response)


async def websocket_login(request):

    ws = web.WebSocketResponse()
    request.app['channels'].append(ws)
    await ws.prepare(request)
    async for msg in ws:
        data = json.loads(msg.data)
        response = UserServices().check(data)
        await ws.send_json(response)


async def websocket_item(request):

    ws = web.WebSocketResponse()
    await ws.prepare(request)
    async for msg in ws:
        response = ItemService().get()
        await ws.send_json(response)


async def websocket_echo(request):

    ws = web.WebSocketResponse()
    request.app['channels'].append(ws)
    await ws.prepare(request)
    async for msg in ws:
        for client in request.app['channels']:
            await client.send_json(msg.data)