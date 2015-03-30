import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.httpserver
import json
import sys
import datetime
import pytz

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
from aviastudent_backend.models import Telemetry, Vehicle


jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_user_id_from_payload = api_settings.JWT_PAYLOAD_GET_USER_ID_HANDLER

import django
django.setup()


def get_subscriptions(userId):
    user_obj = get_user_model().objects.get(id=userId)
    if hasattr(user_obj, 'subscribed_vehicles'):
        l = user_obj.subscribed_vehicles.values_list('id', flat=True)
        return l
    else:
        return []


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    clients = []
    telemetry_entry_list = []

    def open(self, *args):
        self.user_id = None
        self.vehicle_id = None
        self.token = ""
        self.closed_manually = False
        print("open", "WebSocketHandler")
        WebSocketHandler.clients.append(self)

        # d = serializers.serialize("json", get_user_model().objects.all(), ensure_ascii=False)
        # self.write_message(d)

    def on_message(self, message):
        if self not in WebSocketHandler.clients or self.closed_manually:
            return
        try:
            msg = json.loads(message)
        except:
            self.write_message(json.dumps({'error': 'not a valid json'}))
            self.close()
            return
        if 'token' in msg:
            self.token = msg['token']
        if self.token == "":
            return
        try:
            user_info = jwt_decode_handler(self.token)
            if self.user_id != user_info['user_id']:
                self.user_id = user_info['user_id']
                user_obj = get_user_model().objects.get(id=self.user_id)
                print('user_id', user_info['user_id'])
                if hasattr(user_obj, 'vehicle'):
                    self.vehicle_id = user_obj.vehicle.id
                    print('Vehicle : ', user_obj.vehicle.id)
                subscr = get_subscriptions(self.user_id)
                if len(subscr) > 0:
                    print('Subscriptions: ', subscr)
        except jwt.ExpiredSignatureError:
            try:
                self.closed_manually = True
                self.write_message(json.dumps({'error': 'not authorized'}))
            except:
                pass
                print('cannot write to client ', self.user_id)
            print({'error': 'not authorized'}, self.user_id)
            self.close()
            return
        except Exception as e:
            print(e)
        if 'ping' in msg:
            self.write_message(json.dumps({'pong': ''}))
            return
        if 'msg_type' in msg:
            # print(msg)
            if msg['msg_type'] == 'push_telem':
                if self.vehicle_id is not None:
                    if 'data' in msg and '_mt_timestamp' in msg:
                        new_m = {}
                        new_m['vehicle_id'] = self.vehicle_id
                        new_m["msg_type"] = "telem_update"
                        new_m["data"] = msg['data']
                        new_m["timestamp"] = msg['_mt_timestamp']
                        WebSocketHandler.telemetry_entry_list.insert(0, new_m)
                        self.saveTelemtry(self.vehicle_id, msg['data'], msg['_mt_timestamp'])

    def saveTelemtry(self, id, data, timestamp):
        t = Telemetry(vehicle=Vehicle.objects.get(id=id), record=data, timestamp=datetime.datetime.fromtimestamp(timestamp, tz=pytz.UTC))
        t.save()

    def on_close(self):
        print('closed', self.user_id)
        if self in WebSocketHandler.clients:
            WebSocketHandler.clients.remove(self)

    def check_origin(self, origin):
        return True

    def send_to_clients():
        try:
            for socket in WebSocketHandler.clients:
                if not socket.closed_manually and socket.vehicle_id is None and socket.token != "":
                    try:
                        jwt_decode_handler(socket.token)
                        to_send = reversed(WebSocketHandler.telemetry_entry_list)
                        subscr = get_subscriptions(socket.user_id)
                        for d_entry in to_send:
                            id = d_entry["vehicle_id"]
                            if id in subscr:
                                socket.write_message(json.dumps(d_entry, ensure_ascii=False))
                    except jwt.ExpiredSignatureError:
                        # print('Bad recepient')
                        socket.closed_manually = True
                        socket.write_message(json.dumps({'error': 'not authorized'}))
                        socket.close()
        except Exception as e:
            print(e)
        finally:
            WebSocketHandler.telemetry_entry_list = []


ssl_options = {
    "certfile": "ssl-certs/tornado.crt",
    "keyfile": "ssl-certs/tornado.key"
}
http_server = tornado.httpserver.HTTPServer(tornado.web.Application([(r'/ws', WebSocketHandler)]), ssl_options=ssl_options)
http_server.listen(444)
tornado.ioloop.PeriodicCallback(WebSocketHandler.send_to_clients, 100, tornado.ioloop.IOLoop.instance()).start()
tornado.ioloop.IOLoop.instance().start()
