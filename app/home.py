#app/home.py 
import streamlit as st
from .style import load_styles
from .ui.components import app_banner, styled_card
from .modes import normal_mode, telugu_mode, quest_mode

def show():
    load_styles()

    st.markdown("""
        <style>
        .hover-card {
            transition: all 0.25s ease;
        }
        .hover-card:hover {
            transform: translateY(-6px) scale(1.02);
            box-shadow: 0 6px 18px rgba(0,0,0,0.15);
        }
        </style>
        """, unsafe_allow_html=True)

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
            st.markdown('<div class="hover-card">', unsafe_allow_html=True)
            styled_card(icon="📚", title="Study Mode", content="Classic Q&A format.")
            st.markdown('</div>', unsafe_allow_html=True)
            if st.button("Start Studying", key="study_mode_btn_1"):
                st.session_state.mode = "Study"
                st.rerun()

        with col2:
            st.markdown('<div class="hover-card">', unsafe_allow_html=True)
            styled_card(icon="😂", title="Telugu Mode", content="Learn in telugu.")
            st.markdown('</div>', unsafe_allow_html=True)
            if st.button("Start Laughing", key="meme_mode_btn_1"):
                st.session_state.mode = "Meme"
                st.rerun()

        with col3:
            st.markdown('<div class="hover-card">', unsafe_allow_html=True)
            styled_card(icon="🎯", title="Quest Mode", content="Gamified learning.")
            st.markdown('</div>', unsafe_allow_html=True)
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
