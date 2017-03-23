import time
import re
import json
import socket
import sys
import threading
import logging
import posixpath
import urllib
import urlparse
import BaseHTTPServer
import os


__version__ = "0.1"

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')

# common message


class Message:

    def __str__(self):
        return '\n'.join(['%s:%s' % item for item in self.__dict__.items()])

# yee light


class YeeLight:

    @property
    def location(self):
        self._location

    @location.setter
    def location(self, value):
        self._location = value

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def power(self):
        return self._power

    @power.setter
    def power(self, value):
        self._power = value

    @property
    def bright(self):
        return self._bright

    @bright.setter
    def bright(self, value):
        self._bright = value

    @property
    def hue(self):
        return self._hue

    @hue.setter
    def hue(self, value):
        self._hue = value

    @property
    def rgb(self):
        return self._rgb

    @rgb.setter
    def rgb(self, value):
        self._rgb = value

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, value):
        self._model = value

    @property
    def color_mode(self):
        return self._color_mode

    @color_mode.setter
    def color_mode(self, value):
        self._color_mode = value

    def to_dict(self):
        dict = {}
        for item in self.__dict__.items():
            key, value = item
            dict[key] = value
        return dict

    def __str__(self):
        return '\n'.join(['%s:%s' % item for item in self.__dict__.items()])

#
# ApiClient
#


class YeeLightServer:

    __instance = None

    SUDDEN = 'sudden'

    #  gradual fashion
    SMOOTH = 'smooth'

    # success
    OK = 'HTTP/1.1 200 OK'

    # ssdp search
    SEARCH = 'M-SEARCH * HTTP/1.1'

    # ssdp notify
    NOTIFY = 'NOTIFY * HTTP/1.1'

    # default yeelight addr
    HOST_YEELIGHT = '239.255.255.250'

    PORT_YEELIGHT = 1982

    # enter
    CR = '\r'

    # new line
    LF = '\n'

    # enter + new line
    CRLF = CR + LF

    def __init__(self):
        self._socket_scan = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._yeelights = []

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(Singleton, cls).__new__(
                cls, *args, **kwargs)
        return cls.__instance

    # yeelight command get_prop
    def get_prop(self, addr, arg):
        return self._cmd(addr, 'get_prop', arg.get('prop', []))

    # yeelight command set_scene
    def set_scene(self, addr, arg):
        return self._cmd(addr, 'set_scene', arg.get('class', []))

    # yeelight command power_on
    def power_on(self, addr, arg):
        return self.set_power(addr, 'on', arg.get('effect', self.SMOOTH), arg.get('duration', 500))

    # yeelight command power_off
    def power_off(self, addr, arg):
        return self.set_power(addr, 'off', arg.get('effect', self.SMOOTH), arg.get('duration', 500))

    # yeelight command set_power
    def set_power(self, addr, stat, effect, duration):
        return self._cmd(addr, 'set_power', [stat, effect, duration])

    # yeelight command start_cf
    def start_cf(self, addr, arg):
        return self._cmd(addr, 'start_cf', [arg.get('count', 0), arg.get('action', 0), arg.get('flow_expression', "")])

    # yeelight command stop_cf
    def stop_cf(self, addr, arg):
        return self._cmd(addr, 'stop_cf', [])

    # yeelight command cron_add
    def cron_add(self, addr, arg):
        return self._cmd(addr, 'cron_add', [0, arg.get('value', 0)])

    # yeelight command cron_get
    def cron_get(self, addr, arg):
        return self._cmd(addr, 'cron_get', [0])

    # yeelight command cron_del
    def cron_del(self, addr, arg):
        return self._cmd(addr, 'cron_del', [0])

    # yeelight command set_adjust
    def set_adjust(self, addr, arg):
        return self._cmd(addr, 'set_adjust', [arg.get('action', 'increase'), arg.get('prop', 'bright')])

    # yeelight command set_bright
    def set_bright(self, addr, arg):
        return self._cmd(addr, 'set_bright', [arg.get('brightness', 30),  arg.get('effect', self.SMOOTH), arg.get('duration', 500)])

    # yeelight command set_rgb
    def set_rgb(self, addr, arg):
        return self._cmd(addr, 'set_rgb', [arg.get('rgb', 16777215),  arg.get('effect', self.SMOOTH), arg.get('duration', 500)])

    # yeelight command set_hsv
    def set_hsv(self, addr, arg):
        return self._cmd(addr, 'set_hsv', [arg.get('hue', 0), arg.get('sat', 0), arg.get('effect', self.SMOOTH), arg.get('duration', 500)])

    # yeelight command set_ct_abx
    def set_ct_abx(self, addr, arg):
        return self._cmd(addr, 'set_ct_abx', [arg.get('ct_value', 1700), arg.get('effect', self.SMOOTH), arg.get('duration', 500)])

    # yeelight command set_default
    def set_default(self, addr, arg):
        return self._cmd(addr, 'set_default', [])

    # yeelight command toggle
    def toggle(self, addr, arg):
        return self._cmd(addr, 'toggle', [])

    # yeelight command set_name
    def set_name(self, addr, arg):
        return self._cmd(addr, 'set_name', arg.get('name', 'no name'))

    # yeelight command set_music
    def set_music(self, addr, arg):
        pass

    # yeelight
    def get_yeelights(self):
        return self._yeelights

    # yeelight command search
    def search(self):
        command = self.SEARCH + self.CRLF + \
            'HOST: %s:%s' % (self.HOST_YEELIGHT, self.PORT_YEELIGHT) + self.CRLF + \
            'MAN: "ssdp:discover"' + self.CRLF + \
            'ST: wifi_bulb' + self.CRLF
        self.socket_scan.sendto(
            command, 0, (self.HOST_YEELIGHT, self.PORT_YEELIGHT))

    # control command
    def ccmd(self, location, method, param):
        param = param or {}
        try:
            obj = json.loads(param)
        except Exception, e:
            obj = {}
        try:
            getattr(self, method)(location, obj)
        except Exception, e:
            logging.warning('method(%s) error', e)

    # parse header
    def _parse(self, data):
        message = Message()
        try:
            headers = data.split(self.LF)
            if headers and len(headers) > 0:
                for header in headers:
                    header = header.strip()
                    if header == '':
                        continue
                    kv = header.split(':', 1)
                    if kv and len(kv) > 1:
                        key = kv[0].strip().lower()
                        value = kv[1].strip()
                    else:
                        key = 'status'
                        value = kv[0]
                    setattr(message, key, value)
        except Exception, e:
            logging.error(e)
        return message

    # send command to yeelight
    def _cmd(self, addr, method, data):
        try:
            str = json.dumps(
                {'id': int(time.time()), 'method': method, 'params': data})
            logging.debug('send command [%s]', str)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            host, port = addr.split(':')
            sock.connect((host, int(port)))
            sock.send(str + self.CRLF)
            response = sock.recv(2048)
            sock.close()
            return response
        except Exception, e:
            logging.error(e)

    # discover
    def _discover(self, message):
        try:
            yeelight = YeeLight()
            yeelight.id = message.id
            yeelight.name = message.name
            yeelight.power = message.power
            yeelight.model = message.model
            yeelight.color_mode = message.color_mode
            yeelight.hue = message.hue
            yeelight.rgb = message.rgb
            yeelight.bright = message.bright
            yeelight.location = message.location

            for tmp_yeelight in self._yeelights:
                if yeelight.id == tmp_yeelight.id:
                    self._yeelights.remove(tmp_yeelight)
                    break

            self._yeelights.append(yeelight)

        except Exception, e:
            logging.error('parse yeelight error(%s)', e)

    # empty
    def _empty(self, *args):
        logging.debug('empty: %s', args)

    # _start_scan server
    def _start_scan(self):
        while True:
            try:
                data, addr = self._socket_scan.recvfrom(2048)
                logging.debug('Received:%s from %s',
                              re.compile('[\r|\n]').sub(' ', data), addr)
                self._discover(self._parse(data))
            except socket.error, e:
                pass
            time.sleep(2)
        self._socket_scan.close()

    # passive server
    def _start_passive(self):
        local_ip = socket.gethostbyname(socket.gethostname())
        self._socket_passive = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket_passive.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # bind
        self._socket_passive.bind(('', self.PORT_YEELIGHT))
        # add yeelight mcast
        self._socket_passive.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP,
                                        socket.inet_aton(self.HOST_YEELIGHT) + socket.inet_aton(local_ip))

        while True:
            try:
                data, addr = self._socket_passive.recvfrom(2048)
                logging.debug('Received:%s from %s',
                              re.compile('[\r|\n]').sub(' ', data), addr)
                self._discover(self._parse(data))
            except socket.error, e:
                logging.error(e)

        # leave yeelight mcast
        self._socket_passive.setsockopt(socket.SOL_IP, socket.IP_DROP_MEMBERSHIP,
                                        socket.inet_aton(HOST_YEELIGHT) +
                                        socket.inet_aton(local_ip))
        self._socket_passive.close()

    # start
    def start(self):
        # passive create  thread
        t1 = threading.Thread(target=self._start_passive)
        t1.setDaemon(True)
        t1.start()

        # scan create thread
        t2 = threading.Thread(target=self._start_scan)
        t2.setDaemon(True)
        t2.start()


class YeeLightHttpdServer(BaseHTTPServer.HTTPServer):

    @property
    def yeelight_server(self):
        return self._yeelight_server

    def run(self):
        self._yeelight_server = YeeLightServer()
        self._yeelight_server.start()
        self.serve_forever()


class YeeLightHttpdHandle(BaseHTTPServer.BaseHTTPRequestHandler):

    def yeelight_handle(self, location, method, param=None):
        return self.server.yeelight_server.ccmd(location, method, param)

    def do_CMD(self):
        method = self.headers.get('method', None)
        location = self.headers.get('location', None)
        param = self.headers.get('param', None)
        self.send_response(200)
        self.end_headers()
        if method and location:
            self.yeelight_handle(location, method, param)
        return

    def do_DEVICES(self):
        self.send_response(200)
        self.end_headers()
        result = []
        for yeelight in self.server.yeelight_server.get_yeelights():
            result.append(yeelight.to_dict())
        self.wfile.write(json.dumps(result))
        return

    def do_GET(self):
        return

    def translate_path(self, path):
        # abandon query parameters
        path = path.split('?', 1)[0]
        path = path.split('#', 1)[0]
        # Don't forget explicit trailing slash when normalizing. Issue17324
        trailing_slash = path.rstrip().endswith('/')
        path = posixpath.normpath(urllib.unquote(path))
        words = path.split('/')
        words = filter(None, words)
        path = os.getcwd()
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir):
                continue
            path = os.path.join(path, word)
        if trailing_slash:
            path += '/'
        return path


def run():
    httpd = YeeLightHttpdServer(("", 8866), YeeLightHttpdHandle)
    httpd.run()

if __name__ == '__main__':
    run()
