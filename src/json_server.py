import http.server
import socketserver

PORT = 3000
class JSONRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        with open("logs.json", "r") as f:
            self.wfile.write(f.read().encode("utf-8"))

with socketserver.TCPServer(("localhost", PORT), JSONRequestHandler) as httpd:
    print(f"Server started on port {PORT}")
    httpd.serve_forever()
    