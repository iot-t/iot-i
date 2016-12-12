import logging
from pecan import conf
from pecan.hooks import PecanHook
from pecan.hooks import TransactionHook

from iot import model
from iot.model import imp_redis
from iot.model import imp_mongo

LOG = logging.getLogger(__name__)

class RedisDbHook(PecanHook):

    def before(self, state):
        # setup redis db client to context
        state.request.context['_iot_redis'] = imp_redis.redisClient(dict(conf.redis))

    def after(self, state):
        # check if exist, In some case, framework
        # only call hooks after if route not found
        if '_iot_redis' in state.request.context:
            state.request.context['_iot_redis'].connectionClose()

class MongoDbHook(PecanHook):

    def before(self, state):
        state.request.context['iot_mongo'] = imp_mongo.mongoClient(dict(conf.mongo)['url'])

    def after(self, state):
        if '_iot_mongo' in state.request.context:
            state.request.context['iot_mongo'].connectionClose()

class SqlalchemyTransactionHook(TransactionHook):

    def __init__(self):
        super(SqlalchemyTransactionHook, self).__init__(
                model.start, model.start, model.commit,
                model.rollback, model.clear)
