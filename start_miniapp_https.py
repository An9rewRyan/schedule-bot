#!/usr/bin/env python3
"""
Скрипт для автоматического запуска Mini App с HTTPS через ngrok
- Запускает ngrok туннели по конфигурации
- Автоматически обновляет CORS настройки в backend
- Обновляет URL в frontend
- Запускает все необходимые сервисы
"""

import subprocess
import time
import requests
import json
import re
import os
import signal
import sys
from pathlib import Path
import logging
from datetime import datetime

class MiniAppStarter:
    def __init__(self):
        self.ngrok_process = None
        self.backend_process = None
        self.frontend_process = None
        self.bot_process = None
        self.frontend_url = None
        self.backend_url = None
        self.logs_dir = Path("logs")
        self.setup_logging()
        
    def setup_logging(self):
        """Настройка логирования для каждого сервиса"""
        # Создаем директорию для логов
        self.logs_dir.mkdir(exist_ok=True)
        
        # Очищаем старые логи
        for log_file in self.logs_dir.glob("*.log"):
            log_file.unlink()
            
        # Настраиваем основной логгер
        self.logger = logging.getLogger('MiniAppStarter')
        self.logger.setLevel(logging.INFO)
        
        # Создаем форматтер
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Обработчик для главного лога
        main_handler = logging.FileHandler(self.logs_dir / "miniapp_starter.log")
        main_handler.setFormatter(formatter)
        self.logger.addHandler(main_handler)
        
        # Обработчик для консоли
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(console_handler)
        
        self.logger.info("Система логирования инициализирована")
        
    def cleanup(self):
        """Остановка всех процессов"""
        self.logger.info("🧹 Остановка всех процессов...")
        
        # Остановка ngrok
        if self.ngrok_process:
            self.logger.info("Остановка ngrok...")
            self.ngrok_process.terminate()
            
        # Остановка других процессов
        for process_name, process in [
            ("backend", self.backend_process),
            ("frontend", self.frontend_process),
            ("bot", self.bot_process)
        ]:
            if process:
                self.logger.info(f"Остановка {process_name}...")
                process.terminate()
                
        # Убиваем все процессы ngrok
        subprocess.run(["pkill", "-f", "ngrok"], capture_output=True)
        
        # Убиваем процессы на портах
        for port in [8000, 3000, 4040]:
            result = subprocess.run(["lsof", "-ti", f":{port}"], capture_output=True, text=True)
            if result.stdout.strip():
                pids = result.stdout.strip().split('\n')
                for pid in pids:
                    subprocess.run(["kill", "-9", pid], capture_output=True)
                    
        self.logger.info("Все процессы остановлены")
                    
    def signal_handler(self, signum, frame):
        """Обработчик сигналов для корректного завершения"""
        self.logger.info(f"\n🛑 Получен сигнал {signum}, завершаем работу...")
        self.cleanup()
        sys.exit(0)
        
    def start_ngrok(self):
        """Запуск ngrok по конфигурации"""
        self.logger.info("🚀 Запуск ngrok туннелей...")
        
        # Остановка существующих процессов ngrok
        subprocess.run(["pkill", "-f", "ngrok"], capture_output=True)
        time.sleep(2)
        
        # Запуск ngrok с конфигурацией и логированием
        ngrok_log_file = self.logs_dir / "ngrok.log"
        self.ngrok_process = subprocess.Popen(
            ["ngrok", "start", "--config", "ngrok.yml", "--all"],
            stdout=open(ngrok_log_file, 'w'),
            stderr=subprocess.STDOUT
        )
        
        # Ждем запуска ngrok
        self.logger.info("⏳ Ждем запуска ngrok...")
        time.sleep(5)
        
        # Получаем URL туннелей
        return self.get_ngrok_urls()
        
    def get_ngrok_urls(self):
        """Получение URL туннелей из ngrok API"""
        try:
            response = requests.get("http://localhost:4040/api/tunnels")
            data = response.json()
            
            urls = {}
            for tunnel in data.get('tunnels', []):
                name = tunnel.get('name', '')
                public_url = tunnel.get('public_url', '')
                if public_url:
                    urls[name] = public_url
                    
            if 'frontend' in urls and 'backend' in urls:
                self.frontend_url = urls['frontend']
                self.backend_url = urls['backend']
                
                self.logger.info(f"✅ Frontend URL: {self.frontend_url}")
                self.logger.info(f"✅ Backend URL: {self.backend_url}")
                return True
            else:
                self.logger.error("❌ Не удалось получить URL туннелей")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Ошибка получения ngrok URLs: {e}")
            return False
            
    def update_cors_settings(self):
        """Обновление CORS настроек в backend"""
        self.logger.info("🔧 Обновление CORS настроек...")
        
        backend_main_path = Path("backend/src/main.py")
        if not backend_main_path.exists():
            self.logger.error("❌ Файл backend/src/main.py не найден")
            return False
            
        # Читаем содержимое файла
        with open(backend_main_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Находим секцию origins
        origins_pattern = r'origins = \[(.*?)\]'
        match = re.search(origins_pattern, content, re.DOTALL)
        
        if not match:
            self.logger.error("❌ Не найдена секция origins в main.py")
            return False
            
        # Создаем новый список origins
        new_origins = [
            '"http://localhost:3000"',
            '"http://127.0.0.1:3000"',
            f'"{self.frontend_url}"',
            f'"{self.backend_url}"'
        ]
        
        new_origins_str = f"origins = [\n    " + ",\n    ".join(new_origins) + "\n]"
        
        # Заменяем в содержимом
        new_content = re.sub(origins_pattern, new_origins_str, content, flags=re.DOTALL)
        
        # Записываем обновленное содержимое
        with open(backend_main_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
        self.logger.info("✅ CORS настройки обновлены")
        return True
        
    def update_frontend_config(self):
        """Обновление URL в frontend"""
        self.logger.info("🔧 Обновление frontend конфигурации...")
        
        frontend_app_path = Path("frontend/app.js")
        if not frontend_app_path.exists():
            self.logger.error("❌ Файл frontend/app.js не найден")
            return False
            
        # Читаем содержимое файла
        with open(frontend_app_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Обновляем URL в функции getBaseURL
        pattern = r"return 'https://[^']+\.ngrok-free\.app/api';"
        replacement = f"return '{self.backend_url}/api';"
        
        new_content = re.sub(pattern, replacement, content)
        
        # Записываем обновленное содержимое
        with open(frontend_app_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
        self.logger.info("✅ Frontend конфигурация обновлена")
        return True
        
    def update_telegram_bot_config(self):
        """Обновление URL в Telegram боте"""
        self.logger.info("🔧 Обновление Telegram bot конфигурации...")
        
        bot_start_path = Path("tg_bot/handlers/start.py")
        if not bot_start_path.exists():
            self.logger.error("❌ Файл tg_bot/handlers/start.py не найден")
            return False
            
        # Читаем содержимое файла
        with open(bot_start_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Обновляем MINI_APP_URL
        pattern = r'MINI_APP_URL = "https://[^"]+\.ngrok-free\.app"'
        replacement = f'MINI_APP_URL = "{self.frontend_url}"'
        
        new_content = re.sub(pattern, replacement, content)
        
        # Записываем обновленное содержимое
        with open(bot_start_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
        self.logger.info("✅ Telegram bot конфигурация обновлена")
        return True
        
    def start_backend(self):
        """Запуск backend сервера"""
        self.logger.info("🚀 Запуск backend сервера...")
        
        # Логирование backend в отдельный файл
        backend_log_file = self.logs_dir / "backend.log"
        self.backend_process = subprocess.Popen(
            ["python", "-m", "src.main"],
            cwd="backend",
            stdout=open(backend_log_file, 'w'),
            stderr=subprocess.STDOUT
        )
        
        # Ждем запуска backend
        time.sleep(3)
        
        # Проверяем, что backend запустился
        try:
            response = requests.get("http://localhost:8000/health", timeout=5)
            if response.status_code == 200:
                self.logger.info("✅ Backend сервер запущен")
                self.logger.info(f"📄 Логи backend: {backend_log_file}")
                return True
        except Exception as e:
            self.logger.error(f"❌ Ошибка запуска backend: {e}")
            
        self.logger.error("❌ Не удалось запустить backend сервер")
        return False
        
    def start_frontend(self):
        """Запуск frontend сервера"""
        self.logger.info("🚀 Запуск frontend сервера...")
        
        # Логирование frontend в отдельный файл
        frontend_log_file = self.logs_dir / "frontend.log"
        self.frontend_process = subprocess.Popen(
            ["python", "no_cache_server.py"],
            cwd="frontend",
            stdout=open(frontend_log_file, 'w'),
            stderr=subprocess.STDOUT
        )
        
        # Ждем запуска frontend
        time.sleep(2)
        
        # Проверяем, что frontend запустился
        try:
            response = requests.get("http://localhost:3000", timeout=5)
            if response.status_code == 200:
                self.logger.info("✅ Frontend сервер запущен")
                self.logger.info(f"📄 Логи frontend: {frontend_log_file}")
                return True
        except Exception as e:
            self.logger.error(f"❌ Ошибка запуска frontend: {e}")
            
        self.logger.error("❌ Не удалось запустить frontend сервер")
        return False
        
    def start_telegram_bot(self):
        """Запуск Telegram бота"""
        self.logger.info("🚀 Запуск Telegram бота...")
        
        # Логирование bot в отдельный файл
        bot_log_file = self.logs_dir / "telegram_bot.log"
        self.bot_process = subprocess.Popen(
            ["python", "main.py"],
            cwd="tg_bot",
            stdout=open(bot_log_file, 'w'),
            stderr=subprocess.STDOUT
        )
        
        time.sleep(2)
        self.logger.info("✅ Telegram бот запущен")
        self.logger.info(f"📄 Логи telegram bot: {bot_log_file}")
        return True
        
    def run(self):
        """Главная функция запуска"""
        # Регистрируем обработчик сигналов
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        try:
            self.logger.info("🎯 Запуск Mini App с HTTPS поддержкой")
            self.logger.info("=" * 50)
            
            # 1. Запуск ngrok
            if not self.start_ngrok():
                self.logger.error("❌ Не удалось запустить ngrok")
                return False
                
            # 2. Обновление конфигураций
            if not self.update_cors_settings():
                return False
                
            if not self.update_frontend_config():
                return False
                
            if not self.update_telegram_bot_config():
                return False

            # 2.5 Очистка таймслотов
            self.logger.info("🧹 Очистка всех бронирований и таймслотов...")
            subprocess.run(["python", "backend/src/utilities/scripts/clear_timeslots.py"])
            self.logger.info("✅ Таймслоты очищены")
                
            # 3. Запуск сервисов
            if not self.start_backend():
                return False
                
            if not self.start_frontend():
                return False
                
            if not self.start_telegram_bot():
                return False
                
            self.logger.info("\n" + "=" * 50)
            self.logger.info("🎉 Все сервисы запущены успешно!")
            self.logger.info(f"🌐 Frontend: {self.frontend_url}")
            self.logger.info(f"🔧 Backend: {self.backend_url}")
            self.logger.info(f"💻 Локальный frontend: http://localhost:3000")
            self.logger.info(f"🔗 Локальный backend: http://localhost:8000")
            self.logger.info("\n📱 Используйте эти URL для настройки Mini App в Telegram:")
            self.logger.info(f"   Mini App URL: {self.frontend_url}")
            self.logger.info(f"\n📁 Логи сервисов сохранены в директории: {self.logs_dir}")
            self.logger.info("   - miniapp_starter.log - основной лог")
            self.logger.info("   - ngrok.log - логи ngrok")
            self.logger.info("   - backend.log - логи backend сервера")
            self.logger.info("   - frontend.log - логи frontend сервера")
            self.logger.info("   - telegram_bot.log - логи Telegram бота")
            self.logger.info("\n🛑 Нажмите Ctrl+C для остановки всех сервисов")
            self.logger.info("=" * 50)
            
            # Ожидание завершения
            while True:
                time.sleep(1)
                
        except KeyboardInterrupt:
            self.signal_handler(signal.SIGINT, None)
        except Exception as e:
            self.logger.error(f"❌ Ошибка: {e}")
            self.cleanup()
            return False

if __name__ == "__main__":
    starter = MiniAppStarter()
    starter.run() 