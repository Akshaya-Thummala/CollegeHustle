import streamlit as st
import app.home as home
import app.profile as profile
import app.settings as settings

st.set_page_config(page_title="CollegeHustle 🚀", layout="wide")

st.title("CollegeHustle 🚀")

tab = st.sidebar.radio("Navigation",["🏠 Home","👤 Profile","⚙️ Settigs"],label_visibility = "collapsed")

if tab == "🏠 Home":
    home.show()
elif tab == "👤 Profile":
    profile.show()
elif tab == "⚙️ Settigs":
    settings.show()
else:
    home.show()                             #default