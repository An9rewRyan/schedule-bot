# 📊 Руководство по системе логирования Mini App

## 🎯 Обзор

Система автоматического логирования записывает работу каждого сервиса в отдельный файл, что позволяет:
- Отслеживать ошибки каждого компонента отдельно
- Мониторить производительность сервисов
- Анализировать логи без смешивания разных сервисов
- Архивировать логи для дальнейшего анализа

## 📁 Структура логов

```
logs/
├── miniapp_starter.log    # Основной лог управления
├── ngrok.log             # Логи ngrok туннелей
├── backend.log           # Логи FastAPI сервера
├── frontend.log          # Логи frontend сервера
└── telegram_bot.log      # Логи Telegram бота
```

## 🔧 Команды просмотра логов

### Основные команды:

```bash
# Показать все логи всех сервисов
python view_logs.py

# Показать логи конкретного сервиса
python view_logs.py -s main      # Основной лог
python view_logs.py -s backend   # Backend сервер
python view_logs.py -s frontend  # Frontend сервер
python view_logs.py -s ngrok     # Ngrok туннели
python view_logs.py -s bot       # Telegram бот
```

### Продвинутые команды:

```bash
# Мониторинг в реальном времени (как tail -f)
python view_logs.py -f backend.log
python view_logs.py -f telegram_bot.log

# Показать последние N строк
python view_logs.py -t 100       # Последние 100 строк всех логов
python view_logs.py -s backend -t 50  # Последние 50 строк backend

# Информация о файлах логов
python view_logs.py -l           # Список файлов с размерами
```

## 🚀 Практические примеры

### Запуск с мониторингом:

**Терминал 1** - Запуск сервисов:
```bash
python start_miniapp_https.py
```

**Терминал 2** - Мониторинг backend:
```bash
python view_logs.py -f backend.log
```

**Терминал 3** - Мониторинг бота:
```bash
python view_logs.py -f telegram_bot.log
```

### Отладка ошибок:

```bash
# Проверить последние ошибки всех сервисов
python view_logs.py -t 20

# Найти ошибки в backend
python view_logs.py -s backend -t 100 | grep -i error

# Мониторить ngrok для проблем с туннелями
python view_logs.py -f ngrok.log
```

### Анализ производительности:

```bash
# Проверить время запуска сервисов
python view_logs.py -s main

# Анализ запросов к API
python view_logs.py -s backend | grep "ВХОДЯЩИЙ ЗАПРОС"

# Проверить статус ngrok туннелей
python view_logs.py -s ngrok
```

## 📊 Что логируется

### miniapp_starter.log:
- Запуск и остановка сервисов
- Получение ngrok URL
- Обновление конфигураций
- Общий статус системы

### backend.log:
- Запуск FastAPI сервера
- Все HTTP запросы и ответы
- Ошибки API
- Время обработки запросов
- CORS запросы

### frontend.log:
- Запуск HTTP сервера
- Обслуживание статических файлов
- Ошибки сервера

### telegram_bot.log:
- Запуск Telegram бота
- Обработка команд
- Ошибки бота
- Взаимодействие с пользователями

### ngrok.log:
- Статус туннелей
- Подключения
- Ошибки туннелирования

## 🛠 Настройка логирования

Логирование настраивается автоматически при запуске `start_miniapp_https.py`:

1. **Создается директория** `logs/`
2. **Очищаются старые логи** при каждом запуске
3. **Настраивается форматирование** с временными метками
4. **Перенаправляется вывод** каждого сервиса в свой файл

## 🔍 Поиск и фильтрация

### Поиск ошибок:
```bash
# Все ошибки
python view_logs.py | grep -i error

# Ошибки backend
python view_logs.py -s backend | grep -i error

# Ошибки с контекстом
python view_logs.py -s backend | grep -B 2 -A 2 -i error
```

### Фильтрация по времени:
```bash
# Логи за последние 10 минут (примерно)
python view_logs.py -t 200

# Конкретное время
python view_logs.py -s backend | grep "17:52:"
```

### Анализ трафика:
```bash
# Все HTTP запросы
python view_logs.py -s backend | grep "ВХОДЯЩИЙ ЗАПРОС"

# Только POST запросы
python view_logs.py -s backend | grep "POST"

# Время обработки запросов
python view_logs.py -s backend | grep "Время обработки"
```

## 🎛 Автоматизация

### Скрипт для автоматического мониторинга:
```bash
#!/bin/bash
# monitor.sh
python view_logs.py -f backend.log &
python view_logs.py -f telegram_bot.log &
wait
```

### Архивирование логов:
```bash
# Создать архив логов
tar -czf logs_$(date +%Y%m%d_%H%M%S).tar.gz logs/

# Очистить старые логи
rm -rf logs/*
```

## 📈 Мониторинг в продакшене

Для продакшена рекомендуется:

1. **Ротация логов** - настроить logrotate
2. **Централизованное логирование** - использовать ELK stack
3. **Алерты** - настроить уведомления об ошибках
4. **Метрики** - собирать статистику из логов

## 🆘 Частые проблемы

### Логи не создаются:
```bash
# Проверить права доступа
ls -la logs/

# Проверить, запущен ли основной процесс
ps aux | grep start_miniapp_https.py
```

### Файлы логов пустые:
```bash
# Проверить, что процессы запущены
ps aux | grep -E "(ngrok|python.*main|python.*start_miniapp)"

# Проверить статус сервисов
curl http://localhost:8000/health
curl http://localhost:3000
```

### Логи слишком большие:
```bash
# Проверить размер файлов
python view_logs.py -l

# Очистить логи
rm -rf logs/*.log
```

## 🎯 Заключение

Система логирования предоставляет полную видимость работы всех компонентов Mini App. Используйте различные команды для мониторинга, отладки и анализа производительности вашего приложения. 