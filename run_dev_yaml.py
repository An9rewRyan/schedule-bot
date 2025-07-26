#!/usr/bin/env python3

import sys
import subprocess
from pathlib import Path

def colored_print(text, color_code):
    colors = {
        'green': '\033[32m',
        'yellow': '\033[33m',
        'red': '\033[31m',
        'cyan': '\033[36m',
        'reset': '\033[0m'
    }
    print(f"{colors.get(color_code, '')}{text}{colors['reset']}")

def show_menu():
    """Показать интерактивное меню"""
    print("\n" + "="*60)
    colored_print(" Mini App Development Server (YAML) ", 'cyan')
    print("="*60)
    print("Выберите сервисы для запуска:")
    print("1. Backend API (FastAPI)")
    print("2. Frontend Server")
    print("3. Telegram Bot")
    print("4. ngrok (HTTPS tunnels)")
    print("5. Backend + Bot")
    print("6. Frontend + ngrok (с обновлением конфигурации)")
    print("7. ВСЕ СЕРВИСЫ (с ngrok и обновлением конфигурации)")
    print("8. Backend + Frontend + Bot (локально без ngrok)")
    print("0. Выход")
    print("="*60)

    try:
        choice = input("Выберите опцию (0-8): ").strip()
        return choice
    except KeyboardInterrupt:
        return "0"

def run_services(service_names=None):
    """Запуск сервисов через service_composer_mp.py"""
    config_path = "run_dev_replica.yaml"

    if not Path(config_path).exists():
        colored_print(f"Конфигурация не найдена: {config_path}", 'red')
        return False

    try:
        # Строим команду для запуска
        cmd = ["python", "service_composer_mp.py", "-c", config_path]

        # В service_composer_mp.py пока нет поддержки выборочного запуска сервисов
        # Поэтому запускаем все сервисы из конфигурации
        if service_names:
            colored_print(f"Запуск сервисов: {', '.join(service_names)} (через конфигурацию)", 'green')
            colored_print("Примечание: service_composer_mp.py запустит все сервисы из конфигурации", 'yellow')
        else:
            colored_print("Запуск всех сервисов", 'green')

        colored_print(f"Команда: {' '.join(cmd)}", 'yellow')

        # Запускаем service_composer_mp.py с нашей конфигурацией
        result = subprocess.run(cmd)
        return result.returncode == 0

    except Exception as e:
        colored_print(f"Ошибка запуска: {e}", 'red')
        return False

def main():
    """Главная функция"""

    # Проверка аргументов командной строки
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()

        # Маппинг аргументов на профили (пока используем все сервисы для всех профилей)
        # В будущем можно будет добавить поддержку профилей в service_composer_mp.py
        profile_map = {
            "backend": "backend",
            "frontend": "frontend",
            "bot": "bot",
            "ngrok": "ngrok",
            "local": "local",
            "all": "all"
        }

        if arg in profile_map:
            colored_print(f"Запуск в режиме: {arg}", 'cyan')

            # Маппинг аргументов на сервисы
            if arg == "backend":
                run_services(['backend'])
            elif arg == "frontend":
                run_services(['frontend'])
            elif arg == "bot":
                run_services(['telegram_bot'])
            elif arg == "ngrok":
                run_services(['ngrok'])
            elif arg == "local":
                run_services(['backend', 'frontend', 'telegram_bot'])
            elif arg == "all":
                run_services()  # Все сервисы
        else:
            colored_print(f"Неизвестный аргумент: {arg}", 'red')
            colored_print("Доступные: backend, frontend, bot, ngrok, local, all", 'yellow')
            sys.exit(1)
    else:
        # Интерактивное меню
        while True:
            choice = show_menu()

            if choice == "0":
                colored_print("До свидания!", 'cyan')
                break
            elif choice in ["1", "2", "3", "4", "5", "6", "7", "8"]:
                profile_names = {
                    "1": "backend",
                    "2": "frontend",
                    "3": "bot",
                    "4": "ngrok",
                    "5": "backend+bot",
                    "6": "frontend+ngrok",
                    "7": "all",
                    "8": "local"
                }

                colored_print(f"Запуск профиля: {profile_names[choice]}", 'cyan')

                # Маппинг выбора меню на сервисы
                if choice == "1":  # backend
                    success = run_services(['backend'])
                elif choice == "2":  # frontend
                    success = run_services(['frontend'])
                elif choice == "3":  # bot
                    success = run_services(['telegram_bot'])
                elif choice == "4":  # ngrok
                    success = run_services(['ngrok'])
                elif choice == "5":  # backend+bot
                    success = run_services(['backend', 'telegram_bot'])
                elif choice == "6":  # frontend+ngrok
                    success = run_services(['frontend', 'ngrok'])
                elif choice == "7":  # all
                    success = run_services()
                elif choice == "8":  # local
                    success = run_services(['backend', 'frontend', 'telegram_bot'])

                if success:
                    break
            else:
                colored_print("Неверный выбор, попробуйте снова", 'red')

if __name__ == "__main__":
    main()