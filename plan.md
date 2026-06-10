# Project Status: ITMS (Inquiry Ticket Routing and Management System)

## Phase 1: Data & Knowledge Base (COMPLETE)
We have successfully prepared the "Brain" and the "Rulebook" for the agentic system.

### Completed Tasks:
- [x] **Dataset Acquisition:** Downloaded the Bitext Customer Support dataset (~26k records).
- [x] **Master Knowledge Base:** Created `master_knowledge_base.json` with 27 intent-specific Standard Operating Procedures (SOPs) categorized into 5 archetypes (Account, Order, Shipping, Financial, Relations).
- [x] **Agentic Fine-tuning Dataset:** Created `agentic_fine_tune_v2.jsonl` containing 81 high-fidelity multi-turn trajectories (Positive, Negative, and Error cases) in ShareGPT format.
- [x] **Data Scrutiny:** Verified structural integrity and logical adherence to the SOPs using specialized sub-agents.
- [x] **Hardware Feasibility:** Performed diagnostics; identified In-Context Learning (ICL) as the most efficient strategy for the hackathon due to VRAM constraints.

### Key Files:
- `master_knowledge_base.json`: The procedural SOP rulebook.
- `agentic_fine_tune_v2.jsonl`: The curated training/few-shot dataset.
- `generate_procedural_kb.py`: The script used to generate the refined KB.

## Phase 2: Database & Workflow Planning (NEXT)
The next step is to build the "Body" of the system.

### Upcoming Tasks:
1. **Mock ITMS Database:** Design and implement a JSON-based state tracker for tickets, orders, and user history.
2. **ADK Workflow Integration:** Map the natural language SOPs into functional Google ADK nodes.
3. **MCP Tool Implementation:** Create tools for ticket creation, status updates, and email triggers.

---
*Updated: Tuesday, 9 June 2026*
