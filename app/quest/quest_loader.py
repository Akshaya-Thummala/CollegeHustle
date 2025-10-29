import streamlit as st
import json
import os

def load_all_quests():
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "quests.json"))
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

        # if file is a list, convert to dict {id: quest}
        if isinstance(data, list):
            data = {str(quest["id"]): quest for quest in data}

        return data

def load_quest(quest_id):
    quests = load_all_quests()
    if not quests:
        return None

    quest_id = str(quest_id)
    quest = quests.get(quest_id)

    # Fallback: if quest not found, show a warning instead of crashing
    if quest is None:
        st.error(f"❌ Quest '{quest_id}' not found in quests.json")
        st.stop()

    return quest
