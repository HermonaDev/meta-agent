import sys
import os

# 1. Setup paths so we can find /src and /demo/runner
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(root_dir)
sys.path.append(current_dir)

# 2. Correct Imports
from src.factory.meta_agent import MetaAgentFactory
from runner import AgentRunner  # Standard import from the same folder

def run_google_test():
    print("🏗️  Step 1: Meta-Agent Factory building Google Agent...")
    
    # Path to the JSON
    json_path = os.path.join(current_dir, "google_test_workflow.json")
    
    # Generate the brain
    factory = MetaAgentFactory(json_path)
    brain_paths = factory.build_all_agents()
    
    print("\n🤖 Step 2: Starting the Generated Agent in LIVE mode...")
    # Execute the brain
    runner = AgentRunner(brain_paths[0])
    runner.run_live()

if __name__ == "__main__":
    run_google_test()