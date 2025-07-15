#!/usr/bin/env python3
import http.server
import socketserver
from datetime import datetime

class NoCacheHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def log_message(self, format, *args):
        print(f"[{datetime.now().strftime('%d/%b/%Y %H:%M:%S')}] {format % args}")

if __name__ == "__main__":
    PORT = 3000
    with socketserver.TCPServer(("", PORT), NoCacheHTTPRequestHandler) as httpd:
        print(f"🎨 Frontend server запущен на http://localhost:{PORT}")
        print("📝 Кэширование отключено для разработки")
        print("🔄 Нажмите Ctrl+C для остановки")
        httpd.serve_forever() 