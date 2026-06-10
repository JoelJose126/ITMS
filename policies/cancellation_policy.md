# Cancellation Policy

This policy defines the rules for order cancellations based on the physical state of the shipment.

## 1. Fulfillment States & Actions

### State: Not Packed
*   **Action:** Autonomous Cancellation permitted.
*   **Fee:** 0% cancellation fee.
*   **Outcome:** Full refund triggered immediately.

### State: Packed
*   **Action:** Human-Verified Cancellation required.
*   **Logic:** The agent must flag the order to halt shipping. A human warehouse specialist must confirm the package has been intercepted before the agent can finalize the cancellation.
*   **Fee:** A restocking fee of **5%** may apply.

### State: Shipped
*   **Action:** Autonomous Rejection (Standard).
*   **Logic:** Once an order is in transit with the courier, it cannot be cancelled. 
*   **Exception:** For **VIP users** or **High-Value Orders (>$500)**, the agent may escalate to a Human Agent to attempt a carrier reroute/intercept.

## 2. Partial Cancellations
*   If a user wishes to cancel only a portion of an order, the request must follow the **Order Modification Policy**.
