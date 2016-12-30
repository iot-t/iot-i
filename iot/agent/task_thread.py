from tornado import concurrent


class NoExecutor(object):
    def submmit(self, fn, *args, **kwargs):
        print 'call', args , kwargs
        return fn(*args, **kwargs)


try:
    # TODO This only support in python 3.5
    executor = concurrent.futures.ThreadPoolExecutor(8)
except Exception:
    excutor = NoExecutor()

def get_executors():
    return excutor
