from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# our mock database
data = [
    {"name": "Samuel", "track": "Backend Developer"},
    {"name": "Yemi", "track": "AI Engineer"},
    {"name": "John", "track": "Data Analyst"}
]

class BasicAPI(BaseHTTPRequestHandler):
    # helper function to send JSON responses
    def send_data(self, payload, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode())

    # GET - read all data
    def do_GET(self):
        self.send_data({
            "message": "All data fetched successfully",
            "data": data
        })

    # POST - add new record
    def do_POST(self):
        content_size = int(self.headers.get("Content-Length", 0))
        raw_data = self.rfile.read(content_size)
        post_data = json.loads(raw_data)
        data.append(post_data)

        self.send_data({
            "message": "Data added successfully",
            "data": post_data
        }, status=201)

    # PUT - replace or add
    def do_PUT(self):
        content_size = int(self.headers.get("Content-Length", 0))
        raw_data = self.rfile.read(content_size)
        put_data = json.loads(raw_data)
        update_name = put_data.get("name")
        updated = False

        for entry in data:
            if entry["name"].lower() == update_name.lower():
                entry.update(put_data)
                updated = True
                break

        if not updated:
            data.append(put_data)

        self.send_data({
            "message": "Data updated successfully",
            "all_data": data
        }, status=200)

    # PATCH - partial update
    def do_PATCH(self):
        content_size = int(self.headers.get("Content-Length", 0))
        raw_data = self.rfile.read(content_size)
        patch_data = json.loads(raw_data)
        update_name = patch_data.get("name")
        updated = False

        for entry in data:
            if entry["name"].lower() == update_name.lower():
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
        })

    # DELETE - remove a record
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
    print("Unified BasicAPI running on port 5000...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
