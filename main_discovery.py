import os
import sys
import time

from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.database import DatabaseManager
from src.discovery.exporter import WorkflowExporter
from src.discovery.repetition import PatternMatcher
from src.discovery.vision_labeler import VisionLabeler

load_dotenv()

def run_task_1():
    db = DatabaseManager("data/test_data.db")
    matcher = PatternMatcher(window_size=4)
    labeler = VisionLabeler(api_key=os.getenv("GEMINI_API_KEY"))
    
    final_output = []

    print("🚀 Starting Task 1: Autonomous Workflow Discovery...")

    for emp_id in db.get_employee_ids():
        print(f"\nAnalyzing Employee: {emp_id}")
        events = db.get_joined_data(emp_id)
        
        blueprints = matcher.find_repetitive_blueprints(events)
        high_value = [b for b in blueprints if b.persistence.is_2day_persistent]
        
        # We'll label the top 3 per employee
        for b in high_value[:3]:
            print(f"  👁️  AI Labeling workflow {b.workflow_id}...")
            enriched_b = labeler.enrich_blueprint(b)
            final_output.append(enriched_b)
            
            # THE FIX: Wait 2 seconds between calls to avoid 429 errors
            time.sleep(2)

    WorkflowExporter.export_to_json(final_output)

if __name__ == "__main__":
    run_task_1()