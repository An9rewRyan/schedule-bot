#!/usr/bin/env python3
"""
Скрипт для запуска Telegram Mini App с HTTPS через ngrok
"""

import subprocess
import sys
import os
import time
import signal
import threading
import requests
import json
from pathlib import Path
import platform

def free_port(port):
    """Освобождает порт, если он занят (macOS/Linux)"""
    try:
        # lsof -i :<port> | awk 'NR>1 {print $2}' | xargs kill -9
        result = subprocess.run(
            f"lsof -ti :{port}", shell=True, capture_output=True, text=True
        )
        pids = result.stdout.strip().split('\n')
        for pid in pids:
            if pid:
                print(f"🛑 Завершаю процесс {pid} на порту {port}")
                subprocess.run(["kill", "-9", pid])
    except Exception as e:
        print(f"⚠️  Не удалось освободить порт {port}: {e}")

class MiniAppHTTPSLauncher:
    def __init__(self):
        self.processes = []
        self.running = True
        self.ngrok_url = None
        
    def check_ngrok(self):
        """Проверяет, установлен ли ngrok"""
        try:
            result = subprocess.run(['ngrok', 'version'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Ngrok найден")
                return True
        except FileNotFoundError:
            pass
        
        print("❌ Ngrok не найден!")
        print("Установите ngrok:")
        print("  macOS: brew install ngrok")
        print("  Windows: скачайте с https://ngrok.com/")
        print("  Linux: https://ngrok.com/download")
        return False
    
    def stop_existing_ngrok(self):
        """Останавливает существующие ngrok процессы"""
        try:
            # Пытаемся остановить ngrok через API
            requests.post('http://localhost:4040/api/tunnels', timeout=2)
        except:
            pass
        
        # Останавливаем процессы ngrok
        try:
            subprocess.run(['pkill', '-f', 'ngrok'], capture_output=True)
            time.sleep(1)
        except:
            pass
    
    def start_ngrok(self):
        print("🔗 Проверка и освобождение порта 4040 для ngrok...")
        free_port(4040)
        """Запускает ngrok туннель"""
        print("🔗 Запуск ngrok туннеля...")
        
        # Сначала проверяем, не запущен ли уже ngrok
        try:
            response = requests.get('http://localhost:4040/api/tunnels', timeout=2)
            tunnels = response.json()['tunnels']
            for tunnel in tunnels:
                if tunnel['proto'] == 'https':
                    self.ngrok_url = tunnel['public_url']
                    print(f"✅ Ngrok уже запущен: {self.ngrok_url}")
                    return True
        except:
            pass  # Ngrok не запущен, продолжаем
        
        # Останавливаем существующие процессы ngrok
        self.stop_existing_ngrok()
        
        try:
            # Запускаем ngrok в фоне
            process = subprocess.Popen(['ngrok', 'http', '3000'], 
                                     stdout=subprocess.PIPE, 
                                     stderr=subprocess.PIPE)
            self.processes.append(("Ngrok", process))
            
            # Ждем запуска и получаем URL с повторными попытками
            max_attempts = 10
            for attempt in range(max_attempts):
                time.sleep(2)  # Увеличиваем время ожидания
                try:
                    response = requests.get('http://localhost:4040/api/tunnels', timeout=5)
                    if response.status_code == 200:
                        tunnels = response.json()['tunnels']
                        for tunnel in tunnels:
                            if tunnel['proto'] == 'https':
                                self.ngrok_url = tunnel['public_url']
                                print(f"✅ Ngrok туннель создан: {self.ngrok_url}")
                                return True
                except requests.exceptions.RequestException:
                    if attempt < max_attempts - 1:
                        print(f"⏳ Ожидание запуска ngrok... (попытка {attempt + 1}/{max_attempts})")
                        continue
                    else:
                        print("❌ Не удалось получить ngrok URL после всех попыток")
                        return False
            
            print("❌ Не удалось получить ngrok URL")
            return False
                
        except Exception as e:
            print(f"❌ Ошибка запуска ngrok: {e}")
            return False
    
    def start_backend(self):
        print("🚀 Проверка и освобождение порта 8000 для backend...")
        free_port(8000)
        """Запуск FastAPI бэкенда"""
        print("🚀 Запуск бэкенда...")
        backend_dir = Path("backend")
        if not backend_dir.exists():
            print("❌ Папка backend не найдена!")
            return False
            
        try:
            cmd = [sys.executable, "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
            process = subprocess.Popen(cmd, cwd=backend_dir)
            self.processes.append(("Backend", process))
            print("✅ Бэкенд запущен на http://localhost:8000")
            return True
        except Exception as e:
            print(f"❌ Ошибка запуска бэкенда: {e}")
            return False
    
    def start_frontend(self):
        print("🎨 Проверка и освобождение порта 3000 для frontend...")
        free_port(3000)
        """Запуск фронтенд сервера"""
        print("🎨 Запуск фронтенда...")
        frontend_dir = Path("frontend")
        if not frontend_dir.exists():
            print("❌ Папка frontend не найдена!")
            return False
            
        try:
            cmd = [sys.executable, "no_cache_server.py"]
            process = subprocess.Popen(cmd, cwd=frontend_dir)
            self.processes.append(("Frontend", process))
            print("✅ Фронтенд запущен на http://localhost:3000")
            return True
        except Exception as e:
            print(f"❌ Ошибка запуска фронтенда: {e}")
            return False
    
    def start_bot(self):
        """Запуск Telegram бота"""
        print("🤖 Запуск бота...")
        bot_dir = Path("tg_bot")
        if not bot_dir.exists():
            print("❌ Папка tg_bot не найдена!")
            return False
            
        try:
            constants_file = bot_dir / "constants.py"
            if not constants_file.exists():
                print("❌ Файл tg_bot/constants.py не найден!")
                print("Создайте файл с BOT_TOKEN = 'ваш_токен'")
                return False
            
            cmd = [sys.executable, "main.py"]
            process = subprocess.Popen(cmd, cwd=bot_dir)
            self.processes.append(("Bot", process))
            print("✅ Бот запущен")
            return True
        except Exception as e:
            print(f"❌ Ошибка запуска бота: {e}")
            return False
    
    def update_cors(self):
        """Обновляет CORS настройки в бэкенде"""
        if not self.ngrok_url:
            return False
            
        try:
            cors_file = Path("backend/src/main.py")
            if not cors_file.exists():
                return False
            
            # Читаем файл
            with open(cors_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Добавляем ngrok URL в CORS
            ngrok_domain = self.ngrok_url.replace('https://', '').replace('http://', '')
            
            if ngrok_domain not in content:
                # Находим строку с allow_origins и добавляем наш домен
                import re
                pattern = r'allow_origins=\[\s*([^\]]*)\]'
                match = re.search(pattern, content)
                
                if match:
                    origins = match.group(1)
                    if ngrok_domain not in origins:
                        new_origins = origins.rstrip() + f'\n        "{ngrok_domain}",'
                        content = re.sub(pattern, f'allow_origins=[{new_origins}]', content)
                        
                        # Записываем обратно
                        with open(cors_file, 'w', encoding='utf-8') as f:
                            f.write(content)
                        
                        print(f"✅ CORS обновлен для домена: {ngrok_domain}")
                        return True
            
            return True
        except Exception as e:
            print(f"⚠️  Не удалось обновить CORS: {e}")
            return False
    
    def show_info(self):
        """Показать информацию о проекте"""
        print("=" * 70)
        print("🎯 Telegram Mini App с HTTPS - Система записи на тренировки")
        print("=" * 70)
        
        if self.ngrok_url:
            print(f"🔗 HTTPS URL: {self.ngrok_url}")
            print(f"📱 Mini App URL: {self.ngrok_url}/index.html")
        
        print("📁 Структура проекта:")
        print("  ├── backend/     - FastAPI бэкенд (порт 8000)")
        print("  ├── frontend/    - Mini App интерфейс (порт 3000)")
        print("  └── tg_bot/      - Telegram бот")
        print()
        print("🌐 Доступные URL:")
        print("  - Бэкенд API: http://localhost:8000/api")
        print("  - Документация API: http://localhost:8000/api/docs")
        print("  - Фронтенд (локально): http://localhost:3000/index.html")
        
        if self.ngrok_url:
            print(f"  - Фронтенд (HTTPS): {self.ngrok_url}/index.html")
        
        print()
        print("📋 Следующие шаги:")
        print("  1. Настройте токен бота в tg_bot/constants.py")
        print("  2. Создайте Mini App в @BotFather")
        if self.ngrok_url:
            print(f"  3. Используйте URL: {self.ngrok_url}/index.html")
        print("  4. Протестируйте через Telegram")
        print("=" * 70)
    
    def stop_all(self):
        """Остановка всех процессов"""
        print("\n🛑 Остановка всех сервисов...")
        for name, process in self.processes:
            try:
                process.terminate()
                process.wait(timeout=5)
                print(f"✅ {name} остановлен")
            except subprocess.TimeoutExpired:
                process.kill()
                print(f"⚠️  {name} принудительно остановлен")
            except Exception as e:
                print(f"❌ Ошибка остановки {name}: {e}")
    
    def signal_handler(self, signum, frame):
        """Обработчик сигналов для корректного завершения"""
        print("\n🛑 Получен сигнал завершения...")
        self.running = False
        self.stop_all()
        sys.exit(0)
    
    def run(self):
        """Основной метод запуска"""
        # Регистрируем обработчик сигналов
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # Проверяем ngrok
        if not self.check_ngrok():
            return
        
        # Запускаем сервисы
        services_started = 0
        
        if self.start_backend():
            services_started += 1
            time.sleep(2)
        
        if self.start_frontend():
            services_started += 1
            time.sleep(2)
        
        if self.start_ngrok():
            services_started += 1
            time.sleep(2)
            
            # Обновляем CORS
            self.update_cors()
        
        if self.start_bot():
            services_started += 1
        
        if services_started == 0:
            print("❌ Не удалось запустить ни одного сервиса!")
            return
        
        # Показываем информацию
        self.show_info()
        
        print(f"\n✅ Запущено сервисов: {services_started}/4")
        print("🎯 Проект готов к работе!")
        print("⏹️  Для остановки нажмите Ctrl+C")
        
        # Ждем завершения
        try:
            while self.running:
                time.sleep(1)
                # Проверяем, что все процессы еще работают
                for name, process in self.processes:
                    if process.poll() is not None:
                        print(f"⚠️  {name} неожиданно завершился")
                        self.running = False
                        break
        except KeyboardInterrupt:
            pass
        finally:
            self.stop_all()

def main():
    launcher = MiniAppHTTPSLauncher()
    launcher.run()

if __name__ == "__main__":
    main() 