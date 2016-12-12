from pecan import request

class contextManager(object):

    def get_session_token(self):
        if 'session' in request:
            return request['session']
        else:
            return None

    def set_session_token(self, user_id):
        # TODO set to redis
        pass

    def session_token_is_vaild(self):
        # compare with redis record
        pass

    def is_admin(self):
        # get user role
        pass

    def redis_db(self):
        return request.context['_iot_redis']

    def mongo_db(self):
        return request.context['_iot_mongo']

context = contextManager()

