import hashlib
from collections import Counter
from typing import List, Dict
from .models import WorkflowPattern
from ..core.database import CapturedEvent

class PatternMatcher:
    def __init__(self, window_size: int = 5):
        self.window_size = window_size

    def find_patterns(self, events: List[CapturedEvent]) -> List[WorkflowPattern]:
        patterns = {}
        
        # Slide through events to find sequences
        for i in range(len(events) - self.window_size + 1):
            window = events[i : i + self.window_size]
            
            # Create a unique signature based on App and Window Title
            # We ignore specific timestamps to find repetitions
            sig_list = [f"{e.app_name}|{e.window_title}" for e in window]
            sig_str = "->".join(sig_list)
            pattern_hash = hashlib.md5(sig_str.encode()).hexdigest()
            
            date = window[0].timestamp.split('T')[0]
            
            if pattern_hash not in patterns:
                patterns[pattern_hash] = {
                    "hash": pattern_hash,
                    "apps": [e.app_name for e in window],
                    "titles": [e.window_title for e in window],
                    "event_ids": [e.event_id for e in window],
                    "counts": Counter(),
                    "raw_sig": sig_str
                }
            
            patterns[pattern_hash]["counts"][date] += 1

        # Filter for patterns that actually repeat
        results = []
        for p_hash, data in patterns.items():
            days_active = len(data["counts"])
            total_occurrences = sum(data["counts"].values())
            
            # Only keep patterns that happen more than once or across multiple days
            if total_occurrences > 1:
                results.append(WorkflowPattern(
                    pattern_hash=p_hash,
                    description=f"Task involving {data['apps'][0]} and {data['apps'][-1]}",
                    app_sequence=data["apps"],
                    representative_event_ids=data["event_ids"],
                    daily_counts=dict(data["counts"]),
                    persistence_score=days_active
                ))
        
        return sorted(results, key=lambda x: (x.persistence_score, sum(x.daily_counts.values())), reverse=True)