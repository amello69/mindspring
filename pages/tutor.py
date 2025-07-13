import streamlit as st

if __name__ == "__page__":
    st.title("🗣️ AI English Tutor")
    st.write("Here you can practice English, ask grammar questions, or generate sample essays.")

    user_input = st.text_area("Ask your tutor anything:")
    if st.button("Submit"):
        if user_input.strip():
            st.write(f"🤖 Tutor: I see you asked: '{user_input}'. Here’s a helpful answer!")
        else:
            st.warning("Please enter a question or topic.")
