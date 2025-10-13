import streamlit as st
import app.home as home
import app.profile as profile
import app.settings as settings

st.set_page_config(page_title="CollegeHustle 🚀", layout="wide")

st.title("CollegeHustle 🚀")

# Initialize selected page in session state
if 'page' not in st.session_state:
    st.session_state.page = "Home"

def set_page(page):
    st.session_state.page = page

# Define pages and their labels
pages = {
    "🏠 Home": home.show,
    "👤 Profile": profile.show,
    "⚙️ Settings": settings.show
}

# Sidebar buttons for navigation (vertical & clickable)
st.sidebar.subheader("Navigation")
for page_name in pages:
    is_selected = page_name == st.session_state.page

    button_style = """
        <style>
        div[data-testid="stSidebar"] button.selected {
            background-color: #4CAF50 !important;
            color: white !important;
            border-radius: 8px;
            font-weight: bold;
        }
        </style>
    """
    st.markdown(button_style, unsafe_allow_html=True)

    # Add a unique key so Streamlit doesn’t reuse buttons
    if st.sidebar.button(page_name, use_container_width=True, key=page_name):
        st.session_state.page = page_name

    # Highlight the selected button using JS-style class targeting
    if is_selected:
        st.markdown(
            f"""<script>
            const btns = parent.document.querySelectorAll('button[kind="secondary"]');
            btns.forEach(btn => {{
                if (btn.innerText.trim() === "{page_name}") {{
                    btn.classList.add("selected");
                }}
            }});
            </script>""",
            unsafe_allow_html=True
        )


if st.session_state.page == "🏠 Home":
    home.show()
elif st.session_state.page == "👤 Profile":
    profile.show()
elif st.session_state.page == "⚙️ Settings":
    settings.show()
else:
    home.show()                             #default