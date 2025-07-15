#!/usr/bin/env python3
"""
Файл для запуска Telegram бота
"""

import sys
import os

# Добавляем путь к tg_bot в PYTHONPATH
sys.path.insert(0, os.path.dirname(__file__))

if __name__ == "__main__":
    from main import main
    import asyncio
    
    asyncio.run(main()) 