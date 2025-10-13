import streamlit as st
from .modes import normal_mode as normal
from .modes import telugu_mode as telugu
from .modes import quest_mode as quest
from .helpers.user_data_loader import load_all_users, save_all_users

def show():
    st.markdown("<h3 style='color:#4CAF50;'>Your study wingman — because textbooks don’t high-five you. ✋🎓</h3>", unsafe_allow_html=True)
    
    users_data = load_all_users()

    if 'mode' not in st.session_state:
        st.session_state.mode = None
    
    username = st.session_state.get("username","Guest")
    user_data = users_data.get(username, {
        "xp": 0,
        "badges": [],
        "streak": 0,
        "last_login": "2025-06-01",
        "quests_completed": []
    })

    if st.session_state.mode is None:
        st.markdown(f"#### Hello, {username}!")

        st.markdown(f"""
<div style='background-color:#F9F9F9; padding: 15px; border-radius: 10px;'>
    <p style='color:#212121;'>
    🌟 <b>XP:</b> {user_data.get("xp",0)} &nbsp;&nbsp; 
    🏅 <b>Badges:</b> {len(user_data.get("badges",0))} &nbsp;&nbsp;
    🔥 <b>Streak:</b> {user_data.get("streak",0)}
    </p>
</div>
""", unsafe_allow_html=True)
    
        st.markdown("<h4 style='color:#00BCD4;'>🎮 Choose your Mode</h3>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("📘 Study mode"):
                st.session_state.mode = "normal"
        
        with col2:
            if st.button("🎭 Telugu mode"):
                st.session_state.mode = "telugu"
        
        with col3:
            if st.button("🎯 Quest mode"):
                st.session_state.mode = "quest"
    
    else:
        if st.session_state.mode == "normal":
            normal.run_normal_mode()

        elif st.session_state.mode == "telugu":
            telugu.run_telugu_mode()

        elif st.session_state.mode == "quest":
            quest.run_quest_mode()
        
        if st.sidebar.button("🔙 Back to Home"):
            st.session_state.mode = None