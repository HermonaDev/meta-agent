import json
import time
import os
from playwright.sync_api import sync_playwright

class AgentRunner:
    """The 'Body' that executes a 'Brain' JSON using Playwright."""
    
    def __init__(self, brain_path: str):
        if not os.path.exists(brain_path):
            raise FileNotFoundError(f"Brain file not found: {brain_path}")
            
        with open(brain_path, 'r') as f:
            self.brain = json.load(f)

    def run_live(self):
        """The 'Operational' execution requested by Task 2."""
        print(f"🚀 [LIVE MODE] Agent {self.brain['metadata']['agent_id']} is taking control...")
        
        with sync_playwright() as p:
            # Launch browser
            browser = p.chromium.launch(headless=False) 
            page = browser.new_page()
            
            for step in self.brain['execution_plan']:
                print(f"➡️ Executing: {step['description']}")
                
                action = step['action'].lower()
                params = step.get('params', {})

                if action == "navigation":
                    page.goto(params['url'])
                elif action == "type":
                    selector = params.get('selector', 'textarea')
                    page.fill(selector, params['text'])
                elif action == "click" or action == "wait":
                    if "key" in params:
                        page.keyboard.press(params['key'])
                    else:
                        # Fallback for search button
                        page.keyboard.press("Enter")
                
                time.sleep(2) # Delay so you can see it!

            print(f"✅ Mission Complete. Closing browser.")
            browser.close()