import struct
from tornado import websocket
from tornado import gen

from iot.agent import ws_manager
from iot.agent import redis_db
 
REDIS_CONN = redis_db.get_redis_connection()
WS_MANAGER = ws_manager.get_manager()

class wsConnection(websocket.WebSocketHandler):

    def check_origin(self, origin):
        return True

    @gen.coroutine
    def open(self, *args, **kwargs):
        print "on open===="
        self._id = kwargs['id']
        token = None
        ret = yield gen.Task(REDIS_CONN.get, token)
        if ret:
            # TODO Close connection
            self.send_error()
        print "wbsocket connection"
        WS_MANAGER.add_client(self._id, self)
        # init to client if possible
        profile_type = kwargs['profile_type']
        profile = self._get_device_profile(profile_type)
        if profile:
            self.write_message(profile['data'], profile['binary'])

    def on_message(self, msg):
        print msg

    def on_close(self):
        print "wbsocket close"
        WS_MANAGER.del_connection(self._id, self)

    def _get_device_profile(self, profile_type):
        ret = {}
        if profile_type == '2':
            # streaming apps
            ret['binary'] = True
            width = 640
            height = 480
            ret['data'] = struct.Struct('>4sHH').pack('jsmp', width, height)
        return ret
