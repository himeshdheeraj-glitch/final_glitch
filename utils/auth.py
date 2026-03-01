import json
import os

DB_FILE = 'users_db.json'

def read_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, 'w') as f:
            json.dump({"users": []}, f)
        return {"users": []}
    try:
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    except:
        return {"users": []}

def write_db(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def register_user(username, email, blood_type, password):
    db = read_db()
    
    # Check if exists
    if any(u['username'].lower() == username.lower() or u['email'].lower() == email.lower() for u in db['users']):
        return False, "User or Email already exists"
    
    new_user = {
        "id": str(len(db['users']) + 1),
        "username": username,
        "email": email,
        "blood_type": blood_type or "Unknown",
        "password": password
    }
    
    db['users'].append(new_user)
    write_db(db)
    return True, new_user

def login_user(username, password):
    db = read_db()
    user = next((u for u in db['users'] if u['username'].lower() == username.lower() and u['password'] == password), None)
    
    if user:
        return True, user
    return False, "Invalid credentials"

def get_all_users():
    db = read_db()
    return [{"username": u['username'], "email": u['email'], "blood_type": u['blood_type']} for u in db['users']]
