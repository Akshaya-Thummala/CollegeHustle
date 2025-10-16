import streamlit as st
from .style import load_styles
from .ui.components import xp_style, styled_card
from .helpers.user_data_loader import load_all_users

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
    all_users = load_all_users()
    user_data = all_users.get(username, {
        "xp": 0, "badges": [], "streak": 0, "quests_completed": []
    })

    # --- User Stats Section ---
    xp = user_data.get("xp", 0)
    # Define levels based on XP. Every 500 XP is a new level.
    level = (xp // 500) + 1
    xp_for_next_level = (level) * 500
    progress = (xp % 500) / 500.0

    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("https://placehold.co/200x200/A8E6CF/373737?text=Avatar", caption=f"@{username}", use_column_width=True)

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

    # --- Badges Section ---
    st.subheader("🏅 Your Badge Collection")
    badges = user_data.get("badges", [])

    if not badges:
        styled_card(
            content="No badges yet! Complete some quests in Quest Mode to start earning them.",
            title="Your collection is empty",
            icon="텅 빈" # Using a Korean character for an empty box look
        )
    else:
        # Display badges in a responsive grid
        num_cols = 4
        badge_cols = st.columns(num_cols)
        for i, badge in enumerate(badges):
            with badge_cols[i % num_cols]:
                st.markdown(f"""
                <div style="
                    text-align: center;
                    padding: 10px;
                    background-color: #F0F8F7;
                    border-radius: 10px;
                    border: 1px solid #A8E6CF;
                ">
                    <p style="font-size: 2.5rem; margin: 0;">{badge['icon']}</p>
                    <p style="font-weight: 600; margin: 5px 0 0 0;">{badge['name']}</p>
                </div>
                """, unsafe_allow_html=True)
                st.write("") # Vertical spacing

    st.write("---")

    # --- Leaderboard Preview Section ---
    st.subheader("🏆 Leaderboard")
    leaderboard = get_leaderboard_data()

    for i, (user, data) in enumerate(leaderboard[:5]): # Show top 5
        rank = i + 1
        is_current_user = (user == username)
        
        st.markdown(f"""
        <div style="
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 15px;
            border-radius: 10px;
            background-color: {'#A8E6CF' if is_current_user else '#FFFFFF'};
            color: {'#373737' if is_current_user else 'inherit'};
            margin-bottom: 8px;
            border: 1px solid #E5E7EB;
        ">
            <span style="font-weight: 600; font-size: 1.1rem;">#{rank} &nbsp; @{user}</span>
            <span style="font-weight: 600; font-size: 1.1rem;">{data.get('xp', 0)} XP</span>
        </div>
        """, unsafe_allow_html=True)
