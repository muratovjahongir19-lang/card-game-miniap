"""
Game session model definition
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()


class DecisionEnum(str, enum.Enum):
    """Game decision enum"""
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    TIMEOUT = "timeout"
    PENDING = "pending"


class GameSession(Base):
    """Game session model - records each bottle spin round"""

    __tablename__ = "game_sessions"

    session_id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey("rooms.room_id"), nullable=False)
    
    # Players
    player1_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    player2_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    # Decisions
    player1_decision = Column(Enum(DecisionEnum), default=DecisionEnum.PENDING)
    player2_decision = Column(Enum(DecisionEnum), default=DecisionEnum.PENDING)

    # Result
    result = Column(Enum(DecisionEnum), nullable=True)  # Final result
    kiss_count = Column(Integer, default=0)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    decision_deadline = Column(DateTime)  # When decisions must be made by
    completed_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<GameSession {self.session_id}: {self.player1_id} vs {self.player2_id}>"

    def is_both_decided(self) -> bool:
        """Check if both players have decided"""
        return (
            self.player1_decision != DecisionEnum.PENDING
            and self.player2_decision != DecisionEnum.PENDING
        )

    def finalize_result(self) -> DecisionEnum:
        """Finalize the game result based on both decisions"""
        if self.player1_decision == DecisionEnum.ACCEPTED and self.player2_decision == DecisionEnum.ACCEPTED:
            self.result = DecisionEnum.ACCEPTED
            self.kiss_count = 1
        else:
            self.result = DecisionEnum.REJECTED
            self.kiss_count = 0

        self.completed_at = datetime.utcnow()
        return self.result
