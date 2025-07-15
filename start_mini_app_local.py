#!/usr/bin/env python3
"""
Скрипт для запуска Telegram Mini App локально (без HTTPS)
"""

import subprocess
import sys
import os
import time
import signal
import threading
from pathlib import Path

class MiniAppLocalLauncher:
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
    
    def show_info(self):
        """Показать информацию о проекте"""
        print("=" * 70)
        print("🎯 Telegram Mini App - Локальная версия")
        print("=" * 70)
        print("📁 Структура проекта:")
        print("  ├── backend/     - FastAPI бэкенд (порт 8000)")
        print("  ├── frontend/    - Mini App интерфейс (порт 3000)")
        print("  └── tg_bot/      - Telegram бот")
        print()
        print("🌐 Доступные URL:")
        print("  - Бэкенд API: http://localhost:8000/api")
        print("  - Документация API: http://localhost:8000/api/docs")
        print("  - Фронтенд (локально): http://localhost:3000/index.html")
        print()
        print("📋 Следующие шаги:")
        print("  1. Настройте токен бота в tg_bot/constants.py")
        print("  2. Для тестирования Mini App в браузере:")
        print("     - Откройте http://localhost:3000/index.html")
        print("     - Используйте тестовую страницу для симуляции Telegram Web App")
        print("  3. Для тестирования в Telegram:")
        print("     - Используйте ngrok: python start_mini_app_https.py")
        print("     - Или настройте хостинг с HTTPS")
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
        
        # Запускаем сервисы
        services_started = 0
        
        if self.start_backend():
            services_started += 1
            time.sleep(2)
        
        if self.start_frontend():
            services_started += 1
            time.sleep(2)
        
        if self.start_bot():
            services_started += 1
        
        if services_started == 0:
            print("❌ Не удалось запустить ни одного сервиса!")
            return
        
        # Показываем информацию
        self.show_info()
        
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
    launcher = MiniAppLocalLauncher()
    launcher.run()

if __name__ == "__main__":
    main() 