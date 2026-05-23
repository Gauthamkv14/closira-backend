from datetime import datetime, timezone


def get_utcnow() -> datetime:
    """Returns the current UTC time with timezone info."""
    return datetime.now(timezone.utc)
