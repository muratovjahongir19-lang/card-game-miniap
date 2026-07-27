"""
User management service
"""

from sqlalchemy.orm import Session
from bot.models import User
from datetime import datetime, timedelta


class UserService:
    """Service for user operations"""

    @staticmethod
    def get_or_create_user(
        session: Session,
        user_id: int,
        username: str = None,
        first_name: str = None,
        last_name: str = None,
    ) -> User:
        """Get existing user or create new one"""
        user = session.query(User).get(user_id)

        if user:
            return user

        # Create new user
        user = User(
            user_id=user_id,
            username=username,
            first_name=first_name or username,
            last_name=last_name,
            coins_balance=100,
            energy=100,
            stars_balance=0,
        )
        session.add(user)
        session.commit()

        return user

    @staticmethod
    def update_profile(
        session: Session,
        user_id: int,
        first_name: str = None,
        last_name: str = None,
        bio: str = None,
        age: int = None,
        gender: str = None,
    ) -> User:
        """Update user profile"""
        user = session.query(User).get(user_id)

        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if bio:
            user.bio = bio
        if age:
            user.age = age
        if gender:
            user.gender = gender

        user.updated_at = datetime.utcnow()
        session.commit()

        return user

    @staticmethod
    def add_coins(session: Session, user_id: int, amount: int) -> User:
        """Add coins to user"""
        user = session.query(User).get(user_id)
        user.coins_balance += amount
        session.commit()
        return user

    @staticmethod
    def add_stars(session: Session, user_id: int, amount: int) -> User:
        """Add stars to user"""
        user = session.query(User).get(user_id)
        user.stars_balance += amount
        session.commit()
        return user

    @staticmethod
    def add_popularity(session: Session, user_id: int, amount: int) -> User:
        """Add popularity points"""
        user = session.query(User).get(user_id)
        user.popularity_score += amount
        session.commit()
        return user

    @staticmethod
    def consume_energy(session: Session, user_id: int, amount: int) -> bool:
        """Try to consume energy"""
        user = session.query(User).get(user_id)

        if user.energy >= amount:
            user.energy -= amount
            session.commit()
            return True

        return False

    @staticmethod
    def recover_energy(session: Session, user_id: int) -> User:
        """Recover energy over time"""
        user = session.query(User).get(user_id)
        now = datetime.utcnow()
        minutes_passed = (now - user.last_energy_update).total_seconds() / 60
        energy_gained = int(minutes_passed * 1)  # 1 energy per minute

        user.energy = min(user.energy + energy_gained, 100)
        user.last_energy_update = now
        session.commit()

        return user

    @staticmethod
    def activate_vip(
        session: Session, user_id: int, months: int = 1
    ) -> User:
        """Activate VIP subscription"""
        user = session.query(User).get(user_id)
        user.vip_until = datetime.utcnow() + timedelta(days=30 * months)
        session.commit()
        return user

    @staticmethod
    def get_leaderboard(
        session: Session, limit: int = 10
    ) -> list:
        """Get popularity leaderboard"""
        return (
            session.query(User)
            .order_by(User.popularity_score.desc())
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_top_kiss_givers(
        session: Session, limit: int = 10
    ) -> list:
        """Get users with most kisses"""
        return (
            session.query(User)
            .order_by(User.total_kisses.desc())
            .limit(limit)
            .all()
        )
