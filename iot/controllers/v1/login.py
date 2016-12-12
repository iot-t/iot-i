from pecan import expose
from pecan.rest import RestController


class LoginController(RestController):

    @expose('json')
    def post(self):
        return {"admin": "adminPort"}
