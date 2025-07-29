import json, os
from datetime import datetime
 
DB_PATH = "user_db.json"
HISTORY_PATH = "password_history.json"
RESET_LOG = "reset_log.json"
 
for path in [DB_PATH, HISTORY_PATH, RESET_LOG]:
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write("[]")
 
def load_users():
    with open(DB_PATH) as f:
        return json.load(f)
 
def save_user(user):
    users = load_users()
    users.append(user)
    with open(DB_PATH, "w") as f:
        json.dump(users, f, indent=2)
 
def get_user_by_username(username):
    return next((u for u in load_users() if u['username'] == username), None)
 
def update_user_password(username, hashed):
    users = load_users()
    for u in users:
        if u['username'] == username:
            u['password'] = hashed
            u['password_updated_at'] = datetime.now().isoformat()
    with open(DB_PATH, "w") as f:
        json.dump(users, f, indent=2)
 
def update_user_contact(username, new_contact):
    users = load_users()
    for u in users:
        if u['username'] == username:
            u['username'] = new_contact
    with open(DB_PATH, "w") as f:
        json.dump(users, f, indent=2)
 
def store_password_history(username, hashed):
    with open(HISTORY_PATH) as f:
        history = json.load(f)
    history.append({"username": username, "password": hashed, "time": datetime.now().isoformat()})
    with open(HISTORY_PATH, "w") as f:
        json.dump(history, f, indent=2)
 
def count_recent_password_resets(username):
    with open(RESET_LOG) as f:
        resets = json.load(f)
    now = datetime.now()
    recent = [r for r in resets if r['username'] == username and (now - datetime.fromisoformat(r['time'])).days < 1]
    resets.append({"username": username, "time": now.isoformat()})
    with open(RESET_LOG, "w") as f:
        json.dump(resets, f, indent=2)
    return len(recent)