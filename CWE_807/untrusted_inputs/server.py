from http.server import *
import cgi
import json
import base64
from urllib.parse import urlparse, parse_qs


class AuthNServerHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm="Test')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        key = self.server.get_auth_key()

        if self.headers.get('Authorization') == None:
            self.do_AUTHHEAD()
            response = {
                'success': False,
                'error': 'Auth Header not received'
            }
            self.wfile.write(bytes(json.dumps(response), 'utf-8'))
        elif self.headers.get('Authorization') == 'Basic ' + str(key):
            self.send_response(200)
            self.send_header('Set-Cookie', 'auth_level=None')
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            getvars = self._parse_GET()
            response = {
                'path': self.path,
                'get_vars': str(getvars)
            }
            if self.path == '/admin':
                cookies = self.parse_cookies(self.headers['Cookie'])
                if cookies['auth_level'] == 'admin':
                #todo
                    self.wfile.write(bytes('<html><head></head><body><p>welcome admin</p></body></html>', 'utf-8'))
                else:
                    self.wfile.write(bytes('<html><head></head><body><p>You need to be an admin to view this page</p></body></html>', 'utf-8'))
            elif self.path == '/somepath':
                #todo
                pass
        
            self.wfile.write(bytes(json.dumps(response), 'utf-8'))
        else:
            self.do_AUTHHEAD()
            response = {
                'success': False,
                'error': 'Invalid credentials'
            }

            self.wfile.write(bytes(json.dumps(response), 'utf-8'))

    def do_POST(self):
        key = self.server.get_auth_key()
        if self.headers.get('Authorization') == None:
            self.do_AUTHHEAD()
            response = {
                'success': False,
                'error': "No auth header received"
            }
            self.wfile.write(bytes(json.dumps(response), 'utf-8'))
        elif self.headers.get('Authorization') == 'Basic ' + str(key):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            postvars = self._parse_POST()
            getvars = self._parse_GET()

            response = {
                'path': self.path,
                'get_Vars': str(getvars),
                'post_vars': str(postvars)
            }
            if self.path == '/':
                #todo
                pass
            elif self.path == '/somepath':
                #todo
                pass
            self.wfile.write(bytes(json.dumps(response), 'utf-8'))

        response = {
            'path': self.path,
            'get_vars': str(getvars),
            'post_vars': str(postvars)
        }

        self.wfile.write(bytes(json.dumps(response), 'utf-8'))
    
    def _parse_POST(self):
        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        if ctype == 'multipart/form-data':
            postvars = cgi.parse_multipart(self.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers.getheader('content-length'))
            postvars = cgi.parse_qs(
                self.rfile.read(length), keep_blank_values=1)
        else:
            postvars = {}

        return postvars

    def _parse_GET(self):
        getvars = parse_qs(urlparse(self.path).query)
        return getvars
    def parse_cookies(self, cookie_list):
        if cookie_list:
            return dict(((c.split("=")) for c in cookie_list.split(";")))
        else:
            return {}

class PyHTTPServer(HTTPServer):
    key = ''
    
    def __init__(self, address, handlerClass=AuthNServerHandler):
        super().__init__(address, handlerClass)
    def set_auth(self, username, password):
        self.key = base64.b64encode(bytes(f'{username}:{password}', 'utf-8')).decode('ascii')
    def get_auth_key(self):
        return self.key

host = 'localhost'
PORT = 8080
handler = AuthNServerHandler

if __name__ == '__main__':
    server = PyHTTPServer((host, PORT), handler)
    with open('auth.json') as f:
        auth = json.load(f)
        uname = str(auth['username'])
        pword = str(auth['password'])
    server.set_auth(uname,pword)
    print(f'running at http://{host}:{PORT}')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
    print("server killed")