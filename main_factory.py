from src.factory.meta_agent import MetaAgentFactory


def run_task_2_generation():
    print("🏗️  Starting Meta-Agent Factory...")
    
    # 1. Point to the output of Task 1
    blueprint_path = "outputs/discovered_workflows.json"
    
    # 2. Initialize the Factory (The 'Agent Builder')
    factory = MetaAgentFactory(blueprint_path)
    
    # 3. Dynamically construct the Agents
    brain_files = factory.build_all_agents()
    
    print(f"\n✅ Orchestration Complete: Generated {len(brain_files)} Agent Brains.")
    print("Location: /agent_configs/")

if __name__ == "__main__":
    run_task_2_generation()