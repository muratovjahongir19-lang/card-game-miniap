"""
Room model definition
"""

from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Room(Base):
    """Room (virtual table) model"""

    __tablename__ = "rooms"

    room_id = Column(Integer, primary_key=True)
    room_name = Column(String(255))
    description = Column(String(500), nullable=True)
    max_players = Column(Integer, default=8)
    current_players_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    is_private = Column(Boolean, default=False)
    
    # Room settings
    language = Column(String(10), default="en")
    age_restriction = Column(Integer, default=18)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    expires_at = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(hours=1))

    def __repr__(self):
        return f"<Room {self.room_id}: {self.room_name}>"

    def is_full(self) -> bool:
        """Check if room is full"""
        return self.current_players_count >= self.max_players

    def is_expired(self) -> bool:
        """Check if room has expired"""
        return datetime.utcnow() > self.expires_at

    def can_join(self, user_age: int) -> bool:
        """Check if user can join room"""
        if self.is_full() or self.is_expired() or not self.is_active:
            return False
        if user_age and user_age < self.age_restriction:
            return False
        return True


class RoomMember(Base):
    """Room member relation model"""

    __tablename__ = "room_members"

    member_id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey("rooms.room_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    position = Column(Integer)  # Position in circle
    joined_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<RoomMember room={self.room_id}, user={self.user_id}>"
