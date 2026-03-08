import os
import json

def display_workforce():
    config_dir = "agent_configs"
    if not os.path.exists(config_dir):
        print("❌ No agents generated yet. Run main_factory.py.")
        return

    configs = [f for f in os.listdir(config_dir) if f.endswith(".json")]
    print(f"💼 CURRENT DIGITAL WORKFORCE: {len(configs)} Specialized Agents\n")
    print(f"{'AGENT ID':<15} | {'EMPLOYEE':<10} | {'INTENT'}")
    print("-" * 75)

    for cfg in configs:
        with open(os.path.join(config_dir, cfg), 'r') as f:
            data = json.load(f)
            meta = data['metadata']
            # Clean up the intent for display
            intent = data['logic']['intent'].replace('\n', ' ').strip()
            if len(intent) > 45: intent = intent[:42] + "..."
            
            print(f"{meta['agent_id']:<15} | {meta['target_employee']:<10} | {intent}")

if __name__ == "__main__":
    display_workforce()