import streamlit as st

def run():
    st.title("🗣️ AI English Tutor")
    username = st.session_state.get("logged_in_user", "")
    name = st.session_state.get("logged_in_name", "")
    st.write(f"Hello, **{name}** (username: `{username}`)! Ready to start?")
    
    user_input = st.text_area("Ask your tutor anything:")
    if st.button("Submit"):
        if user_input.strip():
            st.write(f"🤖 Tutor: Here's a helpful answer to '{user_input}'")
        else:
            st.warning("Please enter a question or topic.")
