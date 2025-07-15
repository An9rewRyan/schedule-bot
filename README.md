# Telegram Mini App - Система записи на тренировки

Telegram Mini App для записи на тренировки с современным веб-интерфейсом и FastAPI бэкендом.

## 🚀 Быстрый запуск

### Автоматический запуск (рекомендуется)
```bash
# Интерактивное меню
python run_dev.py

# Или запуск всех сервисов сразу
python run_dev.py all
```

### Запуск отдельных сервисов
```bash
python run_dev.py backend   # Backend API (порт 8000)
python run_dev.py frontend  # Frontend Server (порт 3000)  
python run_dev.py bot       # Telegram Bot
python run_dev.py ngrok     # ngrok туннели
python run_dev.py local     # Backend + Frontend + Bot (без ngrok)

# Остановка сервисов
python stop_miniapp.py       # Остановка всех сервисов
```

## 📁 Структура проекта

```
schedule-bot-1/
├── run_dev.py            # 🚀 Основной скрипт запуска
├── update_config.py      # 🔧 Обновление конфигураций
├── backend/              # FastAPI бэкенд
│   ├── src/
│   │   ├── api/         # API endpoints и роутеры
│   │   ├── models/      # Модели базы данных и схемы
│   │   ├── services/    # Бизнес-логика
│   │   ├── repository/  # Работа с БД и CRUD операции
│   │   └── utilities/   # Утилиты и исключения
│   └── requirements.txt
├── frontend/             # Mini App интерфейс
│   ├── index.html       # Главная страница
│   ├── styles.css       # Стили
│   ├── app.js          # JavaScript логика
│   ├── config.js       # Конфигурация API
│   └── server.py       # Локальный сервер
├── tg_bot/              # Telegram бот
│   ├── handlers/        # Обработчики команд
│   ├── keyboards/       # Клавиатуры
│   ├── api/            # API клиенты
│   ├── middlewares/    # Мидлвары
│   └── main.py         # Основной файл бота
└── logs/               # Логи всех сервисов
```

## ⚙️ Настройка

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

### 3. Настройка ngrok (для HTTPS)
```bash
# Проверка и настройка ngrok
python check_ngrok.py

# Ручная установка (если нужно)
# macOS: brew install ngrok
# Windows/Linux: скачайте с https://ngrok.com/download

# Настройка authtoken
ngrok config add-authtoken YOUR_TOKEN
```

## 🌐 Доступные URL

После запуска с ngrok (`python run_dev.py all`):
- **Frontend (HTTPS):** https://XXXXXX.ngrok-free.app
- **Backend API (HTTPS):** https://YYYYYY.ngrok-free.app/api
- **API Документация:** https://YYYYYY.ngrok-free.app/api/docs

После локального запуска (`python run_dev.py local`):
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000/api
- **API Документация:** http://localhost:8000/api/docs

## 📱 Настройка Mini App в Telegram

1. Откройте @BotFather в Telegram
2. Выберите команду `/newapp` 
3. Выберите вашего бота
4. Введите название: "Запись на тренировки"
5. Введите описание: "Система бронирования тренировок"
6. Введите URL Mini App (покажется после запуска `run_dev.py all`)

## 🎯 Основные функции

### Для пользователей:
- ✅ Просмотр доступных временных слотов
- ✅ Выбор времени тренировки
- ✅ Подтверждение записи
- ✅ Просмотр своих записей
- ✅ Отмена записей

### Для администраторов:
- ✅ Просмотр всех записей
- ✅ Создание расписания тренировок
- ✅ Управление пользователями
- ✅ Статистика посещений

## 🔧 Разработка

### Горячая перезагрузка
Все сервисы запускаются с автоматической перезагрузкой при изменении файлов:
- Backend: uvicorn с флагом `--reload`
- Frontend: встроенный сервер с автообновлением
- Bot: автоматический перезапуск при изменениях

### Логирование
Все логи отображаются в терминале с цветными префиксами:
- `[Backend API]` - зеленый
- `[Frontend]` - синий  
- `[Telegram Bot]` - фиолетовый
- `[ngrok]` - голубой

### Обновление конфигураций
При запуске с ngrok автоматически обновляются:
- CORS настройки в backend
- API URL в frontend
- Mini App URL в боте

## 🐛 Отладка

### Проверка системы
```bash
python diagnose.py  # Полная диагностика проекта
```

### Просмотр логов
```bash
python view_logs.py           # Все логи
python view_logs.py -s backend # Только backend
python view_logs.py -f         # В реальном времени
```

### Очистка данных
```bash
python clear_timeslots.py    # Очистка временных слотов
```

## 🛠️ Устранение неполадок

### Ошибки импорта
1. Убедитесь, что виртуальное окружение активировано
2. Установите зависимости: `pip install -r requirements.txt`

### Проблемы с ngrok
1. Проверьте установку: `python check_ngrok.py`
2. Используйте локальный запуск: `python run_dev.py local`

### Проблемы с ботом
1. Проверьте токен в `tg_bot/constants.py`
2. Убедитесь, что бот запущен: `/start` в Telegram

## 📋 Требования

- **Python:** 3.10+
- **PostgreSQL:** 12+ (или SQLite для разработки)
- **ngrok:** Для HTTPS поддержки (опционально)
- **Telegram Bot Token:** От @BotFather

## 🚀 Развертывание в продакшене

### Подготовка
1. Настройте PostgreSQL базу данных
2. Обновите переменные окружения
3. Настройте HTTPS домен

### Развертывание backend
```bash
cd backend
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

### Развертывание frontend
Загрузите файлы из `frontend/` на веб-сервер или CDN.

### Развертывание бота
```bash
cd tg_bot  
python main.py
```

## 📄 Лицензия

Этот проект распространяется под лицензией Creative Commons BY-NC-SA 4.0:
- ✅ Можно изучать и улучшать код
- ✅ Можно использовать в некоммерческих целях
- ❌ Запрещено коммерческое использование
- ❌ При модификации должна сохраняться та же лицензия

## 🤝 Вклад в проект

1. Fork репозитория
2. Создайте ветку для новой функции
3. Внесите изменения
4. Создайте Pull Request

## 📞 Поддержка

При возникновении проблем:
1. Проверьте [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Запустите диагностику: `python diagnose.py`
3. Создайте Issue с описанием проблемы

## 📄 Лицензия

CC BY-NC-SA 4.0
