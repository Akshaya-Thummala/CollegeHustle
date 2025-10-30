# app/modes/telugu_mode.py
import streamlit as st
import json
from app.helpers.data_loader import get_topic_content, find_best_match, load_all_data
from app.helpers.user_data_loader import update_streak, add_xp, check_and_award_milestone

def run_telugu_mode():
    st.markdown("<h4 style='color:#FFC107;'>🎭 Telugu - fun mode activated!</h4>", unsafe_allow_html=True)

    data = load_all_data()

    if isinstance(data,str) and data in ["File not found.","Error reading JSON file."]:
        st.error("Oops! Couldn't load data.")
        return
    else:
        subject = st.selectbox("Choose subject",list(data.keys()))
        topic = st.selectbox("Choose topic", list(data[subject].keys()))

        content_list = get_topic_content(subject, topic)

        if content_list and content_list[0]["q"] in ("File not found.","Error reading JSON file."):
            st.error("Oops! Something went wrong! Please try again.")
            return
        else:
            doubt = st.text_area("Confused? Ask your doubt here")

            if st.button("🔍 Get Answer"):
            
                username = st.session_state.get("username")
                if doubt.strip():
                    best = find_best_match(doubt,content_list)

                    if best:
                        st.markdown(f"**Q: {best['q']}**")
                        st.divider()
                        st.markdown(f"👉{best['a']['telugu']}")

                        add_xp(username, 2)
                        update_streak(username)
                        m = check_and_award_milestone(username)
                        if m:
                            st.success(f"🔥 Milestone unlocked: {m['badge_name']}! You're on fire!")
                            st.balloons()
                    else:
                        st.warning("Couldn't find a good match. Try rephrasing your doubt.")
                else:
                    st.info("ℹ️ No doubt entered. Showing all available Q&A in this topic:")
                    for qa in content_list:
                        st.markdown(f"**Q: {qa['q']}**")
                        st.markdown(f"👉{qa['a']['telugu']}")
                        st.divider()

                    add_xp(username, 1)
                    update_streak(username)
                    m = check_and_award_milestone(username)
                    if m:
                        st.success(f"🔥 Milestone unlocked: {m['badge_name']}! You're on fire!")
                        st.balloons()
