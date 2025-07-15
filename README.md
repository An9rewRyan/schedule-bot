# Telegram Mini App - Система записи на тренировки

Telegram Mini App для записи на тренировки с современным веб-интерфейсом и FastAPI бэкендом.

## 🚀 Быстрый запуск

### Вариант 1: Локальный запуск (без HTTPS)
```bash
python start_mini_app_local.py
```

### Вариант 2: Запуск с HTTPS через ngrok
```bash
python start_mini_app_https.py
```

### Вариант 3: Проверка и установка ngrok
```bash
python check_ngrok.py
```

## 🔧 Решение проблем

### Проблемы с ngrok

Если у вас возникают ошибки с ngrok:

1. **Проверьте установку ngrok:**
   ```bash
   python check_ngrok.py
   ```

2. **Установите ngrok вручную:**
   - macOS: `brew install ngrok`
   - Windows/Linux: скачайте с https://ngrok.com/download

3. **Настройте authtoken:**
   ```bash
   ngrok config add-authtoken YOUR_TOKEN
   ```

4. **Если ngrok не работает, используйте локальную версию:**
   ```bash
   python start_mini_app_local.py
   ```

### Проблемы с импортами

Если возникают ошибки `ModuleNotFoundError`:

1. **Убедитесь, что вы в корневой папке проекта**
2. **Активируйте виртуальное окружение:**
   ```bash
   source .venv/bin/activate  # macOS/Linux
   # или
   .venv\Scripts\activate     # Windows
   ```

3. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

### Проблемы с ботом

1. **Создайте файл `tg_bot/constants.py`:**
   ```python
   BOT_TOKEN = "ваш_токен_бота"
   ```

2. **Получите токен у @BotFather в Telegram**

## 📁 Структура проекта

```
schedule-bot-1/
├── backend/           # FastAPI бэкенд
│   ├── src/
│   │   ├── api/      # API endpoints
│   │   ├── models/   # База данных
│   │   └── services/ # Бизнес-логика
│   └── requirements.txt
├── frontend/          # Mini App интерфейс
│   ├── index.html    # Главная страница
│   ├── style.css     # Стили
│   ├── script.js     # JavaScript
│   └── server.py     # Локальный сервер
├── tg_bot/           # Telegram бот
│   ├── handlers/     # Обработчики команд
│   ├── keyboards/    # Клавиатуры
│   └── main.py       # Основной файл бота
└── scripts/          # Скрипты запуска
```

## 🌐 Доступные URL

После запуска:

- **Бэкенд API:** http://localhost:8000/api
- **Документация API:** http://localhost:8000/api/docs
- **Фронтенд (локально):** http://localhost:3000/index.html
- **Фронтенд (HTTPS):** https://your-ngrok-url.ngrok.io/index.html

## 📱 Тестирование

### В браузере
1. Откройте http://localhost:3000/index.html
2. Используйте тестовую страницу для симуляции Telegram Web App

### В Telegram
1. Создайте Mini App в @BotFather
2. Укажите URL вашего фронтенда
3. Протестируйте через бота

## 🔧 Настройка

### 1. Создание бота
1. Напишите @BotFather в Telegram
2. Создайте нового бота: `/newbot`
3. Получите токен и сохраните в `tg_bot/constants.py`

### 2. Создание Mini App
1. Напишите @BotFather: `/newapp`
2. Выберите вашего бота
3. Укажите название и описание
4. Добавьте URL фронтенда

### 3. Настройка базы данных
1. Установите PostgreSQL
2. Создайте базу данных
3. Обновите настройки в `backend/src/repository/db.py`

## 🛠️ Разработка

### Запуск отдельных сервисов

**Бэкенд:**
```bash
cd backend
python -m uvicorn src.main:app --reload
```

**Фронтенд:**
```bash
cd frontend
python server.py
```

**Бот:**
```bash
cd tg_bot
python main.py
```

### Добавление новых функций

1. **API endpoints:** `backend/src/api/endpoints/`
2. **Модели БД:** `backend/src/models/`
3. **Фронтенд:** `frontend/`
4. **Обработчики бота:** `tg_bot/handlers/`

## 📋 Требования

- Python 3.8+
- PostgreSQL
- ngrok (для HTTPS)
- Telegram Bot Token

## 🚀 Развертывание

### Локальное развертывание
```bash
# Клонируйте репозиторий
git clone <repository-url>
cd schedule-bot-1

# Создайте виртуальное окружение
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# или .venv\Scripts\activate  # Windows

# Установите зависимости
pip install -r requirements.txt

# Запустите проект
python start_mini_app_local.py
```

### Продакшн развертывание
1. Настройте HTTPS сервер (nginx + SSL)
2. Разверните бэкенд на сервере
3. Настройте домен для фронтенда
4. Обновите URL в настройках бота

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для новой функции
3. Внесите изменения
4. Создайте Pull Request

## 📄 Лицензия

MIT License
