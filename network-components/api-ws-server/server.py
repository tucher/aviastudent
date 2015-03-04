import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.httpserver
import json
import sys


# the mock-0.3.1 dir contains testcase.py, testutils.py & mock.py

from django.core import serializers
sys.path.append('../aviastudent_backend')

from os import environ
environ.setdefault("DJANGO_SETTINGS_MODULE", "aviastudent_backend.settings")
from django.conf import settings as dj_settings
import jwt
from rest_framework import exceptions
from rest_framework_jwt import utils
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import get_user_model

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_user_id_from_payload = api_settings.JWT_PAYLOAD_GET_USER_ID_HANDLER

import django
django.setup()


clients = []


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self, *args):
        self.authorized = False
        print("open", "WebSocketHandler")
        clients.append(self)

        d = serializers.serialize("json", get_user_model().objects.all(), ensure_ascii=False)
        for client in clients:
            client.write_message(d)


    def on_message(self, message):
        try:
            msg = json.loads(message)
        except:
            self.write_message(json.dumps({'error': 'not a valid json'}))
            return
        if 'ping' in msg:
            self.write_message(json.dumps({'pong': ''}))
            return
        if self.authorized == False:
            if 'token' in msg:
                print('token', msg['token'])
                try:
                    user_info = jwt_decode_handler(msg['token'])
                except:
                    self.write_message(json.dumps({'error': 'cannot decode token'}))
                    return
                print('user_id', user_info['user_id'])
            else:
                self.write_message(json.dumps({'error': 'not authorized'}))
                return
        else:
            pass
        # for client in clients:
        #     client.write_message(message)

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