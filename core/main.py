from aiohttp import web

from views import websocket_registration
import asyncio


loop = asyncio.get_event_loop()

app = web.Application(loop=loop)


app.add_routes([
    web.get('/api/registration/', websocket_registration),
])

web.run_app(app)