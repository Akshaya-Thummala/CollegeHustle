# app/quest/quest_home.py
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
            if isinstance(js, list):
                return js
            return js
    except Exception:
        return FALLBACK_QUESTS

def show():
    st.title("🗡️ Quest Mode")
    st.markdown("""
    <style>
    .quest-card {
        padding:14px;
        border-radius:14px;
        background-image: linear-gradient(135deg, #e3fdf5 0%, #f9fdfb 100%);
        border:1px solid rgba(0,0,0,0.06);
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
        transition: all 0.25s ease;
    }
    .quest-card:hover {
        box-shadow: 0 6px 16px rgba(0,0,0,0.18);
        transform: translateY(-3px);
    }
    </style>
    """, unsafe_allow_html=True)
        
    st.write("Welcome, hero — pick a quest and earn XP, badges & lore!")
    st.write("---")

    username = st.session_state.get("username")
    if not username:
        st.error("⚠️ No user logged in. Return to Home and log in.")
        return

    all_users = ensure_user_exists(username)
    user = all_users[username]

    quests = load_quests()
    normalized = []
    for q in quests:
        if isinstance(q, dict) and "id" in q:
            q_copy = dict(q)
            q_copy["id"] = str(q_copy["id"])

            # ✅ AUTO-SCALE REWARD HERE
            qs = q_copy.get("questions", [])
            count = len(qs)
            # real reward = (each question 5xp) + (quest bonus 10xp)
            q_copy["reward"] = count * 5 + 10

            normalized.append(q_copy)

    if not normalized:
        normalized = FALLBACK_QUESTS

    st.subheader("📘 Topic Quests")
    cols = st.columns(2)

    for i, quest in enumerate(normalized):
        col = cols[i % 2]
        with col:
            qid = quest["id"]
            title = quest.get("title", f"Quest {qid}")
            desc = quest.get("motivational_line", "")
            reward = quest.get("reward", None)

            # ✅ Show — XP if no reward
            reward_display = f"{reward} XP" if reward is not None else "— XP"

            quest_prog = user.get("quest_progress", {}).get(qid, 0)
            completed = qid in user.get("quests_completed", [])

            st.markdown(f"""
                <div class="quest-card">
                    <h4 style="margin:6px 0;">{quest.get('badge','')} {title}</h4>
                    <div style="font-size:13px;color:#333;margin-bottom:8px;">{desc}</div>
                    <div style="font-size:12px;color:#444;margin-bottom:6px;">
                        <b>Reward:</b> {reward_display}
                    </div>
                </div>
            """, unsafe_allow_html=True)

            if completed:
                st.markdown(f"""
                    <div style="margin-top:5px; padding:6px 10px; display:inline-block; 
                                background:#ffd700; color:#000; border-radius:6px;
                                font-size:12px; font-weight:600;">
                        ✅ Completed
                    </div>
                """, unsafe_allow_html=True)
                st.progress(1.0)
                st.button("Replay Quest", key=f"replay_{qid}", use_container_width=True, disabled=True)
            else:
                goal = quest.get("goal", 3)
                frac = min(1.0, quest_prog / goal) if goal > 0 else 0.0
                st.progress(frac)
                if st.button("Start Quest", key=f"start_{qid}", use_container_width=True):
                    st.session_state.current_quest = qid
                    st.session_state.page = "🗡️ Quest - Run"
                    st.session_state.quest_index = 0
                    st.session_state.quest_score = 0
                    st.rerun()

            st.write("")

    st.write("---")
    st.info("Tip: Complete quests to earn XP and badges. Good luck!")