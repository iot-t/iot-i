from pecan import expose
from pecan.rest import RestController


class RegisterController(RestController):

    @expose('json')
    def post(self):
        return {"register": "register"}
