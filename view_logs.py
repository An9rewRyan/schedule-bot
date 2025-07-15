#!/usr/bin/env python3
"""
Скрипт для просмотра логов всех сервисов Mini App
"""

import os
import sys
import time
from pathlib import Path
import argparse

def tail_file(file_path, lines=50):
    """Показать последние строки файла"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            file_lines = f.readlines()
            return file_lines[-lines:]
    except FileNotFoundError:
        return [f"Файл {file_path} не найден\n"]
    except Exception as e:
        return [f"Ошибка чтения файла {file_path}: {e}\n"]

def follow_file(file_path):
    """Следить за файлом в реальном времени"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            # Переходим в конец файла
            f.seek(0, 2)
            
            print(f"📄 Следим за файлом: {file_path}")
            print("🔄 Нажмите Ctrl+C для остановки\n")
            
            while True:
                line = f.readline()
                if line:
                    print(line.rstrip())
                else:
                    time.sleep(0.1)
                    
    except KeyboardInterrupt:
        print("\n👋 Остановка мониторинга...")
    except FileNotFoundError:
        print(f"❌ Файл {file_path} не найден")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

def show_all_logs(lines=50):
    """Показать логи всех сервисов"""
    logs_dir = Path("logs")
    
    if not logs_dir.exists():
        print("❌ Директория logs не найдена. Запустите сначала start_miniapp_https.py")
        return
        
    log_files = {
        "🚀 Основной лог": "miniapp_starter.log",
        "🌐 Ngrok": "ngrok.log", 
        "🔧 Backend": "backend.log",
        "💻 Frontend": "frontend.log",
        "🤖 Telegram Bot": "telegram_bot.log"
    }
    
    for title, filename in log_files.items():
        log_path = logs_dir / filename
        print(f"\n{'='*60}")
        print(f"{title} ({filename})")
        print(f"{'='*60}")
        
        if log_path.exists():
            log_lines = tail_file(log_path, lines)
            for line in log_lines:
                print(line.rstrip())
        else:
            print(f"❌ Файл {filename} не найден")

def list_log_files():
    """Показать список доступных файлов логов"""
    logs_dir = Path("logs")
    
    if not logs_dir.exists():
        print("❌ Директория logs не найдена")
        return
        
    print("📁 Доступные файлы логов:")
    print("-" * 40)
    
    for log_file in logs_dir.glob("*.log"):
        size = log_file.stat().st_size
        size_str = f"{size:,} байт" if size < 1024 else f"{size/1024:.1f} КБ"
        print(f"📄 {log_file.name} ({size_str})")
        
    if not list(logs_dir.glob("*.log")):
        print("Файлы логов не найдены")

def main():
    parser = argparse.ArgumentParser(
        description="Просмотр логов Mini App сервисов",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  python view_logs.py                    # Показать все логи
  python view_logs.py -f backend.log     # Следить за backend логом
  python view_logs.py -t 100             # Показать последние 100 строк
  python view_logs.py -l                 # Список файлов логов
  python view_logs.py -s ngrok           # Показать только ngrok лог
        """
    )
    
    parser.add_argument('-f', '--follow', 
                       help='Следить за файлом в реальном времени')
    parser.add_argument('-t', '--tail', type=int, default=50,
                       help='Количество последних строк для показа (по умолчанию: 50)')
    parser.add_argument('-l', '--list', action='store_true',
                       help='Показать список доступных файлов логов')
    parser.add_argument('-s', '--service', 
                       choices=['main', 'ngrok', 'backend', 'frontend', 'bot'],
                       help='Показать логи только одного сервиса')
    
    args = parser.parse_args()
    
    if args.list:
        list_log_files()
        return
        
    if args.follow:
        log_path = Path("logs") / args.follow
        follow_file(log_path)
        return
        
    if args.service:
        logs_dir = Path("logs")
        service_files = {
            'main': 'miniapp_starter.log',
            'ngrok': 'ngrok.log',
            'backend': 'backend.log', 
            'frontend': 'frontend.log',
            'bot': 'telegram_bot.log'
        }
        
        log_file = logs_dir / service_files[args.service]
        if log_file.exists():
            print(f"📄 Логи сервиса {args.service}:")
            print("-" * 40)
            log_lines = tail_file(log_file, args.tail)
            for line in log_lines:
                print(line.rstrip())
        else:
            print(f"❌ Файл логов для сервиса {args.service} не найден")
        return
    
    # По умолчанию показываем все логи
    show_all_logs(args.tail)

if __name__ == "__main__":
    main() 