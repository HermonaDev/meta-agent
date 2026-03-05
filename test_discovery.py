import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from src.core.database import DatabaseManager
from src.discovery.processor import WorkflowDiscovery

db = DatabaseManager("data/test_data.db")
discoverer = WorkflowDiscovery(gap_threshold_minutes=10)

for emp_id in db.get_employee_ids():
    events = db.get_joined_data(emp_id)
    workflows = discoverer.segment_into_workflows(events)
    
    print(f"Employee {emp_id}:")
    print(f"  - Raw Events: {len(events)}")
    print(f"  - Discovered Workflows: {len(workflows)}")
    
    if workflows:
        longest_wf = max(workflows, key=lambda x: x.event_count)
        print(f"  - Longest Workflow: {longest_wf.event_count} events using {longest_wf.app_sequence}")
    print("-" * 30)