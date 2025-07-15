#!/usr/bin/env python3
"""
Скрипт для запуска Telegram Mini App проекта
"""

import subprocess
import sys
import os
import time
import signal
import threading
from pathlib import Path

class MiniAppLauncher:
    def __init__(self):
        self.processes = []
        self.running = True
        
    def start_backend(self):
        """Запуск FastAPI бэкенда"""
        print("🚀 Запуск бэкенда...")
        backend_dir = Path("backend")
        if not backend_dir.exists():
            print("❌ Папка backend не найдена!")
            return False
            
        try:
            # Устанавливаем зависимости если нужно
            if not (backend_dir / "venv").exists():
                print("📦 Установка зависимостей бэкенда...")
                subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                             cwd=backend_dir, check=True)
            
            # Запускаем бэкенд
            cmd = [sys.executable, "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
            process = subprocess.Popen(cmd, cwd=backend_dir)
            self.processes.append(("Backend", process))
            print("✅ Бэкенд запущен на http://localhost:8000")
            return True
        except Exception as e:
            print(f"❌ Ошибка запуска бэкенда: {e}")
            return False
    
    def start_frontend(self):
        """Запуск фронтенд сервера"""
        print("🎨 Запуск фронтенда...")
        frontend_dir = Path("frontend")
        if not frontend_dir.exists():
            print("❌ Папка frontend не найдена!")
            return False
            
        try:
            cmd = [sys.executable, "server.py"]
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
            # Проверяем наличие токена
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
    
    def check_dependencies(self):
        """Проверка зависимостей"""
        print("🔍 Проверка зависимостей...")
        
        required_packages = [
            "fastapi",
            "uvicorn",
            "aiogram",
            "httpx"
        ]
        
        missing_packages = []
        for package in required_packages:
            try:
                __import__(package)
            except ImportError:
                missing_packages.append(package)
        
        if missing_packages:
            print(f"❌ Отсутствуют пакеты: {', '.join(missing_packages)}")
            print("Установите их командой: pip install " + " ".join(missing_packages))
            return False
        
        print("✅ Все зависимости установлены")
        return True
    
    def show_info(self):
        """Показать информацию о проекте"""
        print("=" * 60)
        print("🎯 Telegram Mini App - Система записи на тренировки")
        print("=" * 60)
        print("📁 Структура проекта:")
        print("  ├── backend/     - FastAPI бэкенд (порт 8000)")
        print("  ├── frontend/    - Mini App интерфейс (порт 3000)")
        print("  └── tg_bot/      - Telegram бот")
        print()
        print("🌐 Доступные URL:")
        print("  - Бэкенд API: http://localhost:8000/api")
        print("  - Документация API: http://localhost:8000/api/docs")
        print("  - Mini App: http://localhost:3000/index.html")
        print()
        print("📋 Следующие шаги:")
        print("  1. Настройте токен бота в tg_bot/constants.py")
        print("  2. Создайте Mini App в @BotFather")
        print("  3. Обновите URL в конфигурации")
        print("  4. Протестируйте через Telegram")
        print("=" * 60)
    
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
        
        # Показываем информацию
        self.show_info()
        
        # Проверяем зависимости
        if not self.check_dependencies():
            return
        
        # Запускаем сервисы
        services_started = 0
        
        if self.start_backend():
            services_started += 1
            time.sleep(2)  # Даем время на запуск
        
        if self.start_frontend():
            services_started += 1
            time.sleep(1)
        
        if self.start_bot():
            services_started += 1
        
        if services_started == 0:
            print("❌ Не удалось запустить ни одного сервиса!")
            return
        
        print(f"\n✅ Запущено сервисов: {services_started}/3")
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
    launcher = MiniAppLauncher()
    launcher.run()

if __name__ == "__main__":
    main() 