import time
import binascii
import struct
from tornado import gen
from tornado import web

from iot.agent import ws_manager
from iot.agent import parse_subdata

WS_MANAGER = ws_manager.get_manager()

class subCallback(web.RequestHandler):
    # not streaming app
    # All data in short post body
    
    @gen.coroutine
    def get(self):
        a = 'sucess'
        self.finish(a)
        
    def _test(self, **k):
        time.sleep(10)
        k['callback']('sub get sucess')

    @gen.coroutine    
    def post(self, **kwargs):
        id = kwargs.get('id')
        profile_type = kwargs.get('profile_type')
        profile_type = '1' 
        msg = self.request.body
        # TODO need async
        # Parse by profile_type
        msg = parse_subdata.parse_data_by_profile_type(msg, profile_type)
        if msg is not None:
            print msg
            WS_MANAGER.send_to_client(id, msg)
        self.finish('iot-gateway')
