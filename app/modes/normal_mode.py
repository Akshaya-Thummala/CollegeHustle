import streamlit as st
import json
from app.helpers.data_loader import get_topic_content, find_best_match, load_all_data

def run_normal_mode():
    st.write("📘 Study mode activated!")

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

            if st.button("Get Answer"):
            
                if doubt.strip():
                    best = find_best_match(doubt,content_list)

                    if best:
                        st.markdown(f"**Q: {best['q']}**")
                        st.divider()
                        st.markdown(f"👉{best['a']['normal']}")
                    else:
                        st.warning("Couldn't find a good match. Try rephrasing your doubt.")
                else:
                    st.info("No doubt entered. Showing all available Q&A in this topic:")
                    for qa in content_list:
                        st.markdown(f"**Q: {qa['q']}**")
                        st.markdown(f"👉{qa['a']['normal']}")
                        st.divider()