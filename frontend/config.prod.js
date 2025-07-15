// Конфигурация для продакшена
// Скопируйте этот файл в config.js и измените URL на ваши

const config = {
    // API URL - замените на ваш продакшн URL
    API_BASE_URL: 'https://your-domain.com/api',
    
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
    },
    
    // Настройки для продакшена
    PRODUCTION: {
        debug: false,
        logLevel: 'error',
        enableAnalytics: true
    }
};

// Экспорт конфигурации
if (typeof module !== 'undefined' && module.exports) {
    module.exports = config;
} else {
    window.APP_CONFIG = config;
} 