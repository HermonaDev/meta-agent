import sqlite3
import pandas as pd
import numpy as np # Add this import
from typing import List, Optional
from pydantic import BaseModel

class CapturedEvent(BaseModel):
    capture_id: str
    event_id: str
    timestamp: str
    id_employee: str
    app_name: Optional[str] = None
    window_title: Optional[str] = None
    event_type: Optional[str] = None
    image_path: str
    url: Optional[str] = None
    # We use Optional[str] = None to allow for missing data safely
    clipboard_content: Optional[str] = None

class DatabaseManager:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def get_joined_data(self, employee_id: str) -> List[CapturedEvent]:
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
        
        with sqlite3.connect(self.db_path) as conn:
            df = pd.read_sql_query(query, conn, params=(employee_id,))
            
            # THE FIX: Replace all NaN values with None
            # Pydantic understands 'None', but it hates 'NaN' (float)
            df = df.replace({np.nan: None})
            
        return [CapturedEvent(**row) for row in df.to_dict('records')]

    def get_employee_ids(self) -> List[str]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT id_employee FROM captures")
            return [row[0] for row in cursor.fetchall()]