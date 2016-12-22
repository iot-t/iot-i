import tornado.ioloop
import tornado.web

from iot.agent import ws_connection
from iot.agent import sub_callback

def make_app():
    return tornado.web.Application([
        (r"/ws_socket", ws_connection.wsConnection),
        (r"/sub_call", sub_callback.subCallback),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

