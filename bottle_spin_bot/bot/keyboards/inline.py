"""
Inline keyboard builders
"""

from telegram import InlineKeyboardMarkup, InlineKeyboardButton


def main_keyboard() -> InlineKeyboardMarkup:
    """Main menu keyboard"""
    keyboard = [
        [
            InlineKeyboardButton("🎮 Join Room", callback_data="join_room"),
            InlineKeyboardButton("➕ Create", callback_data="create_room"),
        ],
        [
            InlineKeyboardButton("👤 Profile", callback_data="profile"),
            InlineKeyboardButton("🏆 Leaderboard", callback_data="leaderboard"),
        ],
        [
            InlineKeyboardButton("🎁 Gifts", callback_data="gifts"),
            InlineKeyboardButton("🏪 Shop", callback_data="shop"),
        ],
        [
            InlineKeyboardButton("📚 Help", callback_data="help"),
            InlineKeyboardButton("⚙️ Settings", callback_data="settings"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def rooms_keyboard(rooms: list) -> InlineKeyboardMarkup:
    """Rooms list keyboard"""
    keyboard = []

    for room in rooms:
        button_text = f"{room.room_name} ({room.current_players_count}/{room.max_players})"
        keyboard.append(
            [
                InlineKeyboardButton(
                    button_text,
                    callback_data=f"join_room_id_{room.room_id}",
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                "🎲 Random Room", callback_data="random_room"
            ),
            InlineKeyboardButton("🔙 Back", callback_data="back"),
        ]
    )

    return InlineKeyboardMarkup(keyboard)


def game_keyboard() -> InlineKeyboardMarkup:
    """Game decision keyboard"""
    keyboard = [
        [
            InlineKeyboardButton("❤️ Kiss", callback_data="decision_accept"),
            InlineKeyboardButton("❌ Skip", callback_data="decision_reject"),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def shop_keyboard() -> InlineKeyboardMarkup:
    """Shop keyboard"""
    keyboard = [
        [
            InlineKeyboardButton("🌟 Monthly VIP\n99 ⭐", callback_data="vip_monthly"),
            InlineKeyboardButton(
                "🌟 3-Month VIP\n249 ⭐", callback_data="vip_quarterly"
            ),
        ],
        [
            InlineKeyboardButton(
                "🌟 6-Month VIP\n449 ⭐", callback_data="vip_biannual"
            ),
        ],
        [
            InlineKeyboardButton(
                "💰 Buy Coins\n1000 coins = 50 ⭐", callback_data="buy_coins"
            ),
        ],
        [
            InlineKeyboardButton(
                "⚡ Recover Energy\n100 energy = 10 ⭐", callback_data="recover_energy"
            ),
        ],
        [
            InlineKeyboardButton("🔙 Back", callback_data="back"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)
