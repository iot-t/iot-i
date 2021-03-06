from pecan import expose, redirect
from webob.exc import status_map

from iot.controllers.v1 import controller

class RootController(object):

    def __init__(self):
        # version
        self.v1 = controller.v1Controller()

    @expose(generic=True, template='index.html')
    def index(self):
        return dict()
    
    @expose(generic=True, template='home.html')
    def home(self):
        return {'user': True}
    
    @expose(generic=True, template='home_test.html')
    def home_test(self):
        return {'user': True,
                'topic_device':{'test_topic':['device-123','device-234','device-345'],
                                'test_notify': ['notify-123', 'notfiy-345','notif-567']}
                }

    @expose(generic=True, template='doc.html')
    def doc(self):
        return {'user': True}

    @index.when(method='POST')
    def index_post(self, q):
        redirect('https://pecan.readthedocs.io/en/latest/search.html?q=%s' % q)

    @expose('error.html')
    def error(self, status):
        try:
            status = int(status)
        except ValueError:  # pragma: no cover
            status = 500
        message = getattr(status_map.get(status), 'explanation', '')
        return dict(status=status, message=message)
