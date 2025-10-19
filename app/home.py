import streamlit as st
from .style import load_styles
from .ui.components import app_banner, styled_card
from .modes import normal_mode, telugu_mode, quest_mode

def show():
    load_styles()
    username = st.session_state.get("username", "Hustler")

    # --- Show home UI only if no mode is selected ---
    if 'mode' not in st.session_state or st.session_state.mode is None:
        # Banner + welcome
        app_banner()
        st.header(f"Welcome back, {username}! 👋")
        st.subheader("Choose Your Hustle")

        # Mode selection cards
        col1, col2, col3 = st.columns(3)
        with col1:
            styled_card(icon="📚", title="Study Mode", content="Classic Q&A format.")
            if st.button("Start Studying", key="study_mode_btn_1"):
                st.session_state.mode = "Study"
                st.rerun()

        with col2:
            styled_card(icon="😂", title="Meme Mode", content="Learn with memes.")
            if st.button("Start Laughing", key="meme_mode_btn_1"):
                st.session_state.mode = "Meme"
                st.rerun()

        with col3:
            styled_card(icon="🎯", title="Quest Mode", content="Gamified learning.")
            if st.button("Start Questing", key="quest_mode_btn_1"):
                st.session_state.mode = "Quest"
                st.rerun()

    # --- Mode page ---
    else:
        # Back button
        if st.button("🔙 Back to Home", key="back_to_home_btn"):
            st.session_state.mode = None
            st.rerun()

        # Show selected mode
        if st.session_state.mode == "Study":
            normal_mode.run_normal_mode()
        elif st.session_state.mode == "Meme":
            telugu_mode.run_telugu_mode()
        elif st.session_state.mode == "Quest":
            quest_mode.run_quest_mode()
