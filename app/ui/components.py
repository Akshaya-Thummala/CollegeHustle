import streamlit as st
from ..style import MINT_GREEN, MINT_GREEN_DARK, WHITE, CHARCOAL_GRAY, CORAL_ACCENT, SUCCESS_GREEN

def app_banner():
    """Displays the main banner for the CollegeHustle app."""
    st.markdown(f"""
        <div style="
            background: linear-gradient(90deg, {MINT_GREEN}, {MINT_GREEN_DARK});
            padding: 2rem 1.5rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        ">
            <h1 style="color: {WHITE}; text-align: center; font-size: 2.5rem; margin: 0;">CollegeHustle 🚀</h1>
            <p style="color: {WHITE}; text-align: center; font-size: 1.1rem; margin-top: 0.5rem;">
                Your study wingman — less stress, more XP. 🎖️
            </p>
        </div>
    """, unsafe_allow_html=True)

def styled_card(content: str, title: str = None, icon: str = ""):
    """
    Creates a styled card using markdown and HTML.
    - content: The main text or markdown content for the card.
    - title: An optional h3 title for the card.
    - icon: An optional emoji icon to display with the title.
    """
    card_html = '<div class="styled-card">'
    if title:
        card_html += f'<h3>{icon} {title}</h3>'
    card_html += f'<p>{content}</p></div>'

    st.markdown(card_html, unsafe_allow_html=True)
    st.write("") # Adds a little vertical space after the card

def xp_style():
    """Custom CSS for the st.progress bar to make it look like an XP bar."""
    st.markdown(f"""
    <style>
        .stProgress > div > div > div > div {{
            background: linear-gradient(90deg, {CORAL_ACCENT}, {SUCCESS_GREEN});
        }}
    </style>
    """, unsafe_allow_html=True)
