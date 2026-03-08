import json
import time
from playwright.sync_api import sync_playwright

class AgentRunner:
    def __init__(self, brain_path: str):
        with open(brain_path, 'r') as f:
            self.brain = json.load(f)

    def run_live(self):
        """The 'Operational' execution requested by Task 2."""
        print(f"🚀 [LIVE MODE] Agent {self.brain['metadata']['agent_id']} is taking control...")
        
        with sync_playwright() as p:
            # 1. Launch the 'Body' (The Browser)
            browser = p.chromium.launch(headless=False) # False so you can see it move!
            page = browser.new_page()
            
            for step in self.brain['execution_plan']:
                print(f"➡️ Executing: {step['description']}")
                
                action = step['action'].lower()
                params = step.get('params', {})

                # 2. Logic Mapping (Brain -> Body)
                if action == "navigation":
                    page.goto(params['url'])
                    
                elif action == "type":
                    # The Agent finds the selector and types
                    selector = params.get('selector', 'textarea')
                    page.fill(selector, params['text'])
                    
                elif action == "click" or action == "wait":
                    # Handle keyboard 'Enter' or mouse clicks
                    if "key" in params:
                        page.keyboard.press(params['key'])
                    else:
                        page.click(params.get('selector', 'button'))
                
                time.sleep(2) # Delay so the interviewer can see the action

            print(f"✅ Mission Complete. Closing browser.")
            browser.close()