import json
import os
from typing import Optional

import bcrypt
from fastapi import HTTPException

# Path to the users file
USER_FILE = os.path.join("database", "users.json")

# Load users data
def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, "r") as f:
        return json.load(f)

# Save users data
def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

# Register a new user
def register_user(username: str, password: str):
    users = load_users()
    if username in users:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    users[username] = {
        "password": hashed_pw.decode('utf-8'),
        "history": {}
    }
    save_users(users)

# Login authentication
def authenticate_user(username: str, password: str) -> bool:
    users = load_users()
    if username not in users:
        return False

    stored_hash = users[username]["password"].encode('utf-8')
    return bcrypt.checkpw(password.encode('utf-8'), stored_hash)

# Store a user's chat history
def store_chat(username: str, chat_id: str, messages: list):
    users = load_users()
    if username in users:
        users[username]["history"][chat_id] = messages
        save_users(users)

# Gets a user's chat history
def get_chat(username: str, chat_id: str) -> Optional[list]:
    users = load_users()
    return users.get(username, {}).get("history", {}).get(chat_id, [])