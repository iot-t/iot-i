import tornadoredis

from iot.agent import configure as conf

pool = tornadoredis.ConnectionPool(**conf.redis_db)
CLIENT = tornadoredis.Client(connection_pool=pool)

def get_redis_connection():
    return CLIENT
