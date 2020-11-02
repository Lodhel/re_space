from tornado.ioloop import IOLoop, PeriodicCallback
from tornado import gen
from tornado.websocket import websocket_connect
import json

from tornado import httpclient


class Client(object):
    def __init__(self, url, timeout):
        self.url = url
        self.timeout = timeout
        self.ioloop = IOLoop.instance()
        self.ws = None
        self.connect()
        PeriodicCallback(self.keep_alive, 20000).start()
        self.ioloop.start()

    @gen.coroutine
    def connect(self):
        print("trying to connect")
        try:

            # create an instace of HTTPRequest with the given url
            request = httpclient.HTTPRequest(self.url, headers={'Cookie': 'id=32'})
            self.ws = yield websocket_connect(request)
        except:
            print("connection error")
        else:
            print("connected")
            self.run()

    @gen.coroutine
    def run(self):
        msg = {
            "phone": "+7009",
            "email": "mail@mail.com",
            "first_name": "Djo",
            "password": "123456",
            "date_birthday": "1994-02-20",
            "gender": "male"
        }
        yield self.ws.write_message(json.dumps(msg))
        msg = yield self.ws.read_message()
        print(msg)
        self.run()

    def keep_alive(self):
        if self.ws is None:
            self.connect()
        else:
            pass
            #  message = "send message"
            #  print(message)
            #  self.ws.write_message(message)


if __name__ == "__main__":
    client = Client("ws://localhost:8080/api/show/", 5)

