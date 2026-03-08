import sqlite3
from typing import List

import numpy as np
import pandas as pd

from src.core.schemas import CapturedEvent


class DatabaseManager:
    """
    Handles all SQLite interactions
    """
    def __init__(self, db_path: str = "data/test_data.db"):
        self.db_path = db_path

    def get_joined_data(self, employee_id: str) -> List[CapturedEvent]:
        """
        Fetches combined Event and Capture data for a specific employee.
        """
        query = """
        SELECT 
            c.id as capture_id,
            c.event_id,
            c.timestamp,
            c.id_employee,
            e.app_name,
            e.window_title,
            e.event as event_type,
            c.image_path,
            e.url,
            e.clipboard_content
        FROM captures c
        JOIN events e ON c.event_id = e.id
        WHERE c.id_employee = ?
        ORDER BY c.timestamp ASC
        """
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                df = pd.read_sql_query(query, conn, params=(employee_id,))
                
                # Critical for Pydantic: Convert NumPy/Pandas NaN to Python None
                df = df.replace({np.nan: None})
                
            return [CapturedEvent(**row) for row in df.to_dict('records')]
        except Exception as e:
            print(f"Error querying database: {e}")
            return []

    def get_employee_ids(self) -> List[str]:
        """Returns a list of all unique employee IDs in the dataset."""
        query = "SELECT DISTINCT id_employee FROM captures"
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return [row[0] for row in cursor.fetchall()]

    def get_full_dataset(self) -> dict[str, List[CapturedEvent]]:
        """
        Returns a dictionary mapping employee_id to their list of events.
        """
        all_data = {}
        ids = self.get_employee_ids()
        for emp_id in ids:
            all_data[emp_id] = self.get_joined_data(emp_id)
        return all_data