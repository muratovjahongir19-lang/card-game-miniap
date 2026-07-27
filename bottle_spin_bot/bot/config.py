"""
Configuration module for Bottle Spin Bot
Loads environment variables and provides central config management
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Main application settings"""

    # Telegram
    telegram_bot_token: str
    telegram_bot_username: str = "bottle_spin_bot"
    webapp_url: str = "https://magnificent-kitten-2245c0.netlify.app"

    # Database
    database_url: str
    
    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # Application
    debug: bool = False
    log_level: str = "INFO"
    environment: str = "development"

    # Game Settings
    max_players_per_room: int = 8
    spin_interval_seconds: int = 30
    decision_timeout_seconds: int = 10
    min_user_age: int = 18

    # Monetization
    vip_monthly_price: int = 99  # Telegram Stars
    vip_quarterly_price: int = 249
    vip_biannual_price: int = 449
    initial_coins: int = 100
    initial_energy: int = 100
    energy_recovery_rate: int = 1  # per minute
    max_energy: int = 100

    # Admin
    admin_user_ids: str = ""  # Comma-separated
    support_chat_id: Optional[int] = None

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_prefix: str = "/api/v1"

    # Security
    secret_key: str = "change-me-in-production"
    algorithm: str = "HS256"

    class Config:
        env_file = ".env"
        case_sensitive = False

    @property
    def admin_user_list(self) -> list[int]:
        """Parse admin user IDs from comma-separated string"""
        if not self.admin_user_ids:
            return []
        return [int(uid.strip()) for uid in self.admin_user_ids.split(",")]


# Load settings
settings = Settings()

# Export for convenience
__all__ = ["settings"]
