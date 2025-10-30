#main.py 
import streamlit as st
from app import home, profile, settings, about
from app.helpers.user_data_loader import load_all_users
from app.style import MINT_GREEN_DARK
from app.login import login_page

# --- Page Configuration ---
st.set_page_config(
    page_title="CollegeHustle 🚀",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    /* Sidebar container text (username, XP, streak, headings) */
    section[data-testid="stSidebar"] * {
        color: #ffffff !important;
    }

    /* Buttons - keep text dark + mint background */
    section[data-testid="stSidebar"] button {
        background-color: #A8E6CF !important;
        color: #000000 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        border: 1px solid rgba(0,0,0,0.1) !important;
    }

    /* Button text specifically (sometimes nested spans override style) */
    section[data-testid="stSidebar"] button * {
        color: #000000 !important;
    }

    /* Navigation header spacing adjustments */
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3 {
        color: #ffffff !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Initialize login state ---
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# --- Show Login or Home Page ---
if not st.session_state["logged_in"]:
    login_page()  # Only login page is rendered
else:
    # --- Sidebar ---
    with st.sidebar:

        st.markdown("""
            <style>
            /* Make all sidebar text brighter */
            [data-testid="stSidebar"] * {
                color: #f5fff5 !important;
            }

            /* But keep buttons readable on hover */
            [data-testid="baseButton-secondary"] {
                color: #002b18 !important;
                font-weight: 600 !important;
            }

            /* Sidebar section headers */
            [data-testid="stSidebar"] h1, 
            [data-testid="stSidebar"] h2, 
            [data-testid="stSidebar"] h3, 
            [data-testid="stSidebar"] h4 {
                color: #ffffff !important;
            }

            /* Metrics (XP / Streak) */
            [data-testid="stMetricValue"] {
                color: #ffffff !important;
            }
            [data-testid="stMetricLabel"] {
                color: #dfe8df !important;
            }
            </style>
            """, unsafe_allow_html=True)

        # 1. App Logo and Title
        st.markdown(
            f"""
            <div style="text-align: center;">
                <h1 style="color: {MINT_GREEN_DARK}; font-weight: 700;">CollegeHustle 🚀</h1>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.write("---")

        # 2. User Information
        username = st.session_state.get("username", "Guest")
        all_users = load_all_users()
        user_data = all_users.get(username, {"xp": 0, "streak": 0})

        st.image(f"https://cdn-icons-png.flaticon.com/512/924/924915.png", use_container_width=False)
        st.subheader(f"@{username}")

        stat_col1, stat_col2 = st.columns(2)
        with stat_col1:
            st.metric(label="⭐ XP", value=user_data.get("xp", 0))
        with stat_col2:
            st.metric(label="🔥 Streak", value=user_data.get("streak", 0))

        st.write("---")

        # 3. Navigation
        st.header("Navigation")
        if 'page' not in st.session_state:
            st.session_state.page = "🏠 Home"

        if st.button("🏠 Home", use_container_width=True):
            st.session_state.page = "🏠 Home"

        if st.button("👤 Profile", use_container_width=True):
            st.session_state.page = "👤 Profile"
        
        if st.button("📖 About", use_container_width=True):
            st.session_state.page = "📖 About"

        if st.button("⚙️ Settings", use_container_width=True):
            st.session_state.page = "⚙️ Settings"

        st.write("---")

        # 4. About/Footer section
        st.markdown("""
        <div style="text-align: center; color: #888;">
            <small>CollegeHustle | Your Study Wingman</small><br>
            <small>Made with ❤️</small>
        </div>
        """, unsafe_allow_html=True)

    # --- Page Rendering ---
    pages = {
        "🏠 Home": home.show,
        "👤 Profile": profile.show,
        "⚙️ Settings": settings.show,
        "📖 About": about.show,
    }

    page_function = pages.get(st.session_state.page, home.show)
    page_function()
