from datetime import datetime, timezone, timedelta

def create_expiration(days: int):
    date = datetime.now(timezone.utc) + timedelta(days=days)
    return date