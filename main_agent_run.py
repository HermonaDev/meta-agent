import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.factory.agent_runner import AgentRunner

def demonstrate_agents():
    # 1. Look for generated brains
    config_dir = "agent_configs"
    brain_files = [f for f in os.listdir(config_dir) if f.endswith(".json")]

    if not brain_files:
        print("❌ No agents found. Run main_factory.py first.")
        return

    print(f"🔎 Found {len(brain_files)} specialized agents.")
    
    # 2. Pick one agent and run it in 'dry_run' mode
    # This demonstrates the 'operational' logic requested in the PDF.
    selected_brain = os.path.join(config_dir, brain_files[0])
    
    runner = AgentRunner(selected_brain)
    runner.run(mode="dry_run")

if __name__ == "__main__":
    demonstrate_agents()