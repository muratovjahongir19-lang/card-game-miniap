# Bottle Spin Bot 🍾

Социальная игра-вечеринка на базе Telegram — виртуальный аналог классической игры «Целуй и знакомься» с механикой вращающейся бутылочки.

## 📋 Описание

Бот создает виртуальные комнаты, где игроки:
- Вращают бутылочку и получают случайного соперника
- Решают: целоваться или пропустить
- Обмениваются виртуальными подарками
- Общаются в чате комнаты и личных сообщениях
- Зарабатывают очки популярности

## 🎮 Основные фичи

- ✅ Виртуальные столы (комнаты) с чередованием парней и девушек
- ✅ Автоматическое вращение бутылочки каждые 30 сек
- ✅ Система принятия/отклонения (кнопки за 5-10 сек)
- ✅ Счетчик поцелуев между игроками
- ✅ Виртуальные подарки (цветы, напитки, сладости)
- ✅ Уровень популярности
- ✅ Общий и приватный чат
- ✅ VIP-статус и монетизация
- ✅ Система энергии/лимитов
- ✅ Telegram Stars платежи

## 🛠 Стек технологий

- **Python 3.10+**
- **python-telegram-bot** (AsyncIO)
- **SQLAlchemy** (ORM для БД)
- **PostgreSQL/SQLite** (зависит от окружения)
- **Redis** (кэширование и сессии)
- **Aiogram** или нативный API

## 📁 Структура проекта

```
bottle_spin_bot/
├── bot/
│   ├── __init__.py
│   ├── main.py                 # Главная точка входа
│   ├── config.py               # Конфигурация и переменные окружения
│   ├── handlers/
│   │   ├── __init__.py
│   │   ├── start.py            # /start команда
│   │   ├── rooms.py            # Создание и управление комнатами
│   │   ├── game.py             # Игровая логика (вращение, решения)
│   │   ├── gifts.py            # Система подарков
│   │   ├── profile.py          # Профили пользователей
│   │   ├── shop.py             # VIP и магазин
│   │   └── callbacks.py        # Callback queries
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py             # Модель пользователя
│   │   ├── room.py             # Модель комнаты
│   │   ├── game_session.py     # Модель игровой сессии
│   │   ├── gift.py             # Модель подарков
│   │   └── transaction.py      # Модель транзакций
│   ├── services/
│   │   ├── __init__.py
│   │   ├── room_service.py     # Логика комнат
│   │   ├── game_service.py     # Логика игры
│   │   ├── user_service.py     # Логика пользователя
│   │   ├── gift_service.py     # Логика подарков
│   │   └── payment_service.py  # Логика платежей (Stars)
│   ├── database/
│   │   ├── __init__.py
│   │   ├── db.py               # Инициализация БД
│   │   └── session.py          # Менеджер сессий
│   ├── keyboards/
│   │   ├── __init__.py
│   │   ├── inline.py           # Inline кнопки
│   │   └── reply.py            # Reply кнопки
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── constants.py        # Константы игры
│   │   ├── validators.py       # Валидация данных
│   │   └── helpers.py          # Вспомогательные функции
│   └── middleware/
│       ├── __init__.py
│       └── auth.py             # Проверка авторизации
├── tests/
│   ├── __init__.py
│   ├── test_game_logic.py
│   ├── test_room_service.py
│   └── test_user_service.py
├── migrations/
│   └── versions/
├── .env.example
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
├── setup.py
└── README.md
```

## 🚀 Быстрый старт

### 1. Клонирование
```bash
git clone https://github.com/muratovjahongir19-lang/card-game-miniap.git
cd card-game-miniap/bottle_spin_bot
```

### 2. Установка зависимостей
```bash
python -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Конфигурация
```bash
cp .env.example .env
# Отредактируйте .env:
# - TELEGRAM_BOT_TOKEN=ваш_токен
# - DATABASE_URL=postgresql://user:pass@localhost/bottle_spin_bot
# - REDIS_URL=redis://localhost:6379
```

### 4. Миграции БД
```bash
alembic upgrade head
```

### 5. Запуск бота
```bash
python bot/main.py
```

## 📊 Схема базы данных

### Users
- `user_id` (PK)
- `username`
- `first_name`
- `last_name`
- `avatar_url`
- `gender` (M/F)
- `bio`
- `stars_balance` (Telegram Stars)
- `coins_balance` (внутриигровая валюта)
- `vip_until` (NULL если нет VIP)
- `energy` (текущая энергия)
- `popularity_score`
- `created_at`
- `updated_at`

### Rooms
- `room_id` (PK)
- `room_name`
- `max_players`
- `current_players_count`
- `is_active`
- `created_at`
- `expires_at`

### Room Members
- `member_id` (PK)
- `room_id` (FK)
- `user_id` (FK)
- `joined_at`
- `position` (порядок в кругу)

### Game Sessions
- `session_id` (PK)
- `room_id` (FK)
- `player1_id` (FK)
- `player2_id` (FK)
- `result` (accepted/rejected)
- `kiss_count`
- `created_at`

### Gifts
- `gift_id` (PK)
- `gift_type` (flower/drink/toy/candy)
- `cost_coins`
- `icon_emoji`

### Gift History
- `history_id` (PK)
- `gift_id` (FK)
- `from_user_id` (FK)
- `to_user_id` (FK)
- `room_id` (FK)
- `sent_at`

### Transactions
- `transaction_id` (PK)
- `user_id` (FK)
- `type` (purchase/refund/gift)
- `amount`
- `description`
- `created_at`

## 🎮 Игровой процесс

### Сценарий игры:
1. Игрок открывает бота → `/start`
2. Выбирает комнату или создает новую
3. Присоединяется к столу (система чередует М/Ж)
4. Каждые 30 сек бутылочка вращается
5. Система выбирает случайного соперника противоположного пола
6. Обоим игрокам отправляются кнопки:
   - ❤️ Целовать (5 сек на ответ)
   - ❌ Пропустить
7. Результат:
   - Оба выбрали ❤️ → kiss_count++, анимация, +5 популярности
   - Хотя бы один ❌ → игра продолжается
8. Между ходами можно:
   - Отправить подарок (+10 популярности получателю)
   - Написать в общий чат
   - Перейти в личное сообщение

## 💰 Монетизация

### Внутриигровая валюта
- **Coins**: Зарабатываются за поцелуи, подарки, участие
- **Telegram Stars**: Покупаются за реальные деньги, конвертируются в Coins

### VIP-пакеты
- **30 дней**: 99 Stars
- **90 дней**: 249 Stars
- **6 месяцев**: 449 Stars

### VIP преимущества
- Выделенный ник (✨ рядом с именем)
- Доступ в закрытые "элитные" комнаты
- 10 бесплатных подарков в день
- Нет рекламы
- +20% к зарабатываемым Coins

### Система энергии
- Начальная энергия: 100
- Вращение = -5 энергии
- Восполнение: +1 в минуту (максимум 100)
- Восстановление полностью за 10 Stars

## 🔒 Безопасность

- ✅ Валидация user_id на каждый запрос
- ✅ Rate limiting (3 вращения в минуту)
- ✅ Блокировка спама (max 5 сообщений в минуту)
- ✅ Проверка возраста (18+)
- ✅ Система репортинга и модерации
- ✅ Шифрование чувствительных данных

## 📚 API эндпоинты (для интеграции)

```
GET  /api/v1/user/{user_id}
GET  /api/v1/rooms
POST /api/v1/rooms
POST /api/v1/rooms/{room_id}/join
POST /api/v1/game/spin
POST /api/v1/game/decide
POST /api/v1/gifts/send
GET  /api/v1/user/{user_id}/profile
POST /api/v1/payments/stars
```

## 📝 Лицензия

MIT License

## 👨‍💻 Контактная информация

- GitHub: [@muratovjahongir19-lang](https://github.com/muratovjahongir19-lang)
- Telegram: [@bottle_spin_bot](https://t.me/bottle_spin_bot)

---

**Made with ❤️ and 🍾**
