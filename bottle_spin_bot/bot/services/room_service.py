"""
Room management service
"""

from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_
from bot.models import Room, RoomMember, User
from bot.utils.helpers import generate_invite_code
from bot.utils.constants import MAX_ROOM_SIZE
import random


class RoomService:
    """Service for room operations"""

    @staticmethod
    def create_room(
        session: Session,
        room_name: str,
        creator_id: int,
        is_private: bool = False,
        language: str = "en",
        age_restriction: int = 18,
    ) -> Room:
        """Create new room"""
        room = Room(
            room_name=room_name,
            description=f"Room by user {creator_id}",
            max_players=MAX_ROOM_SIZE,
            current_players_count=1,
            is_active=True,
            is_private=is_private,
            language=language,
            age_restriction=age_restriction,
            expires_at=datetime.utcnow() + timedelta(hours=1),
        )
        session.add(room)
        session.commit()

        # Add creator as first member
        RoomService.add_member(session, room.room_id, creator_id, position=0)

        return room

    @staticmethod
    def get_active_rooms(session: Session, limit: int = 20) -> list:
        """Get list of active public rooms"""
        rooms = (
            session.query(Room)
            .filter(
                and_(
                    Room.is_active == True,
                    Room.is_private == False,
                    Room.expires_at > datetime.utcnow(),
                    Room.current_players_count < Room.max_players,
                )
            )
            .order_by(Room.current_players_count.desc())
            .limit(limit)
            .all()
        )
        return rooms

    @staticmethod
    def search_rooms(
        session: Session, query: str, language: str = None
    ) -> list:
        """Search rooms by name or language"""
        q = session.query(Room).filter(
            and_(
                Room.is_active == True,
                Room.is_private == False,
                Room.expires_at > datetime.utcnow(),
                Room.room_name.ilike(f"%{query}%"),
            )
        )

        if language:
            q = q.filter(Room.language == language)

        return q.limit(20).all()

    @staticmethod
    def add_member(
        session: Session, room_id: int, user_id: int, position: int = None
    ) -> RoomMember:
        """Add user to room"""
        room = session.query(Room).get(room_id)
        if not room or room.current_players_count >= room.max_players:
            return None

        # Auto-assign position
        if position is None:
            position = room.current_players_count

        member = RoomMember(
            room_id=room_id,
            user_id=user_id,
            position=position,
        )
        session.add(member)
        room.current_players_count += 1
        session.commit()

        return member

    @staticmethod
    def remove_member(session: Session, room_id: int, user_id: int):
        """Remove user from room"""
        member = (
            session.query(RoomMember)
            .filter(
                and_(
                    RoomMember.room_id == room_id,
                    RoomMember.user_id == user_id,
                )
            )
            .first()
        )

        if member:
            room = session.query(Room).get(room_id)
            room.current_players_count -= 1
            session.delete(member)
            session.commit()

    @staticmethod
    def get_room_members(session: Session, room_id: int) -> list:
        """Get all members in room"""
        return (
            session.query(RoomMember)
            .filter(RoomMember.room_id == room_id)
            .all()
        )

    @staticmethod
    def get_random_room(session: Session) -> Room:
        """Get random available room"""
        rooms = RoomService.get_active_rooms(session, limit=100)
        if not rooms:
            return None
        return random.choice(rooms)

    @staticmethod
    def get_opposite_gender_in_room(
        session: Session, room_id: int, user_id: int
    ) -> User:
        """Get random opposite gender user in room"""
        current_user = session.query(User).get(user_id)
        members = RoomService.get_room_members(session, room_id)
        member_ids = [m.user_id for m in members if m.user_id != user_id]

        if not member_ids:
            return None

        opposite_users = (
            session.query(User)
            .filter(
                and_(
                    User.user_id.in_(member_ids),
                    User.gender != current_user.gender,
                )
            )
            .all()
        )

        if not opposite_users:
            return None

        return random.choice(opposite_users)
