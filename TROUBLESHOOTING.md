# 🔧 Устранение неполадок

## Диагностика проблем

Запустите диагностический скрипт для выявления проблем:

```bash
python diagnose.py
```

## Частые проблемы и решения

### 1. Ошибки с ngrok

**Проблема:** `HTTPConnectionPool(host='localhost', port=4040): Max retries exceeded`

**Решение:**
1. Проверьте установку ngrok:
   ```bash
   python check_ngrok.py
   ```

2. Если ngrok не установлен:
   ```bash
   # macOS
   brew install ngrok
   
   # Windows/Linux
   # Скачайте с https://ngrok.com/download
   ```

3. Настройте authtoken:
   ```bash
   ngrok config add-authtoken YOUR_TOKEN
   ```

4. Если ngrok не работает, используйте локальную версию:
   ```bash
   python start_mini_app_local.py
   ```

### 2. Ошибки импорта модулей

**Проблема:** `ModuleNotFoundError: No module named 'api'`

**Решение:**
1. Убедитесь, что вы в корневой папке проекта
2. Активируйте виртуальное окружение:
   ```bash
   source .venv/bin/activate  # macOS/Linux
   # или
   .venv\Scripts\activate     # Windows
   ```
3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

### 3. Проблемы с ботом

**Проблема:** Бот не запускается или не отвечает

**Решение:**
1. Создайте файл `tg_bot/constants.py`:
   ```python
   BOT_TOKEN = "ваш_реальный_токен_бота"
   ```

2. Получите токен у @BotFather в Telegram:
   - Напишите @BotFather
   - Выполните `/newbot`
   - Скопируйте полученный токен

### 4. Проблемы с портами

**Проблема:** Порт уже занят

**Решение:**
1. Найдите процесс, использующий порт:
   ```bash
   # macOS/Linux
   lsof -i :8000
   lsof -i :3000
   
   # Windows
   netstat -ano | findstr :8000
   netstat -ano | findstr :3000
   ```

2. Остановите процесс или измените порт в настройках

### 5. Проблемы с базой данных

**Проблема:** Ошибки подключения к БД

**Решение:**
1. Установите PostgreSQL
2. Создайте базу данных
3. Обновите настройки в `backend/src/repository/db.py`

### 6. Проблемы с CORS

**Проблема:** Ошибки CORS в браузере

**Решение:**
1. Проверьте настройки CORS в `backend/src/main.py`
2. Добавьте ваш домен в `allow_origins`
3. Перезапустите бэкенд

## Команды для быстрого исправления

### Полная диагностика
```bash
python diagnose.py
```

### Проверка ngrok
```bash
python check_ngrok.py
```

### Локальный запуск (без HTTPS)
```bash
python start_mini_app_local.py
```

### Запуск с HTTPS
```bash
python start_mini_app_https.py
```

### Установка зависимостей
```bash
pip install -r requirements.txt
```

### Очистка и переустановка
```bash
# Удалите виртуальное окружение
rm -rf .venv

# Создайте новое
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Логи и отладка

### Просмотр логов бэкенда
```bash
cd backend
python -m uvicorn src.main:app --reload --log-level debug
```

### Просмотр логов бота
```bash
cd tg_bot
python main.py
```

### Тестирование API
```bash
# Проверка бэкенда
curl http://localhost:8000/api

# Проверка фронтенда
curl http://localhost:3000
```

## Получение помощи

Если проблема не решается:

1. Запустите диагностику: `python diagnose.py`
2. Проверьте логи сервисов
3. Убедитесь, что все зависимости установлены
4. Проверьте настройки файлов конфигурации

## Альтернативные решения

### Если ngrok не работает
- Используйте локальную версию: `python start_mini_app_local.py`
- Настройте другой туннель (localtunnel, serveo)
- Разверните на хостинге с HTTPS

### Если бот не работает
- Проверьте токен в `tg_bot/constants.py`
- Убедитесь, что бот не заблокирован
- Проверьте права бота в Telegram

### Если фронтенд не работает
- Проверьте файлы в папке `frontend/`
- Убедитесь, что сервер запущен на порту 3000
- Проверьте консоль браузера на ошибки JavaScript 