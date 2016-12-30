import time
import binascii
import struct
from tornado import gen
from tornado import web

from iot.agent import ws_manager
from iot.agent import parse_subdata
from iot.agent import task_thread 

WS_MANAGER = ws_manager.get_manager()
EXECTORS = task_thread.get_executors()

@web.stream_request_body
class streamCallback(web.RequestHandler):
    # profile streaming app
    PROFILE_ID = '2'
    
    @gen.coroutine
    def get(self):
        a = 'sucess'
        self.finish(a)

    @gen.coroutine 
    def data_received(self, chunk):
        id =  self.path_kwargs['id']
        EXECTORS.submit(WS_MANAGER.send_to_client, id, chunk, True)

    @gen.coroutine    
    def post(self, **kwargs):
        id = kwargs.get('id')
        # TODO need async
        # Parse by profile_type
        #msg = parse_subdata.parse_data_by_profile_type(msg, profile_type)
        self.finish('iot-stream')
