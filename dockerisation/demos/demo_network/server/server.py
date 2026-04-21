from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from datetime import datetime

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        response = {
            'message': 'Hello from server!',
            'timestamp': datetime.now().isoformat(),
            'server': 'Python HTTP Server'
        }

        self.wfile.write(json.dumps(response, indent=2).encode())

    def log_message(self, format, *args):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {format % args}")

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 8000), SimpleHandler)
    print('Server running on http://0.0.0.0:8000')
    server.serve_forever()