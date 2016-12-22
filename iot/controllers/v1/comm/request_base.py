import requests
import logging

LOG = logging.get_logger(__name__)

class requestBase(object):

    def __init__(self, path):
        self.base_path = path

    def post(self, url, **kwargs):
        url = self.base_path + url
        return requests.post(url, data=kwargs)

    def get(self, url, **kwargs):
        url = self.base_path + url
        return requests.get(url, params=kwargs)

    def put(self, url, **kwargs):
        url = self.base_path　+ url
        return requests.put(url, data=kwargs)


class deviceManageClient(requestBase):
    
    def __init__(self, path):
        super(deviceManageClient, self).__init__(path)

    def subscriteEvent(self, username, device_id, return_url):
        sub_url = username + '/' + str(device_id) + '/' + return_url
        try:
            self.get(sub_url)
        except Exception as e:
            LOG.exception(e)
    
    def createDevice(self, device_id):
        url = 'create/' + str(device_id)
        try:
            ret = self.get(url)
        except Exception as e:
            ret = None
            LOG.exception(e)

        return ret

    def deleteDevice(self, device_id):
        url = 'delete/' + str(device_id)
        try:
            ret = self.get(url)
        except Exception as e:
            LOG.exception(e)
        return ret

    def registerDevice(self, device_id):
        url = 'register/' + str(device_id)
        try:
            ret = self.get(url)
        except Exception as e:
            LOG.exception(e)
        return ret

    def unregisterDevice(self, device_id):
        url = 'unregister/' + str(device_id)
        try:
            ret = self.get(url)
        except Exception as e:
            LOG.exception(e)
        return ret

