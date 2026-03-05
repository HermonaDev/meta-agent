from typing import List, Optional
from pydantic import BaseModel

class WorkflowPattern(BaseModel):
    pattern_hash: str
    description: str
    app_sequence: List[str]
    representative_event_ids: List[str] # To look up screenshots later
    daily_counts: dict # e.g., {"2026-02-23": 5}
    persistence_score: int # 1, 2, 3, or 4 days