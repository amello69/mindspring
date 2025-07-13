import streamlit as st

if "logged_in_user" not in st.session_state:
    st.warning("Please log in from the main page.")
    st.stop()

st.title("👤 Your Profile")
username = st.session_state.get("logged_in_user", "")
name = st.session_state.get("logged_in_name", "")
st.write(f"Welcome, **{name}** (username: `{username}`)!")
