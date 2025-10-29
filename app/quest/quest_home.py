import json
import streamlit as st
from pathlib import Path
from ..helpers.user_data_loader import ensure_user_exists, load_all_users

DATA_QUESTS = Path("data") / "quests.json"

# minimal local fallback if file missing
FALLBACK_QUESTS = [
    {"id": "c_loops", "title": "Master Loops (C)", "motivational_line": "Solve 3 loop questions", "reward": 20},
    {"id": "py_datatypes", "title": "Python Data Types", "motivational_line": "Basics of Python types", "reward": 20},
]

def load_quests():
    try:
        with open(DATA_QUESTS, "r", encoding="utf-8") as f:
            js = json.load(f)
            # convert list-of-objects or keep as-is if already list
            if isinstance(js, list):
                return js
            # if file contains list of dicts as earlier, return directly
            return js
    except Exception:
        return FALLBACK_QUESTS

def show():
    st.title("🗡️ Quest Mode")
    st.write("Welcome, hero — pick a quest and earn XP, badges & lore!")
    st.write("---")

    # user guard
    username = st.session_state.get("username")
    if not username:
        st.error("⚠️ No user logged in. Return to Home and log in.")
        return

    # Make sure user exists and has structure
    all_users = ensure_user_exists(username)
    user = all_users[username]

    # load quests
    quests = load_quests()
    # quests.json in your repo uses numeric id keys — convert to unified format if needed
    # If quests loaded as a list-of-dicts (from your data/quests.json) keep it.
    # If it's a list, each item likely has 'id' numeric; we'll make sure id is string
    normalized = []
    for q in quests:
        # If q is a dict with numeric 'id', keep; else if whole file is dict keyed by numeric strings, adapt later
        if isinstance(q, dict) and "id" in q:
            # ensure id is string
            q_copy = dict(q)
            q_copy["id"] = str(q_copy["id"])
            normalized.append(q_copy)
        else:
            # fallback - skip malformed
            continue

    if not normalized:
        # fallback to our small hardcoded set
        normalized = FALLBACK_QUESTS

    st.subheader("📘 Topic Quests")
    cols = st.columns(2)

    for i, quest in enumerate(normalized):
        col = cols[i % 2]
        with col:
            qid = quest["id"]
            title = quest.get("title", f"Quest {qid}")
            desc = quest.get("motivational_line", "")
            reward = quest.get("reward", 0)

            # progress info from user data
            quest_prog = user.get("quest_progress", {}).get(qid, 0)
            # if quests_completed stores ids as strings, check membership
            completed = qid in user.get("quests_completed", [])

            # visual card
            st.markdown(f"""
                <div style="padding:12px;border-radius:10px;border:1px solid rgba(0,0,0,0.08);background:linear-gradient(90deg, rgba(255,255,255,0.6), rgba(255,255,255,0.9));">
                    <h4 style="margin:6px 0;">{quest.get('badge','')} {title}</h4>
                    <div style="font-size:13px;color:#333;margin-bottom:8px;">{desc}</div>
                    <div style="font-size:12px;color:#666;margin-bottom:6px;"><b>Reward:</b> {reward} XP</div>
                </div>
            """, unsafe_allow_html=True)

            # progress line and button
            if completed:
                st.markdown("**✅ Completed**")
                st.progress(1.0)
                st.button("Completed", key=f"completed_{qid}", disabled=True, use_container_width=True)
            else:
                # show a progress fraction if we have a goal (assume 3 questions default)
                goal = quest.get("goal", 3)
                frac = min(1.0, quest_prog / goal) if goal > 0 else 0.0
                st.progress(frac)
                if st.button("Start Quest", key=f"start_{qid}", use_container_width=True):
                    st.session_state.current_quest = qid
                    st.session_state.page = "🗡️ Quest - Run"
                    # initialize runner indices (ensures clean start)
                    st.session_state.quest_index = 0
                    st.session_state.quest_score = 0
                    st.rerun()

            st.write("")  # spacing

    st.write("---")
    st.info("Tip: Complete quests to earn XP and badges. Good luck!")
