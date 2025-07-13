import streamlit as st

if __name__ == "__page__":
    st.title("🗣️ AI English Tutor")

    username = st.session_state.get("logged_in_user", "")
    name = st.session_state.get("logged_in_name", "")

    st.write(f"Hello, **{name}** (username: `{username}`)! Ready to start your session?")

    user_input = st.text_area("Ask your tutor anything:")
    if st.button("Submit"):
        if user_input.strip():
            st.write(f"🤖 Tutor: Thanks for your question: '{user_input}'. Here’s a helpful answer!")
        else:
            st.warning("Please enter a question or topic.")
