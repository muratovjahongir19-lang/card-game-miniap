"""
Game handlers with multiplayer features
"""

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from bot.middleware.auth import require_user
from bot.services.game_service import GameService
from bot.services.room_service import RoomService
from bot.database import SessionLocal
from bot.models import DecisionEnum
from bot.keyboards.inline import game_keyboard


@require_user
async def spin_bottle_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle bottle spin in room"""
    session = context.user_data.get("session") or SessionLocal()
    user_id = update.effective_user.id
    room_id = context.user_data.get("current_room")

    if not room_id:
        await update.callback_query.answer(
            "❌ You're not in a room!",
            show_alert=True,
        )
        return

    # Get opposite gender player
    opponent = RoomService.get_opposite_gender_in_room(session, room_id, user_id)

    if not opponent:
        await update.callback_query.answer(
            "❌ No opposite gender player found!",
            show_alert=True,
        )
        return

    # Create game session
    game = GameService.create_game_session(
        session,
        room_id,
        user_id,
        opponent.user_id,
    )

    text = f"🍾 **BOTTLE SPIN!**\n\n"
    text += f"{update.effective_user.first_name} 💚 {opponent.first_name}\n\n"
    text += f"⏱️ You have 10 seconds to decide!"

    # Send to both players
    await update.callback_query.edit_message_text(
        text,
        reply_markup=game_keyboard(),
        parse_mode="Markdown",
    )

    # Store game info
    context.user_data["current_game"] = game.session_id


@require_user
async def decision_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE, decision: str
) -> None:
    """Handle player decision (kiss/skip)"""
    session = context.user_data.get("session") or SessionLocal()
    user_id = update.effective_user.id
    game_id = context.user_data.get("current_game")

    if not game_id:
        return

    # Set decision
    decision_enum = DecisionEnum.ACCEPTED if decision == "accept" else DecisionEnum.REJECTED
    GameService.set_player_decision(session, game_id, user_id, decision_enum)

    # Check if both decided
    game = session.query(GameService).get(game_id)
    if game.is_both_decided():
        # Finalize game
        GameService.finalize_game(session, game_id)
        
        text = f"🎉 **Game Result:**\n\n"
        if game.result == DecisionEnum.ACCEPTED:
            text += f"💋 **KISS!** Both said YES!\n"
            text += f"💰 +50 coins\n"
            text += f"⭐ +5 popularity"
        else:
            text += f"❌ One player skipped"

        await update.callback_query.edit_message_text(
            text,
            parse_mode="Markdown",
        )


async def kiss_decision(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Player chose kiss"""
    await decision_handler(update, context, "accept")


async def skip_decision(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Player chose skip"""
    await decision_handler(update, context, "reject")
