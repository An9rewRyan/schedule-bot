/**
 * Configuration module
 * Handles ngrok tunnel discovery and API URL configuration
 */
class Config {
    constructor() {
        this.backendUrl = null;
        this.isInitialized = false;
    }

    async initialize() {
        if (this.isInitialized) {
            console.log('Config already initialized, skipping...');
            return;
        }

        console.log('Initializing config...');
        
        try {
            // Делаем запрос к frontend серверу для получения backend URL
            const configUrl = `${window.location.origin}/api/config`;
            console.log(`Fetching backend config from ${configUrl}`);
            
            const response = await fetch(configUrl);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const data = await response.json();
            console.log('Config response:', data);
            
            if (data.status === 'error') {
                throw new Error(data.error);
            }
            
            if (!data.backend_url) {
                throw new Error('Backend URL не получен от сервера');
            }
            
            this.backendUrl = data.backend_url;
            this.isInitialized = true;
            
            console.log(`✅ Config initialized successfully. Backend URL: ${this.backendUrl}`);
            
        } catch (error) {
            console.error('❌ Config initialization failed:', error);
            throw new Error(`Ngrok недоступен: ${error.message}. Попробуйте позже.`);
        }
    }

    getBackendUrl() {
        if (!this.isInitialized) {
            throw new Error('Config не инициализирован. Вызовите initialize() сначала.');
        }
        return this.backendUrl;
    }

    isReady() {
        return this.isInitialized;
    }
}

// Экспортируем singleton экземпляр
export const config = new Config(); 