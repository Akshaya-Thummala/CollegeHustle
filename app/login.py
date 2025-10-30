# app/login.py
import streamlit as st
from app.helpers.user_data_loader import ensure_user_exists, update_streak

EXPO_PASSWORD = "hustle123"

def login_page():
    # ✅ FULL PAGE MINT BACKGROUND
    st.markdown("""
    <style>
        html, body, .stApp {
            background: linear-gradient(180deg, #E8FFF3 0%, #C9F8DF 100%) !important;
        }

        /* Disable leftover hover styling */
        .hover-card {
            box-shadow: none !important;
            background: transparent !important;
            border: none !important;
        }

        /* Headings */
        .login-title {
            color: #217354;
            font-weight: 700;
            text-align: center;
            margin-bottom: 4px;
            font-size: 2rem;
        }
        .login-subtitle {
            color: #3d6d59;
            text-align: center;
            margin-bottom: 1.5rem;
            font-size: 1rem;
        }

        /* Input fields */
        .stTextInput input {
            background-color: #ffffff !important;
            border-radius: 8px !important;
        }

        /* Button */
        .stButton button {
            background-color: #A8E6CF !important;
            color: #00331c !important;
            font-weight: 600 !important;
            border-radius: 8px !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # ✅ Title & Tagline
    st.markdown('<h1 class="login-title">CollegeHustle 🚀</h1>', unsafe_allow_html=True)
    st.markdown('<p class="login-subtitle">Your study wingman — less stress, more XP</p>', unsafe_allow_html=True)

    # ✅ Just inputs, no box
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Continue"):
        if not username.strip():
            st.warning("Please enter a valid username.")
        elif password != EXPO_PASSWORD:
            st.error("Incorrect password.")
        else:
            ensure_user_exists(username)
            update_streak(username)
            st.session_state["username"] = username
            st.session_state["logged_in"] = True
            st.rerun()
