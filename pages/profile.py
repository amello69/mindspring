import streamlit as st

def run():
    st.title("👤 Your Profile")
    username = st.session_state.get("username", "")
    name = st.session_state.get("name", "")
    st.write(f"Welcome, **{name}** (username: `{username}`)!")

if __name__ == "__page__":
    run()
