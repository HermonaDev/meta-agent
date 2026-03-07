import hashlib
from collections import Counter
from typing import List, Dict
from src.core.schemas import CapturedEvent, WorkflowBlueprint, WorkflowStep
from src.core.utils import calculate_persistence_metrics, map_raw_event_to_action

class PatternMatcher:
    def __init__(self, window_size: int = 4):
        self.window_size = window_size

    def find_repetitive_blueprints(self, events: List[CapturedEvent]) -> List[WorkflowBlueprint]:
        patterns = {}
        
        # 1. SLIDING WINDOW (Syntactic Matching)
        for i in range(len(events) - self.window_size + 1):
            window = events[i : i + self.window_size]
            
            # REDUCED HASH: We only care about the sequence of App + Action.
            # This allows us to find the 'Work' even if the 'Document Name' changes.
            sig_parts = [f"{e.app_name}|{e.event_type}" for e in window]
            sig_str = "->".join(sig_parts)
            pattern_hash = hashlib.md5(sig_str.encode()).hexdigest()
            
            date = window[0].timestamp.split('T')[0]
            
            if pattern_hash not in patterns:
                patterns[pattern_hash] = {
                    "events": window,
                    "counts": Counter()
                }
            patterns[pattern_hash]["counts"][date] += 1

        # 2. FILTER & CONVERT (Task 1.2 Persistence Counting)
        blueprints = []
        for p_hash, data in patterns.items():
            persistence = calculate_persistence_metrics(data["counts"])
            
            # Criteria for 'High Value': 
            # 1. Must happen on at least 2 different days.
            # 2. Total occurrences >= 3.
            if persistence.is_2day_persistent and persistence.total_occurrences >= 3:
                steps = []
                for idx, e in enumerate(data["events"]):
                    steps.append(WorkflowStep(
                        step_id=idx,
                        action=map_raw_event_to_action(e.event_type or ""),
                        app_name=e.app_name or "Unknown",
                        window_title=e.window_title,
                        description="Discovered action step",
                        screenshot_url=e.image_path
                    ))

                blueprints.append(WorkflowBlueprint(
                    workflow_id=f"WP-{p_hash[:8]}",
                    employee_id=data["events"][0].id_employee,
                    intent_summary="Discovered Repetitive Task", # To be enriched by AI next
                    persistence=persistence,
                    steps=steps
                ))
        
        # Sort by total occurrences to find the 'Hottest' workflows
        return sorted(blueprints, key=lambda x: x.persistence.total_occurrences, reverse=True)