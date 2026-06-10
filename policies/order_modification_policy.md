# Order Modification Policy

This policy covers changes to delivery addresses and cart contents.

## 1. Address Changes
*   **Permitted:** Only if the status is **'Not Packed'** or **'Packed'**.
*   **Autonomous:** The agent updates the shipping destination in the registry and confirms to the user.
*   **Restricted:** If **'Shipped'**, the agent must inform the user that changes are not possible autonomously and provide the courier's tracking link for a direct redirect attempt.

## 2. Cart Modifications (Items/Quantity)
*   **State Dependency:** Changes are only permitted in the **'Not Packed'** state.
*   **Price Increases:** If the new items result in a higher total, the agent must generate and send a **Secure Payment Link**. The modification is only finalized after payment is confirmed.
*   **Price Decreases:** If the total is lower, the agent must inform the user that a **Partial Refund** will be initiated automatically **POST-DELIVERY** to ensure the items are received first.
*   **Inventory Check:** Before proposing a change, the agent MUST query the inventory database. If an item is out of stock, the agent must inform the user and suggest alternatives.
