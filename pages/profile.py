# pages/profile.py
import streamlit as st

def run():
    st.title("👤 Your Profile")
    user = st.session_state.get("username", "")
    name = st.session_state.get("name", "")
    st.write(f"Welcome, **{name}** (username: `{user}`)!")
    # Add more profile-editing widgets here...
