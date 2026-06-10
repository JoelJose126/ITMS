import json
import os
from datetime import datetime

DB_FILE = "itms_db.json"

class ITMS_API:
    def __init__(self):
        self.load_db()

    def load_db(self):
        if not os.path.exists(DB_FILE):
            raise FileNotFoundError(f"Database file {DB_FILE} not found.")
        with open(DB_FILE, "r") as f:
            self.db = json.load(f)

    def save_db(self):
        with open(DB_FILE, "w") as f:
            json.dump(self.db, f, indent=2)

    def create_ticket(self, type, sub_type, user_email, description):
        ticket_id = f"TKT-{self.db['config']['next_ticket_id']}"
        self.db['config']['next_ticket_id'] += 1
        
        new_ticket = {
            "id": ticket_id,
            "type": type,
            "sub_type": sub_type,
            "user_email": user_email,
            "status": "OPEN",
            "created_at": datetime.now().isoformat(),
            "description": description,
            "comments": [f"[{datetime.now().isoformat()}] Ticket created and categorized as {type}/{sub_type}."]
        }
        self.db['tickets'].append(new_ticket)
        self.save_db()
        return ticket_id

    def add_comment(self, ticket_id, comment):
        for ticket in self.db['tickets']:
            if ticket['id'] == ticket_id:
                ticket['comments'].append(f"[{datetime.now().isoformat()}] {comment}")
                self.save_db()
                return True
        return False

    def update_status(self, ticket_id, status):
        for ticket in self.db['tickets']:
            if ticket['id'] == ticket_id:
                ticket['status'] = status
                ticket['comments'].append(f"[{datetime.now().isoformat()}] Status changed to {status}.")
                self.save_db()
                return True
        return False

    def get_order_details(self, order_id, user_email):
        for order in self.db['orders']:
            if order['id'] == order_id and order['owner'] == user_email:
                return order
        return None

    def get_user_history(self, user_email):
        for user in self.db['users']:
            if user['email'] == user_email:
                return user['history']
        return []

if __name__ == "__main__":
    # Quick sanity test
    api = ITMS_API()
    tid = api.create_ticket("Order", "Tracking", "user1@example.com", "Checking status of last order.")
    print(f"Created Ticket: {tid}")
    api.add_comment(tid, "Workflow Step 1: Sentiment analysis complete.")
    api.update_status(tid, "RESOLVED")
    api.update_status(tid, "CLOSED")
    print("Database updated successfully.")
