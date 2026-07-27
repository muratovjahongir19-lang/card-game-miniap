"""
Start command handler
"""

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from telegram.ext import ContextTypes
from bot.config import settings
from bot.utils.constants import MESSAGES, EMOJI_MAP


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command"""
    user = update.effective_user

    # Create inline keyboard
    keyboard = [
        [
            InlineKeyboardButton("🍾 Открыть мини-апп", web_app=WebAppInfo(url=settings.webapp_url)),
        ],
        [
            InlineKeyboardButton("🎮 Join Room", callback_data="join_room"),
            InlineKeyboardButton("➕ Create Room", callback_data="create_room"),
        ],
        [
            InlineKeyboardButton("👤 Profile", callback_data="profile"),
            InlineKeyboardButton("🏪 Shop", callback_data="shop"),
        ],
        [
            InlineKeyboardButton("📚 Help", callback_data="help"),
            InlineKeyboardButton("⚙️ Settings", callback_data="settings"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_text = f"""
{EMOJI_MAP['bottle']} **Welcome, {user.first_name}!**

*Bottle Spin Bot* — A fun party game where you meet new people through the classic "spin the bottle" mechanic!

{EMOJI_MAP['fire']} **How to play:**
1. Join or create a room
2. Spin the bottle and get matched with someone
3. You both decide: Kiss or Skip?
4. Send gifts to show your interest
5. Climb the popularity ladder!

{EMOJI_MAP['sparkles']} **Features:**
• Real-time matching with opposite gender
• Send virtual gifts
• Chat with other players
• VIP status & special rooms
• Leaderboards & rewards

Ready to play?
"""
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command"""
    help_text = """
🍾 **Bottle Spin Bot Help**

**Basic Commands:**
/start - Start the bot
/profile - View your profile
/rooms - List available rooms
/join - Join a room
/create - Create a room
/shop - Shop & VIP
/help - This message

**How to Play:**
1. Join a room with players
2. Wait for your turn
3. Bottle spins and picks someone
4. Decide: Kiss ❤️ or Skip ❌ (10 seconds)
5. If both kiss → gain coins & popularity!

**Energy System:**
• Each spin costs 5 energy
• Energy recovers 1/minute (max 100)
• Buy full recovery for 10 Stars

**Gifts:**
• Send gifts to show interest (+10 popularity)
• Different gifts cost different coins
• VIP members get 10 free gifts/day

**VIP Benefits:**
• Highlighted profile (✨)
• Access to elite rooms
• 20% bonus coins
• No ads
• 10 free gifts daily

**Need Help?**
Contact support: /support
"""
    
    await update.message.reply_text(help_text, parse_mode="Markdown")


async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /cancel command"""
    await update.message.reply_text("❌ Cancelled.")
