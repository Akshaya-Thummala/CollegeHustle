import streamlit as st
from ..style import load_styles
from ..ui.components import styled_card
from ..helpers.user_data_loader import load_all_users, save_all_users, add_xp, add_badge

# --- Pre-defined Quests ---
# A list of dictionaries, where each dictionary represents a quest.
# This can be easily expanded or moved to a separate JSON file later.
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
    all_users = load_all_users()
    user_data = all_users.get(username, {})
    completed_quests = user_data.get("quests_completed", [])
    
    # Use columns for a cleaner, grid-like layout
    col1, col2 = st.columns(2)
    quest_columns = [col1, col2]

    for i, quest in enumerate(AVAILABLE_QUESTS):
        with quest_columns[i % 2]:
            is_completed = quest["id"] in completed_quests
            
            # Create a container for the card and button
            with st.container():
                styled_card(
                    icon="✅" if is_completed else "🎯",
                    title=quest["title"],
                    content=f"{quest['description']}<br><b>Reward: {quest['xp']} XP</b>"
                )

                if is_completed:
                    st.button("Completed!", key=f"completed_{quest['id']}", disabled=True, use_container_width=True)
                else:
                    if st.button(f"Claim Reward", key=quest['id'], use_container_width=True):
                        # --- Logic to handle quest completion ---
                        # 1. Add XP
                        add_xp(username, quest['xp'])
                        
                        # 2. Mark quest as completed
                        user_data["quests_completed"].append(quest["id"])
                        
                        # 3. Award badge if there is one
                        if "badge_reward" in quest:
                            # Check if user already has the badge
                            badge_names = [b['name'] for b in user_data.get("badges", [])]
                            if quest["badge_reward"]["name"] not in badge_names:
                                add_badge(username, quest["badge_reward"])
                                st.balloons()
                                st.toast(f"Badge Unlocked: {quest['badge_reward']['name']} {quest['badge_reward']['icon']}", icon="🏅")

                        # 4. Save data and show feedback
                        save_all_users(all_users)
                        st.toast(f"+{quest['xp']} XP!", icon="⭐")
                        st.rerun()

            st.write("") # Vertical spacer between cards in the same column
