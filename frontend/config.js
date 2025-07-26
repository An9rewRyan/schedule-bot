// Конфигурация для Telegram Mini App
const config = {
    // API URL - замените на ваш бэкенд URL
    API_BASE_URL: 'https://7db1d64ccc1e.ngrok-free.app/api',
    
    // Mini App настройки
    MINI_APP: {
        title: 'Запись на тренировки',
        description: 'Система бронирования тренировок',
        version: '1.0.0'
    },
    
    // Настройки темы
    THEME: {
        primaryColor: '#2481cc',
        secondaryColor: '#f5f5f5',
        successColor: '#4CAF50',
        errorColor: '#f44336',
        warningColor: '#ff9800'
    },
    
    // Настройки тренировок
    TRAINING: {
        duration: 90, // длительность в минутах
        maxVisitors: 4, // максимальное количество посетителей
        timeSlots: 30 // длительность слота в минутах
    },
    
    // Настройки локализации
    LOCALE: {
        language: 'ru',
        dateFormat: 'ru-RU',
        timeFormat: 'HH:mm'
    }
};

// Экспорт конфигурации
if (typeof module !== 'undefined' && module.exports) {
    module.exports = config;
} else {
    // Делаем конфигурацию доступной глобально
    window.config = config;
    window.APP_CONFIG = config; // Оставляем для обратной совместимости
} 