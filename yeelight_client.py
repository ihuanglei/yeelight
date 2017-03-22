#-*- coding: utf-8 -*-

import time
from yeelight import *

HOST_CMD = '239.255.255.251'
PORT_CMD = 1982


def send(host, port, cmd, param):
    command = 'CMD * HTTP/1.1\r\nlocation:%s:%s\r\nmethod:%s\r\nparam:%s' % (
        host, port, cmd, param)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(command, 0, (HOST_CMD, PORT_CMD))
    sock.close()

host = '192.168.1.100'
port = 1234

send(host, port, 'power_on', '{}')
time.sleep(5)
send(host, port, 'power_off', '{}')
