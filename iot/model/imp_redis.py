import redis

class redisClient(object):
    KEY_PREFIX = "iot_"
    HNAME_PREFIX = "ioth_"

    def __init__(self, kwargs):
        self.redisCli = redis.StrictRedis(**kwargs)

    def set_key(self, key, value):
        key = self.KEY_PREFIX + str(key)
        # todo check if success
        self.redisCli.set(key, value)

    def set_key_with_timeout(self, key, value, timeout):
        key = self.KEY_PREFIX + str(key)
        return self.redisCli.setex(key, timeout, value)

    def get_key(self, key):
        key = self.KEY_PREFIX + str(key)
        return self.redisCli.get(key)

    def key_exists(self, key):
        key = self.KEY_PREFIX + str(key)
        return self.redisCli.exists(key)

    def del_keys(self, *keys):
        _keys = []
        for _k in keys:
            _keys.append(str(_k) + self.KEY_PREFIX)
        return self.redisCli.delete(_keys)

    # Hash keys function
    def get_hkeys(self, name):
        name = str(name) + self.HNAME_PREFIX
        return self.redisCli.hkeys(name)

    def hkeys_exists(self, name, key):
        name = str(name) + self.HNAME_PREFIX
        key  = str(key) + self.KEY_PREFIX
        return self.redisCli.hexists(name, key)

    def get_hvalue(self, name, key):
        name = str(name) + self.HNAME_PREFIX
        key  = str(key) + self.KEY_PREFIX
        return self.redisCli.hget(name, key)

    def get_all_hvalue(self, name):
        name = str(name) + self.HNAME_PREFIX
        return self.redisCli.hvals(name)

    def del_hkeys(sel, name, *keys):
        name = str(name) + self.HNAME_PREFIX
        _keys = []
        for _k in keys:
            _keys.append(str(_k) + self.KEY_PREFIX)
        return self.redisCli.hdel(name, _keys)

    def set_hkey(self, name, key, value):
        name = str(name) + self.HNAME_PREFIX
        key = str(key) + self.KEY_PREFIX
        return self.redisCli.hset(name, key, value)

    def connectionClose(self):
        # close on every incoming request ?
        # FIXME
        self.redisCli.connection_pool.disconnect()

