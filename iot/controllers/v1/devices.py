from pecan import expose
from pecan.rest import RestController


class DevicesController(RestController):

    @expose()
    def get_one(self, id):
        # TODO get devices detail
        pass
    @expose()
    def get_all(self):
        #TODO get all devices
        pass
    @expose()
    def new(self):
        # display a page to create a new resource
        pass

    @expose()
    def edit(self):
        # display a page to edit an existing resource
        pass

    @expose('json')
    def post(self):
        # create a new record
        return {"register": "register"}

    @expose()
    def put(self, id):
        # update an existing record
        pass

    @expose()
    def get_delete(self, id):
        # dispaly a delete confirmation page
        pass

    @expose()
    def delete(self, id):
        #delete an existing record
        pass

