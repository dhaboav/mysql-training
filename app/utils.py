from datetime import datetime, timezone


def get_datetime_utc() -> datetime:
    """Utility Function for UTC timezone"""
    return datetime.now(timezone.utc)


def get_current_year_utc() -> int:
    """Utility Function for get year UTC timezone"""
    return datetime.now(timezone.utc).year
