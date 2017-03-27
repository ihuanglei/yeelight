#-*- coding: utf-8 -*-

import time
import json
from yl_auto_server import *

HOST_CMD = '239.255.255.250'
PORT_CMD = 1982


def send():
    s = '''
NOTIFY * HTTP/1.1
Host: 239.255.255.250:1982
Cache-Control: max-age=3600
Location:   yeelight://192.168.1.239:55443
NTS: ssdp:alive
Server: POSIX, UPnP/1.0 YGLC/1
id: 0x200000000015243f
model: color
fw_ver: 18
support: get_prop set_default set_power toggle set_bright start_cf stop_cf set_scene
cron_add cron_get cron_del set_ct_abx set_rgb
power: on
bright: 50
color_mode: 2
ct: 4000
rgb: 16711680
hue: 100
sat: 35
name: 厨房
'''
    # s = '111'
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(s, 0, (HOST_CMD, PORT_CMD))
    # data, addr = sock.recvfrom(2048)
    # print data
    # sock.close()


# host = '192.168.1.100'
# port = 1234

# send(host, port, 'power_on', '{}')
# time.sleep(5)
# send(host, port, 'power_off', '{}')
send()
