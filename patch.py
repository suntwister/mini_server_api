from http.server import BaseHTTPRequestHandler, HTTPServer
import json

data = [
    {"name": "Samuel", "track": "Backend Engineer"},
    {"name": "Yemi", "track":"AI Engineer"}
]

class BasicAPI(BaseHTTPRequestHandler):
    def send_data(self, payload, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode())

    def do_PATCH(self):
        content_size = int(self.headers.get("Content-Length",0))
        raw_data = self.rfile.read(content_size)
        patch_data = json.loads(raw_data)

        update_name = patch_data.get("name")
        updated = False

        for entry in data:
            if entry["name"] ==update_name:
                entry.update(patch_data)
                updated = True
                break
        
        if updated:
            message = "Data partially updated"
        else:
            message = "Record not found"

        self.send_data({
            "message": message,
            "all_data": data
        }, status=200)

def run(server_class=HTTPServer, handler_class=BasicAPI):
    server_address = ('', 5000)
    httpd = server_class(server_address, handler_class)
    print("PATCH server running on port 5000...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()