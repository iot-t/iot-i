import os
import binascii
from pecan import expose, abort
from pecan.rest import RestController

from iot.model.sqlalchemy_db import user
from iot.context import context
from iot.controllers.v1.comm import send_email

class LoginController(RestController):
    
    _custom_actions = {
        "reset_passwd": ["GET"],
        "ajax_reset_passwd": ["POST"],
        "forget_passwd": ["GET"],
        "ajax_forget_passwd": ["POST"]
    }

    @expose("login.html")
    def get_all(self):
        return {'user': False}

    @expose("forget_passwd.html")
    def forget_passwd(self):
        return {}    

    @expose('json')
    def ajax_forget_passwd(self):
        ret = {"sucess": False}
        user_name = context.get_post_data_with_key('name')
        user_email = context.get_post_data_with_key('email')
        
        if len(user_name) > 20:
            return ret
        
        db_session = context.get_db_session()
        user_db = db_session.query(user.User).filter_by(name=user_name, email=user_email).first()
        if user_db:
            timeout = 24 * 60 * 60
            redis_db = context.redis_db()
            reset_key = binascii.hexlify(os.urandom(50))
            redis_key = 'reset_' + reset_key
            redis_db.set_key_with_timeout(redis_key, user_db.id, timeout)
            # TODO send email
            email = send_email.send_email(user_db.email, 'forget_passwd')
            email.send_email({'reset_key': reset_key})
            ret['sucess'] = True
        return ret

    @expose("reset_passwd.html")
    def reset_passwd(self, reset_key):
        redis_db = cntext.redis_db()
        if redis_db.key_exists('reset_' + reset_key):
            return {'reset_key': reset_key}
        
        return abort(404)
    
    @expose('json')
    def ajax_reset_passwd(self):
        ret = {'sucess': False}
        reset_key = context.get_post_data_with_key('reset_key')
        # TODO need check passwd length
        new_passwd = context.get_post_data_with_key('new_passwd')
        reset_key = 'reset_' + reset_key
        redis_db = context.redis_db()
        reset_user_id = redis_db.get_key(reset_key)
        if reset_user_id and new_passwd:
            redis_db.del_key(reset_key)
            db_session = context.get_db_session()
            user_db = db_session.query(user.User).filter_by(id=reset_user_id)
            if user_db:
                user_db.salt = binascii.hexlify(os.urandom(20))
                passwd = new_passwd + user_db.salt
                user_db.passwd = hashlib.sha256(passwd.encode("utf-8")).hexdigest()
                ret['sucess'] = True

        return ret

    @expose('json')
    def post(self):
        return {"admin": "adminPort"}
