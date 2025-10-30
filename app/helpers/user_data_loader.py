# app/helpers/user_data_loader.py
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
        logging.error(f"I/O error while reading {DATA_FILE}: {e}. Returning empty data")
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
            "streak": 1,
            "last_login": datetime.today().strftime("%Y-%m-%d"),
            "quests_completed": [],
            "quest_progress": {},
            "unlocked_features": [],
            "milestones_claimed": []
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
        if "unlocked_features" not in data[username]:
            data[username]["unlocked_features"] = []
        if "milestones_claimed" not in data[username]:
            data[username]["milestones_claimed"] = []

    save_all_users(data)
    return data

def add_xp(username, amount):
    if amount == 0:
        return
    data = load_all_users()
    if username in data:
        try:
            data[username]["xp"] = int(data[username].get("xp", 0)) + int(amount)
        except Exception:
            data[username]["xp"] = data[username].get("xp", 0) + amount
        save_all_users(data)
    else:
        logging.error(f"Warning: User '{username}' not found when adding XP.")

def add_badge(username, badge):
    """
    badge: dict with keys 'name', 'icon', 'desc', 'earned_on'
    """
    data = load_all_users()
    if username not in data:
        logging.error(f"Warning: User '{username}' not found while adding badge.")
        return

    user = data[username]
    existing_badge_names = [b['name'] if isinstance(b, dict) else str(b) for b in user.get("badges", [])]

    if badge['name'] not in existing_badge_names:
        # ensure structure
        b = {
            "name": badge.get("name"),
            "icon": badge.get("icon", "🏅"),
            "desc": badge.get("desc", ""),
            "earned_on": badge.get("earned_on", datetime.today().strftime("%Y-%m-%d"))
        }
        user["badges"].append(b)
        save_all_users(data)

def update_streak(username):
    """
    Call this when the user performs a meaningful action (ask doubt / answer question).
    This will:
      - update streak and last_login
      - then check milestones and award (milestones are only surfaced to user when they open the app)
    """
    data = load_all_users()
    if username not in data:
        logging.error(f"Warning: user '{username}' not found when updating streak.")
        return

    today = datetime.today().date()
    last_login_str = data[username].get("last_login", today.strftime("%Y-%m-%d"))
    try:
        last_login = datetime.strptime(last_login_str, "%Y-%m-%d").date()
    except Exception:
        last_login = today

    # Ensure fields exist
    if "streak" not in data[username]:
        data[username]["streak"] = 0
    if "unlocked_features" not in data[username]:
        data[username]["unlocked_features"] = []
    if "milestones_claimed" not in data[username]:
        data[username]["milestones_claimed"] = []

    # Update streak
    if today == last_login:
        # already counted today; nothing to change
        pass
    elif today == last_login + timedelta(days=1):
        data[username]["streak"] += 1
    else:
        data[username]["streak"] = 1

    data[username]["last_login"] = today.strftime("%Y-%m-%d")
    save_all_users(data)

def check_and_award_milestone(username):
    """
    Check if user's streak matches a milestone (10,20,30) and award:
      - milestone XP (30/40/50)
      - milestone badge
      - unlock feature entry
    This function is idempotent; it won't re-award if milestones_claimed contains the day.
    """
    data = load_all_users()
    if username not in data:
        return None

    user = data[username]
    streak = int(user.get("streak", 0))

    milestones = {
        10: {"badge_name": "Daily Learner", "badge_icon": "📚", "xp": 30, "feature": "theme_mint"},
        20: {"badge_name": "Consistent Scholar", "badge_icon": "📖", "xp": 40, "feature": "theme_gold"},
        30: {"badge_name": "Disciplined Achiever", "badge_icon": "🧠", "xp": 50, "feature": "theme_diamond"},
    }

    if streak in milestones and streak not in user.get("milestones_claimed", []):
        m = milestones[streak]

        # award xp
        user["xp"] = int(user.get("xp", 0)) + int(m["xp"])

        # award badge
        badge = {
            "name": f"{m['badge_name']} ({streak}-Day)",
            "icon": m["badge_icon"],
            "desc": f"Reached {streak}-day streak",
            "earned_on": datetime.today().strftime("%Y-%m-%d")
        }
        # append badge if not already
        existing_badge_names = [b['name'] if isinstance(b, dict) else str(b) for b in user.get("badges", [])]
        if badge["name"] not in existing_badge_names:
            user.setdefault("badges", []).append(badge)

        # unlock feature
        feature = {"feature": m["feature"], "unlocked_on": datetime.today().strftime("%Y-%m-%d")}
        unlocked = [f["feature"] for f in user.get("unlocked_features", [])]
        if m["feature"] not in unlocked:
            user.setdefault("unlocked_features", []).append(feature)

        # mark milestone claimed
        user.setdefault("milestones_claimed", []).append(streak)

        save_all_users(data)
        return m  # return details for UI notification

    return None

def check_new_unlock(username):
    """
    Returns the most recent unlocked feature if it was unlocked today (so UI can show popup).
    Otherwise returns None.
    """
    data = load_all_users()
    user = data.get(username, {})
    if not user:
        return None

    unlocked = user.get("unlocked_features", [])
    if not unlocked:
        return None

    latest = unlocked[-1]
    try:
        unlocked_on = datetime.strptime(latest["unlocked_on"], "%Y-%m-%d").date()
    except Exception:
        return None

    if unlocked_on == datetime.today().date():
        return latest
    return None

def load_user_data(username):
    data = load_all_users()
    if username not in data:
        data = ensure_user_exists(username)

    user = data.get(username, {})

    # Normalize fields
    if not isinstance(user.get("quests_completed", []), list):
        user["quests_completed"] = []
    if not isinstance(user.get("quest_progress", {}), dict):
        user["quest_progress"] = {}
    if not isinstance(user.get("unlocked_features", []), list):
        user["unlocked_features"] = []
    if not isinstance(user.get("milestones_claimed", []), list):
        user["milestones_claimed"] = []

    # Fix badges that might be stored as strings
    fixed_badges = []
    for b in user.get("badges", []):
        if isinstance(b, str):
            fixed_badges.append({
                "name": b,
                "icon": "🏅",
                "desc": "",
                "earned_on": ""
            })
        else:
            fixed_badges.append(b)
    user["badges"] = fixed_badges

    save_all_users(data)
    return user
