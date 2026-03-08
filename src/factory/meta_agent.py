import json
import os
from typing import List, Dict
from src.core.schemas import WorkflowBlueprint

class MetaAgentFactory:
    """
    The 'Agent Builder System'. 
    It reads extractor output and dynamically constructs a 
    functioning Agent configuration (The 'Brain').
    """
    
    def __init__(self, blueprint_path: str):
        if not os.path.exists(blueprint_path):
            raise FileNotFoundError(f"Blueprint not found at {blueprint_path}")
            
        with open(blueprint_path, 'r') as f:
            self.blueprints = [WorkflowBlueprint(**b) for b in json.load(f)]

    def build_all_agents(self) -> List[str]:
        """
        Constructs a configuration manifest for every workflow.
        Returns a list of paths to the generated 'Brain' files.
        """
        generated_paths = []
        
        for blueprint in self.blueprints:
            print(f"🛠️  Factory: Engineering 'Brain' for {blueprint.workflow_id}...")
            
            # The 'System Prompt' is the DNA of the generated agent.
            # It tells the secondary LLM how to reason about this specific task.
            system_prompt = f"""
            ROLE: Specialized Automation Agent ({blueprint.workflow_id})
            CONTEXT: Operating within {blueprint.steps[0].app_name} for Employee {blueprint.employee_id}.
            GOAL: {blueprint.intent_summary}
            
            DYNAMIC INSTRUCTIONS:
            {self._format_steps(blueprint)}
            
            OPERATIONAL GUARDRAILS:
            1. Use 'wait_for_visual' before every click to ensure the UI is ready.
            2. If the 'window_title' does not match the step requirement, retry once then pause.
            3. Always log the result of a 'copy_paste' action.
            
            AVAILABLE TOOLSET:
            - click_ui(target_label: str): Performs a visual-anchored click.
            - type_into_field(text: str, field_name: str): Types text into a targeted input.
            - switch_context(app_name: str): Focuses the target application.
            - verify_state(image_url: str): Uses Vision to confirm the UI matches the expected step.
            """
            
            agent_manifest = {
                "metadata": {
                    "agent_id": blueprint.workflow_id,
                    "target_employee": blueprint.employee_id,
                    "complexity": len(blueprint.steps)
                },
                "logic": {
                    "system_prompt": system_prompt,
                    "intent": blueprint.intent_summary,
                    "visual_anchors": [s.screenshot_url for s in blueprint.steps]
                },
                "execution_plan": [s.model_dump() for s in blueprint.steps]
            }
            
            path = self._save_config(agent_manifest)
            generated_paths.append(path)
            
        return generated_paths

    def _format_steps(self, blueprint: WorkflowBlueprint) -> str:
        return "\n".join([f"Step {s.step_id}: {s.description}" for s in blueprint.steps])

    def _save_config(self, manifest: Dict) -> str:
        os.makedirs("agent_configs", exist_ok=True)
        filename = f"agent_configs/brain_{manifest['metadata']['agent_id']}.json"
        with open(filename, "w") as f:
            json.dump(manifest, f, indent=2)
        return filename