import os
import sys
from loguru import logger

# 1. Ensure the 'src' directory is in the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import your new consolidated Runtime
try:
    from src.factory.runtime import AgentRuntime
except ImportError as e:
    print(f"❌ Critical Import Error: {e}")
    sys.exit(1)

def run_demo():
    # 2. Path to your generated brains
    config_dir = "agent_configs"
    
    if not os.path.exists(config_dir):
        logger.error(f"Folder '{config_dir}' not found. Did you run main_factory.py?")
        return

    # 3. Find all brain files
    brain_files = [f for f in os.listdir(config_dir) if f.endswith(".json")]

    if not brain_files:
        logger.warning(f"No agent brains found in {config_dir}")
        return

    logger.info(f"🔎 Found {len(brain_files)} agents. Initializing demo for the first one...")

    # 4. Pick one agent (e.g., the SQL query agent) and run it in simulation mode
    selected_brain_path = os.path.join(config_dir, brain_files[0])
    
    try:
        runner = AgentRuntime(selected_brain_path)
        # We use live_mode=False for the simulation required by the demo
        runner.run(live_mode=False) 
    except Exception as e:
        logger.exception(f"Failed to execute agent: {e}")

if __name__ == "__main__":
    run_demo()