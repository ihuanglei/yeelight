import time
import re
import json
import socket
import sys
import threading
import logging


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')

# common message


class Message:

    def __str__(self):
        return '\n'.join(['%s:%s' % item for item in self.__dict__.items()])

# yee light


class YeeLight:

    @property
    def host(self):
        self._host

    @host.setter
    def host(self, value):
        self._host = value

    @property
    def port(self):
        self._port

    @port.setter
    def port(self, value):
        self._port = value

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

    def __str__(self):
        return '\n'.join(['%s:%s' % item for item in self.__dict__.items()])

#
# ApiClient
#


class YeeLightApi:

    SUDDEN = 'sudden'

    #  gradual fashion
    SMOOTH = 'smooth'

    # success
    OK = 'HTTP/1.1 200 OK'

    # ssdp search
    SEARCH = 'M-SEARCH * HTTP/1.1'

    # ssdp notify
    NOTIFY = 'NOTIFY * HTTP/1.1'

    # command custom
    COMMAND = 'CMD * HTTP/1.1'

    # default yeelight addr
    HOST_YEELIGHT = '239.255.255.250'

    PORT_YEELIGHT = 1982

    # default command addr
    HOST_CMD = '239.255.255.251'

    # enter
    CR = '\r'

    # new line
    LF = '\n'

    # enter + new line
    CRLF = CR + LF

    # yeelight command get_prop
    @staticmethod
    def get_prop(addr, arg):
        return YeeLightApi._cmd(addr, 'get_prop', arg.get('prop', []))

    # yeelight command set_scene
    @staticmethod
    def set_scene(addr, arg):
        return YeeLightApi._cmd(addr, 'set_scene', arg.get('class', []))

    # yeelight command power_on
    @staticmethod
    def power_on(addr, arg):
        return YeeLightApi.set_power(addr, 'on', arg.get('effect', YeeLightApi.SMOOTH), arg.get('duration', 500))

    # yeelight command power_off
    @staticmethod
    def power_off(addr, arg):
        return YeeLightApi.set_power(addr, 'off', arg.get('effect', YeeLightApi.SMOOTH), arg.get('duration', 500))

    # yeelight command set_power
    @staticmethod
    def set_power(addr, stat, effect, duration):
        return YeeLightApi._cmd(addr, 'set_power', [stat, effect, duration])

    # yeelight command start_cf
    @staticmethod
    def start_cf(addr, arg):
        return YeeLightApi._cmd(addr, 'start_cf', [arg.get('count', 0), arg.get('action', 0), arg.get('flow_expression', "")])

    # yeelight command stop_cf
    @staticmethod
    def stop_cf(addr, arg):
        return YeeLightApi._cmd(addr, 'stop_cf', [])

    # yeelight command cron_add
    @staticmethod
    def cron_add(addr, arg):
        return YeeLightApi._cmd(addr, 'cron_add', [0, arg.get('value', 0)])

    # yeelight command cron_get
    @staticmethod
    def cron_get(addr, arg):
        return YeeLightApi._cmd(addr, 'cron_get', [0])

    # yeelight command cron_del
    @staticmethod
    def cron_del(addr, arg):
        return YeeLightApi._cmd(addr, 'cron_del', [0])

    # yeelight command set_adjust
    @staticmethod
    def set_adjust(addr, arg):
        return YeeLightApi._cmd(addr, 'set_adjust', [arg.get('action', 'increase'), arg.get('prop', 'bright')])

    # yeelight command set_bright
    @staticmethod
    def set_bright(addr, arg):
        return YeeLightApi._cmd(addr, 'set_bright', [arg.get('brightness', 30),  arg.get('effect', YeeLightApi.SMOOTH), arg.get('duration', 500)])

    # yeelight command set_rgb
    @staticmethod
    def set_rgb(addr, arg):
        return YeeLightApi._cmd(addr, 'set_rgb', [arg.get('rgb', 16777215),  arg.get('effect', YeeLightApi.SMOOTH), arg.get('duration', 500)])

    # yeelight command set_hsv
    @staticmethod
    def set_hsv(addr, arg):
        return YeeLightApi._cmd(addr, 'set_hsv', [arg.get('hue', 0), arg.get('sat', 0), arg.get('effect', YeeLightApi.SMOOTH), arg.get('duration', 500)])

    # yeelight command set_ct_abx
    @staticmethod
    def set_ct_abx(addr, arg):
        return YeeLightApi._cmd(addr, 'set_ct_abx', [arg.get('ct_value', 1700), arg.get('effect', YeeLightApi.SMOOTH), arg.get('duration', 500)])

    # yeelight command set_default
    @staticmethod
    def set_default(addr, arg):
        return YeeLightApi._cmd(addr, 'set_default', [])

    # yeelight command toggle
    @staticmethod
    def toggle(addr, arg):
        return YeeLightApi._cmd(addr, 'toggle', [])

    # yeelight command set_name
    @staticmethod
    def set_name(addr, arg):
        return YeeLightApi._cmd(addr, 'set_name', arg.get('name', 'no name'))

    # yeelight command set_music
    @staticmethod
    def set_music(addr, arg):
        pass

    # parse header
    @staticmethod
    def _parse(data):
        message = Message()
        headers = data.split(YeeLightApi.LF)
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
        return message

    # send command to yeelight
    @staticmethod
    def _cmd(addr, method, data):
        try:
            str = json.dumps(
                {'id': int(time.time()), 'method': method, 'params': data})
            logging.debug(str)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(6)
            strs = addr.split(':')
            host = strs[0]
            port = int(strs[1])
            sock.connect((host, port))
            sock.send(str + YeeLightApi.CRLF)
            response = sock.recv(1024)
            sock.close()
            return response
        except Exception, e:
            logging.error(e)

    # discover
    @staticmethod
    def _discover(message, callback):
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
            addr = message.location.split('//')[1].split(':')
            yeelight.host = addr[0]
            yeelight.port = addr[1]
            callback(yeelight)
        except Exception, e:
            logging.error('parse yeelight error(%s)', e)

    # control command
    @staticmethod
    def _ccmd(command, *args):
        try:
            method = command.method
            addr = command.location
            obj = json.loads(command.param)
            getattr(YeeLightApi, method)(addr, obj)
        except ValueError, e:
            logging.warning('params(%s) error', e)
        except AttributeError, e:
            logging.warning('method(%s) error', e)
        except Exception, e:
            logging.error(e)

    # empty
    @staticmethod
    def _empty(*args):
        logging.debug('empty: %s', args)

    # yeelight command search
    @staticmethod
    def _search(callback=None):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        command = YeeLightApi.SEARCH + YeeLightApi.CRLF + \
            'HOST: %s:%s' % (YeeLightApi.HOST_YEELIGHT, YeeLightApi.PORT_YEELIGHT) + YeeLightApi.CRLF + \
            'MAN: "ssdp:discover"' + YeeLightApi.CRLF + \
            'ST: wifi_bulb' + YeeLightApi.CRLF
        sock.sendto(command, 0, (YeeLightApi.HOST_YEELIGHT,
                                 YeeLightApi.PORT_YEELIGHT))
        data, addr = sock.recvfrom(1024)
        sock.close()
        logging.debug('Received:%s from %s',
                      re.compile('[\r|\n]').sub(' ', data), addr)
        message = YeeLightApi._parse(data)
        yeelight = YeeLightApi._discover(message)
        callback(yeelight)

    # udp server
    @staticmethod
    def _start_server(callback):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        local_ip = socket.gethostbyname(socket.gethostname())
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # bind
        sock.bind(('', YeeLightApi.PORT_YEELIGHT))
        # add yeelight mcast
        sock.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP,
                        socket.inet_aton(YeeLightApi.HOST_YEELIGHT) + socket.inet_aton(local_ip))

        # add cmd mcast
        sock.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP,
                        socket.inet_aton(YeeLightApi.HOST_CMD) + socket.inet_aton(local_ip))
        c = {
            YeeLightApi.COMMAND: YeeLightApi._ccmd,
            YeeLightApi.NOTIFY: YeeLightApi._discover
        }
        while True:
            data, addr = sock.recvfrom(1024)
            logging.debug('Received:%s from %s',
                          re.compile('[\r|\n]').sub(' ', data), addr)
            message = YeeLightApi._parse(data)
            fun = c.get(message.status, YeeLightApi._empty)
            fun(message, callback)

        # leave yeelight mcast
        sock.setsockopt(socket.SOL_IP, socket.IP_DROP_MEMBERSHIP,
                        socket.inet_aton(YeeLightApi.HOST_YEELIGHT) +
                        socket.inet_aton(local_ip))

        # leave cmd mcast
        sock.setsockopt(socket.SOL_IP, socket.IP_DROP_MEMBERSHIP,
                        socket.inet_aton(YeeLightApi.HOST_CMD) +
                        socket.inet_aton(local_ip))
        sock.close()

    # start
    @staticmethod
    def start(callback=None):
        # create thread
        t = threading.Thread(
            target=YeeLightApi._start_server, args=(callback,))
        t.setDaemon(True)
        t.start()
        t.join()

    # search
    def search(callback=None):
        # create thread
        t = threading.Thread(target=YeeLightApi._search, args=(callback,))
        t.setDaemon(True)
        t.start()
