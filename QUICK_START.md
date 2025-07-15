# 🚀 Быстрый старт Telegram Mini App

## Что это?

Telegram Mini App версия системы записи на тренировки. Пользователи могут записываться через удобный веб-интерфейс прямо в Telegram.

## ⚡ Быстрый запуск

### 1. Установка зависимостей

```bash
# Создание виртуального окружения
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# или .venv\Scripts\activate  # Windows

# Установка зависимостей
pip install -r requirements.txt
```

### 2. Настройка токена бота

Создайте файл `tg_bot/constants.py`:
```python
BOT_TOKEN = "ваш_токен_от_botfather"
```

### 3. Запуск проекта

```bash
# Интерактивный запуск с меню выбора
python run_dev.py

# Или автоматический запуск всех сервисов
python run_dev.py all
```

### Варианты запуска:

```bash
python run_dev.py           # Интерактивное меню
python run_dev.py all       # Все сервисы с ngrok
python run_dev.py local     # Без ngrok (только локально)
python run_dev.py backend   # Только backend API
python run_dev.py frontend  # Только frontend
python run_dev.py bot       # Только Telegram bot
python run_dev.py ngrok     # Только ngrok туннели
```

## 🌐 Доступные URL

### С ngrok (рекомендуется для разработки):
- **Mini App**: https://XXXXXX.ngrok-free.app
- **API**: https://YYYYYY.ngrok-free.app/api
- **Документация**: https://YYYYYY.ngrok-free.app/api/docs

### Локально:
- **Mini App**: http://localhost:3000
- **API**: http://localhost:8000/api
- **Документация**: http://localhost:8000/api/docs

## 📱 Создание Mini App в Telegram

1. Откройте @BotFather
2. Отправьте `/newapp`
3. Выберите вашего бота
4. Введите название: "Запись на тренировки"
5. Введите описание: "Система бронирования тренировок"
6. Загрузите иконку (512x512)
7. Введите URL из вывода `run_dev.py all`

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

## ⚙️ Автоматические функции

### Обновление конфигураций
При запуске с ngrok автоматически обновляются:
- ✅ CORS настройки в backend
- ✅ API URL в frontend
- ✅ Mini App URL в Telegram боте
- ✅ Все конфигурационные файлы

### Цветное логирование
Все сервисы логируются с цветными префиксами:
- `[Backend API]` - зеленый
- `[Frontend]` - синий
- `[Telegram Bot]` - фиолетовый
- `[ngrok]` - голубой

### Горячая перезагрузка
- Backend перезагружается при изменении Python файлов
- Frontend обновляется при изменении HTML/CSS/JS
- Bot автоматически подхватывает изменения

## 🔧 Настройка для продакшена

### 1. Разместите frontend

Загрузите файлы из папки `frontend/` на хостинг:
- Vercel: `npx vercel --prod`
- Netlify: перетащите папку в Netlify
- GitHub Pages: включите в настройках репозитория

### 2. Разверните backend

```bash
# На сервере
cd backend
uvicorn src.main:app --host 0.0.0.0 --port 8000

# Или с Docker
docker build -t schedule-backend .
docker run -p 8000:8000 schedule-backend
```

### 3. Обновите конфигурацию

В `frontend/config.js`:
```javascript
API_BASE_URL: 'https://your-domain.com/api'
```

В `tg_bot/handlers/start.py`:
```python
MINI_APP_URL = "https://your-domain.com"
```

### 4. Обновите CORS в backend

В `backend/src/main.py`:
```python
allow_origins=[
    "https://web.telegram.org",
    "https://your-domain.com",  # Ваш домен
]
```

## 🎯 Основные функции

### Пользователи могут:
- ✅ Просматривать доступные дни и время
- ✅ Записываться на тренировки
- ✅ Просматривать свои записи
- ✅ Отменять записи

### Администраторы могут:
- ✅ Создавать расписание тренировок
- ✅ Просматривать все записи
- ✅ Управлять пользователями
- ✅ Получать статистику

## 🎨 Кастомизация

### Изменение цветов

В `frontend/styles.css`:
```css
:root {
    --tg-theme-button-color: #007AFF;
    --tg-theme-bg-color: #ffffff;
    --primary-color: #007AFF;
}
```

### Изменение настроек тренировок

В `frontend/config.js`:
```javascript
TRAINING: {
    duration: 90,        // длительность тренировки (минуты)
    maxVisitors: 4,      // максимум посетителей
    timeSlots: 30        // длительность слота (минуты)
}
```

## 🐛 Отладка

### Проверка системы
```bash
python diagnose.py  # Полная диагностика
```

### Проверка логов
```bash
python view_logs.py                 # Все логи
python view_logs.py -s backend      # Только backend
python view_logs.py -f backend.log  # В реальном времени
```

### Проверка API
```bash
# Тест API
curl http://localhost:8000/api/docs

# Проверка пользователя  
curl http://localhost:8000/api/users/check/123456
```

### Устранение проблем

**Ошибки импорта:**
- Активируйте venv: `source .venv/bin/activate`
- Установите зависимости: `pip install -r requirements.txt`

**Проблемы с ngrok:**
- Проверьте: `python check_ngrok.py`
- Используйте локально: `python run_dev.py local`

**Бот не отвечает:**
- Проверьте токен в `tg_bot/constants.py`
- Убедитесь что бот запущен

## 🎉 Результат

После успешного запуска у вас будет:
- ✅ Работающий Mini App в Telegram
- ✅ REST API с документацией
- ✅ Telegram бот с командами
- ✅ Веб-интерфейс для записи
- ✅ Автоматическое обновление конфигураций
- ✅ Цветные логи всех сервисов 