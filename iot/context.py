import os

from pecan import request
from iot import model

class contextManager(object):

    def get_session_token(self):
        if 'session' in request.environ['beaker.session']:
            return request['beaker.session']['session']
        else:
            return None
    
    def set_session_token(self, user_id):
        # TODO set to redis
        redis = self.redis_db()
        token = os.urandom(20)
        redis.set_key(token, user_id)
        request.environ['beaker.session']['session'] = token
        request.environ['beaker.session'].save()

    def session_token_is_vaild(self):
        # compare with redis record
        if '_iot_token_vaild' in request.context:
            return request.context['_iot_token_vaild']

        request.context['_iot_token_vaild'] = False
        redis = self.redis_db()
        user_id = redis.get_key(self.get_session_token())
        if user_id:
            self.user_id = user_id
            request.context['_iot_token_vaild'] = True
        return request.context['_iot_token_vaild']

    @property
    def user_id(self):
        if hasattr(self, 'user_id'):
            return self.user_id
        self.user_id = None
        return self.user_id
    
    @property
    def user(self):
        if not hasattr(self.user):
            self.user = None
            if self.user_id is not None:
                db = self.get_db_session()
                user_db = db.query(user.User).filter_by(id=self.user_id).first()
                if user_db:
                    self.user = user_db
        return self.user

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
    
    def get_get_data_with_key(self, key):
        data = request.GET.get(key)
        # why post data is unicode?
        if isinstance(data, unicode):
            data = data.encode('UTF-8')
        return data


    def redis_db(self):
        return request.context['_iot_redis']

    def mongo_db(self):
        return request.context['_iot_mongo']

context = contextManager()

