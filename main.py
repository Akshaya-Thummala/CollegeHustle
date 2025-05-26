import streamlit as st
import json
import os

def run_Normal_mode():
    st.write("Normal mode is running...")

def run_Telugu_mode():
    st.write("Telugu mode is running...")

def run_Quest_mode():
    st.write("Quest mode is running...")

def get_topic_content(subject,topic):
    with open("data/answers.json","r") as f:
        data = json.load(f)
    return(data.get(subject,{}).get(topic,[]))

def find_best_match(doubt,content_list):
    doubt.lower()
    best_match=None
    max_matches=0
    for item in content_list:
        matches = sum(1 for keywords in item["keywords"] if keywords in doubt)
        if matches > max_matches:
            max_matches = matches
            best_match = item
    return best_match

st.title("CollegeHustle 🚀")

mode = st.radio("Choose a mode:", ['Normal mode','Telugu mode','Quest mode'])
st.write(f"You chose: {mode}")

if mode == "Normal mode":
    run_Normal_mode()

if mode == "Telugu mode":
    run_Telugu_mode()

if mode == "Quest mode":
    run_Quest_mode()

subjects = { "Programming for Problem Solving": ["Algorithms and Flow Charts","Data Types","Variables and Constants",
                                                 "Operators","Control Statements","Functions"],
             "Scientific Programming": ["Python Syntax","Object-oriented Programming","Functions","Exception Handling","Modules"]}

selected_subject = st.selectbox("Select a subject:", list(subjects.keys()))

selected_topic = st.selectbox("Select Topic:", subjects[selected_subject])

st.markdown(f"##### You Picked: **{selected_subject} → {selected_topic}**")