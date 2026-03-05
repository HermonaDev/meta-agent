import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from src.core.database import DatabaseManager

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
            print(f"Employee: {emp_id}")
            print(f"  - Visually Anchored Events: {len(data)}")
            
            if data:
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