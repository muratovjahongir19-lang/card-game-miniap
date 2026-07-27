"""
Room handlers with open table and random join features
"""

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from bot.middleware.auth import require_user
from bot.services.room_service import RoomService
from bot.database import SessionLocal
from bot.keyboards.inline import rooms_keyboard


@require_user
async def join_room_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show available rooms to join"""
    session = context.user_data.get("session") or SessionLocal()
    user_id = update.effective_user.id

    # Get active rooms
    rooms = RoomService.get_active_rooms(session, limit=20)

    if not rooms:
        await update.callback_query.answer(
            "❌ No available rooms!",
            show_alert=True,
        )
        return

    text = "🍾 **Available Rooms:**\n\n"
    for room in rooms:
        text += f"📌 {room.room_name}\n"
        text += f"   👥 {room.current_players_count}/{room.max_players}\n"
        text += f"   🌍 {room.language}\n"
        text += f"   ⏱️ Expires in 1h\n\n"

    await update.callback_query.edit_message_text(
        text,
        reply_markup=rooms_keyboard(rooms),
        parse_mode="Markdown",
    )


@require_user
async def random_room_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Join random available room"""
    session = context.user_data.get("session") or SessionLocal()
    user_id = update.effective_user.id

    # Get random room
    room = RoomService.get_random_room(session)

    if not room:
        await update.callback_query.answer(
            "❌ No available rooms to join!",
            show_alert=True,
        )
        return

    # Add user to room
    member = RoomService.add_member(session, room.room_id, user_id)

    if member:
        text = f"✅ Joined room: **{room.room_name}**\n\n"
        text += f"👥 Players: {room.current_players_count}/{room.max_players}\n"
        text += f"🎮 Game will start soon..."
        await update.callback_query.edit_message_text(
            text,
            parse_mode="Markdown",
        )
    else:
        await update.callback_query.answer(
            "❌ Could not join room!",
            show_alert=True,
        )


@require_user
async def create_room_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Create new room"""
    session = context.user_data.get("session") or SessionLocal()
    user_id = update.effective_user.id

    # Create room
    room = RoomService.create_room(
        session,
        room_name=f"Room by {update.effective_user.first_name}",
        creator_id=user_id,
        is_private=False,
        language="en",
    )

    keyboard = [
        [
            InlineKeyboardButton("👥 Invite Friends", callback_data="invite_friends"),
            InlineKeyboardButton("🔐 Make Private", callback_data="make_private"),
        ],
        [
            InlineKeyboardButton("⏳ Wait for Players", callback_data="wait_players"),
            InlineKeyboardButton("🔙 Leave", callback_data="leave_room"),
        ],
    ]

    text = f"🎉 **Room Created!**\n\n"
    text += f"📝 Name: {room.room_name}\n"
    text += f"👥 Players: {room.current_players_count}/{room.max_players}\n"
    text += f"🌍 Language: {room.language}\n"
    text += f"🔓 Status: Public\n"

    await update.callback_query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown",
    )


@require_user
async def search_rooms_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Search for rooms"""
    session = context.user_data.get("session") or SessionLocal()

    # Ask for search query
    await update.callback_query.edit_message_text(
        "🔍 Enter room name to search:\n\n(or /cancel)"
    )

    # Store state
    context.user_data["state"] = "searching_rooms"
