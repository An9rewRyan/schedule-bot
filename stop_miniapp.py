#!/usr/bin/env python3
"""
Скрипт для остановки всех процессов Mini App
"""

import subprocess
import time

def stop_processes():
    """Остановка всех процессов"""
    print("🧹 Остановка всех процессов Mini App...")
    
    # Остановка ngrok
    print("🔸 Остановка ngrok...")
    subprocess.run(["pkill", "-f", "ngrok"], capture_output=True)
    
    # Остановка процессов на портах
    ports = [8000, 3000, 4040, 4041]
    for port in ports:
        print(f"🔸 Освобождение порта {port}...")
        result = subprocess.run(["lsof", "-ti", f":{port}"], capture_output=True, text=True)
        if result.stdout.strip():
            pids = result.stdout.strip().split('\n')
            for pid in pids:
                subprocess.run(["kill", "-9", pid], capture_output=True)
    
    # Остановка Python процессов
    print("🔸 Остановка Python процессов...")
    subprocess.run(["pkill", "-f", "python.*main.py"], capture_output=True)
    subprocess.run(["pkill", "-f", "python.*src.main"], capture_output=True)
    subprocess.run(["pkill", "-f", "python.*no_cache_server.py"], capture_output=True)
    
    time.sleep(2)
    print("✅ Все процессы остановлены")

if __name__ == "__main__":
    stop_processes() 