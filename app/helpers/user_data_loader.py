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

def add_badge(username, badge):
    """
    badge: dict with keys 'name', 'icon', 'desc', 'earned_on'
    """
    data = load_all_users()
    if username in data:
        existing_badge_names = [b['name'] if isinstance(b, dict) else str(b) for b in data[username]["badges"]]
        if badge['name'] not in existing_badge_names:
            data[username]["badges"].append(badge)
            save_all_users(data)
    else:
        print(f"Warning: User '{username}' not found while adding badge.")

def update_streak(username):
    data = load_all_users()
    if username not in data:
        print(f"Warning: User '{username}' not found when updating streak.")
        return

    today = datetime.today().date()
    
    # Ensure 'last_login' exists
    last_login_str = data[username].get("last_login", today.strftime("%Y-%m-%d"))
    last_login = datetime.strptime(last_login_str, "%Y-%m-%d").date()
    
    # Ensure 'streak' exists
    if "streak" not in data[username]:
        data[username]["streak"] = 0

    # --- Update streak logic ---
    if today == last_login:
        pass  # already logged in today
    elif today == last_login + timedelta(days=1):
        data[username]["streak"] += 1
    else:
        data[username]["streak"] = 1

    # Update last_login
    data[username]["last_login"] = today.strftime("%Y-%m-%d")
    save_all_users(data)

def load_user_data(username):
    data = load_all_users()
    if username not in data:
        data = ensure_user_exists(username)
    
    user = data.get(username, {})

    # Fix quests_completed if not a list
    if not isinstance(user.get("quests_completed", []), list):
        user["quests_completed"] = []

    # Fix badges if any are strings (convert to dict with default icon)
    fixed_badges = []
    for b in user.get("badges", []):
        if isinstance(b, str):
            fixed_badges.append({
                "name": b,
                "icon": "🏅",   # default icon
                "desc": "",
                "earned_on": ""
            })
        else:
            fixed_badges.append(b)
    user["badges"] = fixed_badges

    save_all_users(data)
    return user
