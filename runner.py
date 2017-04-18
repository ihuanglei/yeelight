#!/usr/bin/env python

import sys
import os
import glob
import getopt
import re
from server.YLAutoHttpdServer import YLAutoHttpdServer
from server.YLAutoHttpdServer import YLAutoHttpdHandle

__author__ = 'Lei Huang'
__version__ = '0.2-dev'
__license__ = 'MIT'


def load_server():
    '''
        load server
        filename end with *Server.py
    '''
    servers = []
    thirdparty_path = sys.path[
        0] + os.path.sep + 'thirdparty' + os.path.sep + '*' + os.path.sep + '*Server.py'
    for server_file in glob.glob(thirdparty_path):
        server_dir = os.path.dirname(server_file)
        server_name = os.path.basename(server_file)[0:-3]
        package = 'thirdparty.%s.%s' % (
            server_dir.split(os.path.sep)[-1], server_name)
        sys.path.append(server_dir)
        try:
            module_meta = __import__(
                package, globals(), locals(), [server_name])
            class_meta = getattr(module_meta, server_name)
            servers.append(class_meta)
        except Exception, e:
            print 'Load Server error %s' % e
    return servers


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
    for server in load_server():
        httpd.add_server(server())
    httpd.run()
