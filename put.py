from http.server import BaseHTTPRequestHandler, HTTPServer
import json

data = [
    {"name": "Samuel", "track": "Backend Engineer"},
    {"name": "Yemi", "track": "AI Engineer"}
]

class BasicAPI(BaseHTTPRequestHandler):
    def send_data(self, payload, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode())

    def do_PUT(self):
        content_size = int(self.headers.get("Content-Length", 0))
        raw_data = self.rfile.read(content_size)
        put_data = json.loads(raw_data)

        update_name = put_data.get("name")
        updated = False

        for entry in data:
            if entry["name"] == update_name:
                entry.update(put_data)
                updated = True

        if not updated:
            data.append(put_data)

        self.send_data({
            "message": "Data updated successfully",
            "all_data": data
        }, status=200)

def run(server_class=HTTPServer, handler_class=BasicAPI):
    server_address = ('', 5000)
    httpd = server_class(server_address, handler_class)
    print("PUT server running on port 5000...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()