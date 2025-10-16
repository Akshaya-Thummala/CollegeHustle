import streamlit as st
from .style import load_styles
from .ui.components import styled_card

def show():
    """Renders the settings page."""
    load_styles()

    st.header("⚙️ Settings")
    st.write("---")

    styled_card(
        icon="🚧",
        title="Under Construction",
        content="This page is still being developed. Check back later for options to customize your experience!"
    )
