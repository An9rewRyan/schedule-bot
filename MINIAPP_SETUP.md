# 🚀 Автоматический запуск Mini App с HTTPS

Этот набор скриптов автоматизирует запуск Mini App с HTTPS поддержкой через ngrok.

## 📋 Что делает скрипт

1. **Запускает ngrok** по конфигурации из `ngrok.yml`
2. **Автоматически обновляет CORS** настройки в backend
3. **Обновляет URL** в frontend и Telegram боте
4. **Запускает все сервисы** (backend, frontend, bot)
5. **Показывает все URL** для настройки

## 🔧 Использование

### Запуск всех сервисов:
```bash
python start_miniapp_https.py
```

### Остановка всех сервисов:
```bash
python stop_miniapp.py
```

## 📁 Файлы конфигурации

### `ngrok.yml`
```yaml
version: "2"
authtoken: YOUR_AUTHTOKEN

tunnels:
  frontend:
    proto: http
    addr: 3000
    
  backend:
    proto: http
    addr: 8000
```

## 🎯 Что происходит при запуске

1. **Остановка старых процессов**
   - Убивает все процессы ngrok
   - Освобождает порты 8000, 3000, 4040

2. **Запуск ngrok**
   - Запускает туннели по конфигурации
   - Получает новые HTTPS URL

3. **Обновление конфигураций**
   - `backend/src/main.py` - обновляет CORS origins
   - `frontend/app.js` - обновляет backend URL
   - `tg_bot/handlers/start.py` - обновляет Mini App URL

4. **Запуск сервисов**
   - Backend на порту 8000
   - Frontend на порту 3000  
   - Telegram бот

## 📱 Настройка в Telegram

После запуска скрипта используйте показанный URL для настройки Mini App в BotFather:

```
Mini App URL: https://XXXXXX.ngrok-free.app
```

## 🛠 Отладка

### Проверка статуса ngrok:
```bash
curl http://localhost:4040/api/tunnels | python -m json.tool
```

### Проверка backend:
```bash
curl http://localhost:8000/health
```

### Проверка frontend:
```bash
curl http://localhost:3000
```

## 🔄 Автоматические обновления

Скрипт автоматически:
- ✅ Обновляет CORS настройки с новыми ngrok URL
- ✅ Обновляет frontend конфигурацию
- ✅ Обновляет Telegram bot конфигурацию
- ✅ Показывает все необходимые URL

## 🚨 Остановка

Для корректной остановки всех сервисов:
- Нажмите `Ctrl+C` в терминале с запущенным скриптом
- Или запустите `python stop_miniapp.py`

## 📝 Логи

Каждый сервис логируется в отдельный файл в директории `logs/`:

### Файлы логов:
- `miniapp_starter.log` - основной лог запуска и управления
- `ngrok.log` - логи ngrok туннелей
- `backend.log` - логи backend сервера (FastAPI)
- `frontend.log` - логи frontend сервера
- `telegram_bot.log` - логи Telegram бота

### Команды для просмотра логов:

```bash
# Просмотр всех логов
python view_logs.py

# Просмотр конкретного сервиса
python view_logs.py -s backend
python view_logs.py -s frontend
python view_logs.py -s ngrok
python view_logs.py -s bot
python view_logs.py -s main

# Мониторинг в реальном времени
python view_logs.py -f backend.log
python view_logs.py -f telegram_bot.log

# Показать последние N строк
python view_logs.py -t 100

# Список файлов логов
python view_logs.py -l
```

### Пример использования:
```bash
# Запуск всех сервисов
python start_miniapp_https.py

# В другом терминале - мониторинг backend
python view_logs.py -f backend.log

# В третьем терминале - мониторинг бота
python view_logs.py -f telegram_bot.log
```

## ⚠️ Требования

- Python 3.7+
- ngrok установлен и настроен
- Все зависимости установлены (`pip install -r requirements.txt`)
- Настроенная база данных PostgreSQL 