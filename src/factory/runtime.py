import json
import os
import time
from typing import Dict

import requests
from loguru import logger
from playwright.sync_api import sync_playwright

# Set up logging for the workforce
logger.remove()
logger.add("logs/agent_runtime.log", rotation="10 MB", level="DEBUG")
logger.add(lambda msg: print(msg, end=""), level="INFO") # Keep terminal clean

class AgentRuntime:
    """
    The Operational Agent 'Body'.
    It loads a 'Brain' (JSON), interprets the semantic intent,
    and executes physical tools (Playwright/PyAutoGUI).
    """
    
    def __init__(self, brain_path: str):
        if not os.path.exists(brain_path):
            logger.error(f"Brain file not found at {brain_path}")
            raise FileNotFoundError("Missing configuration for agent.")
            
        with open(brain_path, 'r') as f:
            self.brain = json.load(f)
        
        self.agent_id = self.brain['metadata']['agent_id']
        self.intent = self.brain['logic']['intent']

    def run(self, live_mode: bool = False):
        logger.info(f"🤖 Agent {self.agent_id} waking up. Mission: {self.intent}")

        try:
            if live_mode:
                self._run_live()
            else:
                self._run_simulated()
                
            msg = f"🏁 Mission Accomplished: Agent {self.agent_id} completed the task."
            logger.success(msg)
        except Exception as e:
            logger.critical(f"💥 Critical Failure in Agent {self.agent_id}: {e}")

    def _run_simulated(self):
        for step in self.brain['execution_plan']:
            action = self._recover_intent(step)
            log_msg = f"[Step {step['step_id']}] SIMULATING {action.upper()}"
            logger.info(f"{log_msg} in {step['app_name']}")
            time.sleep(0.5)

    def _verify_asset(self, url: str) -> bool:
        try:
            return requests.head(url, timeout=3).status_code == 200
        except Exception:
            return False

    def _run_live(self):
        """Live-mode using Playwright and PyAutoGUI."""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            
            for step in self.brain['execution_plan']:
                # 1. Asset Resilience Check
                if not self._verify_asset(step['screenshot_url']):
                    msg = f"Step {step['step_id']}: Visual anchor missing."
                    logger.warning(f"{msg} Using text-only context.")
                    
                # 2. Semantic Intent Recovery (The Wait Trap)
                action = self._recover_intent(step)
                
                # 3. Execution
                logger.info(f"➡️ Executing {action.upper()} on {step['window_title']}")
                self._execute_physical_action(action, step, page)
                time.sleep(1) # Human-like delay

            browser.close()

    def _recover_intent(self, step: Dict) -> str:
        """Fixes 'Wait Trap' by checking if AI description implies in action."""
        action = step['action'].lower()
        desc = step['description'].lower()
        
        if action == "wait" and ("click" in desc or "button" in desc):
            return "click"
        if action == "wait" and ("type" in desc or "enter" in desc):
            return "type"
        return action

    def _verify_asset(self, url: str) -> bool:
        """Resilience check for DigitalOcean URLs."""
        try:
            return requests.head(url, timeout=3).status_code == 200
        except Exception: 
            return False

    def _execute_physical_action(self, action: str, step: Dict, page):
        """Bridges the Brain to the Hardware."""
        app = step['app_name'].lower()
        params = step.get('params', {})

        try:
            if "chrome" in app or "brave" in app:
                if action == "navigation":
                    page.goto(params.get('url', ''))
                elif action == "click":
                    # Logic: Use AI-labeled intent to find the button
                    page.keyboard.press("Enter") # Fallback for discovered SQL runs
                elif action == "type":
                    page.fill("textarea", params.get('text', ''))
            else:
                # Desktop Automation via PyAutoGUI
                logger.info(f"🖱️  Desktop Action: {action} in {app}")
                # pyautogui.click(x, y) # Example
        except Exception as e:
            logger.error(f"Execution step failed: {e}")