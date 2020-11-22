import os
import ssl

from aiohttp import web

from views import websocket_registration, websocket_login, websocket_item, websocket_echo, websocket_food
from views import websocket_friend
import asyncio


loop = asyncio.get_event_loop()

app = web.Application(loop=loop)
app['channels'] = []

app.add_routes([
    web.get('/api/registration/', websocket_registration),
    web.get('/api/login/', websocket_login),
    web.get('/api/item/', websocket_item),
    web.get('/api/echo/', websocket_echo),
    web.get('/api/food/', websocket_food),
    web.get('/api/friend/', websocket_friend)
])

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
crt = "{}/{}".format(BASE_DIR, "domain_srv.crt")
key = "{}/{}".format(BASE_DIR, "domain_srv.key")
ssl_context.load_cert_chain(crt, key)

web.run_app(app, ssl_context=ssl_context)