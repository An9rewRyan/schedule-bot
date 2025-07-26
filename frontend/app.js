// Telegram Web App initialization
let tg = window.Telegram.WebApp;
tg.ready();
tg.expand();

// Подробное логирование Telegram WebApp
console.log('=== TELEGRAM WEBAPP INITIALIZATION ===');
console.log('Telegram WebApp version:', tg.version);
console.log('Telegram WebApp platform:', tg.platform);
console.log('Telegram WebApp initData:', tg.initData);
console.log('Telegram WebApp initDataUnsafe:', tg.initDataUnsafe);
console.log('User data available:', !!tg.initDataUnsafe?.user);
if (tg.initDataUnsafe?.user) {
    console.log('User ID type:', typeof tg.initDataUnsafe.user.id);
    console.log('User ID value:', tg.initDataUnsafe.user.id);
    console.log('User first_name:', tg.initDataUnsafe.user.first_name);
    console.log('User last_name:', tg.initDataUnsafe.user.last_name);
    console.log('User username:', tg.initDataUnsafe.user.username);
}
console.log('=== END TELEGRAM WEBAPP INITIALIZATION ===');

// Улучшенное логирование с debug окном
class DebugLogger {
    constructor() {
        this.logs = [];
        this.maxLogs = 100;
        this.debugDiv = null;
        this.debugBtn = null;
        this.isVisible = false;
        this.init();
    }

    init() {
        this.createDebugUI();
        this.log('🚀 Debug Logger инициализирован');
    }

    createDebugUI() {
        // Debug окно
        this.debugDiv = document.createElement('div');
        this.debugDiv.id = 'debug-console';
        this.debugDiv.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0,0,0,0.95);
            color: #00ff00;
            padding: 20px;
            font-family: 'Courier New', monospace;
            font-size: 11px;
            z-index: 10000;
            overflow-y: auto;
            display: none;
            white-space: pre-wrap;
            word-wrap: break-word;
        `;
        document.body.appendChild(this.debugDiv);

        // Debug кнопка
        this.debugBtn = document.createElement('button');
        this.debugBtn.textContent = '🐛';
        this.debugBtn.style.cssText = `
            position: fixed;
            top: 10px;
            right: 10px;
            z-index: 10001;
            background: #007bff;
            color: white;
            border: none;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            font-size: 16px;
            cursor: pointer;
            box-shadow: 0 2px 10px rgba(0,0,0,0.3);
        `;
        this.debugBtn.onclick = () => this.toggle();
        document.body.appendChild(this.debugBtn);

        // Кнопка очистки логов
        const clearBtn = document.createElement('button');
        clearBtn.textContent = '🗑️ Очистить';
        clearBtn.style.cssText = `
            position: fixed;
            top: 60px;
            right: 10px;
            z-index: 10001;
            background: #dc3545;
            color: white;
            border: none;
            border-radius: 15px;
            padding: 5px 10px;
            font-size: 12px;
            cursor: pointer;
            display: none;
        `;
        clearBtn.onclick = () => this.clear();
        clearBtn.id = 'clear-debug-btn';
        document.body.appendChild(clearBtn);
    }

    log(message, type = 'info') {
        const timestamp = new Date().toLocaleTimeString();
        const logEntry = {
            timestamp,
            message,
            type
        };

        this.logs.push(logEntry);
        if (this.logs.length > this.maxLogs) {
            this.logs.shift();
        }

        const color = this.getColor(type);
        console.log(`%c[${timestamp}] ${message}`, `color: ${color}`);

        this.updateDebugDisplay();
    }

    getColor(type) {
        const colors = {
            'info': '#00ff00',
            'error': '#ff0000',
            'warning': '#ffff00',
            'api': '#00bfff',
            'response': '#ffa500',
            'success': '#00ff00'
        };
        return colors[type] || '#ffffff';
    }

    updateDebugDisplay() {
        if (!this.debugDiv) return;

        const content = this.logs.map(log => {
            const color = this.getColor(log.type);
            return `<span style="color: ${color}">[${log.timestamp}] ${log.message}</span>`;
        }).join('\n');

        this.debugDiv.innerHTML = content;
        this.debugDiv.scrollTop = this.debugDiv.scrollHeight;
    }

    toggle() {
        this.isVisible = !this.isVisible;
        this.debugDiv.style.display = this.isVisible ? 'block' : 'none';
        document.getElementById('clear-debug-btn').style.display = this.isVisible ? 'block' : 'none';
        this.debugBtn.textContent = this.isVisible ? '❌' : '🐛';
    }

    clear() {
        this.logs = [];
        this.updateDebugDisplay();
        this.log('🗑️ Логи очищены');
    }

    // Специальные методы для разных типов сообщений
    apiRequest(url, method, headers, body) {
        this.log(`🌐 ${method} ${url}`, 'api');
        this.log(`📤 Headers: ${JSON.stringify(headers, null, 2)}`, 'api');
        if (body) {
            this.log(`📤 Body: ${JSON.stringify(body, null, 2)}`, 'api');
        }
    }

    apiResponse(url, status, headers, body) {
        const type = status >= 200 && status < 300 ? 'success' : 'error';
        this.log(`📥 Response ${status} from ${url}`, type);
        if (headers) {
            this.log(`📥 Response Headers: ${JSON.stringify(headers, null, 2)}`, 'response');
        }
        if (body) {
            this.log(`📥 Response Body: ${JSON.stringify(body, null, 2)}`, 'response');
        }
    }

    error(message) {
        this.log(`❌ ${message}`, 'error');
    }

    warning(message) {
        this.log(`⚠️ ${message}`, 'warning');
    }

    success(message) {
        this.log(`✅ ${message}`, 'success');
    }
}

// Создаем глобальный экземпляр логгера
const debugLogger = new DebugLogger();

// Добавляем отладочную информацию в интерфейс для Telegram
function addDebugInfo() {
    debugLogger.log('=== TELEGRAM WEBAPP INFO ===');
    debugLogger.log(`Version: ${tg.version}`);
    debugLogger.log(`Platform: ${tg.platform}`);
    debugLogger.log(`User available: ${!!tg.initDataUnsafe?.user}`);

    if (tg.initDataUnsafe?.user) {
        debugLogger.log(`User ID: ${tg.initDataUnsafe.user.id} (${typeof tg.initDataUnsafe.user.id})`);
        debugLogger.log(`User name: ${tg.initDataUnsafe.user.first_name} ${tg.initDataUnsafe.user.last_name || ''}`);
    }
    debugLogger.log('=== END TELEGRAM WEBAPP INFO ===');
}

// Функция для добавления отладочной информации (обратная совместимость)
function debugLog(message) {
    debugLogger.log(message);
}

// Перехватываем ошибки
window.addEventListener('error', (e) => {
    debugLogger.error(`${e.message} at ${e.filename}:${e.lineno}`);
});

window.addEventListener('unhandledrejection', (e) => {
    debugLogger.error(`UNHANDLED PROMISE REJECTION: ${e.reason}`);
});

// Инициализируем отладку
document.addEventListener('DOMContentLoaded', () => {
    addDebugInfo();

    // Добавляем информацию о Telegram WebApp
    debugLog('=== TELEGRAM WEBAPP INFO ===');
    debugLog(`Version: ${tg.version}`);
    debugLog(`Platform: ${tg.platform}`);
    debugLog(`User available: ${!!tg.initDataUnsafe?.user}`);
    if (tg.initDataUnsafe?.user) {
        debugLog(`User ID: ${tg.initDataUnsafe.user.id} (${typeof tg.initDataUnsafe.user.id})`);
        debugLog(`User name: ${tg.initDataUnsafe.user.first_name} ${tg.initDataUnsafe.user.last_name}`);
    }
    debugLog('=== END TELEGRAM WEBAPP INFO ===');
});

// Global variables
let currentUser = null;
let isAdmin = false;
let selectedDay = null;
let selectedTime = null;
let availableDays = [];
let availableTimes = [];

// Registration variables
let currentStep = 1;
let registrationData = {};

// Вспомогательная функция для API запросов с детальным логированием и таймаутами
async function apiRequest(url, options = {}) {
    const defaultOptions = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'ngrok-skip-browser-warning': 'true',
            'Cache-Control': 'no-cache', // Отключаем кеширование
            'Pragma': 'no-cache'
        },
        mode: 'cors',
        credentials: 'omit'
    };

    // Объединяем опции
    const mergedOptions = {
        ...defaultOptions,
        ...options,
        headers: {
            ...defaultOptions.headers,
            ...(options.headers || {})
        }
    };

    // Логируем запрос
    const method = options.method || 'GET';
    debugLogger.apiRequest(url, method, mergedOptions.headers, options.body);

    try {
        // Добавляем таймаут 10 секунд
        const timeoutPromise = new Promise((_, reject) => {
            setTimeout(() => reject(new Error('Request timeout')), 10000);
        });

        const fetchPromise = fetch(url, mergedOptions);

        const response = await Promise.race([fetchPromise, timeoutPromise]);

        // Получаем заголовки ответа
        const responseHeaders = Object.fromEntries(response.headers.entries());

        // Клонируем response для чтения body без потери данных
        const responseClone = response.clone();
        let responseBody = null;

        // Пытаемся прочитать body как JSON
        try {
            const contentType = response.headers.get('content-type');
            if (contentType && contentType.includes('application/json')) {
                responseBody = await responseClone.json();
            } else {
                responseBody = await responseClone.text();
            }
        } catch (e) {
            debugLogger.warning(`Не удалось прочитать response body: ${e.message}`);
        }

        // Логируем ответ
        debugLogger.apiResponse(url, response.status, responseHeaders, responseBody);

        return response;

    } catch (error) {
        debugLogger.error(`Ошибка API запроса к ${url}: ${error.message}`);
        debugLogger.error(`Stack trace: ${error.stack}`);
        throw error;
    }
}

// API configuration
// Определяем базовый URL из конфигурации
const API_BASE_URL = (() => {
    debugLogger.log('Определяем API_BASE_URL...');

    // Если есть глобальная конфигурация, используем её (приоритет!)
    if (window.config && window.config.API_BASE_URL) {
        debugLogger.log(`✅ Используем API_BASE_URL из config.js: ${window.config.API_BASE_URL}`);
        return window.config.API_BASE_URL;
    }

    // Если config не загружен, но запущено в Telegram WebApp - НЕ используем localhost!
    if (window.Telegram && window.Telegram.WebApp && window.Telegram.WebApp.initData) {
        debugLogger.warning('⚠️ Config.js не загружен! В Telegram WebApp НЕ ДОЛЖНО быть localhost!');
        debugLogger.warning('⚠️ Fallback: будем пытаться использовать localhost, но это может не работать');
        return 'http://localhost:8000/api';
    }

    // Локальная разработка - используем localhost
    debugLogger.log('🏠 Локальная среда разработки - используем localhost');
    return 'http://localhost:8000/api';
})();

// Диагностика конфигурации
debugLogger.log('=== ДИАГНОСТИКА КОНФИГУРАЦИИ ===');
debugLogger.log(`window.config доступен: ${!!window.config}`);
if (window.config) {
    debugLogger.log(`config.API_BASE_URL: ${window.config.API_BASE_URL}`);
} else {
    debugLogger.error('❌ window.config НЕ НАЙДЕН! Config.js не загружен или ошибка');
}
debugLogger.log(`Telegram WebApp доступен: ${!!window.Telegram?.WebApp}`);
debugLogger.log(`initData доступен: ${!!window.Telegram?.WebApp?.initData}`);
debugLogger.log(`ИТОГОВЫЙ API_BASE_URL: ${API_BASE_URL}`);
debugLogger.log('=== КОНЕЦ ДИАГНОСТИКИ ===');

console.log('API_BASE_URL:', API_BASE_URL);

// Initialize the app
document.addEventListener('DOMContentLoaded', async function() {
    debugLogger.log('🌟 === DOM CONTENT LOADED ===');

    // Принудительно скрываем экран загрузки через 3 секунды как fallback
    const loadingFallback = setTimeout(() => {
        debugLogger.warning('⚠️ FALLBACK: Принудительно скрываем экран загрузки');
        const loadingElement = document.getElementById('loading');
        if (loadingElement && loadingElement.style.display !== 'none') {
            loadingElement.style.display = 'none';
            // Если ничего не показано, показываем регистрацию
            const registrationElement = document.getElementById('registration-screen');
            const mainElement = document.getElementById('main-content');
            const successElement = document.getElementById('registration-success-screen');

            if (registrationElement.style.display === 'none' &&
                mainElement.style.display === 'none' &&
                successElement.style.display === 'none') {
                debugLogger.warning('⚠️ Показываем экран регистрации как fallback');
                showRegistrationScreen();
            }
        }
    }, 3000);

    // Добавляем небольшую задержку для стабилизации Telegram WebApp
    setTimeout(async () => {
        try {
            await initializeApp();
            // Отменяем fallback таймер, если инициализация прошла успешно
            clearTimeout(loadingFallback);
        } catch (error) {
            // Отменяем fallback таймер, обработка ошибок уже есть в initializeApp
            clearTimeout(loadingFallback);
        }
    }, 100); // 100ms задержка для стабилизации
});

async function initializeApp() {
    debugLogger.log('🚀 === НАЧАЛО ИНИЦИАЛИЗАЦИИ ПРИЛОЖЕНИЯ ===');

    try {
        // Get user info from Telegram
        const telegramUser = tg.initDataUnsafe?.user;

        // Для тестирования используем тестового пользователя, если данные Telegram недоступны
        if (!telegramUser) {
            debugLogger.warning('⚠️ Telegram user data not available, using test user');
            currentUser = {
                id: 123456,
                firstName: "Test",
                lastName: "User",
                username: "testuser"
            };
        } else {
            debugLogger.log('✅ Telegram user data available');

            // Валидация и приведение типов для user.id
            let userId = telegramUser.id;

            // Проверяем что id является числом или может быть преобразован в число
            if (typeof userId === 'string') {
                userId = parseInt(userId, 10);
            }

            // Проверяем что id является валидным числом
            if (!userId || isNaN(userId) || userId <= 0) {
                debugLogger.error(`❌ Invalid user ID: ${telegramUser.id}`);
                showError('Ошибка получения данных пользователя. Попробуйте перезапустить приложение.');
                return;
            }

            // Initialize user
            currentUser = {
                id: userId,
                firstName: telegramUser.first_name || 'Unknown',
                lastName: telegramUser.last_name || '',
                username: telegramUser.username || ''
            };

            debugLogger.log(`✅ User data processed: ${JSON.stringify(currentUser)}`);
        }

        debugLogger.log('🔍 Проверяем аутентификацию пользователя...');

        // Check if user is authenticated and get admin status
        const userExists = await checkUserAuth();

        debugLogger.log(`🔍 Результат проверки аутентификации: ${userExists}`);

        if (!userExists) {
            debugLogger.log('👤 Пользователь не найден, показываем регистрацию');
            // Явно скрываем экран загрузки перед показом регистрации
            document.getElementById('loading').style.display = 'none';
            showRegistrationScreen();
            return;
        }

        debugLogger.log('✅ Пользователь аутентифицирован, загружаем данные...');

        // Load initial data for authenticated user
        try {
            await loadAvailableDays();
            debugLogger.log('✅ Доступные дни загружены');
        } catch (error) {
            debugLogger.error(`❌ Ошибка загрузки дней: ${error.message}`);
            // Не блокируем приложение, показываем основной экран
        }

        try {
            await loadUserBookings();
            debugLogger.log('✅ Записи пользователя загружены');
        } catch (error) {
            debugLogger.error(`❌ Ошибка загрузки записей: ${error.message}`);
            // Не блокируем приложение
        }

        // Load admin data if user is admin
        if (isAdmin) {
            try {
                await loadAdminData();
                debugLogger.log('✅ Данные админки загружены');
            } catch (error) {
                debugLogger.error(`❌ Ошибка загрузки админ данных: ${error.message}`);
                // Не блокируем приложение
            }
        }

        // Show main content
        // Явно скрываем экран загрузки перед показом основного контента
        document.getElementById('loading').style.display = 'none';
        showMainContent();

        // Set up event listeners
        setupEventListeners();

        debugLogger.log('✅ === ИНИЦИАЛИЗАЦИЯ ЗАВЕРШЕНА УСПЕШНО ===');

    } catch (error) {
        debugLogger.error(`❌ === КРИТИЧЕСКАЯ ОШИБКА ИНИЦИАЛИЗАЦИИ ===`);
        debugLogger.error(`Error: ${error.message}`);
        debugLogger.error(`Stack: ${error.stack}`);

        // КРИТИЧЕСКИ ВАЖНО: скрываем экран загрузки при ошибке
        document.getElementById('loading').style.display = 'none';

        // Показываем ошибку пользователю и предлагаем перезагрузку
        const errorMsg = `Ошибка инициализации: ${error.message}. Попробуйте перезагрузить приложение.`;
        showError(errorMsg);

        // Альтернативный путь - показать регистрацию
        setTimeout(() => {
            debugLogger.log('🔄 Fallback: показываем экран регистрации');
            closeErrorModal();
            showRegistrationScreen();
        }, 3000);
    }
}

async function checkUserAuth() {
    try {
        // Проверяем что currentUser и его id корректны
        if (!currentUser || !currentUser.id || isNaN(currentUser.id)) {
            debugLogger.error(`❌ Invalid current user: ${JSON.stringify(currentUser)}`);
            return false;
        }

        debugLogger.log(`🔍 Checking auth for user ID: ${currentUser.id}`);

        // Добавляем уникальный параметр для избежания кеширования
        const timestamp = new Date().getTime();
        const response = await apiRequest(`${API_BASE_URL}/users/${currentUser.id}?_t=${timestamp}`);

        debugLogger.log(`📡 Auth response status: ${response.status}`);

        if (!response.ok) {
            if (response.status === 404) {
                debugLogger.log('👤 User not found - need registration');
                return false;
            }
            if (response.status >= 500) {
                debugLogger.error(`🔥 Server error ${response.status} - treating as need registration`);
                return false;
            }
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const userData = await response.json();
        debugLogger.log(`✅ User data received: ${JSON.stringify(userData)}`);

        if (userData && userData.id) {
            isAdmin = userData.is_admin || false;
            debugLogger.log(`✅ User authenticated, isAdmin: ${isAdmin}`);

            // Show admin tab if user is admin
            if (isAdmin) {
                const adminTab = document.querySelector('.admin-only');
                if (adminTab) {
                    adminTab.style.display = 'block';
                }
            }

            return true;
        } else {
            debugLogger.log('❌ User data is empty or invalid');
            return false;
        }
    } catch (error) {
        debugLogger.error(`❌ Auth check failed: ${error.message}`);

        // Специальная обработка для разных типов ошибок
        if (error.message.includes('timeout')) {
            debugLogger.error('⏰ Request timeout - treating as need registration');
            return false;
        }

        if (error.message.includes('Failed to fetch') || error.name === 'NetworkError') {
            debugLogger.error('🌐 Network error - treating as need registration');
            return false;
        }

        // Для других ошибок тоже возвращаем false (безопасный fallback)
        return false;
    }
}

// Registration functions
function showRegistrationScreen() {
    debugLogger.log('📝 === ПОКАЗЫВАЕМ ЭКРАН РЕГИСТРАЦИИ ===');

    // Убеждаемся что все экраны скрыты
    document.getElementById('loading').style.display = 'none';
    document.getElementById('main-content').style.display = 'none';
    document.getElementById('registration-success-screen').style.display = 'none';
    document.getElementById('registration-screen').style.display = 'flex';

    // Сбрасываем состояние регистрации
    currentStep = 1;
    registrationData = {};

    // Очищаем все поля
    const form = document.getElementById('registration-form');
    if (form) {
        form.reset();
    }

    // Обновляем UI
    updateRegistrationUI();

    setupRegistrationEventListeners();

    debugLogger.log('✅ Экран регистрации отображен');
}

function showRegistrationSuccessScreen() {
    debugLogger.log('🎉 === ПОКАЗЫВАЕМ ЭКРАН УСПЕШНОЙ РЕГИСТРАЦИИ ===');

    // Скрываем экран регистрации и показываем экран загрузки
    document.getElementById('registration-screen').style.display = 'none';
    document.getElementById('registration-success-screen').style.display = 'flex';

    // Сбрасываем состояние шагов
    const steps = ['step-auth', 'step-schedule', 'step-ready'];
    steps.forEach(stepId => {
        const step = document.getElementById(stepId);
        step.classList.remove('completed', 'active');
    });

    // Первый шаг уже завершен (создание профиля)
    document.getElementById('step-auth').classList.add('completed');

    debugLogger.log('✅ Экран успешной регистрации отображен');
}

async function processRegistrationSteps() {
    debugLogger.log('⚙️ === НАЧИНАЕМ ОБРАБОТКУ ШАГОВ ПОСЛЕ РЕГИСТРАЦИИ ===');

    try {
        // Шаг 2: Загрузка расписания
        const scheduleStep = document.getElementById('step-schedule');
        scheduleStep.classList.add('active');

        await new Promise(resolve => setTimeout(resolve, 800)); // Небольшая пауза для UX

        try {
            await loadAvailableDays();
            scheduleStep.classList.remove('active');
            scheduleStep.classList.add('completed');
            scheduleStep.querySelector('.step-icon').textContent = '✓';
            debugLogger.log('✅ Расписание загружено');
        } catch (error) {
            debugLogger.error(`❌ Ошибка загрузки расписания: ${error.message}`);
            // Продолжаем даже при ошибке
            scheduleStep.classList.remove('active');
            scheduleStep.classList.add('completed');
            scheduleStep.querySelector('.step-icon').textContent = '⚠️';
        }

        await new Promise(resolve => setTimeout(resolve, 500));

        // Шаг 3: Подготовка интерфейса
        const readyStep = document.getElementById('step-ready');
        readyStep.classList.add('active');

        await new Promise(resolve => setTimeout(resolve, 800));

        try {
            await loadUserBookings();
            debugLogger.log('✅ Записи пользователя загружены');
        } catch (error) {
            debugLogger.error(`❌ Ошибка загрузки записей: ${error.message}`);
            // Продолжаем даже при ошибке
        }

        readyStep.classList.remove('active');
        readyStep.classList.add('completed');
        readyStep.querySelector('.step-icon').textContent = '✓';

        await new Promise(resolve => setTimeout(resolve, 800));

        // Финальный переход к основному экрану
        debugLogger.log('🏠 Переходим к основному экрану');

        // Скрываем экран загрузки и показываем основной контент
        document.getElementById('registration-success-screen').style.display = 'none';
        showMainContent();
        setupEventListeners();

        debugLogger.log('✅ === ВСЕ ШАГИ ЗАВЕРШЕНЫ УСПЕШНО ===');

    } catch (error) {
        debugLogger.error(`❌ Критическая ошибка в шагах регистрации: ${error.message}`);

        // Показываем ошибку но все равно переходим к основному экрану
        setTimeout(() => {
            document.getElementById('registration-success-screen').style.display = 'none';
            showMainContent();
            setupEventListeners();
            showError('Некоторые данные не удалось загрузить, но приложение готово к работе.');
        }, 1000);
    }

    // УДАЛИТЕ ВСЕ ЧТО НИЖЕ - ЭТО ДУБЛИРОВАННЫЙ КОД ИЗ showRegistrationScreen()
    // Этот код в конце функции показывает экран регистрации вместо основного!
}

function showMainContent() {
    debugLogger.log('🏠 === ПОКАЗЫВАЕМ ОСНОВНОЙ КОНТЕНТ ===');

    // Убеждаемся что все экраны скрыты
    document.getElementById('loading').style.display = 'none';
    document.getElementById('registration-screen').style.display = 'none';
    document.getElementById('registration-success-screen').style.display = 'none';
    document.getElementById('main-content').style.display = 'block';

    // Set user name in header
    const userNameElement = document.getElementById('user-name');
    if (userNameElement && currentUser) {
        userNameElement.textContent = `${currentUser.firstName} ${currentUser.lastName || ''}`;
    }

    debugLogger.log('✅ Основной контент отображен');
}

function setupRegistrationEventListeners() {
    // Step navigation buttons
    document.getElementById('next-step-1').addEventListener('click', () => {
        if (validateStep1()) {
            nextStep();
        }
    });

    document.getElementById('prev-step-2').addEventListener('click', prevStep);
    document.getElementById('next-step-2').addEventListener('click', () => {
        if (validateStep2()) {
            nextStep();
        }
    });

    document.getElementById('prev-step-3').addEventListener('click', prevStep);

    // Form submission
    document.getElementById('registration-form').addEventListener('submit', handleRegistrationSubmit);

    // Phone number formatting
    document.getElementById('phone_number').addEventListener('input', formatPhoneNumber);

    // Real-time validation
    document.getElementById('first_name').addEventListener('blur', validateFirstName);
    document.getElementById('phone_number').addEventListener('blur', validatePhone);
    document.getElementById('age').addEventListener('blur', validateAge);
}

function validateStep1() {
    const firstName = document.getElementById('first_name').value.trim();

    if (!firstName) {
        showFieldError('first_name', 'Пожалуйста, введите ваше имя');
        return false;
    }

    if (firstName.length < 2) {
        showFieldError('first_name', 'Имя должно содержать минимум 2 символа');
        return false;
    }

    clearFieldError('first_name');

    // Save data
    registrationData.first_name = firstName;
    registrationData.second_name = document.getElementById('second_name').value.trim();

    return true;
}

function validateStep2() {
    const phone = document.getElementById('phone_number').value.trim();
    const age = parseInt(document.getElementById('age').value);

    let isValid = true;

    // Validate phone
    if (!phone) {
        showFieldError('phone_number', 'Пожалуйста, введите номер телефона');
        isValid = false;
    } else if (!isValidPhone(phone)) {
        showFieldError('phone_number', 'Введите корректный номер телефона');
        isValid = false;
    } else {
        clearFieldError('phone_number');
    }

    // Validate age
    if (!age || age < 16 || age > 100) {
        showFieldError('age', 'Возраст должен быть от 16 до 100 лет');
        isValid = false;
    } else {
        clearFieldError('age');
    }

    if (isValid) {
        // Save data
        registrationData.phone_number = phone;
        registrationData.age = age;

        // Update summary
        updateRegistrationSummary();
    }

    return isValid;
}

function validateFirstName() {
    const firstName = document.getElementById('first_name').value.trim();
    if (firstName && firstName.length < 2) {
        showFieldError('first_name', 'Имя должно содержать минимум 2 символа');
        return false;
    }
    clearFieldError('first_name');
    return true;
}

function validatePhone() {
    const phone = document.getElementById('phone_number').value.trim();
    if (phone && !isValidPhone(phone)) {
        showFieldError('phone_number', 'Введите корректный номер телефона');
        return false;
    }
    clearFieldError('phone_number');
    return true;
}

function validateAge() {
    const age = parseInt(document.getElementById('age').value);
    if (age && (age < 16 || age > 100)) {
        showFieldError('age', 'Возраст должен быть от 16 до 100 лет');
        return false;
    }
    clearFieldError('age');
    return true;
}

function isValidPhone(phone) {
    // Очищаем номер от символов
    const cleaned = cleanPhoneNumber(phone);

    // Проверяем что номер состоит из 11 цифр и начинается с 7
    return /^7[0-9]{10}$/.test(cleaned);
}

function formatPhoneNumber(event) {
    let value = event.target.value.replace(/\D/g, '');

    if (value.startsWith('8')) {
        value = '7' + value.slice(1);
    }

    if (value.startsWith('7') && value.length <= 11) {
        value = value.replace(/^7(\d{3})(\d{3})(\d{2})(\d{2})$/, '+7 ($1) $2-$3-$4');
        value = value.replace(/^7(\d{3})(\d{3})(\d{2})$/, '+7 ($1) $2-$3');
        value = value.replace(/^7(\d{3})(\d{3})$/, '+7 ($1) $2');
        value = value.replace(/^7(\d{3})$/, '+7 ($1');
        value = value.replace(/^7(\d{1,2})$/, '+7 ($1');
        value = value.replace(/^7$/, '+7 (');
    }

    event.target.value = value;
}

function showFieldError(fieldId, message) {
    const field = document.getElementById(fieldId);
    const errorElement = document.getElementById(fieldId + '_error');

    field.classList.add('error');
    if (errorElement) {
        errorElement.textContent = message;
        errorElement.classList.add('show');
    }
}

function clearFieldError(fieldId) {
    const field = document.getElementById(fieldId);
    const errorElement = document.getElementById(fieldId + '_error');

    field.classList.remove('error');
    if (errorElement) {
        errorElement.classList.remove('show');
    }
}

function nextStep() {
    currentStep++;
    updateRegistrationUI();
}

function prevStep() {
    currentStep--;
    updateRegistrationUI();
}

function updateRegistrationUI() {
    // Update progress indicators
    document.querySelectorAll('.progress-step').forEach((step, index) => {
        const stepNumber = index + 1;
        step.classList.remove('active', 'completed');

        if (stepNumber < currentStep) {
            step.classList.add('completed');
        } else if (stepNumber === currentStep) {
            step.classList.add('active');
        }
    });

    // Update form steps
    document.querySelectorAll('.form-step').forEach((step, index) => {
        const stepNumber = index + 1;
        step.classList.remove('active');

        if (stepNumber === currentStep) {
            step.classList.add('active');
        }
    });
}

function updateRegistrationSummary() {
    const summaryContainer = document.getElementById('user-info-summary');

    summaryContainer.innerHTML = `
        <div class="user-info-item">
            <span class="user-info-label">Имя:</span>
            <span class="user-info-value">${registrationData.first_name}</span>
        </div>
        ${registrationData.second_name ? `
        <div class="user-info-item">
            <span class="user-info-label">Фамилия:</span>
            <span class="user-info-value">${registrationData.second_name}</span>
        </div>
        ` : ''}
        <div class="user-info-item">
            <span class="user-info-label">Телефон:</span>
            <span class="user-info-value">${registrationData.phone_number}</span>
        </div>
        <div class="user-info-item">
            <span class="user-info-label">Возраст:</span>
            <span class="user-info-value">${registrationData.age} лет</span>
        </div>
        <div class="user-info-item" style="margin-top: 12px; padding-top: 12px; border-top: 1px solid var(--tg-theme-hint-color, #e0e0e0);">
            <span class="user-info-label">Номер для сохранения:</span>
            <span class="user-info-value" style="font-family: monospace;">${cleanPhoneNumber(registrationData.phone_number)}</span>
        </div>
    `;
}

function cleanPhoneNumber(phone) {
    // Убираем все символы кроме цифр
    const digitsOnly = phone.replace(/\D/g, '');

    // Если номер начинается с 8, заменяем на 7
    if (digitsOnly.startsWith('8') && digitsOnly.length === 11) {
        return '7' + digitsOnly.slice(1);
    }

    // Если номер начинается с 7, оставляем как есть
    if (digitsOnly.startsWith('7') && digitsOnly.length === 11) {
        return digitsOnly;
    }

    // Возвращаем как есть для других случаев
    return digitsOnly;
}

async function handleRegistrationSubmit(event) {
    event.preventDefault();

    debugLogger.log('📝 === НАЧАЛО РЕГИСТРАЦИИ ===');

    const submitButton = document.getElementById('submit-registration');
    submitButton.classList.add('btn-loading');
    submitButton.disabled = true;

    try {
        const registerData = {
            telegram_id: currentUser.id,
            first_name: registrationData.first_name,
            second_name: registrationData.second_name || '',
            phone_number: cleanPhoneNumber(registrationData.phone_number), // Очищаем от форматирования
            age: registrationData.age
        };

        debugLogger.log(`📤 Registration data: ${JSON.stringify(registerData)}`);

        // Добавляем уникальный параметр для избежания кеширования
        const timestamp = new Date().getTime();
        const response = await apiRequest(`${API_BASE_URL}/users/register?_t=${timestamp}`, {
            method: 'POST',
            body: JSON.stringify(registerData)
        });

        debugLogger.log(`📡 Registration response status: ${response.status}`);

        if (response.ok) {
            const responseData = await response.json();
            debugLogger.success(`✅ Регистрация успешна! Response: ${JSON.stringify(responseData)}`);

            // Показываем сообщение об успехе на 1.5 секунды
            showSuccess('Регистрация прошла успешно! Добро пожаловать!');

            setTimeout(() => {
                closeSuccessModal();

                // Показываем красивый экран загрузки с шагами
                showRegistrationSuccessScreen();

                // Запускаем пошаговую обработку
                processRegistrationSteps();

            }, 1500);

        } else {
            const errorData = await response.json().catch(() => ({ detail: 'Неизвестная ошибка сервера' }));
            debugLogger.error(`❌ Registration failed: ${JSON.stringify(errorData)}`);

            let errorMessage = 'Ошибка регистрации. Попробуйте снова.';

            if (response.status === 400) {
                errorMessage = errorData.detail || 'Пользователь уже зарегистрирован или некорректные данные.';
            } else if (response.status >= 500) {
                errorMessage = 'Ошибка сервера. Попробуйте позже.';
            }

            showError(errorMessage);
        }

    } catch (error) {
        debugLogger.error(`❌ Registration error: ${error.message}`);
        debugLogger.error(`Stack: ${error.stack}`);

        let errorMessage = 'Ошибка соединения. Проверьте интернет и попробуйте снова.';

        if (error.message.includes('timeout')) {
            errorMessage = 'Превышено время ожидания. Проверьте соединение и попробуйте снова.';
        } else if (error.message.includes('Failed to fetch')) {
            errorMessage = 'Не удается подключиться к серверу. Проверьте интернет соединение.';
        }

        showError(errorMessage);
    } finally {
        submitButton.classList.remove('btn-loading');
        submitButton.disabled = false;
    }
}

// ========================================
// EXISTING BOOKING FUNCTIONS
// ========================================
// Эти функции были в вашем оригинальном коде
// и отвечают за основную логику записи на тренировки

async function loadAvailableDays() {
    try {
        debugLog('=== ЗАГРУЗКА ДОСТУПНЫХ ДНЕЙ ===');
        debugLog(`API URL: ${API_BASE_URL}/slots/available-days`);
        debugLog(`Current user: ${JSON.stringify(currentUser)}`);
        debugLog(`Telegram WebApp data: ${JSON.stringify(tg.initDataUnsafe)}`);
        debugLog(`Telegram WebApp version: ${tg.version}`);
        debugLog(`Telegram WebApp platform: ${tg.platform}`);
        debugLog(`Is Telegram WebApp: ${tg.isVersionAtLeast('6.0')}`);

        // Проверяем доступность API
        debugLog('Проверяем доступность API...');

        // Получаем доступные дни через новый endpoint
        const response = await apiRequest(`${API_BASE_URL}/slots/available-days`);

        debugLog(`Response status: ${response.status}`);
        debugLog(`Response statusText: ${response.statusText}`);
        debugLog(`Response headers: ${JSON.stringify(Object.fromEntries(response.headers.entries()))}`);
        debugLog(`Response ok: ${response.ok}`);
        debugLog(`Response type: ${response.type}`);
        debugLog(`Response url: ${response.url}`);

        if (!response.ok) {
            const errorText = await response.text();
            debugLog(`Response error text: ${errorText}`);
            throw new Error(`HTTP ${response.status} ${response.statusText}: ${errorText}`);
        }

        const data = await response.json();
        debugLog(`Response data: ${JSON.stringify(data)}`);

        // Используем полученные даты
        availableDays = data.available_days || [];
        debugLog(`Available days: ${JSON.stringify(availableDays)}`);

        renderDays();
        debugLog('Days rendered successfully');
    } catch (error) {
        debugLog('=== ОШИБКА ЗАГРУЗКИ ДНЕЙ ===');
        debugLog(`Error type: ${error.constructor.name}`);
        debugLog(`Error message: ${error.message}`);
        debugLog(`Error stack: ${error.stack}`);

        // Дополнительная диагностика для разных типов ошибок
        if (error instanceof TypeError) {
            console.error('TypeError - возможно проблема с сетью или CORS');
            console.error('Network state:', navigator.onLine ? 'online' : 'offline');
        }

        if (error.name === 'NetworkError') {
            console.error('NetworkError - проблема с сетевым соединением');
        }

        if (error.message.includes('Failed to fetch')) {
            console.error('Fetch failed - возможно блокировка CORS или недоступность сервера');
            console.error('Пытаемся проверить доступность сервера...');

            // Попробуем простой запрос для проверки доступности
            try {
                const healthResponse = await fetch(`${API_BASE_URL.replace('/api', '')}/health`, {
                    method: 'GET',
                    mode: 'no-cors'
                });
                console.log('Health check response:', healthResponse);
            } catch (healthError) {
                console.error('Health check failed:', healthError);

                // Если в Telegram WebApp и ngrok недоступен, попробуем localhost
                if (API_BASE_URL.includes('ngrok')) {
                    console.log('Ngrok недоступен, пробуем localhost...');
                    try {
                        const localResponse = await fetch('http://localhost:8000/api/slots/available-days', {
                            method: 'GET',
                            headers: {
                                'Content-Type': 'application/json',
                                'Accept': 'application/json',
                            },
                            mode: 'cors',
                            credentials: 'omit'
                        });
                        console.log('Localhost response:', localResponse);
                        if (localResponse.ok) {
                            console.log('Localhost доступен, но ngrok нет');
                            showError('Сервер недоступен через ngrok. Используйте локальную версию.');
                            return;
                        }
                    } catch (localError) {
                        console.error('Localhost также недоступен:', localError);
                    }
                }
            }
        }

        // Проверим настройки Telegram WebApp
        console.error('=== ДИАГНОСТИКА TELEGRAM WEBAPP ===');
        console.error('tg.initData:', tg.initData);
        console.error('tg.initDataUnsafe:', tg.initDataUnsafe);
        console.error('tg.colorScheme:', tg.colorScheme);
        console.error('tg.themeParams:', tg.themeParams);
        console.error('tg.isExpanded:', tg.isExpanded);
        console.error('tg.viewportHeight:', tg.viewportHeight);
        console.error('tg.viewportStableHeight:', tg.viewportStableHeight);
        console.error('tg.headerColor:', tg.headerColor);
        console.error('tg.backgroundColor:', tg.backgroundColor);
        console.error('tg.isClosingConfirmationEnabled:', tg.isClosingConfirmationEnabled);

        showError(`Ошибка загрузки доступных дней: ${error.message}`);
    }
}

function renderDays() {
    const daysGrid = document.getElementById('days-grid');
    daysGrid.innerHTML = '';

    if (availableDays.length === 0) {
        daysGrid.innerHTML = '<p>Нет доступных дней для записи</p>';
        return;
    }

    availableDays.forEach(day => {
        const dayCard = document.createElement('div');
        dayCard.className = 'day-card';
        dayCard.innerHTML = `
            <div class="day-name">${formatDayName(day)}</div>
            <div class="day-date">${formatDate(day)}</div>
        `;

        dayCard.addEventListener('click', () => selectDay(day));
        daysGrid.appendChild(dayCard);
    });
}

function selectDay(day) {
    selectedDay = day;

    // Update UI
    document.querySelectorAll('.day-card').forEach(card => card.classList.remove('selected'));
    event.target.closest('.day-card').classList.add('selected');

    // Load times for selected day
    loadAvailableTimes(day);
}

async function loadAvailableTimes(day) {
    try {
        debugLog(`Loading available times for day: ${day}`);

        const response = await apiRequest(`${API_BASE_URL}/slots/?selected_date=${day}&telegram_id=${currentUser.id}`);
        const data = await response.json();

        debugLog(`Raw slots data: ${JSON.stringify(data)}`);

        // Backend уже возвращает только подходящие для тренировки слоты
        availableTimes = data.available_periods || [];
        debugLog(`Training slots from backend: ${availableTimes.length}`);

        renderTimes();

        // Show times section
        document.getElementById('times-section').style.display = 'block';
    } catch (error) {
        debugLog(`Failed to load times: ${error.message}`);
        showError('Ошибка загрузки доступного времени');
    }
}

function renderTimes() {
    const timesGrid = document.getElementById('times-grid');
    timesGrid.innerHTML = '';

    if (availableTimes.length === 0) {
        timesGrid.innerHTML = '<p>Нет доступного времени для записи</p>';
        return;
    }

    availableTimes.forEach(slot => {
        const timeSlot = document.createElement('div');
        timeSlot.className = 'time-slot';
        timeSlot.innerHTML = `
            <div class="time">${formatTime(slot.start_time)}</div>
        `;

        timeSlot.addEventListener('click', () => selectTime(slot));
        timesGrid.appendChild(timeSlot);
    });
}

function selectTime(slot) {
    selectedTime = slot;

    // Update UI
    document.querySelectorAll('.time-slot').forEach(timeSlot => timeSlot.classList.remove('selected'));
    event.target.closest('.time-slot').classList.add('selected');

    // Show confirmation
    showConfirmation();
}

function showConfirmation() {
    const confirmationSection = document.getElementById('confirmation-section');
    const bookingDetails = document.getElementById('booking-details');

    bookingDetails.innerHTML = `
        <h3>Подтверждение записи</h3>
        <p><strong>День:</strong> ${formatDayName(selectedDay)}</p>
        <p><strong>Дата:</strong> ${formatDate(selectedDay)}</p>
        <p><strong>Время:</strong> ${formatTime(selectedTime.start_time)}</p>
        <p><strong>Длительность:</strong> 90 минут</p>
    `;

    confirmationSection.style.display = 'block';
}

async function confirmBooking() {
    try {
        // Проверяем, находимся ли мы в режиме переноса
        const isReschedule = window.rescheduleBookingId;
        
        debugLog(isReschedule ? '=== ПЕРЕНОС БРОНИ ===' : '=== СОЗДАНИЕ БРОНИ ===');
        debugLog(`Selected time: ${JSON.stringify(selectedTime)}`);
        debugLog(`Selected day: ${selectedDay}`);
        debugLog(`Current user: ${JSON.stringify(currentUser)}`);
        if (isReschedule) {
            debugLog(`Reschedule booking ID: ${window.rescheduleBookingId}`);
        }

        // Рассчитываем правильное время окончания
        const startTime = new Date(`2000-01-01T${selectedTime.start_time}`);
        const endTime = new Date(startTime);
        endTime.setMinutes(endTime.getMinutes() + 90);

        const calculatedEndTime = endTime.toTimeString().slice(0, 8);
        debugLog(`Calculated end time: ${calculatedEndTime}`);

        if (isReschedule) {
            // Логика переноса: сначала удаляем старое, потом создаем новое
            debugLog('Удаляем старое бронирование...');
            const deleteResponse = await apiRequest(`${API_BASE_URL}/bookings/${window.rescheduleBookingId}?telegram_id=${currentUser.id}`, {
                method: 'DELETE'
            });

            if (!deleteResponse.ok) {
                showError('Ошибка удаления старого бронирования');
                return;
            }
            
            debugLog('Старое бронирование удалено, обновляем доступные слоты...');
            
            // Обновляем доступные дни и времена после удаления
            await loadAvailableDays();
            if (selectedDay) {
                await loadAvailableTimes(selectedDay);
            }
            
            debugLog('Создаем новое бронирование...');
        }

        const bookingData = {
            booking: {
                date: selectedDay,
                start_time: selectedTime.start_time,
                end_time: calculatedEndTime
            },
            user: {
                telegram_id: currentUser.id
            }
        };

        debugLog(`Booking data: ${JSON.stringify(bookingData)}`);

        const response = await apiRequest(`${API_BASE_URL}/bookings/`, {
            method: 'POST',
            body: JSON.stringify(bookingData)
        });

        debugLog(`Response status: ${response.status}`);

        if (response.ok) {
            debugLog(isReschedule ? 'Booking rescheduled successfully' : 'Booking created successfully');
            showSuccess(isReschedule ? 'Бронирование успешно перенесено!' : 'Запись успешно создана!');
            
            // Очищаем режим переноса
            if (isReschedule) {
                window.rescheduleBookingId = null;
                const indicator = document.getElementById('reschedule-indicator');
                if (indicator) {
                    indicator.remove();
                }
            }
            
            resetBookingFlow();
            await loadUserBookings();
            
            // Переключаемся на вкладку "Мои записи"
            switchTab('my-bookings');
        } else {
            const error = await response.json();
            debugLog(`Booking error: ${JSON.stringify(error)}`);
            showError(error.detail || (isReschedule ? 'Ошибка переноса записи' : 'Ошибка создания записи'));
        }
    } catch (error) {
        debugLog(`Booking failed: ${error.message}`);
        showError(isReschedule ? 'Ошибка переноса записи' : 'Ошибка создания записи');
    }
}

function resetBookingFlow() {
    selectedDay = null;
    selectedTime = null;

    document.querySelectorAll('.day-card').forEach(card => card.classList.remove('selected'));
    document.querySelectorAll('.time-slot').forEach(slot => slot.classList.remove('selected'));

    document.getElementById('times-section').style.display = 'none';
    document.getElementById('confirmation-section').style.display = 'none';
    
    // Очищаем индикатор переноса если он есть
    const indicator = document.getElementById('reschedule-indicator');
    if (indicator) {
        indicator.remove();
    }
    window.rescheduleBookingId = null;
}

async function loadUserBookings() {
    try {
        const response = await apiRequest(`${API_BASE_URL}/bookings/user/${currentUser.id}`);
        const bookings = await response.json();
        renderUserBookings(bookings);
    } catch (error) {
        console.error('Failed to load user bookings:', error);
    }
}

function renderUserBookings(bookings) {
    const bookingsList = document.getElementById('bookings-list');
    bookingsList.innerHTML = '';

    if (bookings.length === 0) {
        bookingsList.innerHTML = '<p>У вас нет запланированных тренировок</p>';
        return;
    }

    bookings.forEach(booking => {
        const bookingItem = document.createElement('div');
        bookingItem.className = 'booking-item';
        bookingItem.innerHTML = `
            <div class="booking-info">
                <div class="booking-date">${formatDayName(booking.day)}</div>
                <div class="booking-time">${formatTime(booking.start_time)} - ${formatTime(booking.end_time)}</div>
            </div>
            <div class="booking-actions">
                <button class="btn btn-danger" onclick="cancelBooking(${booking.id})">Отменить</button>
                <button class="btn btn-secondary" onclick="rescheduleBooking(${booking.id})">Перенести</button>
            </div>
        `;
        bookingsList.appendChild(bookingItem);
    });
}

async function cancelBooking(bookingId) {
    try {
        const response = await apiRequest(`${API_BASE_URL}/bookings/${bookingId}?telegram_id=${currentUser.id}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            showSuccess('Бронирование отменено');
            
            // Обновляем список пользовательских бронирований
            await loadUserBookings();
            
            // Если пользователь сейчас на вкладке бронирования, обновляем доступные слоты
            const currentTab = document.querySelector('.nav-tab.active')?.getAttribute('data-tab');
            if (currentTab === 'booking') {
                // Обновляем доступные дни
                await loadAvailableDays();
                
                // Если выбран конкретный день, обновляем доступное время для этого дня
                if (selectedDay) {
                    await loadAvailableTimes(selectedDay);
                }
            }
        } else {
            showError('Ошибка отмены бронирования');
        }
    } catch (error) {
        console.error('Cancel booking failed:', error);
        showError('Ошибка отмены бронирования');
    }
}

async function rescheduleBooking(bookingId) {
    try {
        // Сохраняем ID бронирования для переноса
        window.rescheduleBookingId = bookingId;
        
        // Показываем сообщение о переносе
        showSuccess('Выберите новое время для переноса бронирования');
        
        // Переключаемся на вкладку бронирования
        switchTab('booking');
        
        // Загружаем доступные дни
        await loadAvailableDays();
        
        // Добавляем индикатор режима переноса
        addRescheduleIndicator();
        
    } catch (error) {
        console.error('Reschedule booking failed:', error);
        showError('Ошибка переноса бронирования');
    }
}

function addRescheduleIndicator() {
    // Добавляем индикатор что мы в режиме переноса
    const bookingSection = document.getElementById('booking');
    let indicator = document.getElementById('reschedule-indicator');
    
    if (!indicator) {
        indicator = document.createElement('div');
        indicator.id = 'reschedule-indicator';
        indicator.className = 'reschedule-indicator';
        indicator.innerHTML = `
            <div class="alert alert-info">
                📝 Режим переноса бронирования. Выберите новое время.
                <button onclick="cancelReschedule()" class="btn btn-sm btn-secondary" style="margin-left: 10px;">Отменить перенос</button>
            </div>
        `;
        bookingSection.insertBefore(indicator, bookingSection.firstChild);
    }
}

function cancelReschedule() {
    // Отменяем режим переноса
    window.rescheduleBookingId = null;
    const indicator = document.getElementById('reschedule-indicator');
    if (indicator) {
        indicator.remove();
    }
    
    // Возвращаемся к списку бронирований
    switchTab('my-bookings');
}

async function loadAdminData() {
    try {
        // Load admin statistics
        const statsResponse = await apiRequest(`${API_BASE_URL}/bookings/stats`);
        const stats = await statsResponse.json();

        document.getElementById('total-bookings').textContent = stats.total || 0;
        document.getElementById('today-bookings').textContent = stats.today || 0;

        // Load all bookings
        const bookingsResponse = await apiRequest(`${API_BASE_URL}/bookings/all`);
        const allBookings = await bookingsResponse.json();
        renderAllBookings(allBookings);
    } catch (error) {
        console.error('Failed to load admin data:', error);
    }
}

function renderAllBookings(bookings) {
    const allBookingsContainer = document.getElementById('all-bookings');
    allBookingsContainer.innerHTML = '';

    bookings.forEach(booking => {
        const bookingItem = document.createElement('div');
        bookingItem.className = 'admin-booking-item';
        bookingItem.innerHTML = `
            <div class="user-name">${booking.user_name || 'Неизвестный пользователь'}</div>
            <div class="booking-details">
                ${formatDayName(booking.day)} - ${formatTime(booking.start_time)} - ${formatTime(booking.end_time)}
            </div>
        `;
        allBookingsContainer.appendChild(bookingItem);
    });
}

function setupEventListeners() {
    // Tab navigation
    document.querySelectorAll('.nav-tab').forEach(tab => {
        tab.addEventListener('click', () => {
            const tabName = tab.dataset.tab;
            switchTab(tabName);
        });
    });

    // Booking confirmation
    document.getElementById('confirm-booking').addEventListener('click', confirmBooking);
    document.getElementById('cancel-booking').addEventListener('click', () => {
        // Если в режиме переноса, возвращаемся к списку записей
        if (window.rescheduleBookingId) {
            cancelReschedule();
        } else {
            resetBookingFlow();
        }
    });
}

function switchTab(tabName) {
    // Update tab buttons
    document.querySelectorAll('.nav-tab').forEach(tab => tab.classList.remove('active'));
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');

    // Update tab content
    document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
    document.getElementById(tabName).classList.add('active');

    // Load data for specific tabs
    if (tabName === 'my-bookings') {
        loadUserBookings();
    } else if (tabName === 'admin' && isAdmin) {
        loadAdminData();
    } else if (tabName === 'booking') {
        // Обновляем доступные дни при переходе на вкладку бронирования
        loadAvailableDays();
    }
}

// Utility functions
function formatDayName(dateString) {
    const date = new Date(dateString);
    const days = ['Воскресенье', 'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота'];
    return days[date.getDay()];
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('ru-RU', {
        day: 'numeric',
        month: 'long'
    });
}

function formatTime(timeString) {
    return timeString.slice(0, 5); // Remove seconds
}

function showError(message) {
    document.getElementById('error-message').textContent = message;
    document.getElementById('error-modal').style.display = 'flex';
}

function showSuccess(message) {
    document.getElementById('success-message').textContent = message;
    document.getElementById('success-modal').style.display = 'flex';
}

function closeErrorModal() {
    document.getElementById('error-modal').style.display = 'none';
}

function closeSuccessModal() {
    document.getElementById('success-modal').style.display = 'none';
}

// Global functions for modal buttons
window.closeErrorModal = closeErrorModal;
window.closeSuccessModal = closeSuccessModal;