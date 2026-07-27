"""
Gift model definition
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class GiftType(Base):
    """Gift types catalog"""

    __tablename__ = "gift_types"

    gift_type_id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    emoji = Column(String(10))
    cost_coins = Column(Integer)
    description = Column(String(500), nullable=True)

    def __repr__(self):
        return f"<GiftType {self.emoji} {self.name}>"


class GiftHistory(Base):
    """Gift sending history"""

    __tablename__ = "gift_history"

    history_id = Column(Integer, primary_key=True)
    gift_type_id = Column(Integer, ForeignKey("gift_types.gift_type_id"), nullable=False)
    from_user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    to_user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.room_id"), nullable=True)
    cost_coins = Column(Integer)
    sent_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<GiftHistory {self.from_user_id} -> {self.to_user_id}>"


# Default gift types
DEFAULT_GIFTS = [
    {"name": "Rose", "emoji": "🌹", "cost_coins": 10},
    {"name": "Tulip", "emoji": "🌷", "cost_coins": 10},
    {"name": "Wine", "emoji": "🍷", "cost_coins": 20},
    {"name": "Beer", "emoji": "🍺", "cost_coins": 15},
    {"name": "Cake", "emoji": "🎂", "cost_coins": 25},
    {"name": "Chocolate", "emoji": "🍫", "cost_coins": 15},
    {"name": "Ring", "emoji": "💍", "cost_coins": 50},
    {"name": "Heart", "emoji": "❤️", "cost_coins": 10},
    {"name": "Star", "emoji": "⭐", "cost_coins": 10},
    {"name": "Diamond", "emoji": "💎", "cost_coins": 100},
]
