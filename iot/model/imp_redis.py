import redis

class redisClient(object):
    KEY_PREFIX = "iot_"
    def __init__(self, kwargs):
        self.redisCli = redis.StrictRedis(**kwargs)

    def set_key(self, key, vlaue):
        key = self.KEY_PREFIX + str(key)
        # todo check if success
        self.redisCli.set(key, vlaue)

    def set_key_with_timeout(self, key, vlaue, timeout):
        key = self.KEY_PREFIX + str(key)
        return self.redisCli.setex(key, vlaue, timeout)

    def get_key(self, key):
        key = self.KEY_PREFIX + str(key)
        return self.redisCli.get(key)

    def connectionClose(self):
        # close on every incoming request ?
        # FIXME
        self.redisCli.connection_pool.disconnect()

