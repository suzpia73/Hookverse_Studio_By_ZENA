import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

SAVE_DIR = os.path.abspath("assets/images/IMF2화")
os.makedirs(SAVE_DIR, exist_ok=True)

class FlowImageHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.end_headers()

    def do_POST(self):
        query = parse_qs(urlparse(self.path).query)
        filename = query.get('filename', ['downloaded_image.png'])[0]
        
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        save_path = os.path.join(SAVE_DIR, filename)
        with open(save_path, 'wb') as f:
            f.write(post_data)
            
        print(f"[SUCCESS] Saved {filename} ({len(post_data)} bytes) to {save_path}", flush=True)
        
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(b'{"status":"ok"}')

    def log_message(self, format, *args):
        # Suppress noisy logs
        sys.stderr.write("%s - - [%s] %s\n" % (self.address_string(), self.log_date_time_string(), format%args))

if __name__ == '__main__':
    port = 8999
    server = HTTPServer(('127.0.0.1', port), FlowImageHandler)
    print(f"Flow Image Receiver Server running at http://127.0.0.1:{port}", flush=True)
    server.serve_forever()
