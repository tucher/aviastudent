import requests

import sys
import time
import os
import struct
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

#from pymavlink import mavlinkv10 as mavlink
port = 14550
msrc = mavutil.mavlink_connection('udp:127.0.0.1:{}'.format(port), planner_format=False,
                                  notimestamps=True,
                                  robust_parsing=True)


# simple basic byte pass through, no logging or viewing of packets, or analysis etc
# while True:
# L -> R
#    m = msrc.recv();
#    mdst.write(m);
# R -> L
#    m2 = mdst.recv();
#    msrc.write(m2);


# similar to the above, but with human-readable display of packets on stdout.
# in this use case we abuse the self.logfile_raw() function to allow
# us to use the recv_match function ( whch is then calling recv_msg ) , to still get the raw data stream
# which we pass off to the other mavlink connection without any interference.
# because internally it will call logfile_raw.write() for us.

# here we hook raw output of one to the raw input of the other, and vice versa:
# msrc.logfile_raw = mdst


def msg_to_js(msg):
    ret = dict()
    ret['mavlink_type_id'] = msg._type
    ret['time'] = getattr(msg, '_timestamp', None)
    ret['d'] = dict()
    for a in msg._fieldnames:
        v = getattr(msg, a)
        ret['d'][a] = v
    return ret

fake_mod = True
while True:
    l = msrc.recv_match()
    time.sleep(2)
    payload = {}
    if not fake_mod:
        if l is not None:
            if l.get_type() != 'BAD_DATA':
                payload = msg_to_js(l)
    else:
        payload = {"alt": 10000 + randint(-100,100), "vel": 15 + randint(-5,5)}
    data = {}
    data['data'] = payload
    print(json.dumps(data))
    data['msg_type'] = 'push_telem'
    data['token'] = token
    data['data']['timestamp'] = int(time.time() * 1000)
    try:
        ws.send(json.dumps(data))
    except:
        c = False
        while c is False:
            try:
                ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})
                ws.connect("wss://online.aviastudent.ru:444/ws")
                c = True
                print('WS connected')
                ws.send(json.dumps(data))
            except:
                pass
