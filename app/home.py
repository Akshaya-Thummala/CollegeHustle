import streamlit as st
from .modes import normal_mode as normal
from .modes import telugu_mode as telugu
from .modes import quest_mode as quest

def show():
    mode = st.radio("Choose a mode:", ['Normal mode','Telugu mode','Quest mode'])
    st.write(f"You chose: {mode}")

    if mode == "Normal mode":
        normal.run_normal_mode()

    if mode == "Telugu mode":
        telugu.run_telugu_mode()

    if mode == "Quest mode":
        quest.run_quest_mode()