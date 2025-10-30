import streamlit as st
from .style import load_styles
from .ui.components import styled_card

def show():
    load_styles()

    st.title("📖 About CollegeHustle")
    st.write("Your study wingman — less stress, more XP.")

    styled_card(
        icon="🏁",
        title="Our Mission",
        content=(
            "CollegeHustle is built for students who learn better with *interaction, streaks, and instant feedback* — "
            "rather than boring static notes. We turn studying into a game, so you stay consistent without burnout."
        )
    )

    styled_card(
        icon="🗡️",
        title="Key Features",
        content=(
            "• Quest Mode for gamified learning\n"
            "• XP, streaks, badges & progress tracking\n"
            "• Topic-based micropractice\n"
            "• Future: leaderboard + study-buddy mode"
        )
    )

    styled_card(
        icon="👩‍💻",
        title="Built By",
        content=(
            "Akshaya, Sudhiksha & Sahasra (Second-year CSE)\n"
            "Project under SEEKH Expo 2025."
        )
    )

    styled_card(
        icon="🚀",
        title="Vision",
        content=(
            "Make self-study feel rewarding instead of stressful — "
            "keep students accountable the *Duolingo way*, but for academics."
        )
    )

    st.caption("Version 1.0 • SEEKH Expo • 2025")
