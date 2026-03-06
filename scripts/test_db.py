import sys
import os
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.core.database import DatabaseManager
from src.core.schemas import CapturedEvent
from src.core.utils import verify_image_url


def run_diagnostic():
    db_path = "data/test_data.db"
    
    if not os.path.exists(db_path):
        print(f"Error: Database not found at {db_path}")
        return

    db = DatabaseManager(db_path)
    
    try:
        employees = db.get_employee_ids()
        print(f"✅ Connection Successful. Found {len(employees)} employees: {employees}")
        print("-" * 50)

        for emp_id in employees:
            data = db.get_joined_data(emp_id)
            print(f"Employee: {emp_id} | Events: {len(data)}")
            
            if data:
                # Check first 5 images for reachability
                unreachable = 0
                for event in data[:5]:
                    # Try as local file first, then as URL
                    if not os.path.exists(event.image_path) and not verify_image_url(event.image_path):
                        unreachable += 1
                
                if unreachable > 0:
                    print(f"  - ❌ Assets: {unreachable}/5 samples are inaccessible.")
                else:
                    print(f"  - ✅ Assets: Verified connectivity.")
        
                # Group by date to see the 4-day span
                dates = set(e.timestamp.split('T')[0] for e in data)
                print(f"  - Data Span: {sorted(list(dates))}")
                
                # Show one sample
                sample = data[0]
                print(f"  - Sample App: {sample.app_name} | Event: {sample.event_type}")
            print("-" * 50)
            
    except Exception as e:
        print(f"❌ Diagnostic failed: {e}")

if __name__ == "__main__":
    run_diagnostic()