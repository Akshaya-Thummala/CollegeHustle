import streamlit as st
from app.modes.normal_mode import run_normal_mode
from app.modes.telugu_mode import run_telugu_mode
from app.modes.quest_mode import run_quest_mode
st.title("CollegeHustle 🚀")

mode = st.radio("Choose a mode:", ['Normal mode','Telugu mode','Quest mode'])
st.write(f"You chose: {mode}")

if mode == "Normal mode":
    run_normal_mode()

if mode == "Telugu mode":
    run_telugu_mode()

if mode == "Quest mode":
    run_quest_mode()

subjects = { "Programming for Problem Solving": ["Algorithms and Flow Charts","Data Types","Variables and Constants",
                                                 "Operators","Control Statements","Functions"],
             "Scientific Programming": ["Python Syntax","Object-oriented Programming","Functions","Exception Handling","Modules"]}

selected_subject = st.selectbox("Select a subject:", list(subjects.keys()))

selected_topic = st.selectbox("Select Topic:", subjects[selected_subject])

st.markdown(f"##### You Picked: **{selected_subject} → {selected_topic}**")