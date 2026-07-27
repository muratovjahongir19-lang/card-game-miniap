# Bottle Spin Bot Architecture

## Overview

Bottle Spin Bot is a Telegram-based social party game built with:
- **Bot Framework**: python-telegram-bot (async)
- **Database**: PostgreSQL + SQLAlchemy ORM
- **Cache**: Redis
- **Deployment**: Docker + Docker Compose

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Telegram Client                         │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ Messages & Callbacks
                     │
┌────────────────────▼────────────────────────────────────────┐
│                  Telegram Bot API                           │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ Updates
                     │
┌────────────────────▼────────────────────────────────────────┐
│         python-telegram-bot Application                     │
├─────────────────────────────────────────────────────────────┤
│ • CommandHandler (/start, /help, /profile, etc)             │
│ • CallbackQueryHandler (inline buttons)                     │
│ • MessageHandler (text messages)                            │
│ • ErrorHandler                                              │
└────────────────────┬────────────────────────────────────────┘
                     │
    ┌────────────────┼────────────────┐
    │                │                │
    ▼                ▼                ▼
┌─────────┐  ┌────────────┐  ┌─────────────┐
│ Handlers│  │  Services  │  │  Middleware │
│         │  │            │  │             │
│ start   │  │ room       │  │ auth        │
│ rooms   │  │ game       │  │ rate limit  │
│ game    │  │ user       │  │             │
│ gifts   │  │ gift       │  │             │
│ profile │  │ payment    │  │             │
│ shop    │  │            │  │             │
└─────────┘  └────────────┘  └─────────────┘
    │                │                │
    └────────────────┼────────────────┘
                     │
    ┌────────────────┼────────────────┐
    │                │                │
    ▼                ▼                ▼
┌─────────────┐ ┌─────────┐ ┌──────────────┐
│ PostgreSQL  │ │  Redis  │ │ External API │
│ Database    │ │ Cache   │ │ (Payments)   │
│             │ │         │ │              │
│ • Users     │ │Sessions │ │ Stripe/etc   │
│ • Rooms     │ │Game State│ │              │
│ • Games     │ │Counters  │ │              │
│ • Gifts     │ │          │ │              │
│ • Transactions │        │ │              │
└─────────────┘ └─────────┘ └──────────────┘
```

## Module Structure

### 1. Handlers (`bot/handlers/`)
Entry points for user interactions

- **start.py**: `/start`, `/help`, `/cancel`
- **rooms.py**: Room creation, joining, listing
- **game.py**: Game logic, bottle spin, decisions
- **gifts.py**: Gift selection and sending
- **profile.py**: User profile viewing and editing
- **shop.py**: VIP purchases, coin shop
- **callbacks.py**: All inline button callbacks

### 2. Models (`bot/models/`)
Database ORM models

- **user.py**: User entity with economy, stats, VIP
- **room.py**: Room and RoomMember entities
- **game_session.py**: Game session with decisions
- **gift.py**: Gift types and history
- **transaction.py**: Payment/coin transactions

### 3. Services (`bot/services/`)
Business logic layer

- **room_service.py**: 
  - `create_room()` - Create new room
  - `join_room()` - User joins room
  - `get_opposite_gender()` - Find match
  - `auto_match()` - Automated matching

- **game_service.py**:
  - `spin_bottle()` - Select random opponent
  - `handle_decision()` - Process player decision
  - `finalize_game()` - Calculate rewards
  - `award_coins()` - Give rewards

- **user_service.py**:
  - `get_or_create_user()` - User registration
  - `update_profile()` - Profile editing
  - `add_coins()` / `add_stars()` - Balance updates
  - `consume_energy()` - Energy deduction

- **gift_service.py**:
  - `send_gift()` - Send gift to user
  - `get_available_gifts()` - Gift catalog
  - `calculate_gift_cost()` - VIP discounts

- **payment_service.py**:
  - `process_stars_payment()` - Telegram Stars
  - `convert_stars_to_coins()` - Currency exchange
  - `verify_payment()` - Payment validation

### 4. Database (`bot/database/`)
Database connection and session management

- **db.py**: SQLAlchemy engine, session factory
- **session.py**: Async session context manager

### 5. Keyboards (`bot/keyboards/`)
UI components

- **inline.py**: Inline keyboard builders
- **reply.py**: Reply keyboard builders

### 6. Utils (`bot/utils/`)
Helper functions

- **constants.py**: Game constants, enums, messages
- **validators.py**: Input validation
- **helpers.py**: Utility functions

### 7. Middleware (`bot/middleware/`)
Request processing

- **auth.py**: User authorization checks

## Game Flow

### Room Creation
```
User → /create or "Create Room" button
   ↓
Create new Room entity (DB)
   ↓
Add user as first member
   ↓
Generate invite code (if needed)
   ↓
Display room info + waiting list
```

### Joining Room
```
User → /join or select from list
   ↓
Validate room (not full, not expired, age check)
   ↓
Add to RoomMembers
   ↓
Assign position in circle (alternate M/F)
   ↓
Notify other players
   ↓
Start game loop if ≥2 players
```

### Bottle Spin Round
```
Timer triggers every 30 seconds
   ↓
Check room has ≥2 active players
   ↓
Get last spinner → spin_bottle()
   ↓
Select random opposite gender → select_match()
   ↓
Create GameSession (pending)
   ↓
Send decision buttons to both players
   ↓
Set 10-second timeout
   ↓
Wait for both decisions or timeout
   ↓
Finalize → award coins/popularity
   ↓
Move to next player
```

### Decision Handling
```
Player clicks "Kiss" or "Skip"
   ↓
Update GameSession decision
   ↓
Check if both decided
   ↓
If both ❤️:
   - kiss_count++
   - +50 coins each
   - +5 popularity each
   - Send celebration animation
   ↓
If either ❌:
   - Move on
   - No rewards
   ↓
Update profiles (coins, popularity)
```

## Database Schema

### Key Tables

**users**
```sql
user_id (PK)
username, first_name, last_name
avatar_url, gender, bio, age
stars_balance, coins_balance
vip_until
energy, last_energy_update
popularity_score, total_kisses, total_gifts_sent, total_gifts_received
is_banned, is_verified
created_at, updated_at
```

**rooms**
```sql
room_id (PK)
room_name, description
max_players, current_players_count
is_active, is_private
age_restriction
created_at, updated_at, expires_at
```

**game_sessions**
```sql
session_id (PK)
room_id (FK), player1_id (FK), player2_id (FK)
player1_decision, player2_decision, result
kiss_count
created_at, decision_deadline, completed_at
```

**gift_history**
```sql
history_id (PK)
gift_type_id (FK), from_user_id (FK), to_user_id (FK), room_id (FK)
cost_coins
sent_at
```

## Async Architecture

All operations use async/await:

```python
# Handlers are async
async def start_command(update, context):
    await update.message.reply_text("...")

# Services return coroutines
async def create_room(user_id, room_name):
    session = await get_session()
    room = Room(...)
    session.add(room)
    await session.commit()
    return room

# Database calls are async
async with get_session() as session:
    user = await session.get(User, user_id)
```

## Scaling Considerations

### Horizontal Scaling
- Use connection pooling for PostgreSQL
- Redis for distributed sessions
- Separate worker processes for game loops
- Load balancer for multiple bot instances

### Performance Optimization
- Cache room lists in Redis
- Use database indexes on frequent queries
- Batch updates for bulk operations
- Lazy load user profiles

### Monitoring
- Prometheus metrics
- CloudWatch logs
- Sentry for error tracking
- Custom metrics (active rooms, players, etc)

## Security

1. **Authentication**: Telegram user_id validation
2. **Authorization**: Room access checks
3. **Input Validation**: All user inputs sanitized
4. **Rate Limiting**: Prevent spam (3 spins/min, 5 msgs/min)
5. **Financial**: Verify all payments
6. **Data**: Encrypt sensitive data at rest

## Deployment

### Development
```bash
python bot/main.py
```

### Production (Docker)
```bash
docker-compose up -d
```

### Environment
- `TELEGRAM_BOT_TOKEN`: Bot token from @BotFather
- `DATABASE_URL`: PostgreSQL connection
- `REDIS_URL`: Redis connection
- `ENVIRONMENT`: "production" or "development"

## Future Enhancements

1. **Social Features**
   - Friend lists
   - Following system
   - Direct messaging

2. **Gamification**
   - Achievements/badges
   - Seasonal leaderboards
   - Quests/challenges

3. **Monetization**
   - Premium emotes
   - Room themes
   - Special effects

4. **Analytics**
   - User engagement metrics
   - Revenue analytics
   - Retention cohorts

5. **Mobile App**
   - Native iOS/Android
   - Cross-platform sync
   - Notifications
