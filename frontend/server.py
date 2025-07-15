#!/usr/bin/env python3
"""
Простой веб-сервер для разработки Telegram Mini App
"""

import http.server
import socketserver
import os
import sys
from urllib.parse import urlparse

class CORSHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Добавляем CORS заголовки
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        super().end_headers()
    
    def do_OPTIONS(self):
        # Обработка preflight запросов
        self.send_response(200)
        self.end_headers()
    
    def log_message(self, format, *args):
        # Улучшенное логирование
        sys.stderr.write("[%s] %s\n" % (self.log_date_time_string(), format % args))

def main():
    # Порт для сервера
    PORT = 3000
    
    # Переходим в директорию с файлами
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Создаем сервер
    with socketserver.TCPServer(("", PORT), CORSHTTPRequestHandler) as httpd:
        print(f"🚀 Сервер запущен на http://localhost:{PORT}")
        print(f"📁 Обслуживаемая директория: {os.getcwd()}")
        print(f"🌐 Mini App доступен по адресу: http://localhost:{PORT}/index.html")
        print("⏹️  Для остановки сервера нажмите Ctrl+C")
        print("-" * 50)
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Сервер остановлен")
            httpd.shutdown()

if __name__ == "__main__":
    main() 