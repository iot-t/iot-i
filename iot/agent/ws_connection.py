from tornado import websocket

from iot.agent import ws_manager

WS_MANAGER = ws_manager.get_manager()

class wsConnection(websocket.WebSocketHandler):
  
    def check_origin(self, origin):  
        return True

    def _check_perrimt(self, token):
        return True

    def open(self, *args, **kwargs):
        print "on open===="
        self._id = kwargs['id']
        if not self._check_perrimt(123):
            # TODO Close connection
            return self.close()
        print "wbsocket connection"
        WS_MANAGER.add_client(self._id, self)
        # init to client if possible
        profile_type = kwargs['profile_type']
        profile = self._get_device_profile(profile_type)
        if profile:
            self.write_message(profile)

    def on_message(self, msg):
        print msg

    def on_close(self):
        print "wbsocket close"
        WS_MANAGER.del_connection(self._id, self)

    def _get_device_profile(self, profile_type):
        ret = {}
        if profile_type == '2':
            # streaming apps
            ret['width'] = 300
            ret['high'] = 300
        return ret
