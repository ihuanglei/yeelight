#!/usr/bin/env python

import sys
import getopt
from server.YLAutoHttpdServer import YLAutoHttpdServer
from server.YLAutoHttpdServer import YLAutoHttpdHandle
from thirdparty.YeelightServer import YeelightServer

__author__ = 'Lei Huang'
__version__ = '0.1-dev'
__license__ = 'MIT'


def usage():
    print 'Usage:'
    print '  h|help: print this message'
    print '  d|debug: print debug message'
    print '  v|version: print version'
    sys.exit(1)


def version():
    print __version__
    sys.exit(1)

if __name__ == '__main__':

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hdv")
    except getopt.GetoptError:
        usage()

    for op, value in opts:
        # if op == '-d':
        #     debug = True
        if op == '-h':
            usage()
        if op == '-v':
            version()

    httpd = YLAutoHttpdServer(("", 8866), YLAutoHttpdHandle)
    httpd.add_server(YeelightServer())
    httpd.run()
