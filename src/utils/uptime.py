
from datetime import datetime

def get_uptime(start_time: datetime):
    delta = datetime.now() - start_time
    
    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    
    parts = []
    if days > 0:
        parts.append(f"{days}д.")
    if hours > 0:
        parts.append(f"{hours}ч.")
    if minutes > 0 or not parts:
        parts.append(f"{minutes}мин.")
        
    return " ".join(parts)