#!/usr/bin/env python3
"""
Скрипт для автоматического обновления конфигураций после запуска ngrok
Получает URLs от ngrok API и обновляет все необходимые файлы конфигурации
"""

import requests
import time
import re
import logging
from pathlib import Path

# Настройка логгера
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_ngrok_urls(max_retries=30, delay=2):
    """Получение URLs от ngrok API"""
    logger.info("⏳ Ожидание ngrok API...")

    for attempt in range(max_retries):
        try:
            response = requests.get("http://localhost:4040/api/tunnels", timeout=5)
            if response.status_code == 200:
                data = response.json()
                urls = {}

                for tunnel in data.get('tunnels', []):
                    public_url = tunnel.get('public_url', '')
                    config = tunnel.get('config', {})
                    addr = config.get('addr', '')
                    proto = tunnel.get('proto', 'unknown')
                    name = tunnel.get('name', 'unnamed')

                    # Определяем тип туннеля по порту
                    if addr.endswith(':3000') and public_url:
                        urls['frontend'] = {
                            'url': public_url,
                            'addr': addr,
                            'proto': proto,
                            'name': name
                        }
                    elif addr.endswith(':8000') and public_url:
                        urls['backend'] = {
                            'url': public_url,
                            'addr': addr,
                            'proto': proto,
                            'name': name
                        }

                if urls:
                    logger.info(f"✅ ngrok URLs получены: {len(urls)} туннель(ей)")
                    return urls

        except Exception as e:
            logger.debug(f"Попытка {attempt + 1} неудачна: {e}")

        if attempt < max_retries - 1:
            logger.info(f"⏳ Попытка {attempt + 1}/{max_retries}...")
            time.sleep(delay)

    logger.error("❌ Не удалось получить ngrok URLs")
    return {}

def update_cors_settings(frontend_url):
    """Обновление CORS настроек в backend"""
    main_py_path = Path("backend/src/main.py")
    if not main_py_path.exists():
        logger.warning("⚠️ Файл backend/src/main.py не найден")
        return False

    try:
        content = main_py_path.read_text(encoding='utf-8')

        # Паттерн для поиска origins
        pattern = r'origins = \[(.*?)\]'

        # Новые origins с ngrok URL
        origins_list = [
            '"http://localhost:3000"',
            '"http://127.0.0.1:3000"',
            f'"{frontend_url}"'
        ]

        origins_joined = ',\n    '.join(origins_list)
        new_origins = f'[\n    {origins_joined}\n]'

        # Замена
        new_content = re.sub(pattern, f'origins = {new_origins}', content, flags=re.DOTALL)
        main_py_path.write_text(new_content, encoding='utf-8')

        logger.info(f"✅ CORS обновлен: {frontend_url}")
        return True

    except Exception as e:
        logger.error(f"❌ Ошибка обновления CORS: {e}")
        return False

def update_frontend_config(backend_url):
    """Обновление конфигурации frontend"""
    config_path = Path("frontend/config.js")
    if not config_path.exists():
        logger.warning("⚠️ Файл frontend/config.js не найден")
        return False

    try:
        content = config_path.read_text(encoding='utf-8')

        # Замена API_BASE_URL
        pattern = r"API_BASE_URL: ['\"].*?['\"]"
        replacement = f"API_BASE_URL: '{backend_url}/api'"

        new_content = re.sub(pattern, replacement, content)
        config_path.write_text(new_content, encoding='utf-8')

        logger.info(f"✅ Frontend config обновлен: {backend_url}/api")
        return True

    except Exception as e:
        logger.error(f"❌ Ошибка обновления frontend config: {e}")
        return False

def update_telegram_bot_config(frontend_url):
    """Обновление конфигурации Telegram бота"""
    start_handler_path = Path("tg_bot/handlers/start.py")
    if not start_handler_path.exists():
        logger.warning("⚠️ Файл tg_bot/handlers/start.py не найден")
        return False

    try:
        content = start_handler_path.read_text(encoding='utf-8')

        # Замена MINI_APP_URL
        pattern = r'MINI_APP_URL = ["\'].*?["\']'
        replacement = f'MINI_APP_URL = "{frontend_url}"'

        new_content = re.sub(pattern, replacement, content)
        start_handler_path.write_text(new_content, encoding='utf-8')

        logger.info(f"✅ Bot config обновлен: {frontend_url}")
        return True

    except Exception as e:
        logger.error(f"❌ Ошибка обновления bot config: {e}")
        return False

def update_bot_api_config(backend_url):
    """Обновление конфигурации API в боте"""
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
            logger.error(f"❌ Ошибка обновления {file_path}: {e}")

    if success_count > 0:
        logger.info(f"✅ Bot API config обновлен ({success_count} файлов): {backend_url}")
        return True
    else:
        logger.error("❌ Не удалось обновить API конфигурацию бота")
        return False

def main():
    """Главная функция обновления конфигураций"""
    logger.info("🔄 Обновление конфигураций ngrok URLs...")

    # Получаем URLs от ngrok
    urls = get_ngrok_urls()
    if not urls:
        return False

    # Красивый вывод информации о туннелях
    print("\n" + "="*60)
    print(" 🌐 ИНФОРМАЦИЯ О NGROK ТУННЕЛЯХ")
    print("="*60)

    for service_name, tunnel_info in urls.items():
        print(f"📋 {service_name.upper()}:")
        print(f"   🔗 URL:      {tunnel_info['url']}")
        print(f"   🎯 Target:   {tunnel_info['addr']}")
        print(f"   📡 Protocol: {tunnel_info['proto']}")
        print(f"   🏷️  Name:     {tunnel_info['name']}")
        print()

    print("="*60)

    # Обновляем конфигурации
    success = True

    if 'frontend' in urls:
        success &= update_cors_settings(urls['frontend']['url'])
        success &= update_telegram_bot_config(urls['frontend']['url'])

    if 'backend' in urls:
        success &= update_frontend_config(urls['backend']['url'])
        success &= update_bot_api_config(urls['backend']['url'])

    if success:
        logger.info("✅ Все конфигурации успешно обновлены!")
        if 'frontend' in urls:
            logger.info(f"📱 Mini App URL: {urls['frontend']['url']}")
        logger.info("🔄 Перезапустите Telegram бота для применения изменений!")
    else:
        logger.warning("⚠️ Некоторые конфигурации не удалось обновить")

    return success

if __name__ == "__main__":
    main() 