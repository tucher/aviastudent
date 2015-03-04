import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.httpserver
import json
import sys
from random import randint
from time import time

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





def get_subscriptions(userId):
    return [-1, 2]


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    clients = []
    telemetry_entry_list = []

    def open(self, *args):
        self.authorized = False
        self.user_id = None
        print("open", "WebSocketHandler")
        WebSocketHandler.clients.append(self)

        d = serializers.serialize("json", get_user_model().objects.all(), ensure_ascii=False)
        #self.write_message(d)


    def on_message(self, message):
        try:
            msg = json.loads(message)
        except:
            self.write_message(json.dumps({'error': 'not a valid json'}))
            return
        
        if self.authorized == False:
            if 'token' in msg:
                try:
                    user_info = jwt_decode_handler(msg['token'])
                except:
                    self.write_message(json.dumps({'error': 'token is not valid'}))
                    return
                print('user_id', user_info['user_id'])
                self.user_id = user_info['user_id']
                self.authorized = True
            else:
                self.write_message(json.dumps({'error': 'not authorized'}))
                return
        else:
            if 'ping' in msg:
                self.write_message(json.dumps({'pong': ''}))
                return
        # for client in clients:
        #     client.write_message(message)

    def on_close(self):
        WebSocketHandler.clients.remove(self)

    def check_origin(self, origin):
        return True

    def fake_vehicle_data_generator():
        WebSocketHandler.telemetry_entry_list.insert(0, {"vehicle_id": -1, "timestamp": int(time() * 1000), "data": {"alt": 10000 + randint(-100,100), "vel": 15 + randint(-5,5)}})

    def send_to_clients():
        for d_entry in reversed(WebSocketHandler.telemetry_entry_list):
            id = d_entry["vehicle_id"]
            d_entry["msg_type"] = "telem_update"
            for socket in WebSocketHandler.clients:
                if socket.authorized is True:
                    subscr = get_subscriptions(socket.user_id)
                    if id in subscr:
                        socket.write_message(json.dumps(d_entry, ensure_ascii=False))
        WebSocketHandler.telemetry_entry_list = []


ssl_options = {
        "certfile": "ssl-certs/tornado.crt",
        "keyfile": "ssl-certs/tornado.key"
}
http_server = tornado.httpserver.HTTPServer(tornado.web.Application([(r'/ws', WebSocketHandler)]), ssl_options=ssl_options)
http_server.listen(444)
tornado.ioloop.PeriodicCallback(WebSocketHandler.fake_vehicle_data_generator, 1000, tornado.ioloop.IOLoop.instance()).start()
tornado.ioloop.PeriodicCallback(WebSocketHandler.send_to_clients, 100, tornado.ioloop.IOLoop.instance()).start()
tornado.ioloop.IOLoop.instance().start()