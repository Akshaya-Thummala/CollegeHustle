import streamlit as st
from .style import load_styles
from .ui.components import app_banner, styled_card
from .modes import normal_mode, telugu_mode, quest_mode

def show():
    """Renders the main home page or the selected learning mode."""
    # Load custom CSS styles
    load_styles()

    # If a mode is selected, run it and display a back button
    if 'mode' in st.session_state and st.session_state.mode:
        
        # Central column for the back button for better visibility
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔙 Back to Home"):
                st.session_state.mode = None
                st.rerun()

        if st.session_state.mode == "Study":
            normal_mode.run_normal_mode()
        elif st.session_state.mode == "Meme":
            telugu_mode.run_telugu_mode()
        elif st.session_state.mode == "Quest":
            quest_mode.run_quest_mode()
        
    # Otherwise, show the main home page with mode selection
    else:
        # Display the main app banner
        app_banner()

        username = st.session_state.get("username", "Hustler")
        st.header(f"Welcome back, {username}! 👋")
        st.subheader("Choose Your Hustle")

        # Create a 3-column layout for the mode selection cards
        col1, col2, col3 = st.columns(3)

        with col1:
            styled_card(
                icon="📚",
                title="Study Mode",
                content="The classic, no-fluff way to learn. Clean Q&A format for quick topic understanding and revision."
            )
            if st.button("Start Studying", key="study_mode", use_container_width=True):
                st.session_state.mode = "Study"
                st.rerun()

        with col2:
            styled_card(
                icon="😂",
                title="Meme Mode",
                content="Learn concepts through hilarious Telugu memes and witty slang. Who said studying has to be boring?"
            )
            if st.button("Start Laughing", key="meme_mode", use_container_width=True):
                st.session_state.mode = "Meme"
                st.rerun()

        with col3:
            styled_card(
                icon="🎯",
                title="Quest Mode",
                content="Turn your study session into a game! Complete quests, earn XP, and level up your knowledge."
            )
            if st.button("Start Questing", key="quest_mode", use_container_width=True):
                st.session_state.mode = "Quest"
                st.rerun()
