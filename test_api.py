#!/usr/bin/env python3
"""
Скрипт для тестирования API таймслотов
"""

import requests
import json
from datetime import date

def test_timeslots_api():
    """Тестирует API таймслотов"""
    print("🧪 Тестирование API таймслотов...")
    
    # URL API
    base_url = "http://localhost:8000/api"
    
    try:
        # Тест 1: Получение таймслотов без telegram_id
        print("\n1️⃣ Тест без telegram_id:")
        response = requests.get(f"{base_url}/slots/")
        print(f"Статус: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Доступные периоды: {len(data.get('available_periods', []))}")
            for period in data.get('available_periods', [])[:3]:  # Показываем первые 3
                print(f"  - {period.get('date')} {period.get('start_time')}-{period.get('end_time')}")
        else:
            print(f"Ошибка: {response.text}")
        
        # Тест 2: Получение таймслотов с telegram_id
        print("\n2️⃣ Тест с telegram_id:")
        telegram_id = 123456789  # Тестовый пользователь
        response = requests.get(f"{base_url}/slots/?telegram_id={telegram_id}")
        print(f"Статус: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Доступные периоды: {len(data.get('available_periods', []))}")
            for period in data.get('available_periods', [])[:3]:  # Показываем первые 3
                print(f"  - {period.get('date')} {period.get('start_time')}-{period.get('end_time')}")
        else:
            print(f"Ошибка: {response.text}")
        
        # Тест 3: Получение таймслотов на конкретную дату
        print("\n3️⃣ Тест на конкретную дату:")
        today = date.today()
        response = requests.get(f"{base_url}/slots/?selected_date={today}")
        print(f"Статус: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Доступные периоды на {today}: {len(data.get('available_periods', []))}")
            for period in data.get('available_periods', [])[:3]:  # Показываем первые 3
                print(f"  - {period.get('date')} {period.get('start_time')}-{period.get('end_time')}")
        else:
            print(f"Ошибка: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Не удалось подключиться к API")
        print("Убедитесь, что бэкенд запущен: python -m uvicorn src.main:app --reload")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

def test_backend_health():
    """Тестирует доступность бэкенда"""
    print("🏥 Проверка здоровья бэкенда...")
    
    try:
        response = requests.get("http://localhost:8000/api/docs")
        print(f"Статус API docs: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Бэкенд работает")
            return True
        else:
            print(f"⚠️  Бэкенд отвечает со статусом: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Бэкенд недоступен")
        return False

def main():
    print("=" * 50)
    print("🧪 Тестирование API Telegram Mini App")
    print("=" * 50)
    
    # Проверяем доступность бэкенда
    if not test_backend_health():
        print("\n🔧 Рекомендации:")
        print("1. Запустите бэкенд: cd backend && python -m uvicorn src.main:app --reload")
        print("2. Проверьте настройки базы данных")
        print("3. Создайте тестовые данные: python backend/scripts/create_test_data.py")
        return
    
    # Тестируем API таймслотов
    test_timeslots_api()
    
    print("\n📋 Следующие шаги:")
    print("1. Если API работает, запустите Mini App")
    print("2. Если нет данных, создайте тестовые данные:")
    print("   python backend/scripts/create_test_data.py")

if __name__ == "__main__":
    main() 