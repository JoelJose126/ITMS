import pandas as pd
import json
from datasets import load_dataset

# 1. Load full dataset
print("Loading Bitext dataset for KB construction...")
dataset = load_dataset("Bitext/Bitext-customer-support-llm-chatbot-training-dataset")
df = pd.DataFrame(dataset['train'])

# 2. Define the Operational Logic for each Intent
# This maps the Bitext intent to your specific hackathon requirements
intent_behavior = {
    # --- Autonomous & Link-Based ---
    "create_account": {
        "mode": "Autonomous",
        "requires_human": False,
        "conditions": "Always autonomous.",
        "action_type": "trigger_link",
        "logic_note": "Send registration link via email tool."
    },
    "recover_password": {
        "mode": "Autonomous",
        "requires_human": False,
        "conditions": "Always autonomous.",
        "action_type": "trigger_link",
        "logic_note": "Send password reset link via email tool."
    },
    "edit_account": {
        "mode": "Autonomous",
        "requires_human": False,
        "conditions": "Always autonomous.",
        "action_type": "portal_redirect",
        "logic_note": "Provide link to profile settings."
    },
    "track_order": {
        "mode": "Autonomous",
        "requires_human": False,
        "conditions": "Requires valid Order ID format.",
        "action_type": "api_lookup",
        "logic_note": "Query ITMS/Shipping API."
    },
    
    # --- Conditional Autonomy ---
    "cancel_order": {
        "mode": "Conditional",
        "requires_human": "If Status == 'Shipped' or 'In Transit'",
        "conditions": "Autonomous only if status is 'Pending' or 'Processing'.",
        "action_type": "db_update",
        "logic_note": "Check order status via tool first."
    },
    "change_order": {
        "mode": "Conditional",
        "requires_human": "Always (for item availability/price diff)",
        "conditions": "Complex logic required.",
        "action_type": "human_handoff",
        "logic_note": "Draft change request for human approval."
    },
    
    # --- Human-Led ---
    "complaint": {
        "mode": "Human-Led",
        "requires_human": True,
        "conditions": "High sentiment gravity.",
        "action_type": "escalation",
        "logic_note": "Summarize issue for senior agent."
    },
    "get_refund": {
        "mode": "Human-Led",
        "requires_human": True,
        "conditions": "Financial transaction involved.",
        "action_type": "audit_required",
        "logic_note": "Human must verify refund eligibility."
    }
}

# 3. Create the Knowledge Base (KB)
# We will extract one "Gold" example for each intent and enrich it
kb_entries = []

for intent in df['intent'].unique():
    # Find a clean example (Basic flag 'B', no errors)
    sample = df[(df['intent'] == intent) & (df['flags'].str.contains('B'))].iloc[0]
    
    behavior = intent_behavior.get(intent, {
        "mode": "General",
        "requires_human": True,
        "conditions": "Standard policy apply.",
        "action_type": "info_only",
        "logic_note": "Check KB for latest policy."
    })
    
    entry = {
        "intent": intent,
        "category": sample['category'],
        "thought_process": f"User wants to {intent.replace('_', ' ')}. Identify if this is autonomous or requires human intervention.",
        "resolution_conditions": behavior['conditions'],
        "requires_human_confirmation": behavior['requires_human'],
        "action_type": behavior['action_type'],
        "agent_note": behavior['logic_note'],
        "template_response": sample['response']
    }
    kb_entries.append(entry)

# 4. Save the KB
with open('knowledge_base.json', 'w') as f:
    json.dump(kb_entries, f, indent=4)

# 5. Create Fine-tuning JSONL (Instruction-Tuning Format)
# We embed the "Thought Process" and "Metadata" into the prompt so the model learns the logic
jsonl_data = []
for _, row in df.sample(2000).iterrows(): # Sample 2000 for a fast hackathon fine-tune
    behavior = intent_behavior.get(row['intent'], {"requires_human": True})
    human_flag = "[HUMAN_REQUIRED]" if behavior['requires_human'] else "[AUTONOMOUS]"
    
    jsonl_entry = {
        "instruction": f"{row['instruction']}\n\nTask: Determine resolution path and draft response.",
        "context": f"Intent: {row['intent']} | Category: {row['category']}",
        "response": f"THOUGHT: {human_flag} {row['intent'].replace('_', ' ')}. {row['response']}"
    }
    jsonl_data.append(jsonl_entry)

with open('fine_tune_data.jsonl', 'w') as f:
    for entry in jsonl_data:
        f.write(json.dumps(entry) + '\n')

print(f"Created knowledge_base.json with {len(kb_entries)} entries.")
print(f"Created fine_tune_data.jsonl with {len(jsonl_data)} samples.")
