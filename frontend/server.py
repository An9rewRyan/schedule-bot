#!/usr/bin/env python3
"""
Простой веб-сервер для разработки Telegram Mini App
"""

import http.server
import socketserver
import os
import sys
import mimetypes
import json
from urllib.parse import urlparse

try:
    import requests
except ImportError:
    print("❌ Модуль 'requests' не найден. Установите его командой: pip install requests")
    sys.exit(1)

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

        # Обработка API endpoint для получения конфигурации backend
        if clean_path == '/api/config':
            return self.handle_config_request()

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

    def handle_config_request(self):
        """Обрабатывает запрос конфигурации backend URL"""
        try:
            self.log_message("Config request: fetching ngrok tunnels...")
            
            # Запрашиваем ngrok API локально
            response = requests.get('http://localhost:4040/api/tunnels', timeout=5)
            response.raise_for_status()
            
            data = response.json()
            tunnels = data.get('tunnels', [])
            
            # Ищем туннель для backend (localhost:8000)
            backend_tunnel = None
            for tunnel in tunnels:
                if tunnel.get('config', {}).get('addr') == 'http://localhost:8000':
                    backend_tunnel = tunnel
                    break
            
            if backend_tunnel:
                backend_url = f"{backend_tunnel['public_url']}/api"
                config_data = {
                    "backend_url": backend_url,
                    "status": "success"
                }
                self.log_message("Config success: backend URL = %s", backend_url)
            else:
                config_data = {
                    "error": "Backend tunnel not found. Make sure ngrok is proxying localhost:8000",
                    "status": "error"
                }
                self.log_message("Config error: backend tunnel not found")
            
            # Отправляем JSON ответ
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            json_response = json.dumps(config_data, ensure_ascii=False)
            self.wfile.write(json_response.encode('utf-8'))
            
        except requests.exceptions.RequestException as e:
            # Ошибка запроса к ngrok
            self.log_message("Config error: ngrok API unavailable - %s", str(e))
            error_data = {
                "error": f"Ngrok API недоступен: {str(e)}",
                "status": "error"
            }
            
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            json_response = json.dumps(error_data, ensure_ascii=False)
            self.wfile.write(json_response.encode('utf-8'))
            
        except Exception as e:
            # Общая ошибка
            self.log_message("Config error: unexpected error - %s", str(e))
            error_data = {
                "error": f"Неожиданная ошибка: {str(e)}",
                "status": "error"
            }
            
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            json_response = json.dumps(error_data, ensure_ascii=False)
            self.wfile.write(json_response.encode('utf-8'))

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

