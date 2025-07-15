# 📱 Настройка Telegram Mini App

Подробное руководство по настройке и развертыванию Telegram Mini App для системы записи на тренировки.

## 🏗️ Архитектура проекта

```
schedule-bot-1/
├── run_dev.py              # 🚀 Основной скрипт запуска
├── update_config.py        # 🔧 Автообновление конфигураций  
├── ngrok.yml              # 🌐 Конфигурация ngrok туннелей
├── backend/               # FastAPI REST API
│   ├── src/
│   │   ├── api/          # Endpoints и роутеры
│   │   ├── models/       # Модели БД и схемы
│   │   ├── services/     # Бизнес-логика
│   │   ├── repository/   # CRUD операции
│   │   └── utilities/    # Утилиты и исключения
│   └── requirements.txt
├── frontend/              # Mini App веб-интерфейс
│   ├── index.html        # Главная страница
│   ├── styles.css        # CSS стили
│   ├── app.js           # JavaScript логика
│   ├── config.js        # Конфигурация API
│   └── server.py        # Локальный dev сервер
├── tg_bot/               # Telegram бот
│   ├── handlers/         # Обработчики команд
│   ├── keyboards/        # Inline клавиатуры
│   ├── api/             # API клиенты
│   ├── middlewares/     # Мидлвары
│   └── main.py          # Основной файл бота
└── logs/                # Логи всех сервисов
```

## ⚙️ Автоматическая настройка

### Быстрый старт (рекомендуется)

```bash
# 1. Установка зависимостей
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
pip install -r requirements.txt

# 2. Настройка токена бота
echo 'BOT_TOKEN = "YOUR_TOKEN_HERE"' > tg_bot/constants.py

# 3. Запуск всех сервисов
python run_dev.py all
```

### Что происходит автоматически:

1. **Запуск ngrok** с конфигурацией из `ngrok.yml`
2. **Получение HTTPS URLs** для frontend и backend
3. **Автообновление CORS** настроек в backend
4. **Обновление API URLs** во frontend и боте
5. **Запуск всех сервисов** с цветными логами
6. **Показ URLs** для настройки в BotFather

## 🔧 Детальная настройка

### Шаг 1: Настройка ngrok

#### 1.1 Установка ngrok
```bash
# macOS
brew install ngrok

# Windows/Linux
# Скачайте с https://ngrok.com/download
```

#### 1.2 Получение authtoken
1. Зарегистрируйтесь на https://ngrok.com
2. Скопируйте ваш authtoken
3. Настройте: `ngrok config add-authtoken YOUR_TOKEN`

#### 1.3 Конфигурация ngrok.yml
```yaml
version: "2"
authtoken: YOUR_AUTHTOKEN_HERE

tunnels:
  frontend:
    proto: http
    addr: 3000
    
  backend:
    proto: http
    addr: 8000
```

### Шаг 2: Настройка backend

#### 2.1 CORS настройки
В `backend/src/main.py` автоматически настраиваются CORS origins:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",     # Локальная разработка
        "http://127.0.0.1:3000",
        "https://web.telegram.org",  # Telegram Web App
        "https://YOUR_NGROK_URL",    # Автообновляется
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### 2.2 База данных
По умолчанию используется SQLite. Для PostgreSQL обновите `backend/src/repository/db.py`:

```python
DATABASE_URL = "postgresql://user:password@localhost/dbname"
```

### Шаг 3: Настройка frontend

#### 3.1 API конфигурация
В `frontend/config.js` автоматически обновляется:

```javascript
const config = {
    API_BASE_URL: 'https://YOUR_BACKEND_NGROK_URL/api',
    TRAINING: {
        duration: 90,        // Длительность тренировки (минуты)
        maxVisitors: 4,      // Максимум участников
        timeSlots: 30        // Длительность слота (минуты)
    }
};
```

#### 3.2 Telegram Web App интеграция
Frontend автоматически определяет окружение:
- В Telegram использует WebApp API
- В браузере симулирует Telegram окружение

### Шаг 4: Настройка Telegram бота

#### 4.1 Создание бота
1. Откройте @BotFather в Telegram
2. Отправьте `/newbot`
3. Следуйте инструкциям
4. Сохраните токен в `tg_bot/constants.py`

#### 4.2 Создание Mini App
1. Отправьте @BotFather команду `/newapp`
2. Выберите вашего бота
3. Введите данные:
   - **Название:** "Запись на тренировки"
   - **Описание:** "Система бронирования тренировок"
   - **URL:** (покажется после запуска `run_dev.py all`)

#### 4.3 Настройка Menu Button
1. Отправьте `/mybots` → выберите бота
2. `Bot Settings` → `Menu Button`
3. `Configure menu button`
4. Введите URL вашего Mini App

## 🚀 Режимы запуска

### Разработка

```bash
# Интерактивный выбор сервисов
python run_dev.py

# Все сервисы с HTTPS через ngrok
python run_dev.py all

# Только локально (без ngrok)
python run_dev.py local

# Отдельные сервисы
python run_dev.py backend
python run_dev.py frontend  
python run_dev.py bot
```

### Отладка

```bash
# Диагностика системы
python diagnose.py

# Просмотр логов
python view_logs.py -s backend
python view_logs.py -f frontend.log

# Очистка данных
python clear_timeslots.py
```

## 🌐 Развертывание в продакшене

### Подготовка

1. **Домен и SSL сертификат**
2. **PostgreSQL база данных**
3. **Сервер** (VPS, cloud instance)

### Backend развертывание

```bash
# На сервере
git clone your-repo
cd schedule-bot-1
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Настройка переменных окружения
export DATABASE_URL="postgresql://..."
export BOT_TOKEN="your_token"

# Запуск
cd backend
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

### Frontend развертывание

#### Статический хостинг
```bash
# Vercel
npx vercel --prod

# Netlify
# Перетащите папку frontend в Netlify

# GitHub Pages
# Включите в настройках репозитория
```

#### Собственный сервер
```bash
# Nginx конфигурация
server {
    listen 80;
    server_name your-domain.com;
    root /path/to/frontend;
    index index.html;
}
```

### Бот развертывание

```bash
# Запуск как сервис (systemd)
sudo nano /etc/systemd/system/schedule-bot.service

[Unit]
Description=Schedule Bot
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/schedule-bot-1/tg_bot
ExecStart=/path/to/.venv/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target

# Активация
sudo systemctl enable schedule-bot
sudo systemctl start schedule-bot
```

### Обновление конфигурации

После развертывания обновите:

#### Frontend config.js
```javascript
API_BASE_URL: 'https://api.your-domain.com'
```

#### Backend CORS
```python
allow_origins=[
    "https://web.telegram.org",
    "https://your-domain.com",
]
```

#### Bot Mini App URL
```python
MINI_APP_URL = "https://your-domain.com"
```

## 🔐 Безопасность

### Рекомендации

1. **Используйте HTTPS** в продакшене
2. **Ограничьте CORS** только нужными доменами
3. **Валидируйте** все входящие данные
4. **Используйте переменные окружения** для секретов
5. **Регулярно обновляйте** зависимости

### Переменные окружения

```bash
# .env файл (не коммитьте!)
BOT_TOKEN=your_telegram_bot_token
DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key
NGROK_AUTHTOKEN=your_ngrok_token
```

## 🐛 Устранение неполадок

### Частые проблемы

| Проблема | Решение |
|----------|---------|
| CORS ошибки | Проверьте настройки в `backend/src/main.py` |
| Бот не отвечает | Проверьте токен в `tg_bot/constants.py` |
| API недоступен | Убедитесь что backend запущен на правильном порту |
| ngrok не работает | Проверьте authtoken: `python check_ngrok.py` |
| Ошибки импорта | Активируйте venv: `source .venv/bin/activate` |

### Логи и диагностика

```bash
# Полная диагностика
python diagnose.py

# Проверка ngrok
python check_ngrok.py

# Просмотр логов
python view_logs.py

# Тест API
curl http://localhost:8000/api/docs
```

## ⚡ Оптимизация производительности

### Backend

- Используйте **connection pooling** для БД
- Настройте **кеширование** (Redis)
- Включите **сжатие** ответов
- Используйте **async/await** во всех endpoint'ах

### Frontend

- Минифицируйте **CSS/JS** файлы
- Используйте **CDN** для статических ресурсов
- Оптимизируйте **изображения**
- Включите **browser caching**

### База данных

- Создайте **индексы** для часто запрашиваемых полей
- Используйте **prepared statements**
- Настройте **connection limits**

## 📊 Мониторинг

### Рекомендуемые инструменты

- **Логирование:** Structured logging с JSON
- **Метрики:** Prometheus + Grafana
- **Ошибки:** Sentry для отслеживания исключений
- **Uptime:** UptimeRobot для мониторинга доступности

### Настройка логирования

```python
# backend/src/main.py
import logging
import structlog

# Structured logging
structlog.configure(
    processors=[
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
)
```

## 🤝 Поддержка

При возникновении проблем:

1. Проверьте [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Запустите диагностику: `python diagnose.py`
3. Просмотрите логи: `python view_logs.py`
4. Создайте Issue с подробным описанием

## 📚 Дополнительные ресурсы

- [Telegram Mini Apps API](https://core.telegram.org/bots/webapps)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [aiogram Documentation](https://docs.aiogram.dev/)
- [ngrok Documentation](https://ngrok.com/docs) 