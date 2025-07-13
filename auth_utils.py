import streamlit as st

# Dummy users; replace with real db integration
USERS = {"alice": "password123", "bob": "secret"}

def login():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    st.sidebar.header("🔐 Login")
    if not st.session_state.logged_in:
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Login"):
            if USERS.get(username) == password:
                st.session_state.logged_in = True
                st.session_state.user = username
                st.experimental_rerun()
            else:
                st.sidebar.error("Invalid credentials")
    else:
        st.sidebar.write(f"Hello, {st.session_state.user}!")
        if st.sidebar.button("Logout"):
            st.session_state.clear()
            st.experimental_rerun()
