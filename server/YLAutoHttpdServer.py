import logging
import json
import BaseHTTPServer
import SocketServer


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')


class YLBaseServer(object):

    def name(self):
        pass

    def handle(self, args):
        pass

    def startup(self, *args):
        pass

    def stop(self, *args):
        pass


class YLAutoHttpdServer(SocketServer.ThreadingMixIn, BaseHTTPServer.HTTPServer):

    _yl_servers = []

    def add_server(self, *server):
        self._yl_servers = list(server)

    def handle(self, args):
        logging.debug('handle [%s]', args)
        for yl_server in self._yl_servers:
            if yl_server.name() == args.get('class', ''):
                logging.debug('find server [%s]', yl_server.name())
                return yl_server.handle(args)
        return {}

    def run(self):
        for yl_server in self._yl_servers:
            logging.info('Server [%s] Startup', yl_server.name())
            yl_server.startup()
        self.serve_forever()


class YLAutoHttpdHandle(BaseHTTPServer.BaseHTTPRequestHandler):

    html_index = None

    def do_CMD(self):
        args = {'class': self.headers.get('Class', None),
                'method': self.headers.get('Method', None),
                'location': self.headers.get('Location', None),
                'param': self.headers.get('Param', None)
                }
        result = self.server.handle(args)
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
            self.html_index = open('h5/yl_index.html').read()

        self.wfile.write(self.html_index)
        return
