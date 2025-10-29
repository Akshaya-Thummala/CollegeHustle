import streamlit as st
from ..style import load_styles
from ..quest.quest_home import show as quest_home
from ..quest.quest_runner import show as quest_runner

def run_quest_mode():
    load_styles()

    # If currently playing inside quest runner
    if st.session_state.get("page") == "🗡️ Quest - Run":
        quest_runner()
    else:
        quest_home()
