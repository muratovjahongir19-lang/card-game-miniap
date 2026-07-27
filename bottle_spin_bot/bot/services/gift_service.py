"""
Gift system service
"""

from sqlalchemy.orm import Session
from bot.models import GiftType, GiftHistory, DEFAULT_GIFTS
from datetime import datetime


class GiftService:
    """Service for gift operations"""

    @staticmethod
    def init_gifts(session: Session):
        """Initialize default gift types"""
        existing = session.query(GiftType).first()
        if existing:
            return

        for gift_data in DEFAULT_GIFTS:
            gift = GiftType(
                name=gift_data["name"],
                emoji=gift_data["emoji"],
                cost_coins=gift_data["cost_coins"],
            )
            session.add(gift)

        session.commit()

    @staticmethod
    def get_gifts(session: Session) -> list:
        """Get all available gifts"""
        return session.query(GiftType).all()

    @staticmethod
    def send_gift(
        session: Session,
        gift_type_id: int,
        from_user_id: int,
        to_user_id: int,
        room_id: int = None,
    ) -> GiftHistory:
        """Send gift from one user to another"""
        from bot.models import User

        gift = session.query(GiftType).get(gift_type_id)
        if not gift:
            return None

        # Check sender has enough coins
        sender = session.query(User).get(from_user_id)
        if sender.coins_balance < gift.cost_coins:
            return None

        # Create history record
        history = GiftHistory(
            gift_type_id=gift_type_id,
            from_user_id=from_user_id,
            to_user_id=to_user_id,
            room_id=room_id,
            cost_coins=gift.cost_coins,
            sent_at=datetime.utcnow(),
        )

        # Deduct coins from sender
        sender.coins_balance -= gift.cost_coins

        # Add popularity to receiver
        receiver = session.query(User).get(to_user_id)
        receiver.popularity_score += 10
        receiver.total_gifts_received += 1
        sender.total_gifts_sent += 1

        session.add(history)
        session.commit()

        return history

    @staticmethod
    def get_user_gift_history(
        session: Session, user_id: int, limit: int = 20
    ) -> list:
        """Get gifts received by user"""
        return (
            session.query(GiftHistory)
            .filter(GiftHistory.to_user_id == user_id)
            .order_by(GiftHistory.sent_at.desc())
            .limit(limit)
            .all()
        )
