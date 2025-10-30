# app/quest/quest_runner.py
import streamlit as st
import json
import os
import time
from .quest_loader import load_quest
from app.helpers.user_data_loader import (
    update_streak,
    add_xp,
    ensure_user_exists,
    save_all_users,
    load_all_users,
)
from app.helpers.user_data_loader import check_and_award_milestone

# NOTE:
# - Correct answer: +5 XP (once per question)
# - Completing quest: +10 XP

def _ensure_session_keys(quest_id, total_questions):
    """Initialize session keys used by the runner."""
    base = f"quest_{quest_id}"
    if f"{base}_index" not in st.session_state:
        st.session_state[f"{base}_index"] = 0
    if f"{base}_correct_count" not in st.session_state:
        st.session_state[f"{base}_correct_count"] = 0
    if f"{base}_finished" not in st.session_state:
        st.session_state[f"{base}_finished"] = False
    # track answered questions to avoid duplicate XP on rerun
    if f"{base}_answered" not in st.session_state:
        st.session_state[f"{base}_answered"] = [False] * total_questions

def show():
    # Guard: user logged in
    username = st.session_state.get("username")
    if not username:
        st.error("⚠️ No user logged in. Please return to Home and log in first.")
        st.stop()

    # Guard: current quest set
    if "current_quest" not in st.session_state:
        st.warning("⚠️ No quest selected.")
        return

    quest_id = st.session_state.current_quest
    quest = load_quest(quest_id)
    if not quest:
        st.error("⚠️ Could not load the quest.")
        return

    # normalize quest id (use int or str consistently)
    # load questions
    questions = quest.get("questions", [])
    total_questions = len(questions)

    # initialize per-quest session keys
    _ensure_session_keys(quest_id, total_questions)
    base = f"quest_{quest_id}"
    index = st.session_state[f"{base}_index"]
    correct_count = st.session_state[f"{base}_correct_count"]
    finished = st.session_state[f"{base}_finished"]
    answered_flags = st.session_state[f"{base}_answered"]

    st.title(f"🗡️ Quest: {quest.get('title', 'Unknown Quest')}")
    max_xp = total_questions * 5 + 10
    st.caption(f"💰 Total XP on perfect clear: {max_xp} XP")
    # optional description field in quests; fall back gracefully
    desc = quest.get("motivational_line", "")
    if desc:
        st.write(f"⚔️ {desc}")

    # If quest finished -> summary + reward logic (ensure reward applied once)
    if finished:
        st.success(f"🎉 Quest Completed! You answered {correct_count} / {total_questions} correctly.")
        total_earned = correct_count * 5 + 10
        st.info(f"💰 Total XP Earned: {total_earned} XP  ( {correct_count * 5} from answers + 10 completion bonus )")
        if correct_count == total_questions:
            st.success("🌟 PERFECT RUN! Flawless Victory! (+10 bonus XP)")

        # Give completion XP only once: check user's quest_progress and quests_completed
        all_users = ensure_user_exists(username)
        user_data = all_users[username]
        user_quests_done = user_data.get("quests_completed", [])

        # If quest id not present, mark as completed & give completion XP (+10)
        quest_unique_id = str(quest.get("id", quest_id))
        if quest_unique_id not in user_quests_done:
            # Mark completed and give XP
            user_quests_done.append(quest_unique_id)
            user_data["quests_completed"] = user_quests_done

            # add quest completion XP (+10)
            add_xp(username, 10)

            # Persist and save
            save_all_users(all_users)

            st.info(f"🏆 Quest completion bonus: +10 XP awarded!")
            # give scaled quest reward as main XP
            
        else:
            st.info("🏆 Quest completion already rewarded earlier.")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔁 Replay Quest", use_container_width=True):
                st.session_state[f"{base}_index"] = 0
                st.session_state[f"{base}_correct_count"] = 0
                st.session_state[f"{base}_finished"] = False
                st.session_state[f"{base}_answered"] = [False] * total_questions
                st.rerun()
        with col2:
            if st.button("📜 Quest List", use_container_width=True):
                st.session_state.current_quest = None
                st.session_state.page = "🗡️ Quest"
                st.rerun()

        return

    # Show current question
    if index < 0 or index >= total_questions:
        st.error("⚠️ Question index out of range.")
        return

    qdata = questions[index]
    # Support both 'q' and 'question' keys (your JSON uses 'q')
    question_text = qdata.get("q") or qdata.get("question") or "<no question text>"
    options = qdata.get("options", [])
    correct_answer = qdata.get("answer")

    st.subheader(f"Question {index + 1} / {total_questions}")
    st.write(question_text)

    # radio key must be stable per question
    radio_key = f"radio_{quest_id}_{index}"
    user_answer = st.radio("Choose your answer:", options, key=radio_key)

    submit_key = f"submit_{quest_id}_{index}"
    if st.button("Submit Answer", key=submit_key):
        # prevent awarding XP multiple times for the same question if user re-submits because of rerun
        if not answered_flags[index]:
            # mark as answered
            answered_flags[index] = True
            st.session_state[f"{base}_answered"] = answered_flags  # persist

            # check correctness
            if user_answer == correct_answer:
                # correct -> +5 XP
                add_xp(username, 5)
                st.success("✅ Correct! +5 XP awarded.")
                st.session_state[f"{base}_correct_count"] += 1
            else:
                st.error(f"❌ Wrong! Correct answer: **{correct_answer}**")

            # count this as daily engagement
            try:
                update_streak(username)
                check_and_award_milestone(username)
            except Exception:
                # do not crash UI if streak update fails
                pass

            # Move to next question (or finish)
            if index + 1 < total_questions:
                st.session_state[f"{base}_index"] += 1
            else:
                st.session_state[f"{base}_finished"] = True

            # persist any user file changes (add_xp already saved inside that helper)
            # but ensure quest progress stored as well
            all_users = ensure_user_exists(username)
            user_data = all_users[username]
            if "quest_progress" not in user_data:
                user_data["quest_progress"] = {}
            user_data["quest_progress"][str(quest.get("id", quest_id))] = (
                user_data["quest_progress"].get(str(quest.get("id", quest_id)), 0) + 1
            )
            save_all_users(all_users)

        else:
            st.info("✅ You already submitted this question; move to next one.")

        # slight pause for UX then rerun
        time.sleep(0.6)
        st.rerun()

    # show a small progress indicator for the user
    st.write("")
    st.caption(f"Progress: {index+1}/{total_questions} questions answered. Correct so far: {correct_count}")
