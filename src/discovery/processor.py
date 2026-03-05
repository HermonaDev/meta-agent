from datetime import datetime
from typing import List
from src.core.database import CapturedEvent
from src.discovery.models import Workflow 

class WorkflowDiscovery:
    def __init__(self, gap_threshold_minutes: int = 10):
        self.gap_threshold = gap_threshold_minutes * 60 

    def segment_into_workflows(self, events: List[CapturedEvent]) -> List[Workflow]:
        if not events:
            return []

        workflows = []
        current_workflow_events = [events[0]]

        for i in range(1, len(events)):
            # Fix: Handle both 'Z' and offset-style timestamps
            ts1 = events[i-1].timestamp.replace('Z', '+00:00')
            ts2 = events[i].timestamp.replace('Z', '+00:00')
            
            prev_time = datetime.fromisoformat(ts1)
            curr_time = datetime.fromisoformat(ts2)
            
            gap = (curr_time - prev_time).total_seconds()

            if gap > self.gap_threshold:
                workflows.append(self._create_workflow_object(current_workflow_events))
                current_workflow_events = [events[i]]
            else:
                current_workflow_events.append(events[i])

        if current_workflow_events:
            workflows.append(self._create_workflow_object(current_workflow_events))

        return workflows

    def _create_workflow_object(self, events: List[CapturedEvent]) -> Workflow:
        app_seq = []
        for e in events:
            if not app_seq or app_seq[-1] != e.app_name:
                if e.app_name:
                    app_seq.append(e.app_name)

        return Workflow(
            workflow_id=f"WF-{events[0].capture_id[:8]}",
            employee_id=events[0].id_employee,
            start_time=events[0].timestamp,
            end_time=events[-1].timestamp,
            app_sequence=app_seq,
            window_titles=list(set(e.window_title for e in events if e.window_title)),
            event_count=len(events),
            event_ids=[e.event_id for e in events]
        )