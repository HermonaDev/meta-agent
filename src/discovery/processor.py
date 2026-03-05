from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class Workflow(BaseModel):
    workflow_id: str
    employee_id: str
    start_time: str
    end_time: str
    # A list of app names used in order: e.g. ["chrome.exe", "excel.exe", "chrome.exe"]
    app_sequence: List[str]
    # The unique window titles interacted with
    window_titles: List[str]
    # Total count of atomic actions (clicks, types, etc.)
    event_count: int
    # The raw event IDs for traceability
    event_ids: List[str]
    # To be filled later: A semantic description like "Data Entry in CRM"
    description: Optional[str] = None