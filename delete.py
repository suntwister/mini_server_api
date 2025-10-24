from http.server import BaseHTTPRequestHandler, HTTPServer
import json

data = [
    {"name": "Samuel", "track":"Backend Engineer"},
    {"name": "Yemi", "track":"AI Engineer"},
    {"name": "John", "track": "Data Analyst"}
]

class BasicAPI(BaseHTTPRequestHandler):
    def send_data(self, payload, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode())

    def do_DELETE(self):
        content_size = int(self.headers.get("Content-Length", 0))
        raw_data = self.rfile.read(content_size)
        delete_data = json.loads(raw_data)

        delete_name = delete_data.get("name")
        deleted_item = None

        for entry in data:
            if entry["name"].lower() == delete_name.lower():
                deleted_item = entry
                data.remove(entry)
                break
        
        if deleted_item:
            message = f"{delete_name} deleted successfully"
            status = 200
        else:
            message = f"Record '{delete_name}' not found"
            status = 404

        self.send_data({
            "message": message,
            "remaining_data": data
        }, status=status)

def run(server_class=HTTPServer, handler_class=BasicAPI):
    server_address = ('', 5000)
    httpd = server_class(server_address, handler_class)
    print("DELETE server running on port 5000...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()