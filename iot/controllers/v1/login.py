from pecan import expose
from pecan.rest import RestController


class LoginController(RestController):

    @expose("login.html")
    def get_all(self):
        return {'user': False}

    @expose('json')
    def post(self):
        return {"admin": "adminPort"}
