# Security & Authentication Policy

This policy governs access to sensitive data (Feature 8) and account changes (Feature 10).

## 1. Identity Verification (The Security Gate)
*   **In-Session Validation:** Agents must check for an active authenticated session.
*   **Factor-2 Challenge:** For non-authenticated sessions, the agent must verify at least **two** pieces of info (e.g., Registered Email + Last 4 digits of Order ID) before discussing any account details.

## 2. No-Direct-Edit Rule
*   Agents are strictly prohibited from changing **Passwords** or **Primary Emails** directly within the chat or email body. 
*   **Action:** The agent must only trigger a "Secure Reset Link" sent to the *currently* registered address on file.

## 3. PII Masking
*   Agents must autonomously mask or redact any full credit card numbers or passwords if a user accidentally types them into the interaction.
