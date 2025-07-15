# 🔧 Исправления ошибок

## ✅ Исправленные проблемы

### 1. Ошибка относительного импорта в бэкенде
**Проблема**: `ImportError: attempted relative import with no known parent package`

**Решение**: Изменил относительные импорты на абсолютные в `backend/src/main.py`:
```python
# Было:
from .api.routers import main_router

# Стало:
from api.routers import main_router
```

### 2. Ошибка отсутствующего модуля w3lib
**Проблема**: `ModuleNotFoundError: No module named 'w3lib'`

**Решение**: Заменил w3lib на стандартную библиотеку Python в `tg_bot/api/bookings.py`:
```python
# Было:
from w3lib.url import add_or_replace_parameter

# Стало:
from urllib.parse import urlencode, parse_qs, urlparse, urlunparse
```

И упростил функцию `delete_booking`:
```python
# Было:
url = add_or_replace_parameter(url, "booking_id", str(booking_id))
url = add_or_replace_parameter(url, 'telegram_id', telegram_id)

# Стало:
url = f"{API_BASE_URL}/bookings/{booking_id}?telegram_id={telegram_id}"
```

### 3. Ошибки импорта в боте
**Проблема**: `ModuleNotFoundError: No module named 'tg_bot'`

**Решение**: Убрал префикс `tg_bot.` из всех импортов в файлах:
- `tg_bot/handlers/users.py`
- `tg_bot/handlers/start.py`
- `tg_bot/handlers/start_mini_app.py`
- `tg_bot/handlers/timeslots.py`

## 🚀 Способы запуска

### Вариант 1: Быстрый тест (рекомендуется)
```bash
python quick_test.py
```

### Вариант 2: Полный тест
```bash
python test_local.py
```

### Вариант 3: С HTTPS
```bash
# Установите ngrok
brew install ngrok

# Запустите с HTTPS
python start_mini_app_https.py
```

### Вариант 4: Ручной запуск
```bash
# Терминал 1: Бэкенд
cd backend
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000

# Терминал 2: Фронтенд
cd frontend
python server.py

# Терминал 3: Бот
cd tg_bot
python main.py
```

## 🌐 Доступные URL

После запуска:
- **Frontend**: http://localhost:3000/index.html
- **API документация**: http://localhost:8000/api/docs
- **API**: http://localhost:8000/api

## 📱 Тестирование в браузере

1. Откройте http://localhost:3000/test_in_browser.html
2. Следуйте инструкциям на странице
3. Или выполните в консоли браузера:
```javascript
window.Telegram = {
    WebApp: {
        ready: () => console.log('Ready'),
        expand: () => console.log('Expanded'),
        initDataUnsafe: {
            user: {
                id: 123456789,
                first_name: 'Тест',
                last_name: 'Пользователь',
                username: 'testuser'
            }
        }
    }
};
```

## 🔍 Отладка

### Проверка логов
- **Бэкенд**: смотрите в терминале где запущен uvicorn
- **Фронтенд**: смотрите в терминале где запущен server.py
- **Бот**: смотрите в терминале где запущен бот

### Проверка API
```bash
curl http://localhost:8000/api/docs
```

### Проверка фронтенда
```bash
curl http://localhost:3000/index.html
```

## ⚠️ Важные моменты

1. **Убедитесь, что все зависимости установлены**:
   ```bash
   pip install fastapi uvicorn aiogram httpx
   ```

2. **Настройте токен бота** в `tg_bot/constants.py`:
   ```python
   BOT_TOKEN = "ваш_токен_от_botfather"
   ```

3. **Для Telegram тестирования** нужен HTTPS URL (используйте ngrok)

4. **Если что-то не работает**, проверьте:
   - Все ли порты свободны (8000, 3000)
   - Правильно ли настроен токен бота
   - Доступен ли бэкенд по адресу http://localhost:8000

## 🎯 Результат

После исправлений:
- ✅ Бэкенд запускается без ошибок
- ✅ Бот запускается без ошибок
- ✅ Фронтенд работает корректно
- ✅ Mini App можно тестировать в браузере
- ✅ Все импорты работают правильно 