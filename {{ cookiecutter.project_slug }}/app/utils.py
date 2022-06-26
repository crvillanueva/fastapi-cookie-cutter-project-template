from datetime import datetime
from zoneinfo import ZoneInfo


def get_local_now_datetime(timezone: str) -> datetime:
    return datetime.now().astimezone(ZoneInfo(timezone))
