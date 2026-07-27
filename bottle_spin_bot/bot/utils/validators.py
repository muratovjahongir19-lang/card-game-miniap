"""
Input validators
"""

from bot.utils.constants import MIN_AGE


def validate_age(age: int) -> bool:
    """Validate user age"""
    return age >= MIN_AGE


def validate_room_name(name: str) -> bool:
    """Validate room name"""
    if not name or len(name) < 3 or len(name) > 50:
        return False
    return True


def validate_username(username: str) -> bool:
    """Validate username"""
    if not username or len(username) < 2 or len(username) > 30:
        return False
    return username.isalnum() or '_' in username


def validate_coins(amount: int) -> bool:
    """Validate coin amount"""
    return amount > 0 and amount <= 1000000
