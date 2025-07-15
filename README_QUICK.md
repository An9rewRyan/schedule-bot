# 🚀 Быстрый старт Mini App

## Запуск всех сервисов одной командой:

```bash
python run_dev.py all
```

## Остановка всех сервисов:

```bash
python stop_miniapp.py
```

## Интерактивный запуск:

```bash
python run_dev.py
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

## 🎛️ Интерактивное меню

При запуске `python run_dev.py` доступны опции:

```
🚀 Выберите сервисы для запуска:
1. Backend API (порт 8000)
2. Frontend Server (порт 3000)
3. Telegram Bot
4. ngrok туннели
5. Backend + Bot
6. Frontend + ngrok
7. Все сервисы (Backend + Frontend + Bot + ngrok)
8. Локальный запуск (без ngrok)
9. Обновить конфигурацию ngrok
0. Выход
```

## 📋 Команды запуска

```bash
python run_dev.py           # Интерактивное меню
python run_dev.py all       # Все сервисы с ngrok
python run_dev.py local     # Локальный запуск (без ngrok)
python run_dev.py backend   # Только backend API
python run_dev.py frontend  # Только frontend
python run_dev.py bot       # Только Telegram bot
python run_dev.py ngrok     # Только ngrok туннели

python stop_miniapp.py      # Остановка всех сервисов
python stop_miniapp.py bot  # Остановка конкретного сервиса
```

## 📱 Настройка Mini App в Telegram:

1. Откройте @BotFather в Telegram
2. Выберите вашего бота
3. Bot Settings → Menu Button → Configure menu button
4. Введите URL из вывода `python run_dev.py all`

## 🎨 Автоматические функции

### Цветное логирование
Все сервисы логируются с цветными префиксами:
- `[Backend API]` - зеленый
- `[Frontend]` - синий
- `[Telegram Bot]` - фиолетовый
- `[ngrok]` - голубой

### Горячая перезагрузка
- Backend: автоматическая перезагрузка при изменении Python файлов
- Frontend: обновление при изменении HTML/CSS/JS
- Bot: перезапуск при изменениях

## 📊 Логирование и диагностика:

```bash
# Просмотр логов
python view_logs.py           # Все логи
python view_logs.py -s backend # Только backend
python view_logs.py -f         # В реальном времени

# Диагностика
python diagnose.py            # Проверка системы
python check_ngrok.py         # Проверка ngrok

# Очистка данных
python clear_timeslots.py     # Очистка временных слотов
```

## 🔧 Решение проблем

### Ошибки запуска
1. Активируйте виртуальное окружение: `source .venv/bin/activate`
2. Установите зависимости: `pip install -r requirements.txt`
3. Проверьте токен бота в `tg_bot/constants.py`

### Проблемы с ngrok
1. Проверьте установку: `python check_ngrok.py`
2. Используйте локальный запуск: `python run_dev.py local`

### Бот не отвечает
1. Убедитесь что токен правильный в `tg_bot/constants.py`
2. Проверьте что бот запущен: посмотрите логи `[Telegram Bot]`

## 🎯 Результат

После успешного запуска у вас будет:
- ✅ Работающий Mini App в Telegram
- ✅ REST API с документацией на `/api/docs`
- ✅ Telegram бот с командами
- ✅ Автоматическое обновление всех конфигураций
- ✅ Цветные логи всех сервисов в одном терминале 