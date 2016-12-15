from pecan import expose
from pecan.rest import RestController

from iot.model.sqlalchemy_db import user
from iot.context import context
from iot.controllers.v1.comm import send_email

class RegisterController(RestController):
    NAME_LEN_MIN = 6
    NAME_LEN_MAX = 60
    PWD_LEN_MIN = 8
    PWD_LEN_MAX = 60

    @expose("register.html")
    def get_all(self):
        return {'user': False}

    def _check_email(self, email):
        # Check if has register with this email
        return True

    def _check_user_data_vaild(self, name, pwd, email):
        if not (name and pwd and email):
            return False
        if len(name) < self.NAME_LEN_MIN or len(name) > self.NAME_LEN_MAX:
            return False

        if len(pwd) < self.PWD_LEN_MIN or len(pwd) > self.PWD_LEN_MAX:
            return False

        return self._check_email(email)

    def _set_verify_key(self, user_db):
        redis_db = context.redis_db()
        verify_key = os.urand(60)
        # TODO need to check if exists
        time = 24*60*60
        redis_db.set_key_with_timeout(verify_key, user_db.id, time)
        return verify_key

    def _send_verify_email(self, verify_key, user_db):
        email = send_email.send_email(verify_key, user_db.email) 
        email.send_email()

    @expose('register_sucess')
    def post(self):
        name = context.get_post_data_with_key('name')
        pwd = context.get_post_data_with_key('passwd')
        email = context.get_post_data_with_key('email')

        if not self._check_user_data_vaild(name, pwd, email):
            override_template("register_fail")
            return {'error': 'invaild passwd or name or email'}

        with context.session() as session:
            user_db = user.User(name=name, passwd=pwd, email=email)
            session.add(user_db)

        # send verify email to customer
        verify_key = self._set_verify_key(user_db)
        self._send_verify_email(verify_key, user_db)

        return {"verify_key": verify_key}
