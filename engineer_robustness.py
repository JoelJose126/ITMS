import json

# Enhancing the KB with "Robustness Logic"
robust_kb = [
    {
        "intent": "cancel_order",
        "primary_flow": [
            "Step 1: Validate Order ID format (Regex).",
            "Step 2: Tool call 'mcp-itms:get_order_status'.",
            "Step 3: If Status in ['Pending', 'Processing'], execute 'mcp-itms:cancel_order'.",
            "Step 4: If Status in ['Shipped', 'Delivered'], trigger 'Human-Vetted' branch for return policy."
        ],
        "error_handling": {
            "order_not_found": "Ask user to verify Order ID; provide example format.",
            "tool_timeout": "Escalate to Human Queue with [SYSTEM_ERROR] tag.",
            "permission_denied": "Escalate to Human; check user authentication status."
        },
        "escalation_triggers": [
            "User sentiment becomes highly negative (Score < 0.2).",
            "Third consecutive failed Order ID attempt.",
            "System fails to reach ITMS database."
        ],
        "autonomous_success_message": "Your order has been successfully cancelled. You will receive a confirmation email shortly.",
        "human_handoff_note": "Agent was unable to cancel automatically because order is already [STATUS]. Human intervention needed to discuss return options."
    },
    {
        "intent": "recover_password",
        "primary_flow": [
            "Step 1: Validate Email/Username format.",
            "Step 2: Tool call 'mcp-auth:check_user_exists'.",
            "Step 3: If True, execute 'mcp-email:send_reset_link'.",
            "Step 4: If False, suggest 'create_account' flow."
        ],
        "error_handling": {
            "user_not_found": "Gently inform user the email isn't in our system; offer registration.",
            "email_service_down": "Inform user of technical delay; log ticket for retry; escalate if critical."
        },
        "escalation_triggers": [
            "User reports they no longer have access to the registered email.",
            "Suspicious activity flag (Too many requests from one IP)."
        ],
        "autonomous_success_message": "A password reset link has been sent to your registered email address.",
        "human_handoff_note": "User cannot access registered email. Human required for identity verification."
    }
]

# We will apply this "Robustness Schema" to the top 5 'Hero' intents for the hackathon.
with open('robust_knowledge_base.json', 'w') as f:
    json.dump(robust_kb, f, indent=4)

print("Created robust_knowledge_base.json with failure protocols.")
