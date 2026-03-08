import time
from io import BytesIO

import requests
from google import genai
from PIL import Image

from src.core.schemas import WorkflowBlueprint


class VisionLabeler:
    def __init__(self, api_key: str):
        # The new SDK handles pathing. Use the bare model name.
        self.client = genai.Client(api_key=api_key)
        self.model_id = "gemini-flash-latest" 

    def enrich_blueprint(self, blueprint: WorkflowBlueprint, retries: int = 1) -> WorkflowBlueprint:
        sample_step = blueprint.steps[len(blueprint.steps)//2]
        image_url = sample_step.screenshot_url
        
        for attempt in range(retries + 1):
            try:
                # 1. Fetch image from remote URL
                resp = requests.get(image_url, timeout=10)
                resp.raise_for_status()
                img = Image.open(BytesIO(resp.content))

                # Create a string of all window titles in this sequence
                context_titles = " -> ".join([s.window_title for s in blueprint.steps if s.window_title])

                prompt = (
                    f"The user sequence is: {context_titles}. "
                    f"The current application is {sample_step.app_name}. "
                    "Based on this sequence and the attached screenshot: "
                    "1. What is the business intent? 2. Targeted UI element? "
                    "Format: Goal | Element"
)

                # 2. Call Gemini
                ai_response = self.client.models.generate_content(
                    model=self.model_id,
                    contents=[prompt, img]
                )
                
                raw_text = ai_response.text
                intent = raw_text.split("|")[0].strip() if "|" in raw_text else raw_text
                element = raw_text.split("|")[1].strip() if "|" in raw_text else "UI Component"

                # 3. Handle Frozen Pydantic instances with model_copy
                new_steps = [
                    s.model_copy(update={"description": f"Target: {element} | Goal: {intent}"})
                    for s in blueprint.steps
                ]

                return blueprint.model_copy(update={
                    "intent_summary": intent,
                    "steps": new_steps
                })

            except Exception as e:
                if "429" in str(e):
                    wait = 35 * (attempt + 1)
                    print(f"  ⏳ Rate limit. Waiting {wait}s...")
                    time.sleep(wait)
                    continue
                print(f"  ⚠️ Vision failed for {blueprint.workflow_id}: {e}")
                break

        return blueprint.model_copy(update={"intent_summary": "Discovered Business Process"})