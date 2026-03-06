import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from src.core.database import DatabaseManager
from src.discovery.repetition import PatternMatcher

db = DatabaseManager("data/test_data.db")
matcher = PatternMatcher(window_size=5)

for emp_id in db.get_employee_ids():
    events = db.get_joined_data(emp_id)
    patterns = matcher.find_patterns(events)
    
    print(f"Employee {emp_id}:")
    print(f"  - Unique Repeating Patterns Found: {len(patterns)}")
    
    # Show the top persistent pattern
    if patterns:
        top = patterns[0]
        print(f"  - Top Pattern (Persistence: {top.persistence_score} days):")
        print(f"    Apps: {' -> '.join(top.app_sequence)}")
        print(f"    Daily occurrences: {top.daily_counts}")
    print("-" * 50)