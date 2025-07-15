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

// Вспомогательная функция для API запросов с детальным логированием
async function apiRequest(url, options = {}) {
    const defaultOptions = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'ngrok-skip-browser-warning': 'true'
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
        const response = await fetch(url, mergedOptions);
        
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
    try {
        await initializeApp();
    } catch (error) {
        console.error('Failed to initialize app:', error);
        showError('Ошибка инициализации приложения');
    }
});

async function initializeApp() {
    // Get user info from Telegram
    const telegramUser = tg.initDataUnsafe?.user;
    
    // Для тестирования используем тестового пользователя, если данные Telegram недоступны
    if (!telegramUser) {
        console.log('Telegram user data not available, using test user');
        currentUser = {
            id: 123456,
            firstName: "Test",
            lastName: "User",
            username: "testuser"
        };
    } else {
        console.log('Telegram user data:', telegramUser);
        
        // Валидация и приведение типов для user.id
        let userId = telegramUser.id;
        
        // Проверяем что id является числом или может быть преобразован в число
        if (typeof userId === 'string') {
            userId = parseInt(userId, 10);
        }
        
        // Проверяем что id является валидным числом
        if (!userId || isNaN(userId) || userId <= 0) {
            console.error('Invalid user ID:', telegramUser.id);
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
        
        console.log('Processed user data:', currentUser);
    }

    // Set user name in header
    document.getElementById('user-name').textContent = 
        `${currentUser.firstName} ${currentUser.lastName || ''}`;

    // Check if user is authenticated and get admin status
    await checkUserAuth();

    // Load initial data
    await loadAvailableDays();
    await loadUserBookings();

    // Show main content
    document.getElementById('loading').style.display = 'none';
    document.getElementById('main-content').style.display = 'block';

    // Set up event listeners
    setupEventListeners();
}

async function checkUserAuth() {
    try {
        // Проверяем что currentUser и его id корректны
        if (!currentUser || !currentUser.id || isNaN(currentUser.id)) {
            console.error('Invalid current user:', currentUser);
            showError('Ошибка данных пользователя. Попробуйте перезапустить приложение.');
            return;
        }
        
        console.log('Checking auth for user ID:', currentUser.id);
        
        const response = await apiRequest(`${API_BASE_URL}/users/${currentUser.id}`);
        
        if (!response.ok) {
            console.error('Auth check failed with status:', response.status);
            if (response.status === 404) {
                showError('Пользователь не найден. Пожалуйста, зарегистрируйтесь в боте сначала');
                return;
            }
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const userData = await response.json();
        console.log('User data received:', userData);
        
        if (userData) {
            isAdmin = userData.is_admin || false;
            
            // Show admin tab if user is admin
            if (isAdmin) {
                document.querySelector('.admin-only').style.display = 'block';
                await loadAdminData();
            }
        } else {
            // User not registered, show registration
            showError('Пожалуйста, зарегистрируйтесь в боте сначала');
        }
    } catch (error) {
        console.error('Auth check failed:', error);
        // Если пользователь не найден, показываем сообщение о регистрации
        showError('Пожалуйста, зарегистрируйтесь в боте сначала');
    }
}

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

function processSlotsForTraining(slots) {
    const goodStartTimes = [];
    
    debugLog(`Processing ${slots.length} slots for training`);
    
    // Удаляем дубликаты по id
    const uniqueSlots = slots.filter((slot, index, self) => 
        index === self.findIndex(s => s.id === slot.id)
    );
    
    debugLog(`After removing duplicates: ${uniqueSlots.length} unique slots`);
    
    // Сортируем по времени начала
    uniqueSlots.sort((a, b) => a.start_time.localeCompare(b.start_time));
    
    // Для тренировки нужно 90 минут подряд
    // Слоты по 60 минут, значит нужно найти начальный слот + еще 30 минут в следующем слоте
    for (let i = 0; i < uniqueSlots.length - 1; i++) {
        const currentSlot = uniqueSlots[i];
        const nextSlot = uniqueSlots[i + 1];
        
        // Проверяем, что текущий слот и следующий идут подряд
        if (currentSlot.end_time === nextSlot.start_time) {
            // Проверяем, что у нас есть минимум 90 минут
            const startTime = new Date(`2000-01-01T${currentSlot.start_time}`);
            const endTime = new Date(`2000-01-01T${nextSlot.end_time}`);
            const durationMinutes = (endTime - startTime) / (1000 * 60);
            
            if (durationMinutes >= 90) {
                goodStartTimes.push(currentSlot);
                debugLog(`Valid training slot found: ${currentSlot.start_time} (${durationMinutes} minutes available)`);
            } else {
                debugLog(`Insufficient time at ${currentSlot.start_time}: only ${durationMinutes} minutes available`);
            }
        } else {
            debugLog(`Gap between slots: ${currentSlot.end_time} -> ${nextSlot.start_time}`);
        }
    }
    
    debugLog(`Found ${goodStartTimes.length} valid training slots`);
    return goodStartTimes;
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
        debugLog('=== СОЗДАНИЕ БРОНИ ===');
        debugLog(`Selected time: ${JSON.stringify(selectedTime)}`);
        debugLog(`Selected day: ${selectedDay}`);
        debugLog(`Current user: ${JSON.stringify(currentUser)}`);
        
        // Рассчитываем правильное время окончания
        // Для 90-минутной тренировки нужно найти время окончания через 90 минут
        const startTime = new Date(`2000-01-01T${selectedTime.start_time}`);
        const endTime = new Date(startTime);
        endTime.setMinutes(endTime.getMinutes() + 90);
        
        const calculatedEndTime = endTime.toTimeString().slice(0, 8);
        debugLog(`Calculated end time: ${calculatedEndTime}`);
        
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
            debugLog('Booking created successfully');
            showSuccess('Запись успешно создана!');
            resetBookingFlow();
            await loadUserBookings();
        } else {
            const error = await response.json();
            debugLog(`Booking error: ${JSON.stringify(error)}`);
            showError(error.detail || 'Ошибка создания записи');
        }
    } catch (error) {
        debugLog(`Booking failed: ${error.message}`);
        showError('Ошибка создания записи');
    }
}

function resetBookingFlow() {
    selectedDay = null;
    selectedTime = null;
    
    document.querySelectorAll('.day-card').forEach(card => card.classList.remove('selected'));
    document.querySelectorAll('.time-slot').forEach(slot => slot.classList.remove('selected'));
    
    document.getElementById('times-section').style.display = 'none';
    document.getElementById('confirmation-section').style.display = 'none';
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
            await loadUserBookings();
        } else {
            showError('Ошибка отмены бронирования');
        }
    } catch (error) {
        console.error('Cancel booking failed:', error);
        showError('Ошибка отмены бронирования');
    }
}

async function rescheduleBooking(bookingId) {
    // First cancel the current booking
    await cancelBooking(bookingId);
    
    // Then switch to booking tab
    switchTab('booking');
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
    document.getElementById('cancel-booking').addEventListener('click', resetBookingFlow);
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