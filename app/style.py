import streamlit as st

# =========================
# 🎨 Color Palette ("Fresh Mint Hustle" Theme)
# =========================
MINT_GREEN = "#A8E6CF"
MINT_GREEN_DARK = "#77D8B5"
CORAL_ACCENT = "#FF8A80"
CHARCOAL_GRAY = "#373737"
WHITE = "#FFFFFF"
BLACK = "#212121" # A softer black for UI elements
SUCCESS_GREEN = "#28A745" # For XP bar gradient
LIGHT_GRAY = "#E5E7EB" # For borders

# =========================
# 🪄 Global Styling Function
# =========================
def load_styles():
    """Injects custom CSS into Streamlit app for consistent styling."""
    st.markdown(f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

            /* Hide the default Streamlit header */
            header[data-testid="stHeader"] {{
                visibility: hidden;
                height: 0%;
            }}

            /* Main app background */
            .stApp {{
                background-color: {MINT_GREEN};
            }}

            /* Global Font */
            html, body, [class*="st-"] {{
                font-family: 'Poppins', sans-serif;
            }}

            /* Headings in main content */
            .main h1, .main h2, .main h3 {{
                color: {BLACK};
            }}

            /* Main Content Buttons */
            div.stButton > button:not([kind="secondary"]) {{
                background-color: {BLACK};
                color: {WHITE};
                border: 2px solid {BLACK};
                border-radius: 12px;
                padding: 10px 24px;
                font-weight: 600;
                transition: transform 0.2s ease, box-shadow 0.2s ease;
            }}
            div.stButton > button:not([kind="secondary"]):hover {{
                transform: translateY(-2px);
                box-shadow: 0 4px 10px rgba(0,0,0,0.2);
            }}

            /* Sidebar */
            section[data-testid="stSidebar"] {{
                background-color: {CHARCOAL_GRAY};
                border-right: 1px solid {BLACK};
            }}

            /* Text color inside the dark sidebar */
            div[data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
            div[data-testid="stSidebar"] [data-testid="stMetricLabel"],
            div[data-testid="stSidebar"] h1,
            div[data-testid="stSidebar"] h2,
            div[data-testid="stSidebar"] h3 {{
                color: {WHITE};
            }}

            /* Sidebar Navigation Buttons */
            div[data-testid="stSidebar"] div.stButton > button[kind="secondary"] {{
                background-color: transparent;
                color: {WHITE};
                border: 2px solid {MINT_GREEN};
                justify-content: center;
                border-radius: 8px;
                margin-bottom: 0.5rem;
                transition: all 0.2s ease;
            }}
            div[data-testid="stSidebar"] div.stButton > button[kind="secondary"]:hover {{
                background-color: {MINT_GREEN};
                color: {BLACK};
                border-color: {MINT_GREEN};
            }}
            div[data-testid="stSidebar"] div.stButton > button[kind="secondary"]:focus {{
                background-color: {MINT_GREEN_DARK};
                color: {BLACK};
                border-color: {MINT_GREEN_DARK};
                outline: none;
                box-shadow: none;
            }}

            /* Frosted Glass Card Style */
            .styled-card {{
                background-color: rgba(255, 255, 255, 0.7); /* Slightly less transparent */
                backdrop-filter: blur(12px);
                -webkit-backdrop-filter: blur(12px); /* For Safari */
                border-radius: 15px;
                padding: 25px;
                border: 1px solid rgba(255, 255, 255, 0.3);
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
                color: {BLACK};
                transition: background-color 0.3s ease, box-shadow 0.3s ease;
            }}
            .styled-card:hover {{
                background-color: rgba(255, 255, 255, 0.85);
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
            }}
            .styled-card * {{
                color: {BLACK};
            }}

            /* Custom Styled Progress (XP) Bar */
            .stProgress > div > div > div > div {{
                background: linear-gradient(90deg, {CORAL_ACCENT}, {SUCCESS_GREEN});
                border-radius: 10px;
            }}
        </style>
    """, unsafe_allow_html=True)

