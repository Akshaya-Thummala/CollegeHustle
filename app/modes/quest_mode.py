import streamlit as st
from app.helpers.user_data_loader import load_all_users, save_all_users, ensure_user_exists, add_xp, add_badge, update_streak

def run_quest_mode():
    st.markdown("<h4 style='color:#FFC107;'>🎯 Quest Mode: Learn. Earn. Win.</h4>", unsafe_allow_html=True)

    username = st.text_input("Enter you username", value="Akshaya")

    if username:
        ensure_user_exists(username)
        update_streak(username)

        users = load_all_users()
        user = users[username]

        st.markdown(f"""
<div style="background-color:#FFF8E1; padding:12px; border-radius:10px;">
<p>🔥 <b>Streak:</b> {user['streak']} &nbsp;&nbsp; ⭐ <b>XP:</b> {user['xp']} &nbsp;&nbsp; 🏅 <b>Badges:</b> {', '.join(user['badges']) or 'None'}</p>
</div>
""", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Solve a Doubt (XP +10)"):
            add_xp(username, 10)
            if user["xp"] >= 100 and "Century XP" not in user["badges"]:
                add_badge(username, "Century XP")
                st.balloons()
                st.success("🎉 Congrats! You earned the Century XP badge! 🏅")