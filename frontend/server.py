#!/usr/bin/env python3
"""
Простой веб-сервер для разработки Telegram Mini App
"""

import http.server
import socketserver
import os
import sys
import mimetypes
from urllib.parse import urlparse

class CORSHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Добавляем правильные MIME типы
        mimetypes.add_type('application/javascript', '.js')
        mimetypes.add_type('text/css', '.css')
        mimetypes.add_type('text/html', '.html')
        super().__init__(*args, **kwargs)

    def end_headers(self):
        # Добавляем CORS заголовки
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        # Добавляем заголовки для отключения кэша
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()
    
    def do_GET(self):
        # Логируем запрос
        self.log_message("GET request for %s", self.path)

        # Убираем параметры версии из пути
        parsed_path = urlparse(self.path)
        clean_path = parsed_path.path

        # Если запрашивается корневой путь, отдаем index.html
        if clean_path == '/' or clean_path == '':
            clean_path = '/index.html'
            self.path = '/index.html'

        # Проверяем существование файла
        file_path = self.translate_path(clean_path)
        if os.path.isfile(file_path):
            return super().do_GET()
        else:
            self.log_message("File not found: %s", file_path)
            self.send_error(404, "File not found")

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

