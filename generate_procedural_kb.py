import json
import pandas as pd
from datasets import load_dataset

# 1. Load intents
print("Generating Refined Descriptive Master KB...")
dataset = load_dataset("Bitext/Bitext-customer-support-llm-chatbot-training-dataset")
all_intents = pd.DataFrame(dataset['train'])['intent'].unique()

# 2. Define Descriptive SOP Archetypes
# These define the 'business logic' without naming specific tools.

ARCHETYPES = {
    "ACCOUNT_AUTH": [
        "Step 1: Analyze user sentiment and urgency.",
        "Step 2: Create a support ticket to track the account-related inquiry.",
        "Step 3: Retrieve the specific account security and authentication procedures from the KB.",
        "Step 4: Request user identity credentials (email/username) if not provided.",
        "Step 5: Verify the user's status in the central identity registry.",
        "Step 6: Trigger the appropriate security action (e.g., send reset link, update profile, or escalate for deletion).",
        "Step 7: Ask if any other account settings or preferences need modification.",
        "Step 8: Finalize the ticket status and notify the user of the outcome."
    ],
    "ORDER_MANAGEMENT": [
        "Step 1: Analyze user sentiment and urgency.",
        "Step 2: Create a support ticket to track the order lifecycle event.",
        "Step 3: Retrieve the order processing and cancellation policies from the KB.",
        "Step 4: Extract the Order Reference Number; request it if missing.",
        "Step 5: Query the internal order database to check current fulfillment status.",
        "Step 6: Determine if the request can be fulfilled autonomously (e.g., if not yet shipped).",
        "Step 7: If autonomous, update the order registry; if not, escalate for human manual intervention.",
        "Step 8: Ask if the user wants to add items, change delivery speed, or make other order modifications.",
        "Step 9: Update the ITMS ticket to its final state (Resolved/Escalated) and notify the user."
    ],
    "SHIPPING_LOGISTICS": [
        "Step 1: Analyze user sentiment.",
        "Step 2: Create a support ticket to track the shipping/delivery inquiry.",
        "Step 3: Retrieve shipping zones and delivery period standards from the KB.",
        "Step 4: Identify destination details (Country/Address) from the inquiry.",
        "Step 5: Calculate delivery options or check current transit logs in the logistics database.",
        "Step 6: Provide accurate delivery estimates or shipping alternatives to the user.",
        "Step 7: Ask if any special handling instructions or address updates are required.",
        "Step 8: Close the ticket and confirm the user has the information they need."
    ],
    "FINANCIAL_ADMIN": [
        "Step 1: Analyze user sentiment, focusing on billing frustration.",
        "Step 2: Create a support ticket for the financial/billing inquiry.",
        "Step 3: Retrieve tax, refund, and invoicing policies from the KB.",
        "Step 4: Validate Transaction or Invoice IDs; request them if ambiguous.",
        "Step 5: Query the financial ledger to verify transaction status and amounts.",
        "Step 6: For refunds or payment issues, draft a resolution and escalate for human financial audit.",
        "Step 7: For invoice/payment method queries, provide the data directly from the system.",
        "Step 8: Ask if any other billing details, tax info, or payment methods need updating.",
        "Step 9: Update ticket status and notify the user."
    ],
    "CUSTOMER_RELATIONS": [
        "Step 1: Perform deep sentiment analysis. Identify specific pain points or positive feedback.",
        "Step 2: Create a support ticket for the feedback/complaint inquiry.",
        "Step 3: Retrieve escalation and empathy protocols from the KB.",
        "Step 4: If tone is harsh, pause to request a 'detailed description' of the grievance.",
        "Step 5: Retrieve user's previous satisfaction ratings and interaction history.",
        "Step 6: For complaints, summarize the context and escalate to a human lead immediately.",
        "Step 7: For reviews/subscriptions, process the feedback autonomously in the CRM.",
        "Step 8: Proactively ask if there is anything else that can be done to improve their experience.",
        "Step 9: Finalize the ticket and notify the user."
    ]
}

# 3. Map every intent to an Archetype
MAPPING = {
    # Account
    "create_account": "ACCOUNT_AUTH", "recover_password": "ACCOUNT_AUTH", "edit_account": "ACCOUNT_AUTH",
    "delete_account": "ACCOUNT_AUTH", "switch_account": "ACCOUNT_AUTH", "registration_problems": "ACCOUNT_AUTH",
    # Orders
    "place_order": "ORDER_MANAGEMENT", "cancel_order": "ORDER_MANAGEMENT", "change_order": "ORDER_MANAGEMENT",
    "track_order": "ORDER_MANAGEMENT",
    # Shipping
    "change_shipping_address": "SHIPPING_LOGISTICS", "set_up_shipping_address": "SHIPPING_LOGISTICS",
    "delivery_options": "SHIPPING_LOGISTICS", "delivery_period": "SHIPPING_LOGISTICS",
    # Financial
    "get_invoice": "FINANCIAL_ADMIN", "check_invoice": "FINANCIAL_ADMIN", "check_payment_methods": "FINANCIAL_ADMIN",
    "payment_issue": "FINANCIAL_ADMIN", "get_refund": "FINANCIAL_ADMIN", "check_refund_policy": "FINANCIAL_ADMIN",
    "track_refund": "FINANCIAL_ADMIN", "check_cancellation_fee": "FINANCIAL_ADMIN",
    # Relations
    "complaint": "CUSTOMER_RELATIONS", "review": "CUSTOMER_RELATIONS", "newsletter_subscription": "CUSTOMER_RELATIONS",
    "contact_customer_service": "CUSTOMER_RELATIONS", "contact_human_agent": "CUSTOMER_RELATIONS"
}

# 4. Generate the Refined KB
refined_kb = []

for intent in all_intents:
    archetype_key = MAPPING.get(intent, "CUSTOMER_RELATIONS")
    sop = ARCHETYPES[archetype_key]
    
    entry = {
        "intent": intent,
        "archetype": archetype_key,
        "procedure": sop,
        "logic_summary": f"Standard {archetype_key.replace('_', ' ').lower()} workflow.",
        "mandatory_prerequisites": ["Sentiment Analysis", "Ticket Creation", "KB Policy Retrieval"],
        "proactive_check_required": True,
        "failover_protocol": "On any tool failure or information ambiguity, log error to ITMS and escalate to human agent."
    }
    refined_kb.append(entry)

# 5. Save the Master KB
with open('master_knowledge_base.json', 'w') as f:
    json.dump(refined_kb, f, indent=4)

print(f"Refined Master KB created with {len(refined_kb)} intents across 5 archetypes.")
