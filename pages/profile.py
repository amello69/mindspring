import streamlit as st

def run():
    st.title("👤 Your Profile")
    username = st.session_state.get("logged_in_user", "")
    name = st.session_state.get("logged_in_name", "")
    st.write(f"Welcome, **{name}** (username: `{username}`)!")
