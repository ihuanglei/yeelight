#!/usr/bin/env python

import sys
import getopt
from server.YLAutoHttpdServer import YLAutoHttpdServer
from server.YLAutoHttpdServer import YLAutoHttpdHandle
from thirdparty.YeelightServer import YeeLightServer


def usage():
    print 'runner.py -h -d'
    sys.exit(1)

if __name__ == '__main__':

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hd")
    except getopt.GetoptError:
        usage()

    for op, value in opts:
        if op == '-d':
            debug = True
        if op == '-h':
            usage()

    httpd = YLAutoHttpdServer(("", 8866), YLAutoHttpdHandle)
    httpd.add_server(YeeLightServer())
    httpd.run()
