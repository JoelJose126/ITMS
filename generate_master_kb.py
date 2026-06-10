import json
import pandas as pd
from datasets import load_dataset

# 1. Load full dataset to get all 27 intents
print("Loading intents for full Robust KB construction...")
dataset = load_dataset("Bitext/Bitext-customer-support-llm-chatbot-training-dataset")
all_intents = pd.DataFrame(dataset['train'])['intent'].unique()

# 2. Define Logic Archetypes
# To scale to 27 intents, we define patterns and then apply them.

ARCHETYPES = {
    "AUTONOMOUS_LINK": {
        "flow": ["1. Validate input format", "2. Trigger system-link generation", "3. Send email/display link"],
        "error": {"system_down": "Inform of delay, auto-retry in background", "invalid_input": "Ask for correction"},
        "escalation": ["User requests live agent", "Link fails to generate 3x"]
    },
    "AUTONOMOUS_LOOKUP": {
        "flow": ["1. Extract search parameters", "2. Query Database/API", "3. Format results using template"],
        "error": {"not_found": "Suggest relevant alternatives", "db_timeout": "Escalate with [SYSTEM_ERROR]"},
        "escalation": ["Search returns ambiguous results", "User expresses frustration"]
    },
    "CONDITIONAL_ACTION": {
        "flow": ["1. Verify ID/Authentication", "2. Check state/status (e.g. Shipped?)", "3. Execute or Route to Human"],
        "error": {"status_mismatch": "Explain why action is restricted", "validation_fail": "Handoff to human vetting"},
        "escalation": ["Financial value > $500", "State check tool fails"]
    },
    "HUMAN_LED": {
        "flow": ["1. Perform sentiment audit", "2. Summarize conversation history", "3. Open priority human ticket"],
        "error": {"summarization_fail": "Pass raw transcript to human"},
        "escalation": ["Always (Intent is high-sensitivity)"]
    }
}

# 3. Map every intent to an Archetype
INTENT_MAPPING = {
    # Account
    "create_account": "AUTONOMOUS_LINK",
    "recover_password": "AUTONOMOUS_LINK",
    "edit_account": "AUTONOMOUS_LINK",
    "delete_account": "HUMAN_LED",
    "switch_account": "CONDITIONAL_ACTION",
    "registration_problems": "HUMAN_LED",
    # Orders
    "place_order": "CONDITIONAL_ACTION",
    "cancel_order": "CONDITIONAL_ACTION",
    "change_order": "CONDITIONAL_ACTION",
    "track_order": "AUTONOMOUS_LOOKUP",
    # Shipping/Delivery
    "change_shipping_address": "CONDITIONAL_ACTION",
    "set_up_shipping_address": "AUTONOMOUS_LINK",
    "delivery_options": "AUTONOMOUS_LOOKUP",
    "delivery_period": "AUTONOMOUS_LOOKUP",
    # Financial
    "get_invoice": "AUTONOMOUS_LOOKUP",
    "check_invoice": "AUTONOMOUS_LOOKUP",
    "check_payment_methods": "AUTONOMOUS_LOOKUP",
    "payment_issue": "HUMAN_LED",
    "get_refund": "CONDITIONAL_ACTION",
    "check_refund_policy": "AUTONOMOUS_LOOKUP",
    "track_refund": "AUTONOMOUS_LOOKUP",
    "check_cancellation_fee": "AUTONOMOUS_LOOKUP",
    # Support/Feedback
    "complaint": "HUMAN_LED",
    "review": "AUTONOMOUS_LINK",
    "newsletter_subscription": "AUTONOMOUS_LINK",
    "contact_customer_service": "AUTONOMOUS_LOOKUP",
    "contact_human_agent": "HUMAN_LED"
}

# 4. Generate Robust KB for all 27 intents
robust_kb = []

for intent in all_intents:
    archetype_key = INTENT_MAPPING.get(intent, "HUMAN_LED") # Default to safe human-led
    arch = ARCHETYPES[archetype_key]
    
    # Get a sample response for the template
    sample_df = pd.DataFrame(dataset['train'])
    template = sample_df[sample_df['intent'] == intent].iloc[0]['response']
    
    entry = {
        "intent": intent,
        "archetype": archetype_key,
        "primary_flow": arch["flow"],
        "error_handling": arch["error"],
        "escalation_triggers": arch["escalation"],
        "template_response": template,
        "requires_human_confirmation": (archetype_key in ["HUMAN_LED", "CONDITIONAL_ACTION"])
    }
    robust_kb.append(entry)

# 5. Save the Master KB
with open('robust_knowledge_base.json', 'w') as f:
    json.dump(robust_kb, f, indent=4)

print(f"Master Robust KB created with {len(robust_kb)} intents.")
