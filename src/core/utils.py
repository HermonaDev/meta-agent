import re
from typing import Dict, Optional

import requests

from .schemas import ActionType, WorkflowPersistence


def calculate_persistence_metrics(daily_counts: Dict[str, int]) -> WorkflowPersistence:
    unique_days = len(daily_counts)
    return WorkflowPersistence(
        daily_counts=daily_counts,
        is_2day_persistent=unique_days >= 2,
        is_3day_persistent=unique_days >= 3,
        is_4day_persistent=unique_days >= 4,
        total_occurrences=sum(daily_counts.values())
    )

def verify_image_url(url: str) -> bool:
    """Checks if the screenshot URL is actually reachable."""
    try:
        response = requests.head(url, timeout=5)
        return response.status_code == 200
    except Exception:
        return False

def normalize_window_title(title: Optional[str]) -> str:
    """Removes noise from window titles to allow for better pattern matching."""
    if not title:
        return "unknown"
    
    # Remove common app suffixes
    noise = r' - Google Chrome| - Microsoft Edge| - Excel| - Notepad'
    title = re.sub(noise, '', title, flags=re.I)
    
    # Remove specific IDs/Numbers (e.g., 'Invoice #123' -> 'Invoice #')
    title = re.sub(r'\d+', '#', title)
    return title.strip().lower()

def map_raw_event_to_action(raw_event: str) -> ActionType:
    mapping = {
        "CLICK": ActionType.CLICK,
        "TYPE": ActionType.TYPE,
        "SCROLL": ActionType.SCROLL,
        "APP_SWITCH": ActionType.APP_SWITCH,
        "COPY": ActionType.COPY_PASTE,
        "PASTE": ActionType.COPY_PASTE,
    }
    return mapping.get(raw_event.upper(), ActionType.WAIT)