#!/usr/bin/env python3
"""
Скрипт для диагностики проблем с проектом
"""

import subprocess
import sys
import os
import platform
import requests
from pathlib import Path

def check_python():
    """Проверяет версию Python"""
    print("🐍 Проверка Python...")
    version = sys.version_info
    print(f"Версия Python: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 8:
        print("✅ Python версия подходит")
        return True
    else:
        print("❌ Требуется Python 3.8+")
        return False

def check_virtual_env():
    """Проверяет виртуальное окружение"""
    print("\n🔧 Проверка виртуального окружения...")
    
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Виртуальное окружение активировано")
        print(f"Путь: {sys.prefix}")
        return True
    else:
        print("⚠️  Виртуальное окружение не активировано")
        print("Рекомендуется: source .venv/bin/activate")
        return False

def check_dependencies():
    """Проверяет установленные зависимости"""
    print("\n📦 Проверка зависимостей...")
    
    required_packages = [
        'fastapi',
        'uvicorn',
        'sqlalchemy',
        'psycopg2-binary',
        'aiogram',
        'requests'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n❌ Отсутствуют пакеты: {', '.join(missing_packages)}")
        print("Установите: pip install -r requirements.txt")
        return False
    else:
        print("✅ Все зависимости установлены")
        return True

def check_project_structure():
    """Проверяет структуру проекта"""
    print("\n📁 Проверка структуры проекта...")
    
    required_dirs = [
        'backend',
        'backend/src',
        'backend/src/api',
        'backend/src/models',
        'frontend',
        'tg_bot'
    ]
    
    required_files = [
        'backend/src/main.py',
        'backend/requirements.txt',
        'frontend/index.html',
        'frontend/server.py',
        'tg_bot/main.py'
    ]
    
    missing_items = []
    
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"✅ {dir_path}/")
        else:
            print(f"❌ {dir_path}/")
            missing_items.append(dir_path)
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            missing_items.append(file_path)
    
    if missing_items:
        print(f"\n❌ Отсутствуют: {', '.join(missing_items)}")
        return False
    else:
        print("✅ Структура проекта корректна")
        return True

def check_ports():
    """Проверяет доступность портов"""
    print("\n🔌 Проверка портов...")
    
    ports = [8000, 3000]
    
    for port in ports:
        try:
            response = requests.get(f'http://localhost:{port}', timeout=2)
            print(f"⚠️  Порт {port} занят (статус: {response.status_code})")
        except requests.exceptions.ConnectionError:
            print(f"✅ Порт {port} свободен")
        except Exception as e:
            print(f"✅ Порт {port} свободен")

def check_ngrok():
    """Проверяет ngrok"""
    print("\n🔗 Проверка ngrok...")
    
    try:
        result = subprocess.run(['ngrok', 'version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Ngrok найден: {result.stdout.strip()}")
            
            # Проверяем API ngrok
            try:
                response = requests.get('http://localhost:4040/api/tunnels', timeout=2)
                if response.status_code == 200:
                    print("✅ Ngrok API доступен")
                    tunnels = response.json()['tunnels']
                    for tunnel in tunnels:
                        print(f"  - {tunnel['proto']}: {tunnel['public_url']}")
                else:
                    print("⚠️  Ngrok API недоступен")
            except:
                print("⚠️  Ngrok не запущен")
            
            return True
        else:
            print("❌ Ngrok не найден")
            return False
    except FileNotFoundError:
        print("❌ Ngrok не установлен")
        return False

def check_bot_token():
    """Проверяет токен бота"""
    print("\n🤖 Проверка токена бота...")
    
    constants_file = Path("tg_bot/constants.py")
    if not constants_file.exists():
        print("❌ Файл tg_bot/constants.py не найден")
        return False
    
    try:
        with open(constants_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'BOT_TOKEN' in content:
            print("✅ Файл constants.py найден")
            if 'ваш_токен' in content or 'YOUR_TOKEN' in content:
                print("⚠️  Токен не настроен (используется placeholder)")
                return False
            else:
                print("✅ Токен настроен")
                return True
        else:
            print("❌ BOT_TOKEN не найден в файле")
            return False
    except Exception as e:
        print(f"❌ Ошибка чтения файла: {e}")
        return False

def run_tests():
    """Запускает базовые тесты"""
    print("\n🧪 Запуск тестов...")
    
    # Тест бэкенда
    print("Тестирование бэкенда...")
    try:
        response = requests.get('http://localhost:8000/api', timeout=5)
        if response.status_code == 200:
            print("✅ Бэкенд работает")
        else:
            print(f"⚠️  Бэкенд отвечает со статусом: {response.status_code}")
    except:
        print("❌ Бэкенд недоступен")
    
    # Тест фронтенда
    print("Тестирование фронтенда...")
    try:
        response = requests.get('http://localhost:3000', timeout=5)
        if response.status_code == 200:
            print("✅ Фронтенд работает")
        else:
            print(f"⚠️  Фронтенд отвечает со статусом: {response.status_code}")
    except:
        print("❌ Фронтенд недоступен")

def main():
    print("=" * 60)
    print("🔍 Диагностика Telegram Mini App")
    print("=" * 60)
    
    checks = [
        check_python,
        check_virtual_env,
        check_dependencies,
        check_project_structure,
        check_ports,
        check_ngrok,
        check_bot_token
    ]
    
    results = []
    for check in checks:
        try:
            result = check()
            results.append(result if result is not None else False)
        except Exception as e:
            print(f"❌ Ошибка в проверке: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    print("📊 Результаты диагностики")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"✅ Пройдено проверок: {passed}/{total}")
    
    if passed == total:
        print("🎉 Все проверки пройдены! Проект готов к работе.")
        print("\n🚀 Запустите проект:")
        print("  python run_dev.py")
    else:
        print("⚠️  Есть проблемы, которые нужно исправить.")
        print("\n🔧 Рекомендации:")
        
        if not results[0]:  # Python
            print("- Обновите Python до версии 3.8+")
        
        if not results[1]:  # Virtual env
            print("- Активируйте виртуальное окружение")
        
        if not results[2]:  # Dependencies
            print("- Установите зависимости: pip install -r requirements.txt")
        
        if not results[3]:  # Structure
            print("- Проверьте структуру проекта")
        
        if not results[5]:  # Ngrok
            print("- Установите ngrok: python check_ngrok.py")
        
        if not results[6]:  # Bot token
            print("- Настройте токен бота в tg_bot/constants.py")
    
    print("\n📋 Команды запуска:")
    print("  python run_dev.py         - Интерактивный запуск")
    print("  python run_dev.py all     - Запуск всех сервисов")
    print("  python run_dev.py local   - Локальный запуск (без ngrok)")
    print("  python check_ngrok.py     - Проверка ngrok")

if __name__ == "__main__":
    main() 