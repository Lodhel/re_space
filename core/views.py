from aiohttp import web


async def websocket_show(request):

    ws = web.WebSocketResponse()

    return ws