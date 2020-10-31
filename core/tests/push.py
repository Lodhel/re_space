import json

from websocket import create_connection


class WebsocketService:

    def connect(self, data, port=8080):
        ws = create_connection("ws://127.0.0.1:{}/api/show/".format(port))
        message = json.dumps(data)
        ws.send(message)


WebsocketService().connect(
    {
        "phone": "+7009",
        "email": "mail@mail.com",
        "first_name": "Djo"
    }
)