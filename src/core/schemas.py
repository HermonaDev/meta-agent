from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ActionType(str, Enum):
    CLICK = "click"
    DOUBLE_CLICK = "double_click"
    TYPE = "type"
    SCROLL = "scroll"
    APP_SWITCH = "app_switch"
    COPY = "copy"
    PASTE = "paste"
    # Added for browser/automation completeness
    NAVIGATION = "navigation"      # URL changes
    KEYBOARD_HOTKEY = "hotkey"    # e.g., Ctrl+S, Alt+Tab
    HOVER = "hover"               # Important for modern UI
    WAIT = "wait"                 # Necessary for agent resilience
    DRAG_DROP = "drag_drop"       # Common in file management

class CapturedEvent(BaseModel):
    capture_id: str
    event_id: str
    timestamp: str
    id_employee: str
    app_name: Optional[str] = None
    window_title: Optional[str] = None
    event_type: Optional[str] = None
    image_path: str 
    url: Optional[str] = None
    clipboard_content: Optional[str] = None

class WorkflowPersistence(BaseModel):
    daily_counts: Dict[str, int]
    is_2day_persistent: bool
    is_3day_persistent: bool
    is_4day_persistent: bool
    total_occurrences: int

class WorkflowStep(BaseModel):
    step_id: int
    action: ActionType
    app_name: str
    window_title: Optional[str] = None
    description: str
    params: Dict[str, Any] = Field(default_factory=dict)
    screenshot_url: str

class WorkflowBlueprint(BaseModel):
    workflow_id: str
    employee_id: str
    intent_summary: str
    persistence: WorkflowPersistence
    steps: List[WorkflowStep]
    
    class Config:
        frozen = True # Blueprints are immutable once created