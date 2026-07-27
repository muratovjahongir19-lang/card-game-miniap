"""
Configuration settings
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_file = Path(__file__).parent.parent / ".env"
load_dotenv(env_file)


class Settings:
    """Application settings"""

    # Telegram
    telegram_bot_token: str = os.getenv(
        "TELEGRAM_BOT_TOKEN", "your-token-here"
    )
    telegram_bot_username: str = os.getenv("TELEGRAM_BOT_USERNAME", "bottle_spin_bot")

    # Database
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql://bottle_user:bottle_pass@localhost:5432/bottle_spin_bot",
    )

    # Redis
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # Application
    environment: str = os.getenv("ENVIRONMENT", "development")
    debug: bool = os.getenv("DEBUG", "True").lower() == "true"
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

    # Admin
    admin_user_list: list = [int(uid) for uid in os.getenv("ADMIN_USERS", "").split(",") if uid.strip()]

    # Game settings (can be overridden)
    MAX_ROOM_SIZE: int = 12
    SPIN_INTERVAL: int = 30
    DECISION_TIMEOUT: int = 10
    INITIAL_ENERGY: int = 100


settings = Settings()
