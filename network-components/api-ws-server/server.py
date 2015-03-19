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
    if userId != 1:
        return [-1, 2]
    else:
        return []

def get_vehicle_id(userId):
    if userId == 1:
        return -1
    else:
        None

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    clients = []
    telemetry_entry_list = []

    def open(self, *args):
        self.user_id = None
        self.token = ""
        print("open", "WebSocketHandler")
        WebSocketHandler.clients.append(self)

        d = serializers.serialize("json", get_user_model().objects.all(), ensure_ascii=False)
        #self.write_message(d)


    def on_message(self, message):
        try:
            msg = json.loads(message)
        except:
            self.write_message(json.dumps({'error': 'not a valid json'}))
            self.close()
            WebSocketHandler.clients.remove(self)
            return
        if 'token' in msg:
            self.token = msg['token']
        try:
            user_info = jwt_decode_handler(self.token)
            if self.user_id != user_info['user_id']:
                print('user_id', user_info['user_id'])
            self.user_id = user_info['user_id']
        except:
            self.write_message(json.dumps({'error': 'not authorized'}))
            self.close()
            WebSocketHandler.clients.remove(self)
            print({'error': 'not authorized'}, self.user_id)
            return
        if 'ping' in msg:
            self.write_message(json.dumps({'pong': ''}))
            return
        if 'msg_type' in msg:
            # print(msg)
            if msg['msg_type'] == 'push_telem':
                new_m = {}
                new_m['vehicle_id'] = get_vehicle_id(self.user_id)
                new_m["msg_type"] = "telem_update"
                new_m["data"] = msg['data']
                new_m["timestamp"] = msg['data']['timestamp']
                print(new_m)
                WebSocketHandler.telemetry_entry_list.insert(0, new_m)
        # for client in clients:
        #     client.write_message(message)

    def on_close(self):
        print('closed', self.user_id)
        if self in WebSocketHandler.clients:
            WebSocketHandler.clients.remove(self)

    def check_origin(self, origin):
        return True

    def fake_vehicle_data_generator():
        WebSocketHandler.telemetry_entry_list.insert(0, {"vehicle_id": -1, "timestamp": int(time() * 1000), "data": {"alt": 10000 + randint(-100,100), "vel": 15 + randint(-5,5)}})

    def send_to_clients():
        for d_entry in reversed(WebSocketHandler.telemetry_entry_list):
            id = d_entry["vehicle_id"]
            for socket in WebSocketHandler.clients:
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
# tornado.ioloop.PeriodicCallback(WebSocketHandler.fake_vehicle_data_generator, 1000, tornado.ioloop.IOLoop.instance()).start()
tornado.ioloop.PeriodicCallback(WebSocketHandler.send_to_clients, 100, tornado.ioloop.IOLoop.instance()).start()
tornado.ioloop.IOLoop.instance().start()