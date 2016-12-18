import os

from pecan import request
from iot import model

class contextManager(object):

    def get_session_token(self):
        if 'session' in request:
            return request['session']
        else:
            return None

    def set_session_token(self, user_id):
        # TODO set to redis
        redis = self.redis_db()
        token = os.urandom()
        redis.set_key(token, user_id)

    def session_token_is_vaild(self):
        # compare with redis record
        if '_iot_token_vaild' in request.context:
            return request.context['_iot_token_vaild']

        request.context['_iot_token_vaild'] = False
        redis = self.redis_db()
        if redis.key_exists(self.get_session_token()):
            request.context['_iot_token_vaild'] = True
        return request.context['_iot_token_vaild']

    def is_admin(self):
        # get user role
        pass
    
    def get_db_session(self):
        return model.get_current_session()

    def get_post_data_with_key(self, key):
        data = request.POST.get(key)
        # why post data is unicode?
        if isinstance(data, unicode):
            data = data.encode('UTF-8')
        return data

    def redis_db(self):
        return request.context['_iot_redis']

    def mongo_db(self):
        return request.context['_iot_mongo']

context = contextManager()

