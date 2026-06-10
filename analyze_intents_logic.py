import pandas as pd
import json

# Load dataset
df = pd.read_csv('bitext_sample_100.csv') # Using the sample for structural analysis, but intent list is global

intents = [
    'cancel_order', 'change_order', 'change_shipping_address', 'check_cancellation_fee',
    'check_invoice', 'check_payment_methods', 'check_refund_policy', 'complaint',
    'contact_customer_service', 'contact_human_agent', 'create_account', 'delete_account',
    'delivery_options', 'delivery_period', 'edit_account', 'get_invoice',
    'get_refund', 'newsletter_subscription', 'payment_issue', 'place_order',
    'recover_password', 'registration_problems', 'review', 'set_up_shipping_address',
    'switch_account', 'track_order', 'track_refund'
]

# Analysis Dictionary: Mapping Intents to Workflow, Tools, and Validation
intent_analysis = {
    "track_order": {
        "mode": "Autonomous",
        "tools": ["mcp-itms:get_order_status"],
        "validation": ["Order ID Format (e.g., ORD-\d{5})"],
        "logic": "If Order ID is valid and found, provide real-time status."
    },
    "check_refund_policy": {
        "mode": "Autonomous",
        "tools": ["mcp-kb:get_policy_info"],
        "validation": None,
        "logic": "Provide standard policy text from KB."
    },
    "cancel_order": {
        "mode": "Human-Vetted",
        "tools": ["mcp-itms:cancel_order_request"],
        "validation": ["Order ID", "Reason"],
        "logic": "Agent drafts cancellation; human confirms if within window."
    },
    "complaint": {
        "mode": "Human-Led",
        "tools": ["mcp-itms:escalate_ticket"],
        "validation": None,
        "logic": "High sentiment gravity; agent summarizes history for human lead."
    },
    "payment_issue": {
        "mode": "Human-Vetted",
        "tools": ["mcp-payment:verify_transaction"],
        "validation": ["Transaction ID"],
        "logic": "Verify ID format first; if mismatch, agent asks for correct ID. If match, human reviews."
    }
}

# Plan: We will extend this to all 27 intents.
# For the hackathon, we will focus on 3-5 'Hero' intents to demonstrate the logic.

print("Intent Analysis Framework Drafted.")
with open('intent_delegation_plan.json', 'w') as f:
    json.dump(intent_analysis, f, indent=4)
