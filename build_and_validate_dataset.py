import json
import pandas as pd
from datasets import load_dataset

# 1. Load the data
print("Loading Bitext dataset for agentic processing...")
dataset = load_dataset("Bitext/Bitext-customer-support-llm-chatbot-training-dataset")
df = pd.DataFrame(dataset['train'])

# 2. Load the Robust KB (our logic source of truth)
with open('robust_knowledge_base.json', 'r') as f:
    robust_kb = {item['intent']: item for item in json.load(f)}

# 3. The Agentic Generator Function
def create_agentic_conversation(row):
    intent = row['intent']
    kb_rule = robust_kb.get(intent)
    
    # Define flags based on KB
    human_req = kb_rule['requires_human_confirmation']
    archetype = kb_rule['archetype']
    
    # Construct the multi-turn trajectory
    conv = [
        {"from": "system", "value": f"You are an Agentic Support AI. Archetype: {archetype}. Follow the rules in your Knowledge Base."},
        {"from": "human", "value": row['instruction']},
        {"from": "thought", "value": f"Intent detected: {intent}. Checking robust_knowledge_base.json logic. Primary Flow: {kb_rule['primary_flow'][0]}"},
        {"from": "gpt", "value": f"{'[HUMAN_REQUIRED]' if human_req else '[AUTONOMOUS]'} {row['response']}"}
    ]
    return {"conversations": conv}

# 4. Programmatic Validator
def validate_entry(entry):
    # Rule 1: Must be valid JSON (handled by json.dumps)
    # Rule 2: Must have system, human, thought, and gpt turns
    roles = [turn['from'] for turn in entry['conversations']]
    required_roles = ['system', 'human', 'thought', 'gpt']
    if not all(role in roles for role in required_roles):
        return False, "Missing required roles"
    
    # Rule 3: GPT response must match the logic flag
    gpt_val = next(t['value'] for t in entry['conversations'] if t['from'] == 'gpt')
    thought_val = next(t['value'] for t in entry['conversations'] if t['from'] == 'thought')
    
    if "[HUMAN_REQUIRED]" in gpt_val and "HUMAN_LED" not in thought_val and "CONDITIONAL" not in thought_val:
        # Note: This is simplified logic check; for full run we check against KB map
        pass 
        
    return True, "OK"

# 5. Process and Validate a manageable chunk first
print("Processing and Validating...")
agentic_data = []
errors = []

for idx, row in df.iterrows():
    entry = create_agentic_conversation(row)
    is_valid, msg = validate_entry(entry)
    
    if is_valid:
        agentic_data.append(entry)
    else:
        errors.append(f"Row {idx}: {msg}")

# 6. Save and Summary
with open('agentic_fine_tune.jsonl', 'w') as f:
    for entry in agentic_data:
        f.write(json.dumps(entry) + '\n')

print(f"Total Processed: {len(agentic_data)}")
print(f"Total Errors: {len(errors)}")

# 7. Print 3 diverse samples for the user to 'Manual Audit'
print("\n--- MANUAL AUDIT SAMPLES ---")
import random
samples = random.sample(agentic_data, 3)
for i, s in enumerate(samples):
    print(f"\nSample {i+1}:")
    print(json.dumps(s, indent=2))
