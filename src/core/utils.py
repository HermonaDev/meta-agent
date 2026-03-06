from typing import Dict
import requests 
from .schemas import WorkflowPersistence

def calculate_persistence_metrics(daily_counts: Dict[str, int]) -> WorkflowPersistence:
    active_days = len(daily_counts)
    return WorkflowPersistence(
        daily_counts=daily_counts,
        is_2day_persistent=active_days >= 2,
        is_3day_persistent=active_days >= 3,
        is_4day_persistent=active_days >= 4,
        total_occurrences=sum(daily_counts.values())
    )

def verify_image_url(url: str) -> bool:
    """Checks if the screenshot URL is actually reachable."""
    try:
        response = requests.head(url, timeout=5)
        return response.status_code == 200
    except:
        return False