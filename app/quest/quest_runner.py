import streamlit as st
import json
import os
import time
from .quest_loader import load_quest
from app.helpers.user_data_loader import update_streak, check_new_unlock

def show():

    # Ensure session state variables are initialized
    if "current_quest" not in st.session_state:
        st.session_state.current_quest = 1  # default quest id

    if "current_q_index" not in st.session_state:
        st.session_state.current_q_index = 0

    if "correct_count" not in st.session_state:
        st.session_state.correct_count = 0

    if "quest_finished" not in st.session_state:
        st.session_state.quest_finished = False

    # Load the selected quest
    quest = load_quest(st.session_state.current_quest)
    total_questions = len(quest["questions"])

    st.title(f"🗡️ Quest: {quest['title']}")

    # If quest is finished -> show summary
    if st.session_state.quest_finished:
        st.success(f"🎉 Quest Completed! You answered {st.session_state.correct_count} / {total_questions} correctly.")
        st.info(f"🏆 Reward Earned: {quest['reward']} XP")

        if st.button("🏠 Back to Quest Home", use_container_width=True):
            st.session_state.page = "🗡️ Quest Mode"
            st.session_state.current_q_index = 0
            st.session_state.correct_count = 0
            st.session_state.quest_finished = False

        return

    # Get current question
    qdata = quest["questions"][st.session_state.current_q_index]
    st.subheader(f"Question {st.session_state.current_q_index + 1} / {total_questions}")
    st.write(qdata["q"])

    # Show options as radio buttons
    user_answer = st.radio(
        "Choose your answer:",
        qdata["options"],
        key=f"q_{st.session_state.current_quest}_{st.session_state.current_q_index}"
    )


    # Submit button for each question
    if st.button("Submit Answer"):
        if user_answer == qdata["answer"]:
            st.session_state.correct_count += 1
            st.success("✅ Correct!")
        else:
            st.error(f"❌ Wrong! The correct answer is: **{qdata['answer']}**")

        # ✅ count this as daily engagement
        update_streak(st.session_state.get("username"))
        unlock = check_new_unlock(st.session_state.get("username"))
        if unlock:
            st.success(f"🎉 New milestone unlocked! Feature `{unlock}` is now available!")

        # Move to next question or finish
        if st.session_state.current_q_index + 1 < total_questions:
            st.session_state.current_q_index += 1
        else:
            st.session_state.quest_finished = True

        time.sleep(0.6)
        st.rerun()
