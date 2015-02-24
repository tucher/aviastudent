import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.httpserver

clients = []


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self, *args):
        print("open", "WebSocketHandler")
        clients.append(self)
        self.write_message("Yo from server!")

    def on_message(self, message):
        print(message)
        for client in clients:
            client.write_message(message)

    def on_close(self):
        clients.remove(self)

    def check_origin(self, origin):
        return True

ssl_options = {
        "certfile": "ssl-certs/tornado.crt",
        "keyfile": "ssl-certs/tornado.key"
}
http_server = tornado.httpserver.HTTPServer(tornado.web.Application([(r'/ws', WebSocketHandler)]), ssl_options=ssl_options)
http_server.listen(444)
tornado.ioloop.IOLoop.instance().start()