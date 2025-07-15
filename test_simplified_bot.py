#!/usr/bin/env python3
"""
Тест упрощенного бота с только Mini App функциональностью
"""
import asyncio
import sys
import os
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from aiogram import Bot
from tg_bot.constants import BOT_TOKEN

async def test_simplified_bot():
    """Тестируем упрощенный бот"""
    print("🧪 Тестирование упрощенного бота...")
    print("=" * 50)
    
    # Создаем бота
    bot = Bot(token=BOT_TOKEN)
    
    try:
        # Проверяем, что бот работает
        me = await bot.get_me()
        print(f"✅ Бот подключен: {me.first_name} (@{me.username})")
        
        # Проверяем webhook
        webhook_info = await bot.get_webhook_info()
        print(f"📡 Webhook URL: {webhook_info.url or 'Не установлен (polling)'}")
        
        # Проверяем pending updates
        updates = await bot.get_updates(limit=1)
        print(f"📨 Pending updates: {len(updates)}")
        
        print("\n🎯 Функциональность бота:")
        print("  - /start - Показывает только кнопку Mini App")
        print("  - /app - Быстрый доступ к Mini App")
        print("  - Все остальные функции удалены")
        
        print("\n✅ Упрощенный бот готов к работе!")
        print("💡 Отправьте /start боту в Telegram для тестирования")
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании бота: {e}")
    
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(test_simplified_bot()) 