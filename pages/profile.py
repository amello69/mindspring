import streamlit as st

def run():
    st.title("👤 Your Profile")
    st.write(f"Username: **{st.session_state.user}**")
    # Add editable profile fields

if __name__ == "__page__":
    run()
