import streamlit as st
from app import home
from app import profile
from app import settings
from app.helpers.user_data_loader import load_all_users
from app.style import MINT_GREEN_DARK

# --- Page Configuration ---
st.set_page_config(
    page_title="CollegeHustle 🚀",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Sidebar ---
with st.sidebar:
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

    st.image("https://placehold.co/100x100/A8E6CF/373737?text=🧑‍🎓", use_column_width=False)
    st.subheader(f"@{username}")

    stat_col1, stat_col2 = st.columns(2)
    with stat_col1:
        st.metric(label="⭐ XP", value=user_data.get("xp", 0))
    with stat_col2:
        st.metric(label="🔥 Streak", value=user_data.get("streak", 0))
    
    st.write("---")

    # 3. Navigation
    st.header("Navigation")
    
    # Initialize session state for page navigation
    if 'page' not in st.session_state:
        st.session_state.page = "🏠 Home"

    if st.button("🏠 Home", use_container_width=True):
        st.session_state.page = "🏠 Home"
    
    if st.button("👤 Profile", use_container_width=True):
        st.session_state.page = "👤 Profile"

    if st.button("⚙️ Settings", use_container_width=True):
        st.session_state.page = "⚙️ Settings"
        
    st.write("---")
    
    # 4. About/Footer section
    st.markdown("""
    <div style="text-align: center; color: #888;">
        <small>CollegeHustle | Your Study Wingman</small><br>
        <small>Made for the Expo with ❤️</small>
    </div>
    """, unsafe_allow_html=True)


# --- Page Rendering ---
# A dictionary mapping page names to their render functions
pages = {
    "🏠 Home": home.show,
    "👤 Profile": profile.show,
    "⚙️ Settings": settings.show
}

# Get the function for the selected page and run it
page_function = pages.get(st.session_state.page)
if page_function:
    page_function()
else:
    # Default to home page if something goes wrong
    home.show()

