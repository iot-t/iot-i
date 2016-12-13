from pecan import expose
from pecan.secure import secure

from iot.context import context
from iot.controllers.v1 import admin
from iot.controllers.v1 import register
from iot.controllers.v1 import login
from iot.controllers.v1 import devices

class v1Controller(object):

    def __init__(self):
        self.admin = secure(admin.AdminController(), 'check_admin')
        selfregister = register.RegisterController()
        self.login = login.LoginController()
        self.devices = devices.DevicesController()

    @classmethod
    def check_admin(self):
        return False

    @expose('json')
    def index(self):
        return {"apiversion": "1.0.0"}
