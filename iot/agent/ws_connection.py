from tornado import websocket

class wsConnection(websocket.WebSocketHandler):
    def on_open(self):
        pass

    def on_message(self, msg):
        self.write_message("You said: " + msg)

    def on_close(self):
        pass
