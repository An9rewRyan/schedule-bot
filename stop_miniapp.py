#!/usr/bin/env python3
"""
Скрипт для остановки всех сервисов Mini App
Останавливает процессы, запущенные через run_dev.py
"""

import subprocess
import sys
import os
import signal
import psutil
import time

class MiniAppStopper:
    def __init__(self):
        self.stopped_processes = 0
        
    def find_and_kill_processes(self, process_names):
        """Найти и завершить процессы по именам"""
        killed = 0
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                # Проверяем имя процесса и командную строку
                cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                
                for name in process_names:
                    if (name in proc.info['name'] or 
                        name in cmdline or
                        any(name in arg for arg in proc.info['cmdline'] if arg)):
                        
                        print(f"🛑 Останавливаем {proc.info['name']} (PID: {proc.info['pid']})")
                        proc.terminate()
                        killed += 1
                        
                        # Ждем завершения
                        try:
                            proc.wait(timeout=3)
                        except psutil.TimeoutExpired:
                            print(f"⚠️  Принудительно завершаем процесс {proc.info['pid']}")
                            proc.kill()
                            
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
                
        return killed
    
    def stop_ngrok(self):
        """Остановить все процессы ngrok"""
        print("🌐 Останавливаем ngrok...")
        killed = self.find_and_kill_processes(['ngrok'])
        if killed > 0:
            print(f"✅ Остановлено {killed} процессов ngrok")
        else:
            print("ℹ️  ngrok процессы не найдены")
    
    def stop_backend(self):
        """Остановить backend сервер"""
        print("🚀 Останавливаем Backend API...")
        killed = self.find_and_kill_processes(['uvicorn', 'src.main:app'])
        if killed > 0:
            print(f"✅ Остановлено {killed} backend процессов")
        else:
            print("ℹ️  Backend процессы не найдены")
    
    def stop_frontend(self):
        """Остановить frontend сервер"""
        print("🎨 Останавливаем Frontend...")
        killed = self.find_and_kill_processes(['server.py', 'python server.py'])
        if killed > 0:
            print(f"✅ Остановлено {killed} frontend процессов")
        else:
            print("ℹ️  Frontend процессы не найдены")
    
    def stop_telegram_bot(self):
        """Остановить Telegram бота"""
        print("🤖 Останавливаем Telegram Bot...")
        killed = self.find_and_kill_processes(['main.py', 'python main.py'])
        
        # Дополнительно ищем по содержимому - aiogram
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                if 'aiogram' in cmdline or 'telegram' in cmdline.lower():
                    print(f"🛑 Останавливаем Telegram Bot (PID: {proc.info['pid']})")
                    proc.terminate()
                    killed += 1
                    try:
                        proc.wait(timeout=3)
                    except psutil.TimeoutExpired:
                        proc.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        
        if killed > 0:
            print(f"✅ Остановлено {killed} bot процессов")
        else:
            print("ℹ️  Bot процессы не найдены")
    
    def stop_run_dev_processes(self):
        """Остановить основной процесс run_dev.py"""
        print("⚙️  Останавливаем run_dev.py...")
        killed = self.find_and_kill_processes(['run_dev.py', 'python run_dev.py'])
        if killed > 0:
            print(f"✅ Остановлено {killed} run_dev.py процессов")
        else:
            print("ℹ️  run_dev.py процессы не найдены")
    
    def cleanup_ports(self):
        """Освободить порты, используемые приложением"""
        ports = [3000, 8000, 4040]  # frontend, backend, ngrok admin
        
        print("🔧 Освобождаем порты...")
        for port in ports:
            try:
                # Найти процессы, использующие порт
                result = subprocess.run(
                    ['lsof', '-ti', f':{port}'], 
                    capture_output=True, 
                    text=True
                )
                
                if result.stdout.strip():
                    pids = result.stdout.strip().split('\n')
                    for pid in pids:
                        try:
                            os.kill(int(pid), signal.SIGTERM)
                            print(f"🛑 Освобожден порт {port} (PID: {pid})")
                        except (OSError, ValueError):
                            pass
                            
            except FileNotFoundError:
                # lsof не найден (Windows)
                pass
    
    def stop_all(self):
        """Остановить все сервисы"""
        print("🛑 Останавливаем все сервисы Mini App...")
        print("=" * 50)
        
        # Сначала останавливаем основной процесс
        self.stop_run_dev_processes()
        
        # Даем время для корректного завершения
        time.sleep(1)
        
        # Затем останавливаем отдельные сервисы
        self.stop_telegram_bot()
        self.stop_backend()
        self.stop_frontend()
        self.stop_ngrok()
        
        # Освобождаем порты
        self.cleanup_ports()
        
        print("=" * 50)
        print("✅ Все сервисы остановлены!")
        print("\n📋 Для запуска снова используйте:")
        print("   python run_dev.py")

def main():
    if len(sys.argv) > 1:
        service = sys.argv[1].lower()
        stopper = MiniAppStopper()
        
        if service == "ngrok":
            stopper.stop_ngrok()
        elif service == "backend":
            stopper.stop_backend()
        elif service == "frontend":
            stopper.stop_frontend()
        elif service == "bot":
            stopper.stop_telegram_bot()
        elif service == "all":
            stopper.stop_all()
        else:
            print(f"❌ Неизвестный сервис: {service}")
            print("Доступные: all, ngrok, backend, frontend, bot")
    else:
        # По умолчанию останавливаем все
        stopper = MiniAppStopper()
        stopper.stop_all()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Прервано пользователем")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        sys.exit(1) 