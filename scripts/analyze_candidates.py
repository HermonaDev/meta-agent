import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.database import DatabaseManager
from src.discovery.repetition import PatternMatcher

db = DatabaseManager("data/test_data.db")
# We use a window of 4 to capture granular, automatable segments.
matcher = PatternMatcher(window_size=4) 

for emp_id in db.get_employee_ids():
    events = db.get_joined_data(emp_id)
    blueprints = matcher.find_repetitive_blueprints(events)
    
    print(f"DISCOVERY REPORT FOR {emp_id}:")
    
    p3 = [b for b in blueprints if b.persistence.is_3day_persistent]
    p2 = [b for b in blueprints if b.persistence.is_2day_persistent and not b.persistence.is_3day_persistent]
    
    print(f"  - Total Repeating Workflows Found: {len(blueprints)}")
    print(f"  - 3-Day Persistent (Daily): {len(p3)}")
    print(f"  - 2-Day Persistent (Frequent): {len(p2)}")
    
    if blueprints:
        top = blueprints[0]
        # Show the flow of apps
        flow = " -> ".join([s.app_name for s in top.steps])
        print(f"  - Top Workflow [{top.workflow_id}]: {flow}")
        print(f"    Total Hits: {top.persistence.total_occurrences}")
        print(f"    Persistence: {top.persistence.daily_counts}")
    print("-" * 50)