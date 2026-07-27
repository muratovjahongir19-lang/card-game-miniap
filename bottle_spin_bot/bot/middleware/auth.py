"""
Authentication middleware
"""

from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes
from bot.database import SessionLocal
from bot.services.user_service import UserService


def require_user(func):
    """Decorator to ensure user exists in database"""

    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        session = SessionLocal()

        # Get or create user
        db_user = UserService.get_or_create_user(
            session,
            user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
        )

        # Store user in context for handler
        context.user_data["user"] = db_user
        context.user_data["session"] = session

        try:
            return await func(update, context)
        finally:
            session.close()

    return wrapper


def require_admin(func):
    """Decorator to check if user is admin"""

    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id

        # Get admins list from config
        from bot.config import settings

        if user_id not in settings.admin_user_list:
            await update.message.reply_text("❌ Admin only!")
            return

        return await func(update, context)

    return wrapper
