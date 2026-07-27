# Installation Guide

## Prerequisites

- Python 3.10+
- PostgreSQL 13+
- Redis 6+
- Git
- Docker & Docker Compose (optional)

## Local Development Setup

### 1. Clone Repository

```bash
git clone https://github.com/muratovjahongir19-lang/card-game-miniap.git
cd card-game-miniap/bottle_spin_bot
```

### 2. Create Virtual Environment

```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Setup Environment Variables

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# Get token from @BotFather on Telegram
TELEGRAM_BOT_TOKEN=your_token_here

# PostgreSQL (local)
DATABASE_URL=postgresql://user:password@localhost:5432/bottle_spin_bot

# Redis (local)
REDIS_URL=redis://localhost:6379/0

# Application
ENVIRONMENT=development
DEBUG=True
LOG_LEVEL=DEBUG
```

### 5. Setup PostgreSQL

#### Option A: Using Docker
```bash
docker run --name bottle_spin_db \
  -e POSTGRES_USER=bottle_user \
  -e POSTGRES_PASSWORD=bottle_pass \
  -e POSTGRES_DB=bottle_spin_bot \
  -p 5432:5432 \
  -d postgres:16-alpine
```

#### Option B: Local Installation
```bash
# macOS with Homebrew
brew install postgresql@16
brew services start postgresql@16

# Create database
createuser bottle_user -P
createdb -O bottle_user bottle_spin_bot
```

### 6. Setup Redis

#### Option A: Using Docker
```bash
docker run --name bottle_spin_redis \
  -p 6379:6379 \
  -d redis:7-alpine
```

#### Option B: Local Installation
```bash
# macOS with Homebrew
brew install redis
brew services start redis

# Verify connection
redis-cli ping  # Should respond with PONG
```

### 7. Initialize Database

```bash
# Create tables
alembic upgrade head

# Or run migrations manually
python -c "from bot.database import db; db.init_db()"
```

### 8. Verify Setup

```bash
# Test database connection
python -c "from bot.database import get_session; print('DB OK')"

# Test Redis connection
python -c "import redis; r = redis.from_url('redis://localhost:6379'); print(r.ping())"

# Check bot token
python -c "from bot.config import settings; print(f'Bot: {settings.telegram_bot_username}')"
```

### 9. Run Bot

```bash
python bot/main.py
```

You should see:
```
🚀 Starting Bottle Spin Bot...
Environment: development
Debug mode: True
```

## Docker Compose Setup (Recommended)

### 1. Prepare Environment

```bash
cp .env.example .env
# Edit .env with your TELEGRAM_BOT_TOKEN
```

### 2. Build and Start

```bash
docker-compose up -d
```

This will start:
- PostgreSQL on `localhost:5432`
- Redis on `localhost:6379`
- Bot service

### 3. View Logs

```bash
docker-compose logs -f bot
```

### 4. Stop Services

```bash
docker-compose down
```

### 5. Restart Services

```bash
docker-compose restart
```

## Troubleshooting

### Issue: "No module named 'bot'"

**Solution:**
```bash
# Make sure you're in bottle_spin_bot directory
cd bottle_spin_bot

# Add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Issue: "TELEGRAM_BOT_TOKEN not found"

**Solution:**
1. Get token from @BotFather on Telegram
2. Add to `.env` file
3. Verify with: `echo $TELEGRAM_BOT_TOKEN`

### Issue: "psycopg2 installation error"

**Solution:**
```bash
# macOS
brew install libpq
export LDFLAGS="-L/usr/local/opt/libpq/lib"
export CPPFLAGS="-I/usr/local/opt/libpq/include"
pip install psycopg2

# Ubuntu/Debian
sudo apt-get install libpq-dev
pip install psycopg2

# Windows (use pre-compiled wheel)
pip install psycopg2-binary
```

### Issue: "Redis connection refused"

**Solution:**
1. Check Redis is running: `redis-cli ping`
2. Verify REDIS_URL in `.env`
3. Try: `redis-cli` to enter CLI
4. Restart Redis: `brew services restart redis`

### Issue: "Database connection error"

**Solution:**
1. Verify PostgreSQL is running
2. Test connection: `psql postgresql://user:password@localhost:5432/bottle_spin_bot`
3. Check credentials in `.env`
4. Create database if not exists: `createdb -U bottle_user bottle_spin_bot`

### Issue: "Bot doesn't respond to messages"

**Solution:**
1. Verify token is correct
2. Check bot is in polling mode: `application.run_polling()`
3. Check logs: `python bot/main.py 2>&1 | tee bot.log`
4. Test with @BotFather: `/start` command
5. Verify firewall/VPN not blocking Telegram

## Database Migrations

### Create New Migration

```bash
alembic revision --autogenerate -m "Description of changes"
```

### Apply Migrations

```bash
alembic upgrade head
```

### Revert Migration

```bash
alembic downgrade -1
```

### View Migration History

```bash
alembic current
alembic history
```

## Development Tips

### Hot Reload (Development)

```bash
pip install watchdog
# Then use auto-reloader
# In your editor or with: python-m watchmedo auto-restart -d . -p '*.py' -- python bot/main.py
```

### Running Tests

```bash
pip install pytest pytest-asyncio
pytest tests/
```

### Code Formatting

```bash
pip install black flake8
black bot/
flake8 bot/
```

### Database Inspection

```bash
# Connect to database
psql postgresql://bottle_user:bottle_pass@localhost:5432/bottle_spin_bot

# List tables
\dt

# View table schema
\d users

# View data
SELECT * FROM users LIMIT 5;
```

### Redis Inspection

```bash
# Connect to Redis
redis-cli

# View keys
KEYS *

# View user sessions
HGETALL session:user_id

# Clear cache
FLUSHDB
```

## Production Deployment

### 1. Use Production Settings

```env
ENVIRONMENT=production
DEBUG=False
LOG_LEVEL=INFO
```

### 2. Use Secret Key

```env
SECRET_KEY=generate_a_strong_random_key
```

Generate with:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 3. Use Production Database

```env
DATABASE_URL=postgresql://user:password@prod-server:5432/bottle_spin_bot
```

### 4. Use External Redis

```env
REDIS_URL=redis://:password@redis.prod-server:6379/0
```

### 5. Setup HTTPS (if using webhook)

Certificate from Let's Encrypt:
```bash
certbot certonly --standalone -d yourdomain.com
```

### 6. Deploy with Docker

```bash
docker-compose -f docker-compose.prod.yml up -d
```

### 7. Setup Monitoring

Monitor with:
- New Relic
- DataDog
- Sentry (error tracking)
- Prometheus (metrics)

## Getting Help

1. Check logs: `python bot/main.py`
2. Review README.md
3. Check ARCHITECTURE.md
4. Search GitHub issues
5. Create new issue with:
   - Error message
   - Python version
   - OS
   - Steps to reproduce

## Next Steps

1. ✅ Setup complete!
2. 📝 Review bot/handlers/ for handler examples
3. 🧪 Test with `/start` command
4. 📖 Read ARCHITECTURE.md
5. 💻 Start developing!

---

Happy coding! 🚀
