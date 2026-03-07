import hashlib
from collections import Counter
from typing import List, Dict
from src.core.schemas import CapturedEvent, WorkflowBlueprint, WorkflowStep
from src.core.utils import calculate_persistence_metrics, map_raw_event_to_action, normalize_window_title

class PatternMatcher:
    def __init__(self, window_size: int = 5):
        self.window_size = window_size

    def find_repetitive_blueprints(self, events: List[CapturedEvent]) -> List[WorkflowBlueprint]:
        patterns = {}
        
        # 1. SLIDING WINDOW (Syntactic Clustering)
        for i in range(len(events) - self.window_size + 1):
            window = events[i : i + self.window_size]
            
            # Create a 'Fuzzy Signature'
            # Use Normalized Title + App + Event Type
            sig_parts = []
            for e in window:
                norm_title = normalize_window_title(e.window_title)
                sig_parts.append(f"{e.app_name}|{e.event_type}|{norm_title}")
            
            sig_str = "->".join(sig_parts)
            pattern_hash = hashlib.md5(sig_str.encode()).hexdigest()
            
            date = window[0].timestamp.split('T')[0]
            
            if pattern_hash not in patterns:
                patterns[pattern_hash] = {
                    "sample_events": window,
                    "counts": Counter()
                }
            patterns[pattern_hash]["counts"][date] += 1

        # 2. PERSISTENCE SCORING
        blueprints = []
        for p_hash, data in patterns.items():
            persistence = calculate_persistence_metrics(data["counts"])
            
            # Requirement: Only high-value workflows
            if persistence.total_occurrences > 2: # Found more than twice
                steps = []
                for idx, e in enumerate(data["sample_events"]):
                    steps.append(WorkflowStep(
                        step_id=idx,
                        action=map_raw_event_to_action(e.event_type or ""),
                        app_name=e.app_name or "Unknown",
                        window_title=e.window_title,
                        description="Raw discovered action", # To be filled by AI Labeler
                        screenshot_url=e.image_path
                    ))

                blueprints.append(WorkflowBlueprint(
                    workflow_id=f"WP-{p_hash[:8]}",
                    employee_id=data["sample_events"][0].id_employee,
                    intent_summary="Candidate Workflow", # To be filled by AI Labeler
                    persistence=persistence,
                    steps=steps
                ))
        
        # Sort by Persistence (4-day first, then frequency)
        return sorted(blueprints, key=lambda x: (x.persistence.is_4day_persistent, x.persistence.total_occurrences), reverse=True)