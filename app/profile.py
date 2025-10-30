# app/profile.py
import streamlit as st
from .style import load_styles
from .ui.components import xp_style, styled_card
from .helpers.user_data_loader import load_all_users, load_user_data

# Dummy data for leaderboard display
def get_leaderboard_data():
    """Returns a sorted list of users for the leaderboard."""
    users_data = load_all_users()
    # Sort users by XP in descending order
    sorted_users = sorted(users_data.items(), key=lambda item: item[1].get('xp', 0), reverse=True)
    return sorted_users

def show():
    """Renders the user's profile page with stats and achievements."""
    # Load custom CSS for the page and XP bar
    load_styles()
    xp_style()

    st.header("👤 Your Profile & Progress")
    st.write("---")

    username = st.session_state.get("username", "Guest")
    # Use load_user_data to normalize fields and conversions
    user_data = load_user_data(username)

    # --- User Stats Section ---
    xp = int(user_data.get("xp", 0))
    # Define levels based on XP. Every 100 XP is a new level (faster leveling for expo/demo)
    LEVEL_XP = 100
    level = (xp // LEVEL_XP) + 1
    xp_for_next_level = (level) * LEVEL_XP
    progress = (xp % LEVEL_XP) / float(LEVEL_XP) if LEVEL_XP > 0 else 0.0

    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/924/924915.png", caption=f"@{username}", use_container_width=True)

    with col2:
        st.subheader(f"Level {level} Hustler")
        st.progress(progress)
        st.markdown(f"**{xp_for_next_level - xp} XP** to the next level!")

        st.write("") # Spacer

        stat_col1, stat_col2 = st.columns(2)
        with stat_col1:
            st.metric(label="🔥 Current Streak", value=f"{user_data.get('streak', 0)} Days")
        with stat_col2:
            st.metric(label="✅ Quests Completed", value=len(user_data.get('quests_completed', [])))

    st.write("---")

    # --- Milestones Section (placed under streak & stats) ---
    st.subheader("🔥 Milestones & Progress")
    streak = int(user_data.get("streak", 0))
    milestones_list = [
        {"days": 3, "name": "Consistency Starter", "icon": "🔥"},
        {"days": 7, "name": "Weekly Warrior", "icon": "⚡"},
        {"days": 10, "name": "Hustler Level Up", "icon": "🌟"},
        {"days": 30, "name": "Marathon Mindset", "icon": "👑"},
    ]

    # claimed milestones set (if present)
    claimed = set(user_data.get("milestones_claimed", []))

    ms_cols = st.columns(len(milestones_list))
    for i, m in enumerate(milestones_list):
        with ms_cols[i]:
            achieved = m["days"] <= streak or m["days"] in claimed
            bg = "#A8E6CF" if achieved else "#FFFFFF"
            color = "#373737" if achieved else "#666666"
            st.markdown(f"""
            <div style="
                text-align:center;
                padding:12px;
                border-radius:10px;
                background-color:{bg};
                border: 1px solid #E5E7EB;
            ">
                <div style="font-size:1.6rem;">{m['icon']}</div>
                <div style="font-weight:700; margin-top:6px; color:{color};">{m['name']}</div>
                <div style="font-size:0.9rem; color:{color}; margin-top:4px;">{m['days']}-day</div>
            </div>
            """, unsafe_allow_html=True)

    st.write("")  # spacing
    # Next milestone progress line
    next_m = None
    for m in milestones_list:
        if m["days"] > streak:
            next_m = m
            break
    if next_m:
        need = next_m["days"] - streak
        st.info(f"Next milestone: **{next_m['name']} ({next_m['days']} days)** — {need} more day(s) of activity to unlock.")
    else:
        st.success("You're on top of the milestones — amazing consistency! 🎉")

    st.write("---")

    # --- Badges Section ---
    st.subheader("🏅 Your Badge Collection")
    badges = user_data.get("badges", [])

    if not badges:
        styled_card(
            content="No badges yet! Complete quests or keep a streak to unlock achievements.",
            title="Your collection is empty",
            icon="🎒"
        )
    else:
        # Display badges in a responsive grid
        num_cols = 4
        badge_cols = st.columns(num_cols)
        for i, badge in enumerate(badges):
            # Normalize if badge is a string or dict
            if isinstance(badge, str):
                b_name = badge
                b_icon = "🏅"
            else:
                b_name = badge.get("name", "Badge")
                b_icon = badge.get("icon", "🏅")
            with badge_cols[i % num_cols]:
                st.markdown(f"""
                <div style="
                    text-align: center;
                    padding: 10px;
                    background-color: #F0F8F7;
                    border-radius: 10px;
                    border: 1px solid #A8E6CF;
                ">
                    <p style="font-size: 2.5rem; margin: 0;">{b_icon}</p>
                    <p style="font-weight: 600; margin: 5px 0 0 0;">{b_name}</p>
                </div>
                """, unsafe_allow_html=True)
                st.write("") # Vertical spacing

    st.write("---")

    # --- Unlocked Features Section ---
    st.subheader("🔓 Unlocked Features")
    unlocked = user_data.get("unlocked_features", [])
    if unlocked:
        for f in unlocked:
            # support both dict and plain string entries
            if isinstance(f, str):
                fname = f
                unlocked_on = ""
            else:
                fname = f.get("feature", "feature")
                unlocked_on = f.get("unlocked_on", "")
            st.markdown(f"- **{fname}** {f' (unlocked on {unlocked_on})' if unlocked_on else ''}")
    else:
        st.markdown("No unlocks yet — keep engaging to unlock themes and rewards!")

    st.write("---")

    # --- Leaderboard Preview Section ---
    st.subheader("🏆 Leaderboard")
    leaderboard = get_leaderboard_data()

    for i, (user, data) in enumerate(leaderboard[:5]): # Show top 5
        rank = i + 1
        is_current_user = (user == username)
        entry_bg = "#A8E6CF" if is_current_user else "#FFFFFF"
        entry_color = "#373737" if is_current_user else "inherit"
        st.markdown(f"""
        <div style="
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 15px;
            border-radius: 10px;
            background-color: {entry_bg};
            color: {entry_color};
            margin-bottom: 8px;
            border: 1px solid #E5E7EB;
        ">
            <span style="font-weight: 600; font-size: 1.1rem;">#{rank} &nbsp; @{user}</span>
            <span style="font-weight: 600; font-size: 1.1rem;">{data.get('xp', 0)} XP</span>
        </div>
        """, unsafe_allow_html=True)

    # --- Show current user rank even if not in top 5 ---
    usernames_only = [u for u, _ in leaderboard]
    if username in usernames_only:
        user_rank = usernames_only.index(username) + 1

        if user_rank > 5:  # not in top 5, show separately
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("**— You —**")

            user_xp = leaderboard[user_rank - 1][1].get('xp', 0)
            st.markdown(f"""
            <div style="
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 15px;
                border-radius: 10px;
                background-color: #A8E6CF;
                color: #373737;
                margin-bottom: 8px;
                border: 1px solid #E5E7EB;
            ">
                <span style="font-weight: 600; font-size: 1.1rem;">#{user_rank} &nbsp; @{username}</span>
                <span style="font-weight: 600; font-size: 1.1rem;">{user_xp} XP</span>
            </div>
            """, unsafe_allow_html=True)

    st.write("")  # final spacing
