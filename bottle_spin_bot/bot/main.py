"""
Main bot entry point
"""

import logging
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from bot.config import settings
from bot.handlers.start import start_command, help_command, cancel_command

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=settings.log_level
)
logger = logging.getLogger(__name__)


async def error_handler(update, context):
    """Handle errors"""
    logger.error(f"Update {update} caused error {context.error}")


def main():
    """Main bot function"""
    
    # Create application
    application = Application.builder().token(settings.telegram_bot_token).build()

    # Register handlers
    # Commands
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("cancel", cancel_command))

    # Error handler
    application.add_error_handler(error_handler)

    # Start bot
    logger.info("🚀 Starting Bottle Spin Bot...")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Debug mode: {settings.debug}")

    application.run_polling(allowed_updates=["message", "callback_query"])


if __name__ == "__main__":
    main()
