from aiohttp import web

from views import websocket_registration, websocket_login, websocket_item, websocket_echo
import asyncio


loop = asyncio.get_event_loop()

app = web.Application(loop=loop)
app['channels'] = []

app.add_routes([
    web.get('/api/registration/', websocket_registration),
    web.get('/api/login/', websocket_login),
    web.get('/api/item/', websocket_item),
    web.get('/api/echo/', websocket_echo)
])

web.run_app(app)