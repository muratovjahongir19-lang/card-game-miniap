"""
Game logic service
"""

from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from bot.models import GameSession, DecisionEnum, User
from bot.utils.constants import (
    KISS_ACCEPTED_COINS,
    KISS_ACCEPTED_POPULARITY,
    DECISION_TIMEOUT,
)
import random


class GameService:
    """Service for game operations"""

    @staticmethod
    def create_game_session(
        session: Session,
        room_id: int,
        player1_id: int,
        player2_id: int,
    ) -> GameSession:
        """Create new game session"""
        game = GameSession(
            room_id=room_id,
            player1_id=player1_id,
            player2_id=player2_id,
            player1_decision=DecisionEnum.PENDING,
            player2_decision=DecisionEnum.PENDING,
            created_at=datetime.utcnow(),
            decision_deadline=datetime.utcnow()
            + timedelta(seconds=DECISION_TIMEOUT),
        )
        session.add(game)
        session.commit()
        return game

    @staticmethod
    def set_player_decision(
        session: Session,
        session_id: int,
        player_id: int,
        decision: DecisionEnum,
    ):
        """Set player decision"""
        game = session.query(GameSession).get(session_id)

        if game.player1_id == player_id:
            game.player1_decision = decision
        elif game.player2_id == player_id:
            game.player2_decision = decision

        session.commit()

    @staticmethod
    def check_timeout(session: Session, session_id: int):
        """Check if game session has timed out"""
        game = session.query(GameSession).get(session_id)

        if game.is_both_decided():
            return False

        if datetime.utcnow() > game.decision_deadline:
            # Mark timeout decisions
            if game.player1_decision == DecisionEnum.PENDING:
                game.player1_decision = DecisionEnum.TIMEOUT
            if game.player2_decision == DecisionEnum.PENDING:
                game.player2_decision = DecisionEnum.TIMEOUT

            session.commit()
            return True

        return False

    @staticmethod
    def finalize_game(session: Session, session_id: int) -> GameSession:
        """Finalize game and award prizes"""
        game = session.query(GameSession).get(session_id)
        game.finalize_result()

        if game.result == DecisionEnum.ACCEPTED:
            # Award both players
            player1 = session.query(User).get(game.player1_id)
            player2 = session.query(User).get(game.player2_id)

            player1.coins_balance += KISS_ACCEPTED_COINS
            player1.popularity_score += KISS_ACCEPTED_POPULARITY
            player1.total_kisses += 1

            player2.coins_balance += KISS_ACCEPTED_COINS
            player2.popularity_score += KISS_ACCEPTED_POPULARITY
            player2.total_kisses += 1

        session.commit()
        return game

    @staticmethod
    def get_recent_games(
        session: Session, user_id: int, limit: int = 10
    ) -> list:
        """Get user's recent games"""
        from sqlalchemy import or_

        return (
            session.query(GameSession)
            .filter(
                or_(
                    GameSession.player1_id == user_id,
                    GameSession.player2_id == user_id,
                )
            )
            .order_by(GameSession.completed_at.desc())
            .limit(limit)
            .all()
        )
