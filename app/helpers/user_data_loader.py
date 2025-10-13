import json
import os
import logging
from datetime import datetime, timedelta

DATA_FILE = os.path.join("data","user_data.json")

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def load_all_users():
    try:
        with open(DATA_FILE,"r", encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error(f"File not found: {DATA_FILE}. Returning empty data.")
        return {}
    except json.JSONDecodeError as e:
        logging.error(f"JSON decode error in {DATA_FILE}: {e}. Returning empty data")
        return {}
    except IOError as e:
        logging.error(f"I/O error while reading {DATA_FILE}: {e}. Returnin empty data")
        return {}

def save_all_users(data):
    try:
        with open(DATA_FILE, "w", encoding='utf-8') as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        logging.error(f"Could not write to file {DATA_FILE}: {e}.")

def ensure_user_exists(username):
    data = load_all_users()
    if username not in data:
        data[username] = {
            "xp": 0,
            "badges": [],
            "streak": 0,
            "last_login": datetime.today().strftime("%Y-%m-%d"),
            "quests_completed": []
        }
        save_all_users(data)
    return data

def add_xp(username, amount):
    data = load_all_users()
    if username in data:
        data[username]["xp"] += amount
        save_all_users(data)
    else:
        print(f"Warning: User '{username}' not found when adding XP.")

def add_badge(username,badge_name):
    data = load_all_users()
    if username in data:
        if badge_name not in data[username]["badges"]:
            data[username]["badges"].append(badge_name)
            save_all_users(data)
    else:
        print(f"Warning: User '{username}' not found while adding badge.")

def update_streak(username):
    data = load_all_users()
    if username not in data:
        print(f"Warning: User '{username}' not found when updating streak.")
        return
    
    today = datetime.today().date()
    last_login = datetime.strptime(data[username]["last_login"], "%Y-%m-%d").date()

    if today == last_login:
        return
    elif today == last_login + timedelta(days=1):
        data[username]["streak"] += 1
    else:
        data[username]["streak"] = 1
    
    data[username]["last_login"] = today.strftime("%Y-%m-%d")
    save_all_users(data)