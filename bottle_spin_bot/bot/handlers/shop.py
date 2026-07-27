"""
Shop handlers (VIP, coins, energy)
"""

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from bot.middleware.auth import require_user
from bot.services.user_service import UserService
from bot.database import SessionLocal
from bot.keyboards.inline import shop_keyboard


@require_user
async def shop_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show shop"""
    text = f"🏪 **SHOP**\n\n"
    text += f"💫 **VIP Membership:**\n"
    text += f"• Monthly: 99 ⭐\n"
    text += f"• 3 Months: 249 ⭐\n"
    text += f"• 6 Months: 449 ⭐\n\n"
    text += f"💰 **Buy Coins:**\n"
    text += f"• 1000 coins: 50 ⭐\n\n"
    text += f"⚡ **Energy Recovery:**\n"
    text += f"• Full Energy: 10 ⭐\n"

    await update.callback_query.edit_message_text(
        text,
        reply_markup=shop_keyboard(),
        parse_mode="Markdown",
    )


@require_user
async def vip_purchase_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE, months: int
) -> None:
    """Handle VIP purchase"""
    session = context.user_data.get("session") or SessionLocal()
    user_id = update.effective_user.id

    # Get price
    prices = {1: 99, 3: 249, 6: 449}
    price = prices.get(months, 99)

    # Check user has enough stars
    user = session.query(UserService).get(user_id)
    if user.stars_balance < price:
        await update.callback_query.answer(
            f"❌ Not enough Stars! Need {price}, have {user.stars_balance}",
            show_alert=True,
        )
        return

    # Deduct stars
    user.stars_balance -= price

    # Activate VIP
    UserService.activate_vip(session, user_id, months)

    text = f"✨ **VIP ACTIVATED!**\n\n"
    text += f"📅 Duration: {months} month(s)\n"
    text += f"💫 Stars: -{price}\n\n"
    text += f"🎁 Enjoy exclusive benefits!"

    await update.callback_query.edit_message_text(
        text,
        parse_mode="Markdown",
    )


@require_user
async def buy_coins_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle coin purchase"""
    session = context.user_data.get("session") or SessionLocal()
    user_id = update.effective_user.id

    # Check user has enough stars
    user = session.query(UserService).get(user_id)
    if user.stars_balance < 50:
        await update.callback_query.answer(
            f"❌ Not enough Stars! Need 50, have {user.stars_balance}",
            show_alert=True,
        )
        return

    # Deduct stars and add coins
    user.stars_balance -= 50
    UserService.add_coins(session, user_id, 1000)

    await update.callback_query.answer(
        "💰 1000 coins added!",
        show_alert=True,
    )


@require_user
async def recover_energy_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Handle energy recovery"""
    session = context.user_data.get("session") or SessionLocal()
    user_id = update.effective_user.id

    # Check user has enough stars
    user = session.query(UserService).get(user_id)
    if user.stars_balance < 10:
        await update.callback_query.answer(
            f"❌ Not enough Stars! Need 10, have {user.stars_balance}",
            show_alert=True,
        )
        return

    # Deduct stars and recover energy
    user.stars_balance -= 10
    user.energy = 100
    session.commit()

    await update.callback_query.answer(
        "⚡ Energy fully recovered!",
        show_alert=True,
    )
