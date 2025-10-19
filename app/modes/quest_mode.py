import streamlit as st
from ..style import load_styles
from ..ui.components import styled_card
from ..helpers.user_data_loader import (
    ensure_user_exists,
    save_all_users,
    add_xp,
    add_badge,
)

# --- Pre-defined Quests ---
AVAILABLE_QUESTS = [
    {
        "id": "solve_1_doubt",
        "title": "Knowledge Sharer",
        "description": "Solve your first doubt in any study mode.",
        "xp": 25,
        "badge_reward": {"name": "Helper", "icon": "🤝"},
    },
    {
        "id": "complete_5_quests",
        "title": "Quest Apprentice",
        "description": "Complete a total of 5 daily quests.",
        "xp": 100,
        "badge_reward": {"name": "Apprentice", "icon": "📜"},
    },
    {
        "id": "reach_100_xp",
        "title": "Century Club",
        "description": "Earn your first 100 XP.",
        "xp": 50,
        "badge_reward": {"name": "Century Club", "icon": "💯"},
    },
    {
        "id": "login_3_days",
        "title": "Consistent Hustler",
        "description": "Log in for 3 consecutive days to build a streak.",
        "xp": 75,
        "badge_reward": {"name": "Consistent", "icon": "🗓️"},
    },
]

def run_quest_mode():
    """Renders the gamified Quest Mode page."""
    load_styles()

    st.header("🎯 Your Daily Quests")
    st.write("Complete quests to earn XP, unlock badges, and climb the leaderboard!")
    st.write("---")

    username = st.session_state.get("username", "Guest")
    all_users = ensure_user_exists(username)
    user_data = all_users[username]

    # --- Fix badges format if stored as strings ---
    if isinstance(user_data.get("badges", []), list) and user_data["badges"] and isinstance(user_data["badges"][0], str):
        user_data["badges"] = [{"name": b, "icon": "🏅"} for b in user_data["badges"]]
        save_all_users(all_users)

    # --- Fix quests_completed if wrongly stored as non-list (e.g. 0) ---
    if not isinstance(user_data.get("quests_completed", []), list):
        user_data["quests_completed"] = []
        save_all_users(all_users)


    # Ensure completed_quests is always a list
    completed_quests = user_data.get("quests_completed", [])
    if not isinstance(completed_quests, list):
        completed_quests = []
        user_data["quests_completed"] = completed_quests

    # Columns for layout
    col1, col2 = st.columns(2)
    quest_columns = [col1, col2]

    for i, quest in enumerate(AVAILABLE_QUESTS):
        with quest_columns[i % 2]:
            is_completed = quest["id"] in completed_quests

            with st.container():
                styled_card(
                    icon="✅" if is_completed else "🎯",
                    title=quest["title"],
                    content=f"{quest['description']}<br><b>Reward: {quest['xp']} XP</b>"
                )

                # Use unique keys for buttons
                if is_completed:
                    st.button(
                        "Completed!",
                        key=f"completed_{quest['id']}_{i}",
                        disabled=True,
                        use_container_width=True
                    )
                else:
                    if st.button(
                        "Claim Reward",
                        key=f"claim_{quest['id']}_{i}",
                        use_container_width=True
                    ):
                        # 1. Add XP
                        add_xp(username, quest["xp"])

                        # 2. Mark quest as completed
                        completed_quests.append(quest["id"])
                        user_data["quests_completed"] = completed_quests

                        # 3. Award badge
                        if "badge_reward" in quest:
                            existing_badges = [b["name"] for b in user_data.get("badges", [])]
                            if quest["badge_reward"]["name"] not in existing_badges:
                                add_badge(username, quest["badge_reward"])
                                st.balloons()
                                st.toast(
                                    f"Badge Unlocked: {quest['badge_reward']['name']} {quest['badge_reward']['icon']}",
                                    icon="🏅"
                                )

                        # 4. Save user data
                        save_all_users(all_users)
                        st.toast(f"+{quest['xp']} XP!", icon="⭐")
                        st.rerun()  # Safe rerun after claiming reward

            st.write("")  # Vertical spacer
