"""
Profile and leaderboard handlers
"""

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from bot.middleware.auth import require_user
from bot.services.user_service import UserService
from bot.database import SessionLocal
from bot.utils.helpers import format_number


@require_user
async def profile_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show user profile"""
    session = context.user_data.get("session") or SessionLocal()
    user_id = update.effective_user.id
    user = session.query(UserService).get(user_id)

    vip_status = "✨ VIP" if user.is_vip() else "🆓 Free"
    
    text = f"👤 **{user.first_name} {user.last_name or ''}**\n\n"
    text += f"{vip_status}\n\n"
    text += f"💰 Coins: {format_number(user.coins_balance)}\n"
    text += f"⭐ Stars: {format_number(user.stars_balance)}\n"
    text += f"❤️ Kisses: {user.total_kisses}\n"
    text += f"⚡ Energy: {user.energy}/100\n\n"
    text += f"🏆 Popularity: {format_number(user.popularity_score)}\n"
    text += f"🎁 Gifts Received: {user.total_gifts_received}\n"
    text += f"📤 Gifts Sent: {user.total_gifts_sent}\n"

    keyboard = [
        [
            InlineKeyboardButton("✏️ Edit Profile", callback_data="edit_profile"),
            InlineKeyboardButton("🎁 My Gifts", callback_data="my_gifts"),
        ],
        [
            InlineKeyboardButton("📊 My Stats", callback_data="my_stats"),
            InlineKeyboardButton("🔙 Back", callback_data="back"),
        ],
    ]

    await update.callback_query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown",
    )


@require_user
async def leaderboard_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show leaderboard"""
    session = context.user_data.get("session") or SessionLocal()

    # Get top users by popularity
    leaders = UserService.get_leaderboard(session, limit=10)

    text = f"🏆 **TOP 10 PLAYERS**\n\n"
    for i, user in enumerate(leaders, 1):
        medal = ["🥇", "🥈", "🥉"][i-1] if i <= 3 else f"#{i}"
        text += f"{medal} {user.first_name} - {format_number(user.popularity_score)} ⭐\n"

    text += f"\n💋 **Top Kiss Givers**\n\n"
    kiss_leaders = UserService.get_top_kiss_givers(session, limit=5)
    for i, user in enumerate(kiss_leaders, 1):
        medal = ["🥇", "🥈", "🥉"][i-1] if i <= 3 else f"#{i}"
        text += f"{medal} {user.first_name} - {user.total_kisses} 💋\n"

    keyboard = [
        [
            InlineKeyboardButton("🔄 Refresh", callback_data="leaderboard"),
            InlineKeyboardButton("🔙 Back", callback_data="back"),
        ],
    ]

    await update.callback_query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown",
    )
