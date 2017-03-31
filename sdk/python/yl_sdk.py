import urllib
import urllib2


class YLSdk(object):

    __instance = None

    # 单例
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(Singleton, cls).__new__(
                cls, *args, **kwargs)
        return cls.__instance

    def __init__(self, server_url):
        self._server_url = server_url

    # 发送命令
    def _cmd(self, addr, location, method, params):
        response = urllib2.urlopen(self._server_url, timeout=3)
        return response

    # 查询在线设别
    def get_device():
        pass

    # 设置名称
    def set_name():
        '{"name": "' + encodeURIComponent(name) + '"}'
        return self._cmd(addr)

    # 开灯
    def power_on():
        pass

    # 关灯
    def power_off():
        pass

    # 设置亮度
    def set_bright():
        pass
