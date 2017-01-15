# -*- coding: utf-8 -*-
        
import binascii
import os
import validators
import hashlib

from pecan import expose,override_template
from pecan.rest import RestController

from iot.model.sqlalchemy_db import user
from iot.context import context
from iot.controllers.v1.comm import send_email

class RegisterController(RestController):
    NAME_LEN_MIN = 6
    NAME_LEN_MAX = 20
    PWD_LEN_MIN = 8
    PWD_LEN_MAX = 32

    @expose("register.html")
    def get_all(self):
        return {'user': False}

    def _hash_passwd_with_salt(self, pwd, salt):
        pwd = pwd + salt
        sha256 = hashlib.sha256(pwd.encode('utf-8'))
        return sha256.hexdigest()

    def _check_email(self, email):
        # Check if has register with this email
        try:
            return validators.email(email)
        except validators.ValidationFailure:
            return False

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
        verify_key = binascii.hexlify(os.urandom(60))
        # TODO need to check if exists
        time = 24*60*60
        redis_db.set_key_with_timeout(verify_key, user_db.id, time)
        return verify_key

    def _send_verify_email(self, verify_key, user_db):
        email = send_email.send_email(user_db.email)
        email_context = {'verify_key': verify_key}
        email.send_email(email_context)

    @expose('json')
    def post(self, **kwargs):
        name = context.get_post_data_with_key('name')
        pwd = context.get_post_data_with_key('passwd')
        email = context.get_post_data_with_key('email')
        if not self._check_user_data_vaild(name, pwd, email):
            return {'success': False,
                    'error_msg': 'invaild passwd or name or email'}

        salt = binascii.hexlify(os.urandom(20))
        db_session = context.get_db_session()
        pwd = self._hash_passwd_with_salt(pwd, salt)
        with db_session.begin(subtransactions=True):
            user_db = db_session.query(user.User).filter_by(email=email).first()
            if user_db:
                return {'sucess': False,
                        'error_msg': 'Invaild email'} 
            user_db = user.User(name=name, passwd=pwd, email=email, salt=salt)
            db_session.add(user_db)

        # send verify email to customer
        verify_key = self._set_verify_key(user_db)
        self._send_verify_email(verify_key, user_db)

        return {"success": True}
