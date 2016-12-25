from iot.agent import ws_logging as logging

LOG = logging.getLogger()

class wbManager(object):

    def __init__(self):
        self.all_client = {}

    def add_client(self, id, client):
        print "add client"
        print id
        if id not in self.all_client:
            self.all_client[id] = [client]
        else:
            if len(self.all_client[id]) < 3:
                self.all_client[id].append(client)
            else:
                LOG.error('devices %s client has excess max 3', id)

    def del_client_with_id(self, id):
        if id in self.all_client:
            del self.all_client[id]
        else:
            LOG.error('client not exists')
    
    def del_connection(self, id, conn):
        if id in self.all_client:
            if conn in self.all_client[id]:
                self.all_client[id].remove(conn)
            else:
                LOG.error("device %(id)s not exist connection %(conn)s", {'id': id, 'conn': conn})
            if not self.all_client[id]:
                del self.all_client[id]
        else:
            LOG.error("device %(id)s not exist connecton", {'id': id})
    
    def send_to_client(self, id, msg, binary=False):
        if id in self.all_client:
            # TODO catch error
            try:
                for _client in self.all_client[id]:
                    _client.write_message(str(msg), binary)
            except Exception as e:
                LOG.exception('send to client error %s', e)


_ws_manager = wbManager()

def get_manager():
    return _ws_manager
