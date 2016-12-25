import time
import logging
from pecan import expose, abort
from pecan.rest import RestController

from iot.context import context
from iot.controllers.v1.comm import request_base

dev_mana_url = 'http://www.yunt.top:81/api/dev/'
DEV_MANA_CLI = request_base.deviceManageClient(dev_mana_url)
dev_sub_url = 'http://www.yunt.top:81/api/user/sub/'
DEV_SUB_CLI = request_base.deviceSubClient(dev_sub_url)

LOG = logging.getLogger(__name__)

class DevicesController(RestController):
    _custom_actions = {
        "push_command": ["GET"],
        "ajax_push_command": ["POST"],
        "subscrite_post": ["POST"],
        "subscrite_get": ["GET"],
        "realtime_view": ["GET"],
    }
    
    @expose("push_command.html")
    def push_command(self):
        #abort(505)
        return {}

    @expose('json')
    def ajax_push_command(self):
        return {"sucess": False}
        
    @expose('json')
    def subscrite_post(self):
        user = 'test'
        sub_url = context.get_post_data_with_key('sub_url')
        device_id = context.get_post_data_with_key('device_id')
        if not DEV_SUB_CLI.subscriteEvent(user, device_id, sub_url):
            return {'sucess': False}
        return {'sucess': True}
         
    @expose()
    def subscrite_get(self):
        pass

    def _subscrite(self, user, id, profile_type):
        api = 'sub_call/'
        # streaming apps
        if profile_type == '2':
            api = 'stream_call/'

        data = {
            "username": 'test',
            "deviceid": id,
            "ip": "120.76.52.151:8888",
            "api": api + str(id) + '/' + str(profile_type),
        }
        if not DEV_SUB_CLI.subscriteEvent(data):
            return False
        return True
        

    @expose("realtime_view.html")
    def realtime_view(self):
        user = 'test'
        device_id = context.get_get_data_with_key('device_id')
        device_profile = context.get_get_data_with_key('device_profile')
        if not self._subscrite(user, device_id, device_profile):
            return abort(404)
        sub_call_url = str(device_id) + '/' + str(device_profile)
        
        return {"device_id": device_id,
                'device_profile': device_profile,
                'sub_call_url': sub_call_url}

    @expose()
    def get_one(self, id):
        # TODO get devices detail
        pass

    @expose("list_device.html")
    def get_all(self):
        #TODO get all devices
        test_dev = {
            'device_id': 1234,
            'device_profile': 1,
            'device_name': 'test',
            'device_status': 'Active',
            'update_time': time.ctime(),    
        }
        test_video = {
            'device_id': 12345,
            'device_profile': 2,
            'device_name': 'testvideo',
            'device_status': 'Active',
            'update_time': time.ctime(),    
        }

        devices = [test_dev, test_video]
        return {'devices': devices}

    @expose('create_device.html')
    def new(self):
        # display a page to create a new resource
        return {"sucess": False}

    @expose()
    def edit(self):
        # display a page to edit an existing resource
        pass

    @expose('create_device.html')
    def post(self):
        # create a new record
        user = 'test'
        device_id = context.get_post_data_with_key('device_id')
        profile_type = context.get_post_data_with_key('profile_type')
        LOG.info('device id %s', device_id)
        LOG.info('profile type %s', profile_type)
        if not DEV_MANA_CLI.createDevice(device_id, user, profile_type):
            return {"sucess": False}
        return {"sucess": True}

    @expose()
    def put(self, id):
        # update an existing record
        pass

    @expose()
    def get_delete(self, id):
        # dispaly a delete confirmation page
        pass

    @expose()
    def delete(self, id):
        #delete an existing record
        pass
    
    @expose()
    def _default(self):
        return 'I cannot say hello in that language'
