import streamlit as st
from app.helpers.user_data_loader import ensure_user_exists, update_streak

def login_page():
    st.title("🔐 Login to CollegeHustle")

    username = st.text_input("Enter username")

    if st.button("Login / Register"):
        if not username.strip():
            st.warning("Please enter a valid username.")
            return

        # --- Ensure user exists (auto-register if new) ---
        all_users = ensure_user_exists(username)
        user_data = all_users[username]

        # --- Update streak for returning users ---
        update_streak(username)

        # --- Store session data ---
        st.session_state["username"] = username
        st.session_state["logged_in"] = True

        # --- Optional greeting ---
        if user_data["xp"] == 0 and user_data["streak"] == 1:
            st.success(f"Welcome to CollegeHustle, {username}! 🎉 Your journey begins now.")
        else:
            st.success(f"Welcome back, {username}! 👋")

        # --- Safe rerun to transition to home page ---
        st.rerun()
