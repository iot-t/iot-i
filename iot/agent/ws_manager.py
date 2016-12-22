class wbManager(object):

    def __init__(self):
        self.all_client = {}

    def addClient(self, id, client):
        if id not in self.all_client:
            self.all_client[id] = client
        else:
            LOG.error('client has added')

    def delClient(self, id):
        if id in self.all_client:
            del self.all_client[id]
        else:
            LOG.error('client not exists')

    def sendToClient(self, id, msg):
        if id in self.all_client:
            # TODO catch error
            try:
                self.all_client[id].write_message(msg)
            except Exception as e:
                pass

