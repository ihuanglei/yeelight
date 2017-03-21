#-*- coding: utf-8 -*-

from yeelight import *


def notify(yeelight):
    print '\r\n====='
    print yeelight
    print '\r\n====='

YeeLightApi.start(notify)
