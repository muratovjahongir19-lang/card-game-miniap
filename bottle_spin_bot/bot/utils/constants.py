"""
Game constants and enums
"""

from enum import Enum

# Game mechanics
SPIN_INTERVAL = 30  # seconds
DECISION_TIMEOUT = 10  # seconds
MAX_ROOM_SIZE = 8
MIN_USERS_TO_START = 2

# Energy system
INITIAL_ENERGY = 100
MAX_ENERGY = 100
ENERGY_PER_SPIN = 5
ENERGY_RECOVERY_PER_MINUTE = 1
ENERGY_RECOVERY_COST_STARS = 10

# Rewards
KISS_ACCEPTED_COINS = 50
KISS_ACCEPTED_POPULARITY = 5
GIFT_POPULARITY_BONUS = 10
VIP_COINS_MULTIPLIER = 1.2

# VIP Prices (Telegram Stars)
VIP_MONTHLY = 99
VIP_QUARTERLY = 249
VIP_BIANNUAL = 449

# Rate limiting
MAX_SPINS_PER_MINUTE = 3
MAX_MESSAGES_PER_MINUTE = 5
MAX_GIFTS_PER_HOUR = 20

# Age restrictions
MIN_AGE = 18


class GenderEnum(str, Enum):
    """Gender types"""
    MALE = "M"
    FEMALE = "F"
    OTHER = "O"


class GameResultEnum(str, Enum):
    """Game result types"""
    BOTH_ACCEPTED = "both_accepted"
    ONE_REJECTED = "one_rejected"
    TIMEOUT = "timeout"


EMOJI_MAP = {
    "kiss": "💋",
    "heart": "❤️",
    "star": "⭐",
    "fire": "🔥",
    "bottle": "🍾",
    "love": "💕",
    "sparkles": "✨",
    "tada": "🎉",
}

MESSAGES = {
    "welcome": "🍾 Welcome to Bottle Spin Bot! 🍾\n\nA fun party game where you meet new people!\n\n/join - Join a room\n/create - Create a room\n/profile - Your profile\n/shop - Shop & VIP\n/help - Help",
    "room_full": "❌ This room is full!",
    "not_in_room": "❌ You're not in a room!",
    "not_enough_energy": "⚡ Not enough energy! Cost: {cost}",
    "not_enough_coins": "💰 Not enough coins! Cost: {cost}",
    "gift_sent": "🎁 Gift sent successfully!",
    "already_in_room": "❌ You're already in a room!",
    "room_expired": "❌ This room has expired!",
    "too_young": "⚠️ You must be 18+ to play!",
}
