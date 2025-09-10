# Schedule Bot - Universal Training Booking System

A Telegram Mini App for gyms, fitness centers, and sports clubs to manage training session bookings. Includes a web interface, FastAPI backend, and Telegram bot integration.
https://deepwiki.com/An9rewRyan/schedule-bot.git
## Quick Start

```bash
# Clone the repository
git clone <repository-url>
cd schedule-bot-3

# Install dependencies
pip install -r requirements.txt
# Or if you're using uv:
uv pip install -r requirements.txt

# Start all services
python run_dev_yaml.py all
```

After startup, open the ngrok URL that appears in the logs in your browser.

## Project Structure

```
schedule-bot-3/
├── run_dev_yaml.py           # New YAML-based launcher
├── service_composer_mp.py    # Service orchestration engine  
├── run_dev_replica.yaml     # Service configuration
├── scripts/
│   └── update_ngrok_configs.py # Auto-config updater
├── backend/
│   ├── src/
│   │   ├── main.py          # FastAPI application
│   │   ├── api/             # REST API endpoints
│   │   ├── models/          # Database models and schemas
│   │   ├── services/        # Business logic
│   │   ├── repository/      # CRUD operations  
│   │   └── utilities/       # Helper utilities
│   └── requirements.txt
├── frontend/
│   ├── index.html          # Mini App interface
│   ├── app.js             # Frontend logic
│   ├── styles.css         # Styles
│   └── server.py          # Local web server
├── tg_bot/
│   ├── main.py            # Telegram bot
│   ├── handlers/          # Command handlers
│   ├── keyboards/         # Keyboards
│   └── api/              # API clients
└── ngrok.yml             # ngrok configuration
```

## Running the Application

### All services (recommended)
```bash
python run_dev_yaml.py all
```
Starts ngrok + backend + frontend + telegram bot + auto-config updates.

### Interactive menu
```bash
python run_dev_yaml.py
```
Shows a menu to choose what to run.

### Individual services
```bash
python run_dev_yaml.py backend    # API server only
python run_dev_yaml.py frontend   # Web interface only  
python run_dev_yaml.py bot        # Telegram bot only
python run_dev_yaml.py ngrok      # ngrok tunnels only
python run_dev_yaml.py local      # Without ngrok (local only)
```

### Stopping services
```bash
python stop_miniapp.py
```

## Configuration

### Bot Token
Create `tg_bot/constants.py`:
```python
BOT_TOKEN = "your_bot_token_from_botfather"
```

### ngrok
Required for HTTPS and Telegram Mini App functionality:
```bash
# Installation (macOS)
brew install ngrok

# Or download from https://ngrok.com/download

# Add your authtoken
ngrok config add-authtoken YOUR_TOKEN
```

### Database
**Requires PostgreSQL** - the project is configured to use PostgreSQL with asyncpg driver.

1. Install and start PostgreSQL:
```bash
# macOS
brew install postgresql
brew services start postgresql

# Ubuntu/Debian
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql

# Create database (using default settings from db.py)
sudo -u postgres psql
CREATE DATABASE main;
ALTER USER postgres PASSWORD '1234';
\q
```

2. Default connection (in `backend/src/repository/db.py`):
```python
DB_URL = os.getenv('DATABASE_URL', 'postgresql+asyncpg://postgres:1234@localhost:5432/main')
```

3. To change database credentials, either:
   - Set `DATABASE_URL` environment variable
   - Modify the default URL in `backend/src/repository/db.py`

**Required Python packages**: `asyncpg` (already in requirements.txt)

## How It Works

1. **ngrok** starts first and creates HTTPS tunnels
2. **update_ngrok_configs.py** automatically updates configurations with new URLs
3. **backend** starts with updated CORS settings
4. **frontend** gets the current API URL
5. **telegram bot** gets the current Mini App URL

All the magic happens in `run_dev_replica.yaml` - it describes the startup order and hooks for auto-updates.

## Setting Up Mini App in Telegram

After running `python run_dev_yaml.py all`:

1. Find the frontend URL in logs (like `https://XXXXX.ngrok-free.app`)
2. Open @BotFather in Telegram
3. Use `/newapp` command
4. Select your bot
5. App name: "Training Booking"  
6. Description: "Book your training sessions"
7. Paste the URL from logs
8. Upload an icon (optional)

## Features

### For Users:
- View available time slots for selected dates
- Book training sessions
- View their bookings
- Cancel reservations

### For Admins:
- Create weekly schedules
- View all bookings
- Manage users
- Get attendance statistics

## Development

### Hot Reload
All services support live reloading:
- Backend: uvicorn with `--reload`
- Frontend: built-in live reload
- Bot: auto-restart on file changes

### Logs
Color-coded logs by service:
- `[ngrok]` - cyan
- `[backend]` - green  
- `[frontend]` - blue
- `[telegram_bot]` - magenta

### Useful Scripts
```bash
python diagnose.py           # System diagnostics
python view_logs.py          # View all logs
python clear_timeslots.py    # Clear time slots
python create_schedule.py    # Create test schedule
```

## Troubleshooting

### Backend import errors
All fixed! Wrong paths `backend.src.*` were changed to `src.*`.

### ngrok won't start
1. Check installation: `which ngrok`
2. Check authtoken: `ngrok config check`
3. Or run locally: `python run_dev_yaml.py local`

### Mini App won't open
1. Make sure you're using the HTTPS URL from ngrok
2. Verify CORS is configured correctly (update script should handle this)
3. Open the URL in browser first, then in Telegram

### Hooks not executing
Updated `service_composer_mp.py` to support service-level hooks. The `after_ngrok_start` hook runs right after ngrok starts.

## API

Backend is available at:
- Local: http://localhost:8000/api
- ngrok: https://XXXXX.ngrok-free.app/api
- Documentation: /docs or /redoc

Main endpoints:
- `GET /slots/` - list time slots
- `POST /bookings/` - create booking
- `GET /bookings/user/{telegram_id}` - user bookings
- `DELETE /bookings/{booking_id}` - cancel booking

## Requirements

- Python 3.10+
- ngrok (for Mini App)
- Telegram bot token
- PostgreSQL (optional, for production)

## Customization

This system is designed to be universal for any training-based business:

### Gym/Fitness Center
- Configure time slots for different workout types
- Set up trainer-specific sessions
- Manage equipment bookings

### Sports Club
- Schedule practice sessions
- Book courts/fields
- Manage team training slots

### Martial Arts Studio
- Class scheduling
- Private lesson bookings
- Belt testing appointments

### Dance Studio
- Group class registration
- Private lesson scheduling
- Studio rental bookings

Simply modify the slot names, durations, and business logic in the backend to fit your specific needs.

## License

This project is licensed under **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)**.

What this means:
- ✅ You can use, study, and modify the code
- ✅ You can share it with others
- ✅ You can adapt it for your needs
- ❌ No commercial use without permission
- ❌ If you modify and share it, you must use the same license
- ❌ You must give proper attribution

See the [LICENSE](LICENSE) file for the full legal text.
