import logging
import json
import sys
import os
import BaseHTTPServer
import SocketServer

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')


class YLAutoHttpdServer(SocketServer.ThreadingMixIn, BaseHTTPServer.HTTPServer):

    _yl_servers = []

    def add_server(self, server):
        self._yl_servers.append(server)

    def handle(self, args):
        logging.debug('YLAutoHttpdServer Handle [%s]', args)
        for yl_server in self._yl_servers:
            if yl_server.name() == args.get('class', ''):
                logging.debug(
                    'YLAutoHttpdServer Find server [%s]', yl_server.name())
                return yl_server.handle(args)
        return {}

    def run(self):
        try:
            logging.info(
                'Welcome to YuanLaiWangluo Auto Controller')
            for yl_server in self._yl_servers:
                logging.info(
                    'Server [%s] Startup', yl_server.name())
                yl_server.startup()
            self.serve_forever()
        except KeyboardInterrupt:
            logging.info('Bye Bye')


class YLAutoHttpdHandle(BaseHTTPServer.BaseHTTPRequestHandler):

    html_index = None

    def _parse_request(self, headers):
        return {
            'class': headers.get('Class', None),
            'method': headers.get('Method', None),
            'location': headers.get('Location', None),
            'param': headers.get('Param', None)
        }

    def do_CMD(self):
        result = self.server.handle(self._parse_request(self.headers))
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(result))
        return

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()

        if not self.html_index:
            self.html_index = open(
                sys.path[0] + os.path.sep + 'h5' + os.path.sep + 'yl_index.html').read()

        self.wfile.write(self.html_index)
        return
