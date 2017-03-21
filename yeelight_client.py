#-*- coding: utf-8 -*-

from yeelight import *

HOST_CMD = '239.255.255.251'
PORT_CMD = 1982

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    command = '''NOTIFY * HTTP/1.1
Host: 239.255.255.250:1982
Cache-Control: max-age=3600
Location: yeelight://192.168.1.239:55443
NTS: ssdp:alive
Server: POSIX, UPnP/1.0 YGLC/1
id: 0x000000000015243f
model: color
fw_ver: 18
support: get_prop set_default set_power toggle set_bright start_cf stop_cf set_scene cron_add cron_get cron_del set_ct_abx set_rgb
power: on
bright: 100
color_mode: 2
ct: 4000
rgb: 16711680
hue: 100
sat: 35
name: my_bulb
'''
    command = 'CMD * HTTP/1.1\r\nlocation:192.168.1.1:11234\r\nmethod:power_on\r\nparams:'
    sock.sendto(command, 0, (HOST_CMD, PORT_CMD))
    sock.close()
