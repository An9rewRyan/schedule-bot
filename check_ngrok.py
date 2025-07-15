#!/usr/bin/env python3
"""
Скрипт для проверки и установки ngrok
"""

import subprocess
import sys
import platform
import os

def check_ngrok():
    """Проверяет, установлен ли ngrok"""
    try:
        result = subprocess.run(['ngrok', 'version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Ngrok найден!")
            print(f"Версия: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ Ngrok не найден!")
    return False

def install_ngrok():
    """Устанавливает ngrok в зависимости от ОС"""
    system = platform.system().lower()
    
    print("🔧 Установка ngrok...")
    
    if system == "darwin":  # macOS
        try:
            # Проверяем, установлен ли Homebrew
            result = subprocess.run(['brew', '--version'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("📦 Устанавливаем через Homebrew...")
                subprocess.run(['brew', 'install', 'ngrok'], check=True)
                print("✅ Ngrok установлен через Homebrew!")
                return True
            else:
                print("❌ Homebrew не найден!")
                print("Установите Homebrew: https://brew.sh/")
                return False
        except Exception as e:
            print(f"❌ Ошибка установки: {e}")
            return False
    
    elif system == "linux":
        print("📦 Установка для Linux...")
        print("1. Скачайте ngrok с https://ngrok.com/download")
        print("2. Распакуйте архив")
        print("3. Переместите ngrok в /usr/local/bin/")
        print("4. Зарегистрируйтесь на https://ngrok.com/")
        print("5. Получите authtoken и выполните: ngrok config add-authtoken YOUR_TOKEN")
        return False
    
    elif system == "windows":
        print("📦 Установка для Windows...")
        print("1. Скачайте ngrok с https://ngrok.com/download")
        print("2. Распакуйте архив")
        print("3. Добавьте папку с ngrok в PATH")
        print("4. Зарегистрируйтесь на https://ngrok.com/")
        print("5. Получите authtoken и выполните: ngrok config add-authtoken YOUR_TOKEN")
        return False
    
    else:
        print(f"❌ Неподдерживаемая ОС: {system}")
        return False

def setup_ngrok():
    """Настраивает ngrok"""
    print("🔧 Настройка ngrok...")
    
    # Проверяем, есть ли уже конфигурация
    config_dir = os.path.expanduser("~/.ngrok2")
    if os.path.exists(config_dir):
        print("✅ Конфигурация ngrok найдена")
        return True
    
    print("📝 Для использования ngrok нужно:")
    print("1. Зарегистрироваться на https://ngrok.com/")
    print("2. Получить authtoken в личном кабинете")
    print("3. Выполнить команду: ngrok config add-authtoken YOUR_TOKEN")
    
    token = input("Введите ваш authtoken (или нажмите Enter для пропуска): ").strip()
    
    if token:
        try:
            subprocess.run(['ngrok', 'config', 'add-authtoken', token], check=True)
            print("✅ Authtoken настроен!")
            return True
        except Exception as e:
            print(f"❌ Ошибка настройки authtoken: {e}")
            return False
    else:
        print("⚠️  Authtoken не настроен. Ngrok будет работать с ограничениями.")
        return True

def test_ngrok():
    """Тестирует ngrok"""
    print("🧪 Тестирование ngrok...")
    
    try:
        # Запускаем ngrok на короткое время
        process = subprocess.Popen(['ngrok', 'http', '3000'], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE)
        
        import time
        time.sleep(3)  # Ждем запуска
        
        # Проверяем API
        import requests
        try:
            response = requests.get('http://localhost:4040/api/tunnels', timeout=5)
            if response.status_code == 200:
                tunnels = response.json()['tunnels']
                for tunnel in tunnels:
                    if tunnel['proto'] == 'https':
                        print(f"✅ Ngrok работает! URL: {tunnel['public_url']}")
                        process.terminate()
                        return True
        except:
            pass
        
        process.terminate()
        print("⚠️  Ngrok запустился, но не удалось получить URL")
        return False
        
    except Exception as e:
        print(f"❌ Ошибка тестирования: {e}")
        return False

def main():
    print("=" * 50)
    print("🔍 Проверка и установка ngrok")
    print("=" * 50)
    
    # Проверяем ngrok
    if check_ngrok():
        # Настраиваем ngrok
        if setup_ngrok():
            # Тестируем ngrok
            test_ngrok()
    else:
        # Устанавливаем ngrok
        if install_ngrok():
            # Настраиваем ngrok
            if setup_ngrok():
                # Тестируем ngrok
                test_ngrok()
    
    print("\n📋 Следующие шаги:")
    print("1. Если ngrok работает, запустите: python start_mini_app_https.py")
    print("2. Если есть проблемы с ngrok, используйте: python start_mini_app_local.py")
    print("3. Для тестирования в браузере: http://localhost:3000/index.html")

if __name__ == "__main__":
    main() 