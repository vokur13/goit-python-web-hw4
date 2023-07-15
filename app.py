import logging
import mimetypes
import pathlib
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler

from socket_app import run_client


class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        match pr_url.path:
            case '/':
                self.send_html_file('templates/index.html')
            case '/message':
                self.send_html_file('templates/message.html')
            case _:
                match pathlib.Path().joinpath(pr_url.path[1:]).exists():
                    case True:
                        self.send_static()
                self.nothing_matched_function()

    def do_POST(self):
        data = self.rfile.read(int(self.headers['Content-Length']))
        self.send_response(302)
        self.send_header('Location', '/')
        run_client(data)
        self.end_headers()

    def nothing_matched_function(self):
        self.send_html_file('templates/error.html', 404)

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())

    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", 'text/plain')
        self.end_headers()
        with open(f'.{self.path}', 'rb') as file:
            self.wfile.write(file.read())


def run(server_class=HTTPServer, handler_class=HttpHandler):
    server_address = ('', 3000)
    http = server_class(server_address, handler_class)
    logging.debug(f'http: {server_address=}')
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()
