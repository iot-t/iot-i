from tornado import gen
from tornado import web

import time

class subCallback(web.RequestHandler):
    
    @gen.coroutine
    def get(self):
        a = yield gen.Task(self._test)
        print 'function'
        self.finish(a)
    
    def _test(self, **k):
        time.sleep(10)
        k['callback']('sub get sucess')
    def post(self):
        self.write('sub post success')
