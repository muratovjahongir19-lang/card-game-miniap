"""
Gift handlers
"""

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from bot.middleware.auth import require_user
from bot.services.gift_service import GiftService
from bot.database import SessionLocal


@require_user
async def gifts_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show available gifts"""
    session = context.user_data.get("session") or SessionLocal()

    # Get all gifts
    gifts = GiftService.get_gifts(session)

    if not gifts:
        # Initialize gifts
        GiftService.init_gifts(session)
        gifts = GiftService.get_gifts(session)

    text = f"🎁 **GIFT SHOP**\n\n"
    keyboard = []

    for gift in gifts:
        text += f"{gift.emoji} {gift.name} - {gift.cost_coins} 💰\n"
        keyboard.append(
            [
                InlineKeyboardButton(
                    f"{gift.emoji} Buy",
                    callback_data=f"send_gift_{gift.gift_type_id}",
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton("🔙 Back", callback_data="back"),
        ]
    )

    await update.callback_query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown",
    )


@require_user
async def send_gift_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE, gift_id: int
) -> None:
    """Send gift to user"""
    session = context.user_data.get("session") or SessionLocal()
    sender_id = update.effective_user.id

    # Get recipient from context
    recipient_id = context.user_data.get("gift_recipient")

    if not recipient_id:
        await update.callback_query.answer(
            "❌ No recipient selected!",
            show_alert=True,
        )
        return

    # Send gift
    history = GiftService.send_gift(
        session,
        gift_id,
        sender_id,
        recipient_id,
        room_id=context.user_data.get("current_room"),
    )

    if history:
        await update.callback_query.answer(
            "🎁 Gift sent successfully!",
            show_alert=True,
        )
    else:
        await update.callback_query.answer(
            "❌ Not enough coins!",
            show_alert=True,
        )
