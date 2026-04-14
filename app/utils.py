from datetime import datetime, timezone


def get_datetime_utc() -> datetime:
    """Utility Function for UTC timezone"""
    return datetime.now(timezone.utc)
