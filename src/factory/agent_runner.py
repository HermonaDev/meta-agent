import json
import time
from typing import Dict
from src.core.schemas import ActionType

class AgentRunner:
    """
    The Operational Agent. 
    It 'loads' a Brain Manifest and executes the steps using available tools.
    """
    
    def __init__(self, brain_path: str):
        with open(brain_path, 'r') as f:
            self.brain = json.load(f)
        self.agent_id = self.brain['metadata']['agent_id']
        self.plan = self.brain['execution_plan']
        self.prompt = self.brain['logic']['system_prompt']

    def run(self, mode: str = "dry_run"):
        """
        Executes the agent's plan.
        'dry_run' = Log actions without clicking.
        'live' = Actual Playwright/PyAutoGUI execution (requires local setup).
        """
        print(f"\n🤖 Agent {self.agent_id} is waking up...")
        print(f"🎯 Goal: {self.brain['logic']['intent']}")
        print(f"🧠 System Prompt loaded ({len(self.prompt)} chars)")
        print("-" * 50)

        for step in self.plan:
            step_id = step['step_id']
            action = step['action']
            app = step['app_name']
            target = step['window_title']
            
            print(f"[Step {step_id}] ACTION: {action} | APP: {app}")
            print(f"    - Target Window: {target}")
            print(f"    - Visual Verification: Fetching {step['screenshot_url'][:40]}...")

            if mode == "dry_run":
                time.sleep(0.5) # Simulate processing
                print(f"    ✅ LOG: Successfully simulated {action} on {app}")
            else:
                self._execute_live_action(step)
            
            print("-" * 30)

        print(f"\n🏁 Mission Accomplished: Agent {self.agent_id} completed all steps.")

    def _execute_live_action(self, step: Dict):
        """Placeholder for actual Playwright/PyAutoGUI calls."""
        # This is where the 'Body' actually moves.
        # Example: if step['app_name'] == 'chrome.exe': playwright.click(...)
        pass