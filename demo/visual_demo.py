# Add this to your runner or a new demo script
import webbrowser

def visual_demo(brain):
    print(f"📺 VISUAL DEMO MODE: Agent {brain['metadata']['agent_id']}")
    for step in brain['execution_plan']:
        print(f"Step {step['step_id']}: {step['description']}")
        # Open the screenshot in your default browser to 'simulate' what the agent sees
        webbrowser.open(step['screenshot_url'])
        time.sleep(3) # Give you time to look at the screen during the interview