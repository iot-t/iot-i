from pecan import expose
from pecan.rest import RestController


class AdminController(RestController):

    @expose('json')
    def get_all(self):
        return {"admin": "adminPort"}
