import requests
import time
import json
import ssl
from random import randint

from pymavlink import mavutil
import websocket


token = requests.post("https://online.aviastudent.ru/api/v1/auth/login/",
                      data={"username": "test_vehicle", "password": "123"}, verify=False).json()['token']
print("Token:", token)


ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})
ws.connect("wss://online.aviastudent.ru:444/ws")
print('WS connected')
ws.send(json.dumps({"token": token}))


port = 14550
msrc = mavutil.mavlink_connection('udp:127.0.0.1:{}'.format(port), planner_format=False,
                                  notimestamps=True,
                                  robust_parsing=True)

accum_dict = dict()
last_time = time.time()
prev_msg = None

# def msg_to_js(msg):
#     ret = dict()
#     ret['mavlink_type_id'] = msg._type
#     ret['_timestamp'] = getattr(msg, '_timestamp', None)
#     for a in msg._fieldnames:
#         v = getattr(msg, a)
#         ret[a] = v
#     return ret

fake_mod = False

while True:
    msg = msrc.recv_match()
    time.sleep(0.05)
    payload = {}
    if not fake_mod:
        if msg is not None:
            if msg.get_type() != 'BAD_DATA':
                accum_dict['mavlink_type_id'] = msg._type
                accum_dict['_timestamp'] = getattr(msg, '_timestamp', None)
                for a in msg._fieldnames:
                    accum_dict[a] = getattr(msg, a)
                payload = accum_dict
    else:
        payload = {"alt": 10000 + randint(-100, 100), "vel": 15 + randint(-5, 5)}
    if payload == {}:
        continue
    data = {}
    data['data'] = payload
    # print(json.dumps(data, ensure_ascii=False))
    data['msg_type'] = 'push_telem'
    data['token'] = token
    data['_mt_timestamp'] = time.time()
    if time.time() - last_time > 0.2 and prev_msg != data:
        last_time = time.time()
        try:
            ws.send(json.dumps(data))
            prev_msg = data
        except:
            ws.close()
            c = False
            while c is False:
                try:
                    print("reconnecting")
                    ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})
                    ws.connect("wss://online.aviastudent.ru:444/ws")
                    c = True
                    print('WS connected')
                    token = requests.post("https://online.aviastudent.ru/api/v1/auth/login/",
                          data={"username": "test_vehicle", "password": "123"}, verify=False).json()['token']
                    print("Token:", token)
                    data['token'] = token
                    ws.send(json.dumps(data))
                except:
                    pass
