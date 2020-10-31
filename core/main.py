from aiohttp import web

from views import websocket_show
import asyncio


loop = asyncio.get_event_loop()

app = web.Application(loop=loop)


app.add_routes([
    web.get('/api/show/', websocket_show),
])

web.run_app(app)