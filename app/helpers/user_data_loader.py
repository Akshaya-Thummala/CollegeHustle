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

    # If user doesn't exist, create a new entry
    if username not in data:
        data[username] = {
            "xp": 0,
            "badges": [],
            "streak": 0,
            "last_login": datetime.today().strftime("%Y-%m-%d"),
            "quests_completed": [],
            "quest_progress": {}
        }
    else:
        # Ensure required fields exist for existing users too
        if "xp" not in data[username]:
            data[username]["xp"] = 0
        if "badges" not in data[username]:
            data[username]["badges"] = []
        if "streak" not in data[username]:
            data[username]["streak"] = 0
        if "last_login" not in data[username]:
            data[username]["last_login"] = datetime.today().strftime("%Y-%m-%d")
        if "quests_completed" not in data[username]:
            data[username]["quests_completed"] = []
        if "quest_progress" not in data[username]:
            data[username]["quest_progress"] = {}

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
        print(f"Warning: user '{username}' not found when updating streak.")
        return

    today = datetime.today().date()
    last_login_str = data[username].get("last_login", today.strftime("%Y-%m-%d"))
    last_login = datetime.strptime(last_login_str, "%Y-%m-%d").date()

    # Ensure required fields exist
    if "streak" not in data[username]:
        data[username]["streak"] = 0
    if "unlocked_features" not in data[username]:
        data[username]["unlocked_features"] = []

    # --- Update streak logic ---
    if today == last_login:
        pass  # already counted today
    elif today == last_login + timedelta(days=1):
        data[username]["streak"] += 1
    else:
        data[username]["streak"] = 1  # reset streak

    # Update last login
    data[username]["last_login"] = today.strftime("%Y-%m-%d")

    # --------------------------------
    # ✅ MILESTONE REWARDS (10 / 20 / 30)
    # --------------------------------
    streak = data[username]["streak"]
    milestones = {10: "theme_green", 20: "theme_gold", 30: "theme_diamond"}

    if streak in milestones:
        feature_name = milestones[streak]

        # Check if not already unlocked
        unlocked = [f["feature"] for f in data[username]["unlocked_features"]]
        if feature_name not in unlocked:
            data[username]["unlocked_features"].append({
                "feature": feature_name,
                "unlocked_on": today.strftime("%Y-%m-%d")
            })

            # small XP reward
            data[username]["xp"] += 10

    save_all_users(data)

def check_new_unlock(username):
    data = load_all_users()
    user = data.get(username, {})

    if "unlocked_features" not in user or not user["unlocked_features"]:
        return None

    # get the most recent unlocked feature
    latest = user["unlocked_features"][-1]  
    unlocked_on = datetime.strptime(latest["unlocked_on"], "%Y-%m-%d").date()
    today = datetime.today().date()

    # only return unlock if it happened today
    if unlocked_on == today:
        return latest["feature"]

    return None

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
