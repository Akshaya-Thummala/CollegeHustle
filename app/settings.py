# app/settings.py
import streamlit as st
from .style import load_styles

def toggle_switch(label, key, default=False):
    return st.toggle(label, value=default, key=key)

def show():
    load_styles()

    st.title("⚙️ Settings")
    st.caption("Personalize your CollegeHustle experience ✨")
    st.write("---")

    # 🌿 Theme & UI
    with st.container():
        st.subheader("🎨 Theme & Appearance")
        st.write("Adjust how CollegeHustle looks and feels.")
        toggle_switch("Mint Hustle Theme", "theme_mint", True)
        toggle_switch("Dark Mode", "theme_dark")
        st.write("")

    st.write("---")

    # 🔔 Gamification
    with st.container():
        st.subheader("🔔 Gamification & Alerts")
        st.write("Control motivational nudges and visual effects.")
        toggle_switch("Sound Effects", "sound_fx", True)
        toggle_switch("Confetti Animations", "confetti", True)
        toggle_switch("Streak Reminder Alerts", "streak_alert", True)
        st.write("")

    st.write("---")

    # 📈 Progress Summary (fake but looks legit)
    with st.container():
        st.subheader("📈 Your Progress Summary")
        st.write("Quick glance at your learning stats.")
        st.progress(0.65)  # placeholder visual
        st.caption("🌱 You're growing steady — keep the streak alive!")
        st.write("")

    st.write("---")

    # 🛡️ Privacy & Reset
    with st.container():
        st.subheader("🛡️ Privacy & Data Control")
        st.write("Manage your data visibility and preferences.")
        toggle_switch("Show Achievements Publicly", "privacy_public", True)
        if st.button("Reset Progress", use_container_width=True):
            st.warning("Feature will be available after v1.3 update.")
        st.write("")

    st.write("---")
    st.caption("More customization options coming soon ⚡")
