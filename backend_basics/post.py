from http.server import BaseHTTPRequestHandler, HTTPServer
import json

data = []

class BasicAPI(BaseHTTPRequestHandler):
    def send_data(self, payload, status=201):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode())

    def do_POST(self):
        content_size = int(self.headers.get("Content-Length", 0))

        raw_data = self.rfile.read(content_size)

        post_data = json.loads(raw_data)

        data.append(post_data)

        self.send_data({
            "message": "Data received successfully",
            "stored_data": post_data
        })

def run(server_class=HTTPServer, handler_class=BasicAPI):
    server_address = ('', 5000)
    httpd = server_class(server_address, handler_class)
    print("POST server running on port 5000...")
    httpd.serve_forever()

if  __name__ == "__main__":
    run()