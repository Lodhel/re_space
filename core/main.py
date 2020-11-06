from aiohttp import web

from views import websocket_registration, websocket_login
import asyncio


loop = asyncio.get_event_loop()

app = web.Application(loop=loop)


app.add_routes([
    web.get('/api/registration/', websocket_registration),
    web.get('/api/login/', websocket_login),
])

web.run_app(app)