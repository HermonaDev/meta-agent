import json
import os
from typing import List
from ..core.schemas import WorkflowBlueprint

class WorkflowExporter:
    @staticmethod
    def export_to_json(blueprints: List[WorkflowBlueprint], filename: str = "outputs/discovered_workflows.json"):
        """
        Converts a list of WorkflowBlueprints into a structured JSON file.
        This file serves as the input for Task 2 (The Meta-Agent).
        """
        # Ensure the directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        # Convert Pydantic models to dictionaries
        data = [b.model_dump() for b in blueprints]
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
            
        print(f"📦 Successfully exported {len(blueprints)} blueprints to {filename}")