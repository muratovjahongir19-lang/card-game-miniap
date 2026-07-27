"""
User model definition
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """User model"""

    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=True)
    first_name = Column(String(255))
    last_name = Column(String(255), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    gender = Column(String(1), nullable=True)  # M, F, O
    bio = Column(String(500), nullable=True)
    age = Column(Integer, nullable=True)

    # Economy
    stars_balance = Column(Integer, default=0)  # Telegram Stars
    coins_balance = Column(Integer, default=100)  # In-game currency

    # VIP
    vip_until = Column(DateTime, nullable=True)  # NULL = no VIP

    # Energy
    energy = Column(Integer, default=100)
    last_energy_update = Column(DateTime, default=datetime.utcnow)

    # Stats
    popularity_score = Column(Integer, default=0)
    total_kisses = Column(Integer, default=0)
    total_gifts_sent = Column(Integer, default=0)
    total_gifts_received = Column(Integer, default=0)

    # Flags
    is_banned = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.user_id}: {self.username or self.first_name}>"

    def is_vip(self) -> bool:
        """Check if user has active VIP"""
        if self.vip_until is None:
            return False
        return self.vip_until > datetime.utcnow()

    def add_coins(self, amount: int) -> None:
        """Add coins to balance"""
        self.coins_balance += amount

    def add_stars(self, amount: int) -> None:
        """Add stars to balance"""
        self.stars_balance += amount

    def add_popularity(self, amount: int) -> None:
        """Add popularity points"""
        self.popularity_score += amount

    def add_energy(self, amount: int) -> None:
        """Add energy (capped at max)"""
        self.energy = min(self.energy + amount, 100)

    def consume_energy(self, amount: int) -> bool:
        """Consume energy, return True if successful"""
        if self.energy >= amount:
            self.energy -= amount
            return True
        return False
