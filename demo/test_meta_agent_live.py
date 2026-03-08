import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.factory.meta_agent import MetaAgentFactory
from demo.runner import AgentRunner

def run_google_test():
    # 1. GENERATE: The Meta-Agent builds the Google Agent's configuration
    print("🏗️  Step 1: Meta-Agent Factory building Google Agent...")
    factory = MetaAgentFactory("outputs/google_test_workflow.json")
    brain_paths = factory.build_all_agents()
    
    # 2. EXECUTE: The Operational Agent runs
    print("\n🤖 Step 2: Starting the Generated Agent...")
    runner = AgentRunner(brain_paths[0])
    runner.run_live()

if __name__ == "__main__":
    run_google_test()