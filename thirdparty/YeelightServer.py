import time
import re
import json
import socket
import threading
import base64
import logging
import urllib
import sys
import errno
from server.YLAutoHttpdServer import YLBaseServer


reload(sys)
sys.setdefaultencoding('utf8')


class Message:

    def __str__(self):
        return ' '.join(['%s:%s' % item for item in self.__dict__.items()])


class YeelightException(Exception):
    pass


class Yeelight(object):

    @property
    def location(self):
        return self._location

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
        self._name = base64.b64decode(value)

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
    def sat(self):
        return self._sat

    @sat.setter
    def sat(self, value):
        self._sat = value

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
            # first char _
            dict[key[1:]] = value
        return dict

    def __str__(self):
        return '\n'.join(['%s:%s' % item for item in self.__dict__.items()])


class YeelightClient(object):

    def __init__(self, addr):
        self._addr = addr
        self._host, self._port = addr.split(':')
        self._connected = False
        self._thread = None
        self._sock = None

    def run(self):
        try:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._sock.connect((self._host, int(self._port)))
            self._thread = threading.Thread(target=self._run)
            self._thread.setDaemon(True)
            self._thread.start()
            self._connected = True
        except socket.error, e:
            raise YeelightException('%s(%s)' % (self._addr, e))

    def _run(self):
        while self._connected:
            try:
                response = self._sock.recv(2048)
                if not response:
                    break
                self._sock.settimeout(None)
                logging.debug('<< Yeelight Light Received: %s', response)
                obj = json.loads(response)
                method = obj.get('method', None)
                if method == 'props':
                    params = obj.get('params', None)
                    if params:
                        # self._light.name = params.get('name', self._light.name)
                        self._light.power = params.get(
                            'power', self._light.power)
                        # self._light.model = params.get('model', self._light.model)
                        self._light.color_mode = params.get(
                            'color_mode', self._light.color_mode)
                        self._light.rgb = params.get('rgb', self._light.rgb)
                        self._light.hue = params.get('hue', self._light.hue)
                        self._light.sat = params.get('sat', self._light.sat)
                        self._light.bright = params.get(
                            'bright', self._light.bright)
            except socket.error, e:
                err = e.args[0]
                if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                    break
                logging.error('-- Yeelight (%s)', e)

    def modify_light(data):
        pass

    def send(self, data):
        '''send command to Yeelight'''
        if self._connected:
            try:
                self._sock.send(data)
            except socket.error, e:
                self._connected = False
                logging.error('-- Yeelight (%s)', e)

    def close(self):
        self._connected = False
        self._sock.close()

    @property
    def addr(self):
        '''address host:port'''
        return self._addr

    @property
    def is_connected(self):
        '''client is connected'''
        return self._connected

    @property
    def light(self):
        return self._light

    @light.setter
    def light(self, value):
        self._light = value


class YeelightServer(YLBaseServer):

    SUDDEN = 'sudden'

    #  gradual fashion
    SMOOTH = 'smooth'

    # success
    OK = 'HTTP/1.1 200 OK'

    # ssdp search
    SEARCH = 'M-SEARCH * HTTP/1.1'

    # ssdp notify
    NOTIFY = 'NOTIFY * HTTP/1.1'

    # default Light addr
    HOST_LIGHT = '239.255.255.250'

    PORT_LIGHT = 1982

    # enter
    CR = '\r'

    # new line
    LF = '\n'

    # enter + new line
    CRLF = CR + LF

    def __init__(self):
        self._socket_scan = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._light_clients = []

    # Light prop
    # def get_props(self, addr):
    #     try:
    #         props = {'prop': ['name', 'power', 'hue', 'sat', 'rgb', 'bright']}
    #         ret = self.get_prop(addr, props)
    #         if ret:
    #             result = json.loads(ret).get('result', [])
    #             if len(result) > 0:
    #                 for light in self._lights:
    #                     if light.location == addr:
    #                         light.name = result[0]
    #                         light.power = result[1]
    #                         light.hue = result[2]
    #                         light.sat = result[3]
    #                         light.rgb = result[4]
    #                         light.bright = result[5]
    #                         break
    #         return ret
    #     except Exception, e:
    #         logging.error(e)

    # Light command get_prop
    def get_prop(self, addr, arg):
        return self._cmd(addr, 'get_prop', arg.get('prop', []))

    # Light command set_scene
    def set_scene(self, addr, arg):
        return self._cmd(addr, 'set_scene', arg.get('class', []))

    # Light command power_on
    def power_on(self, addr, arg):
        return self.set_power(addr, 'on', arg.get('effect', self.SMOOTH), arg.get('duration', 500))

    # Light command power_off
    def power_off(self, addr, arg):
        return self.set_power(addr, 'off', arg.get('effect', self.SMOOTH), arg.get('duration', 500))

    # Light command set_power
    def set_power(self, addr, stat, effect, duration):
        return self._cmd(addr, 'set_power', [stat, effect, duration])

    # Light command start_cf
    def start_cf(self, addr, arg):
        return self._cmd(addr, 'start_cf', [arg.get('count', 0), arg.get('action', 0), arg.get('flow_expression', "")])

    # Light command stop_cf
    def stop_cf(self, addr, arg):
        return self._cmd(addr, 'stop_cf', [])

    # Light command cron_add
    def cron_add(self, addr, arg):
        return self._cmd(addr, 'cron_add', [0, arg.get('value', 0)])

    # Light command cron_get
    def cron_get(self, addr, arg):
        return self._cmd(addr, 'cron_get', [0])

    # Light command cron_del
    def cron_del(self, addr, arg):
        return self._cmd(addr, 'cron_del', [0])

    # Light command set_adjust
    def set_adjust(self, addr, arg):
        return self._cmd(addr, 'set_adjust', [arg.get('action', 'increase'), arg.get('prop', 'bright')])

    # Light command set_bright
    def set_bright(self, addr, arg):
        return self._cmd(addr, 'set_bright', [arg.get('brightness', 30),  arg.get('effect', self.SMOOTH), arg.get('duration', 500)])

    # Light command set_rgb
    def set_rgb(self, addr, arg):
        return self._cmd(addr, 'set_rgb', [arg.get('rgb', 16777215),  arg.get('effect', self.SMOOTH), arg.get('duration', 500)])

    # Light command set_hsv
    def set_hsv(self, addr, arg):
        return self._cmd(addr, 'set_hsv', [arg.get('hue', 0), arg.get('sat', 0), arg.get('effect', self.SMOOTH), arg.get('duration', 500)])

    # Light command set_ct_abx
    def set_ct_abx(self, addr, arg):
        return self._cmd(addr, 'set_ct_abx', [arg.get('ct_value', 1700), arg.get('effect', self.SMOOTH), arg.get('duration', 500)])

    # Light command set_default
    def set_default(self, addr, arg):
        return self._cmd(addr, 'set_default', [])

    # Light command toggle
    def toggle(self, addr, arg):
        return self._cmd(addr, 'toggle', [])

    # Light command set_name
    def set_name(self, addr, arg):
        return self._cmd(addr, 'set_name', [base64.b64encode(arg.get('name', 'noname'))])

    # Light command set_music
    def set_music(self, addr, arg):
        pass

    def get_devices(self, *args):
        pass

    # Light command search
    def search(self, *args):
        command = self.SEARCH + self.CRLF + \
            'HOST: %s:%s' % (self.HOST_LIGHT, self.PORT_LIGHT) + self.CRLF + \
            'MAN: "ssdp:discover"' + self.CRLF + \
            'ST: wifi_bulb' + self.CRLF
        logging.debug('>> Yeelight Search %s',
                      re.compile('[\r|\n]').sub(' ', command))
        self._socket_scan.sendto(
            command, 0, (self.HOST_LIGHT, self.PORT_LIGHT))
        return 'ok'

    # control command
    def ccmd(self, location, method, param):
        param = param or {}
        try:
            obj = json.loads(urllib.unquote(param))
        except Exception, e:
            obj = {}
        try:
            return getattr(self, method)(location, obj)
        except socket.error, e:
            logging.error('-- Yeelight connect(%s)', e)
        except Exception, e:
            logging.error('-- Yeelight method(%s)', e)

    # get connect light client
    def _get_light_client(self, addr, is_new=False):
        ret_client = None
        lost_client = None
        for client in self._light_clients:
            if client.addr == addr:
                if client.is_connected:
                    ret_client = client
                else:
                    lost_client = client
                break

        if lost_client:
            '''remove lost connection'''
            self._light_clients.remove(lost_client)

        if not ret_client and not is_new:
            raise YeelightException('%s not found!' % addr)

        if is_new and not ret_client:
            ret_client = YeelightClient(addr)
            self._light_clients.append(ret_client)

        return ret_client

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
            logging.error('-- Yeelight (%s)', e)
        return message

    # send command to Light
    def _cmd(self, addr, method, data):
        str = json.dumps(
            {'id': int(time.time()), 'method': method, 'params': data})
        logging.debug('>> Yeelight Send command %s [%s]', addr, str)
        try:
            light_client = self._get_light_client(addr)
            light_client.send(str + self.CRLF)
            return 'ok'
        except Exception, e:
            logging.error('-- Yeelight (%s)', e)
            return 'error'

    # discover
    def _discover(self, message):
        try:
            if not hasattr(message, 'location'):
                logging.debug(
                    '-- Yeelight Not Yeelight message, drop it (%s)', message)
                return

            match = re.match(
                r'yeelight://[0-9]{1,3}(\.[0-9]{1,3}){3}:([0-9]*)', message.location)
            if match == None:
                return
            addr = message.location.split('//')[1]
            light = Yeelight()
            light.id = message.id
            light.name = message.name
            light.power = message.power
            light.location = addr
            light.model = message.model
            light.color_mode = message.color_mode
            light.rgb = message.rgb
            light.hue = message.hue
            light.sat = message.sat
            light.bright = message.bright
        except Exception, e:
            logging.error('-- Yeelight Parse light error(%s)', e)

        try:
            client = self._get_light_client(addr, True)
            client.light = light
            client.run()
        except YeelightException, e:
            logging.error('-- Yeelight Build client error(%s)', e)

            # empty
    def _empty(self, *args):
        logging.debug('-- Yeelight Empty: %s', args)

    def get_local_ip(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(('8.8.8.8', 80))
        (addr, port) = sock.getsockname()
        sock.close()
        return addr

    # _start_scan server
    def _start_scan(self):
        while True:
            try:
                data, addr = self._socket_scan.recvfrom(2048)
                logging.debug('<< Yeelight Scanner Received:%s from %s',
                              re.compile('[\r|\n]').sub(' ', data), addr)
                self._discover(self._parse(data))
            except socket.error, e:
                pass
        self._socket_scan.close()

    # passive server
    def _start_passive(self):
        local_ip = self.get_local_ip()
        self._socket_passive = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket_passive.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # bind
        self._socket_passive.bind(('', self.PORT_LIGHT))
        # add Light mcast
        self._socket_passive.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP,
                                        socket.inet_aton(self.HOST_LIGHT) + socket.inet_aton(local_ip))

        while True:
            try:
                data, addr = self._socket_passive.recvfrom(2048)
                logging.debug('<< Yeelight Passive Received:%s from %s',
                              re.compile('[\r|\n]').sub(' ', data), addr)
                self._discover(self._parse(data))
            except socket.error, e:
                logging.error('-- Yeelight (%s)', e)

        # leave Light mcast
        self._socket_passive.setsockopt(socket.SOL_IP, socket.IP_DROP_MEMBERSHIP,
                                        socket.inet_aton(HOST_LIGHT) +
                                        socket.inet_aton(local_ip))
        self._socket_passive.close()

    def startup(self):
        # passive create thread
        t1 = threading.Thread(target=self._start_passive)
        t1.setDaemon(True)
        t1.start()

        # scan create thread
        t2 = threading.Thread(target=self._start_scan)
        t2.setDaemon(True)
        t2.start()

        self.search()

    def handle(self, args):
        method = args.get('method')
        ret = self.ccmd(args.get('location'), method, args.get('param'))
        if method == 'get_devices':
            result = []
            for client in self._light_clients:
                result.append(client.light.to_dict())
            return result
        return ret

    def name(self):
        return 'Yeelight'
