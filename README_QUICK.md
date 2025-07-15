# 🚀 Быстрый старт Mini App

## Запуск всех сервисов одной командой:

```bash
python start_miniapp_https.py
```

## Остановка всех сервисов:

```bash
python stop_miniapp.py
```

## Что получаете:

✅ **Автоматически запускается:**
- ngrok туннели (frontend + backend)
- Backend сервер на порту 8000
- Frontend сервер на порту 3000  
- Telegram бот

✅ **Автоматически обновляется:**
- CORS настройки в backend
- URL в frontend
- Mini App URL в Telegram боте

✅ **Готовые URL для использования:**
- Frontend: https://XXXXXX.ngrok-free.app
- Backend: https://YYYYYY.ngrok-free.app

## Текущие активные URL:

- **Frontend**: https://f903f3cfcd39.ngrok-free.app
- **Backend**: https://7d766736699d.ngrok-free.app

## Настройка Mini App в Telegram:

1. Откройте @BotFather в Telegram
2. Выберите вашего бота
3. Bot Settings → Menu Button → Configure menu button
4. Введите URL: `https://f903f3cfcd39.ngrok-free.app`

## 📊 Логирование:

Каждый сервис логируется в отдельный файл в директории `logs/`:

```bash
# Просмотр всех логов
python view_logs.py

# Просмотр конкретного сервиса
python view_logs.py -s backend
python view_logs.py -s frontend
python view_logs.py -s ngrok
python view_logs.py -s bot

# Мониторинг в реальном времени
python view_logs.py -f backend.log

# Список файлов логов
python view_logs.py -l
```

**Файлы логов:**
- `miniapp_starter.log` - основной лог запуска
- `ngrok.log` - логи ngrok туннелей
- `backend.log` - логи backend сервера
- `frontend.log` - логи frontend сервера
- `telegram_bot.log` - логи Telegram бота

## Отладка:

```bash
# Проверка статуса
curl http://localhost:8000/health
curl http://localhost:3000

# Проверка ngrok
curl http://localhost:4040/api/tunnels | python -m json.tool
```

🎯 **Готово к использованию!** 