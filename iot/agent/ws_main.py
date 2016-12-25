import tornado.ioloop
import tornado.web

from iot.agent import ws_connection
from iot.agent import sub_callback
from iot.agent import stream_callback

def make_app():
    return tornado.web.Application([
        (r"/ws_socket/?(?P<id>[A-Za-z0-9]+)?/?(?P<profile_type>[A-Za-z0-9]+)?", ws_connection.wsConnection),
        (r"/sub_call/?(?P<id>[A-Za-z0-9-]+)?/?(?P<profile_type>[A-Za-z0-9-]+)?", sub_callback.subCallback),
        (r"/stream_call/?(?P<id>[A-Za-z0-9-]+)?/?(?P<profile_type>[A-Za-z0-9-]+)?/", stream_callback.streamCallback),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
