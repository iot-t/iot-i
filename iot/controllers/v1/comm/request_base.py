import requests
import logging

LOG = logging.getLogger(__name__)

class requestBase(object):

    def __init__(self, path):
        self.base_path = path

    def post(self, url, kwargs):
        url = self.base_path + url
        print url
        return requests.post(url, data=kwargs)

    def get(self, url, **kwargs):
        url = self.base_path + url
        print url
        return requests.get(url, params=kwargs)

    def put(self, url, **kwargs):
        url = self.base_path + url
        return requests.put(url, data=kwargs)


class deviceManageClient(requestBase):
    
    def __init__(self, path):
        super(deviceManageClient, self).__init__(path)

    def createDevice(self, device_id, user, profile_type):
        url = 'create/' + str(device_id) + '/' + user + '/' + str(profile_type)
        try:
            ret = self.get(url)
            ret.raise_for_status()
        except Exception as e:
            LOG.exception(e)
            return False

        return True

    def deleteDevice(self, device_id):
        url = 'delete/' + str(device_id)
        try:
            ret = self.get(url)
            ret.raise_for_status()
        except Exception as e:
            LOG.exception(e)
            return False

        return True

    def registerDevice(self, device_id):
        url = 'register/' + str(device_id)
        try:
            ret = self.get(url)
            ret.raise_for_status()
        except Exception as e:
            LOG.exception(e)
            return False

        return True

    def unregisterDevice(self, device_id):
        url = 'unregister/' + str(device_id)
        try:
            ret = self.get(url)
            ret.raise_for_status()
        except Exception as e:
            LOG.exception(e)
            return False

        return True

class deviceSubClient(requestBase):
    def __init__(self, path):
        super(deviceSubClient, self).__init__(path)
    
    def pushCommand(self,id, data):
        try:
            print id
            print data
            ret = self.post('', data)
            ret.raise_for_status()
        except Exception as e:
            LOG.exception(e)
            return False

        return True

    def subscriteEvent(self, data):
        try:
            print data
            ret = self.post('', data)
            ret.raise_for_status()
        except Exception as e:
            LOG.exception(e)
            return False

        return True

class deviceCmdClient(requestBase):
    def __init__(self, path):
        super(deviceCmdClient, self).__init__(path)
    
    def pushCommand(self,id, data):
        try:
            print id
            print data
            ret = self.post(id, data)
            print ret
            print ret.text
            ret.raise_for_status()
        except Exception as e:
            LOG.exception(e)
            return False

        return True
