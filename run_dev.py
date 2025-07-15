#!/usr/bin/env python3
"""
Простой скрипт для запуска сервисов Mini App с видимыми логами
Использование:
    python run_dev.py          # Интерактивное меню
    python run_dev.py backend  # Только backend
    python run_dev.py bot      # Только telegram bot  
    python run_dev.py frontend # Только frontend
    python run_dev.py ngrok    # Только ngrok
    python run_dev.py local    # Backend + Frontend + Bot (без ngrok)
    python run_dev.py all      # Все сервисы с ngrok и обновлением конфигурации
"""

import subprocess
import sys
import time
import signal
import os
import threading
import queue
import logging
import re
import requests
from pathlib import Path

# Цвета для логов
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'

def colored_print(text, color, prefix=""):
    """Печать цветного текста с префиксом"""
    print(f"{color}{prefix}{text}{Colors.RESET}")

def print_header(title):
    """Печать красивого заголовка"""
    print("\n" + "="*60)
    colored_print(f" {title} ", Colors.BOLD + Colors.CYAN)
    print("="*60)

class ServiceRunner:
    def __init__(self):
        self.processes = []
        self.threads = []
        self.running = True
        self.ngrok_urls = {}
        self.backend_url = ""
        self.frontend_url = ""
        
        # Настройка логирования
        self.setup_logging()
        
        # Установка обработчика сигналов для корректного завершения
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def setup_logging(self):
        """Настройка логирования"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def signal_handler(self, signum, frame):
        """Обработчик сигналов для корректного завершения"""
        colored_print("\n🛑 Получен сигнал завершения. Останавливаем сервисы...", Colors.YELLOW)
        self.stop_all()
        sys.exit(0)
    
    def stop_all(self):
        """Остановка всех запущенных процессов"""
        self.running = False
        colored_print("🧹 Останавливаем все процессы...", Colors.YELLOW)
        
        for proc in self.processes:
            try:
                proc.terminate()
                proc.wait(timeout=5)
            except:
                try:
                    proc.kill()
                except:
                    pass
        
        for thread in self.threads:
            thread.join(timeout=1)
    
    def read_output(self, proc, service_name, color):
        """Чтение вывода процесса в отдельном потоке"""
        while self.running and proc.poll() is None:
            try:
                line = proc.stdout.readline()
                if line:
                    line = line.decode('utf-8', errors='ignore').rstrip()
                    if line:  # Не печатаем пустые строки
                        colored_print(line, color, f"[{service_name}] ")
            except:
                break
    
    def run_service(self, command, service_name, color, cwd=None):
        """Запуск сервиса с выводом логов"""
        try:
            colored_print(f"🚀 Запуск {service_name}...", Colors.GREEN)
            colored_print(f"Команда: {' '.join(command)}", Colors.BLUE)
            
            proc = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                cwd=cwd,
                bufsize=1,
                universal_newlines=False
            )
            
            self.processes.append(proc)
            
            # Запуск потока для чтения вывода
            thread = threading.Thread(
                target=self.read_output, 
                args=(proc, service_name, color),
                daemon=True
            )
            thread.start()
            self.threads.append(thread)
            
            return proc
            
        except Exception as e:
            colored_print(f"❌ Ошибка запуска {service_name}: {e}", Colors.RED)
            return None
    
    def wait_for_startup(self, seconds=3):
        """Ожидание запуска сервисов"""
        colored_print(f"⏳ Ожидание запуска сервисов ({seconds} сек)...", Colors.YELLOW)
        time.sleep(seconds)
    
    def get_ngrok_urls(self, max_retries=30, delay=2):
        """Получение URLs от ngrok API"""
        for attempt in range(max_retries):
            try:
                response = requests.get("http://localhost:4040/api/tunnels", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    urls = {}
                    
                    for tunnel in data.get('tunnels', []):
                        name = tunnel.get('name', '')
                        public_url = tunnel.get('public_url', '')
                        config = tunnel.get('config', {})
                        addr = config.get('addr', '')
                        
                        # Определяем тип туннеля по порту или имени
                        if ('frontend' in name or addr.endswith(':3000')) and public_url:
                            urls['frontend'] = public_url
                            self.frontend_url = public_url
                        elif ('backend' in name or addr.endswith(':8000')) and public_url:
                            urls['backend'] = public_url
                            self.backend_url = public_url
                    
                    if urls:
                        self.ngrok_urls = urls
                        colored_print("✅ ngrok URLs получены:", Colors.GREEN)
                        for name, url in urls.items():
                            colored_print(f"  {name}: {url}", Colors.CYAN)
                        return urls
                        
            except Exception as e:
                if attempt < max_retries - 1:
                    colored_print(f"⏳ Ожидание ngrok... (попытка {attempt + 1}/{max_retries})", Colors.YELLOW)
                    time.sleep(delay)
                else:
                    colored_print(f"❌ Не удалось получить ngrok URLs: {e}", Colors.RED)
        
        return {}
    
    def update_cors_settings(self, backend_url):
        """Обновление CORS настроек в backend"""
        colored_print("🔧 Обновление CORS настроек...", Colors.YELLOW)
        
        main_py_path = Path("backend/src/main.py")
        if not main_py_path.exists():
            colored_print("❌ Файл backend/src/main.py не найден", Colors.RED)
            return False
            
        try:
            content = main_py_path.read_text(encoding='utf-8')
            
            # Паттерн для поиска origins
            pattern = r'origins = \[(.*?)\]'
            
            # Новые origins с ngrok URL (для CORS нужен frontend URL)
            origins_list = [
                '"http://localhost:3000"',
                '"http://127.0.0.1:3000"'
            ]
            
            # Добавляем frontend URL если есть
            if self.frontend_url:
                origins_list.append(f'"{self.frontend_url}"')
            
            origins_joined = ',\n    '.join(origins_list)
            new_origins = f'''[
    {origins_joined}
]'''
            
            # Замена
            new_content = re.sub(pattern, f'origins = {new_origins}', content, flags=re.DOTALL)
            main_py_path.write_text(new_content, encoding='utf-8')
            
            colored_print(f"✅ CORS обновлен с frontend URL: {self.frontend_url}", Colors.GREEN)
            return True
            
        except Exception as e:
            colored_print(f"❌ Ошибка обновления CORS: {e}", Colors.RED)
            return False
    
    def update_frontend_config(self, backend_url):
        """Обновление конфигурации frontend"""
        colored_print("🎨 Обновление конфигурации frontend...", Colors.YELLOW)
        
        config_path = Path("frontend/config.js")
        if not config_path.exists():
            colored_print("❌ Файл frontend/config.js не найден", Colors.RED)
            return False
            
        try:
            content = config_path.read_text(encoding='utf-8')
            
            # Замена API_BASE_URL
            pattern = r"API_BASE_URL: ['\"].*?['\"]"
            replacement = f"API_BASE_URL: '{backend_url}/api'"
            
            new_content = re.sub(pattern, replacement, content)
            config_path.write_text(new_content, encoding='utf-8')
            
            colored_print(f"✅ Frontend config обновлен с URL: {backend_url}/api", Colors.GREEN)
            return True
            
        except Exception as e:
            colored_print(f"❌ Ошибка обновления frontend config: {e}", Colors.RED)
            return False
    
    def update_telegram_bot_config(self, frontend_url):
        """Обновление конфигурации Telegram бота"""
        colored_print("🤖 Обновление Telegram bot конфигурации...", Colors.YELLOW)
        
        start_handler_path = Path("tg_bot/handlers/start.py")
        if not start_handler_path.exists():
            colored_print("❌ Файл tg_bot/handlers/start.py не найден", Colors.RED)
            return False
            
        try:
            content = start_handler_path.read_text(encoding='utf-8')
            
            # Замена MINI_APP_URL (правильное название переменной)
            pattern = r'MINI_APP_URL = ["\'].*?["\']'
            replacement = f'MINI_APP_URL = "{frontend_url}"'
            
            new_content = re.sub(pattern, replacement, content)
            start_handler_path.write_text(new_content, encoding='utf-8')
            
            colored_print(f"✅ Bot config обновлен с URL: {frontend_url}", Colors.GREEN)
            return True
            
        except Exception as e:
            colored_print(f"❌ Ошибка обновления bot config: {e}", Colors.RED)
            return False
    
    def update_bot_api_config(self, backend_url):
        """Обновление конфигурации API в боте"""
        colored_print("🔧 Обновление API конфигурации бота...", Colors.YELLOW)
        
        files_to_update = [
            "tg_bot/config.py",
            "tg_bot/api/users.py", 
            "tg_bot/api/bookings.py",
            "tg_bot/api/timeslots.py"
        ]
        
        success_count = 0
        
        for file_path in files_to_update:
            path = Path(file_path)
            if not path.exists():
                colored_print(f"⚠️ Файл {file_path} не найден", Colors.YELLOW)
                continue
                
            try:
                content = path.read_text(encoding='utf-8')
                
                # Обновляем BASE_URL и API_BASE_URL
                patterns = [
                    (r'BASE_URL = ["\'].*?["\']', f'BASE_URL = "{backend_url}"'),
                    (r'API_BASE_URL = ["\'].*?["\']', f'API_BASE_URL = "{backend_url}/api"')
                ]
                
                for pattern, replacement in patterns:
                    if re.search(pattern, content):
                        content = re.sub(pattern, replacement, content)
                        
                path.write_text(content, encoding='utf-8')
                success_count += 1
                
            except Exception as e:
                colored_print(f"❌ Ошибка обновления {file_path}: {e}", Colors.RED)
        
        if success_count > 0:
            colored_print(f"✅ API конфигурация бота обновлена ({success_count} файлов)", Colors.GREEN)
            return True
        else:
            colored_print("❌ Не удалось обновить API конфигурацию бота", Colors.RED)
            return False
    
    def update_ngrok_config(self):
        """Принудительное обновление конфигурации ngrok URLs"""
        colored_print("🔄 Принудительное обновление конфигурации ngrok URLs...", Colors.CYAN)
        
        urls = self.get_ngrok_urls()
        if not urls:
            colored_print("❌ Не удалось получить ngrok URLs. Убедитесь, что ngrok запущен.", Colors.RED)
            return False
        
        colored_print("📋 Текущие ngrok URLs:", Colors.CYAN)
        colored_print(f"  Frontend: {self.frontend_url}", Colors.GREEN)
        colored_print(f"  Backend: {self.backend_url}", Colors.GREEN)
        
        success = True
        
        if self.frontend_url:
            success &= self.update_telegram_bot_config(self.frontend_url)
        
        if self.backend_url:
            success &= self.update_bot_api_config(self.backend_url)
            success &= self.update_frontend_config(self.backend_url)
            if self.frontend_url:
                success &= self.update_cors_settings(self.backend_url)
        
        if success:
            colored_print("✅ Все конфигурации успешно обновлены!", Colors.GREEN)
            colored_print("📱 Для настройки Mini App в Telegram:", Colors.YELLOW)
            colored_print(f"   Mini App URL: {self.frontend_url}", Colors.CYAN)
            colored_print("🔄 Не забудьте перезапустить Telegram бота для применения изменений!", Colors.YELLOW)
        else:
            colored_print("⚠️ Некоторые конфигурации не удалось обновить", Colors.RED)
        
        return success
    
    def run_backend(self):
        """Запуск backend API"""
        return self.run_service(
            ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"],
            "Backend API",
            Colors.GREEN,
            cwd="backend"
        )
    
    def run_frontend(self):
        """Запуск frontend сервера"""
        return self.run_service(
            ["python", "server.py"],
            "Frontend",
            Colors.BLUE,
            cwd="frontend"
        )
    
    def run_telegram_bot(self):
        """Запуск Telegram бота"""
        return self.run_service(
            ["python", "main.py"],
            "Telegram Bot",
            Colors.MAGENTA,
            cwd="tg_bot"
        )
    
    def run_ngrok(self):
        """Запуск ngrok"""
        return self.run_service(
            ["ngrok", "start", "--config", "ngrok.yml", "--all"],
            "ngrok",
            Colors.CYAN
        )
    
    def show_menu(self):
        """Показать интерактивное меню"""
        print_header("🚀 Mini App Development Server")
        print("Выберите сервисы для запуска:")
        print("1. 🚀 Backend API (FastAPI)")
        print("2. 🎨 Frontend Server")  
        print("3. 🤖 Telegram Bot")
        print("4. 🌐 ngrok (HTTPS tunnels)")
        print("5. 🔥 Backend + Bot")
        print("6. 🌍 Frontend + ngrok (с обновлением конфигурации)")
        print("7. 🎯 ВСЕ СЕРВИСЫ (с ngrok и обновлением конфигурации)")
        print("8. 💻 Backend + Frontend + Bot (локально без ngrok)")
        print("9. 🔄 Обновить конфигурацию ngrok URLs")
        print("0. ❌ Выход")
        print("="*60)
        
        try:
            choice = input("Выберите опцию (0-9): ").strip()
            return choice
        except KeyboardInterrupt:
            return "0"
    
    def run_by_choice(self, choice):
        """Запуск сервисов по выбору пользователя"""
        services = []
        
        if choice == "1":
            services = [("backend", self.run_backend)]
        elif choice == "2":
            services = [("frontend", self.run_frontend)]
        elif choice == "3":
            services = [("bot", self.run_telegram_bot)]
        elif choice == "4":
            services = [("ngrok", self.run_ngrok)]
        elif choice == "5":
            services = [("backend", self.run_backend), ("bot", self.run_telegram_bot)]
        elif choice == "6":
            services = [("frontend", self.run_frontend), ("ngrok", self.run_ngrok)]
        elif choice == "7":
            services = [
                ("backend", self.run_backend),
                ("frontend", self.run_frontend), 
                ("bot", self.run_telegram_bot),
                ("ngrok", self.run_ngrok)
            ]
        elif choice == "8":
            services = [
                ("backend", self.run_backend),
                ("frontend", self.run_frontend), 
                ("bot", self.run_telegram_bot)
            ]
        elif choice == "9":
            # Обновление конфигурации ngrok URLs
            self.update_ngrok_config()
            return True
        else:
            return False
        
        return self.run_services(services)
    
    def run_services(self, services):
        """Запуск списка сервисов"""
        print_header(f"Запуск {len(services)} сервисов")
        
        has_ngrok = any("ngrok" in service_name for service_name, _ in services)
        has_backend = any("backend" in service_name for service_name, _ in services)
        has_frontend = any("frontend" in service_name for service_name, _ in services)
        has_bot = any("bot" in service_name for service_name, _ in services)
        
        # Если есть ngrok, сначала запускаем его и получаем URLs
        if has_ngrok:
            colored_print("🌐 Запуск ngrok...", Colors.CYAN)
            for service_name, service_func in services:
                if "ngrok" in service_name:
                    proc = service_func()
                    if proc is None:
                        colored_print(f"❌ Не удалось запустить {service_name}", Colors.RED)
                        return False
                    break
            
            # Ожидание запуска ngrok и получение URLs
            time.sleep(3)
            colored_print("🌐 Получение ngrok URLs...", Colors.CYAN)
            urls = self.get_ngrok_urls()
            
            if urls:
                colored_print("📋 Текущие ngrok URLs:", Colors.CYAN)
                colored_print(f"  Frontend: {self.frontend_url}", Colors.GREEN)
                colored_print(f"  Backend: {self.backend_url}", Colors.GREEN)
                
                # Обновление конфигураций ДО запуска сервисов
                if has_backend and self.frontend_url:
                    colored_print("🔧 Обновление CORS перед запуском backend...", Colors.YELLOW)
                    self.update_cors_settings(self.backend_url)
                
                if has_frontend and self.backend_url:
                    self.update_frontend_config(self.backend_url)
                
                if has_bot:
                    if self.frontend_url:
                        self.update_telegram_bot_config(self.frontend_url)
                    if self.backend_url:
                        self.update_bot_api_config(self.backend_url)
            else:
                colored_print("❌ Не удалось получить ngrok URLs", Colors.RED)
        
        # Запуск остальных сервисов (кроме уже запущенного ngrok)
        for service_name, service_func in services:
            if "ngrok" not in service_name:  # ngrok уже запущен
                proc = service_func()
                if proc is None:
                    colored_print(f"❌ Не удалось запустить {service_name}", Colors.RED)
                    return False
                time.sleep(1)  # Небольшая задержка между запусками
        
        self.wait_for_startup()
        
        # Финальное сообщение об успешном запуске
        if has_ngrok and self.frontend_url:
            colored_print("✅ Все конфигурации обновлены", Colors.GREEN)
            colored_print("📱 Для настройки Mini App в Telegram:", Colors.YELLOW)
            colored_print(f"   Mini App URL: {self.frontend_url}", Colors.CYAN)
        
        colored_print("✅ Все сервисы запущены!", Colors.GREEN)
        colored_print("📝 Логи отображаются ниже. Нажмите Ctrl+C для остановки.", Colors.YELLOW)
        print("="*60 + "\n")
        
        try:
            # Ожидание завершения всех процессов
            while self.running and any(proc.poll() is None for proc in self.processes):
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        finally:
            self.stop_all()
        
        return True

def main():
    runner = ServiceRunner()
    
    # Проверка аргументов командной строки
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        
        services_map = {
            "backend": [("backend", runner.run_backend)],
            "frontend": [("frontend", runner.run_frontend)],
            "bot": [("bot", runner.run_telegram_bot)],
            "ngrok": [("ngrok", runner.run_ngrok)],
            "local": [
                ("backend", runner.run_backend),
                ("frontend", runner.run_frontend),
                ("bot", runner.run_telegram_bot)
            ],
            "all": [
                ("backend", runner.run_backend),
                ("frontend", runner.run_frontend),
                ("bot", runner.run_telegram_bot),
                ("ngrok", runner.run_ngrok)
            ]
        }
        
        if arg in services_map:
            runner.run_services(services_map[arg])
        else:
            colored_print(f"❌ Неизвестный аргумент: {arg}", Colors.RED)
            colored_print("Доступные: backend, frontend, bot, ngrok, local, all", Colors.YELLOW)
            sys.exit(1)
    else:
        # Интерактивное меню
        while True:
            choice = runner.show_menu()
            
            if choice == "0":
                colored_print("👋 До свидания!", Colors.CYAN)
                break
            
            if runner.run_by_choice(choice):
                break
            else:
                colored_print("❌ Неверный выбор, попробуйте снова", Colors.RED)

if __name__ == "__main__":
    main() 