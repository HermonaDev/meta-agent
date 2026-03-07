import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.database import DatabaseManager
from src.discovery.repetition import PatternMatcher

db = DatabaseManager("data/test_data.db")
matcher = PatternMatcher(window_size=6) # 6 events is a good "Granular" chunk

for emp_id in db.get_employee_ids():
    events = db.get_joined_data(emp_id)
    blueprints = matcher.find_repetitive_blueprints(events)
    
    print(f"REPORT FOR {emp_id}:")
    # Identify Task 1.2 Multi-Timeframe counts
    p4 = [b for b in blueprints if b.persistence.is_4day_persistent]
    p3 = [b for b in blueprints if b.persistence.is_3day_persistent]
    
    print(f"  - Total Candidates: {len(blueprints)}")
    print(f"  - 4-Day Persistent (Daily Tasks): {len(p4)}")
    print(f"  - 3-Day Persistent (Regular Tasks): {len(p3)}")
    
    if p4:
        top = p4[0]
        apps = " -> ".join(list(dict.fromkeys([s.app_name for s in top.steps])))
        print(f"  - Sample Daily Workflow [{top.workflow_id}]: {apps}")
        print(f"    Occurrences: {top.persistence.daily_counts}")
    print("-" * 50)