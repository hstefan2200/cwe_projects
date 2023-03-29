from http.server import *
import cgi
import json
import base64
from urllib.parse import urlparse, parse_qs


class AuthNServerHandler(BaseHTTPRequestHandler):
    login_attempts = 0
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_AUTHHEAD(self):
        if self.login_attempts <5:
            self.send_response(401)
            self.send_header('WWW-Authenticate', 'Basic realm="Test')
            self.send_header('Content-type', 'text/html')
            self.end_headers()
        else:
            response = {
            'success': False,
            'error': f'Too many attempts[{self.login_attempts}]'
            }
            self.send_response(403)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(json.dumps(response), 'utf-8'))
        
    def do_GET(self):
        key = self.server.get_auth_key()
        if self.headers.get('Authorization') == 'Basic ' + str(key) and self.login_attempts < 5:
            self.login_attempts = 0
        elif self.headers.get('Authorization') == 'Basic ' + str(key) and self.login_attempts >= 5:
            self.login_attempts = 1000


        if self.headers.get('Authorization') == None:
            self.do_AUTHHEAD()
            response = {
                    'success': False,
                    'error': 'Auth Header not received'
                }
            self.send_response(403)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(json.dumps(response), 'utf-8'))


        elif self.headers.get('Authorization') == 'Basic ' + str(key):
            c_val = None
            self.send_response(200)
            self.send_header('Set-Cookie', f'auth_level={c_val}')
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            getvars = self._parse_GET()
            response = {
                'path': self.path,
                'get_vars': str(getvars)
            }
            if self.path == '/admin':
                cookies = self.parse_cookies(self.headers['Cookie'])
                if cookies['auth_level'] == 'admin' and c_val == 'admin':
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
                    'error': 'Auth Header not received'
                }
            self.send_response(403)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(json.dumps(response), 'utf-8'))
        print(f'Number of login attempts: {self.login_attempts}')

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
        AuthNServerHandler.login_attempts += 1
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