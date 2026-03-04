import json
import os

DB_FILE = "data/bots.json"

def load_bots():
    if not os.path.exists(DB_FILE):
        return []
    

    try:
        with open(DB_FILE, "r") as f:
            content = f.read().strip()

            if not content:
                return []
            return json.loads(content)
        
    except json.JSONDecodeError:
        return []

def save_bot(bot):
    bots = load_bots()
    bots.append(bot)

    os.makedirs("data", exist_ok=True)

    with open(DB_FILE, "w") as f:
        json.dump(bots, f, indent=4)

def delete_bot(bot_id):
    bots = load_bots()
    bots  = [b for b in bots if b['bot_id'] != bot_id]

    with open(DB_FILE, "w") as f:
        json.dump(bots, f, indent=4)