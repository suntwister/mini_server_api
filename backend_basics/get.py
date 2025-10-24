from http.server import BaseHTTPRequestHandler, HTTPServer
import json

data = {"name": "Samuel", "track": "Backend Developer"}

class BasicAPI(BaseHTTPRequestHandler):
    def send_data(self, payload, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode())
        self.wfile.flush()
    
    def do_GET(self):
        print("GET request received")
        self.send_data(data)

def run(server_class=HTTPServer, handler_class=BasicAPI):
    server_address = ('', 5000)
    httpd = server_class(server_address, handler_class)
    print("server running on port 5000...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()