#!/usr/bin/env python3
"""
Скрипт для автоматического обновления конфигурации ngrok URLs
"""

import requests
import re
from pathlib import Path

def get_ngrok_urls():
    """Получение текущих URLs от ngrok API"""
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
                
                if ('frontend' in name or addr.endswith(':3000')) and public_url:
                    urls['frontend'] = public_url
                elif ('backend' in name or addr.endswith(':8000')) and public_url:
                    urls['backend'] = public_url
            
            return urls
    except Exception as e:
        print(f"❌ Ошибка получения ngrok URLs: {e}")
        return {}

def update_telegram_bot_config(frontend_url):
    """Обновление конфигурации Telegram бота"""
    print(f"🤖 Обновление Telegram bot конфигурации с URL: {frontend_url}")
    
    start_handler_path = Path("tg_bot/handlers/start.py")
    if not start_handler_path.exists():
        print("❌ Файл tg_bot/handlers/start.py не найден")
        return False
        
    try:
        content = start_handler_path.read_text(encoding='utf-8')
        
        # Замена MINI_APP_URL
        pattern = r'MINI_APP_URL = ["\'].*?["\']'
        replacement = f'MINI_APP_URL = "{frontend_url}"'
        
        new_content = re.sub(pattern, replacement, content)
        start_handler_path.write_text(new_content, encoding='utf-8')
        
        print(f"✅ Bot config обновлен с URL: {frontend_url}")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка обновления bot config: {e}")
        return False

def update_cors_settings(backend_url, frontend_url):
    """Обновление CORS настроек в backend"""
    print(f"🔧 Обновление CORS настроек...")
    
    main_py_path = Path("backend/src/main.py")
    if not main_py_path.exists():
        print("❌ Файл backend/src/main.py не найден")
        return False
        
    try:
        content = main_py_path.read_text(encoding='utf-8')
        
        # Паттерн для поиска origins
        pattern = r'origins = \[(.*?)\]'
        
        # Новые origins с ngrok URL
        new_origins = f'''[
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "{backend_url}",
    "{frontend_url}"
]'''
        
        # Замена
        new_content = re.sub(pattern, f'origins = {new_origins}', content, flags=re.DOTALL)
        main_py_path.write_text(new_content, encoding='utf-8')
        
        print(f"✅ CORS обновлен с URLs: {backend_url}, {frontend_url}")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка обновления CORS: {e}")
        return False

def update_frontend_config(backend_url):
    """Обновление конфигурации frontend"""
    print(f"🎨 Обновление конфигурации frontend...")
    
    config_path = Path("frontend/config.js")
    if not config_path.exists():
        print("❌ Файл frontend/config.js не найден")
        return False
        
    try:
        content = config_path.read_text(encoding='utf-8')
        
        # Замена API_BASE_URL
        pattern = r"API_BASE_URL: ['\"].*?['\"]"
        replacement = f"API_BASE_URL: '{backend_url}/api'"
        
        new_content = re.sub(pattern, replacement, content)
        config_path.write_text(new_content, encoding='utf-8')
        
        print(f"✅ Frontend config обновлен с URL: {backend_url}/api")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка обновления frontend config: {e}")
        return False

def update_bot_api_config(backend_url):
    """Обновление конфигурации API в боте"""
    print(f"🔧 Обновление API конфигурации бота...")
    
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
            print(f"⚠️ Файл {file_path} не найден")
            continue
            
        try:
            content = path.read_text(encoding='utf-8')
            
            # Обновляем BASE_URL и API_BASE_URL
            patterns = [
                (r'BASE_URL = ["\'].*?["\']', f'BASE_URL = "{backend_url}"'),
                (r'API_BASE_URL = ["\'].*?["\']', f'API_BASE_URL = "{backend_url}/api"')
            ]
            
            updated = False
            for pattern, replacement in patterns:
                if re.search(pattern, content):
                    content = re.sub(pattern, replacement, content)
                    updated = True
                    
            if updated:
                path.write_text(content, encoding='utf-8')
                success_count += 1
            
        except Exception as e:
            print(f"❌ Ошибка обновления {file_path}: {e}")
    
    if success_count > 0:
        print(f"✅ API конфигурация бота обновлена ({success_count} файлов)")
        return True
    else:
        print("❌ Не удалось обновить API конфигурацию бота")
        return False

def main():
    print("🔄 Автоматическое обновление конфигурации ngrok URLs...")
    print("=" * 60)
    
    # Получаем текущие URLs от ngrok
    urls = get_ngrok_urls()
    if not urls:
        print("❌ Не удалось получить ngrok URLs. Убедитесь, что ngrok запущен.")
        return
    
    frontend_url = urls.get('frontend')
    backend_url = urls.get('backend')
    
    print(f"📋 Текущие ngrok URLs:")
    print(f"  Frontend: {frontend_url}")
    print(f"  Backend: {backend_url}")
    print()
    
    # Обновляем конфигурации
    success = True
    
    if frontend_url:
        success &= update_telegram_bot_config(frontend_url)
    
    if backend_url:
        success &= update_bot_api_config(backend_url)
        if frontend_url:
            success &= update_cors_settings(backend_url, frontend_url)
            success &= update_frontend_config(backend_url)
    
    print("=" * 60)
    if success:
        print("✅ Все конфигурации успешно обновлены!")
        print()
        print("📱 Для настройки Mini App в Telegram:")
        print(f"   Mini App URL: {frontend_url}")
        print()
        print("🔄 Не забудьте перезапустить Telegram бота для применения изменений!")
    else:
        print("⚠️ Некоторые конфигурации не удалось обновить")

if __name__ == "__main__":
    main() 