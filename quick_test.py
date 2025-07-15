#!/usr/bin/env python3
"""
Быстрый тест Mini App
"""

import subprocess
import sys
import time
import signal
from pathlib import Path

def run_command(cmd, cwd=None, name="Command"):
    """Запускает команду и возвращает процесс"""
    try:
        process = subprocess.Popen(cmd, cwd=cwd)
        print(f"✅ {name} запущен")
        return process
    except Exception as e:
        print(f"❌ Ошибка запуска {name}: {e}")
        return None

def main():
    processes = []
    
    def cleanup():
        print("\n🛑 Остановка всех процессов...")
        for process in processes:
            if process:
                process.terminate()
    
    # Обработчик сигналов
    def signal_handler(signum, frame):
        cleanup()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print("🚀 Быстрый запуск Mini App")
    print("=" * 50)
    
    # Запуск бэкенда
    backend_process = run_command(
        [sys.executable, "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"],
        cwd="backend",
        name="Backend"
    )
    if backend_process:
        processes.append(backend_process)
    
    time.sleep(3)
    
    # Запуск фронтенда
    frontend_process = run_command(
        [sys.executable, "server.py"],
        cwd="frontend",
        name="Frontend"
    )
    if frontend_process:
        processes.append(frontend_process)
    
    time.sleep(2)
    
    # Запуск бота
    bot_process = run_command(
        [sys.executable, "main.py"],
        cwd="tg_bot",
        name="Bot"
    )
    if bot_process:
        processes.append(bot_process)
    
    print("\n" + "=" * 50)
    print("🎯 Все сервисы запущены!")
    print("🌐 Frontend: http://localhost:3000/index.html")
    print("🌐 API: http://localhost:8000/api/docs")
    print("⏹️  Для остановки нажмите Ctrl+C")
    print("=" * 50)
    
    try:
        while True:
            time.sleep(1)
            # Проверяем, что все процессы еще работают
            for i, process in enumerate(processes):
                if process and process.poll() is not None:
                    print(f"⚠️  Процесс {i+1} неожиданно завершился")
                    cleanup()
                    return
    except KeyboardInterrupt:
        pass
    finally:
        cleanup()

if __name__ == "__main__":
    main() 