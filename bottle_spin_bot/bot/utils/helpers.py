"""
Helper functions
"""

import random
from datetime import datetime, timedelta


def generate_invite_code(length: int = 6) -> str:
    """Generate random invite code"""
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return "".join(random.choice(chars) for _ in range(length))


def get_time_ago(dt: datetime) -> str:
    """Get human readable time ago"""
    now = datetime.utcnow()
    diff = now - dt
    
    if diff.days > 0:
        return f"{diff.days}d ago"
    elif diff.seconds >= 3600:
        hours = diff.seconds // 3600
        return f"{hours}h ago"
    elif diff.seconds >= 60:
        minutes = diff.seconds // 60
        return f"{minutes}m ago"
    else:
        return "just now"


def calculate_vip_discount(price: int, is_vip: bool) -> int:
    """Calculate price with VIP discount"""
    if is_vip:
        return int(price * 0.8)  # 20% discount
    return price


def get_random_emoji() -> str:
    """Get random emoji"""
    emojis = ["😊", "😍", "🔥", "✨", "💫", "🎉", "💕", "⭐"]
    return random.choice(emojis)


def format_number(num: int) -> str:
    """Format large numbers"""
    if num >= 1000000:
        return f"{num / 1000000:.1f}M"
    elif num >= 1000:
        return f"{num / 1000:.1f}K"
    return str(num)
