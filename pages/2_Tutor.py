import streamlit as st
from openai import OpenAI

# Load API key securely from secrets.toml
client = OpenAI(api_key=st.secrets["OPENAI"]["API_KEY"])

if "logged_in_user" not in st.session_state:
    st.warning("Please log in from the main page.")
    st.stop()

st.title("🗣️ AI English Tutor")
username = st.session_state.get("logged_in_user", "")
name = st.session_state.get("logged_in_name", "")
st.write(f"Hello, **{name}** (username: `{username}`)! Ready to start?")

user_input = st.text_area("Ask your tutor anything:")

if st.button("Submit"):
    if user_input.strip():
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="gpt-4.1-nano",
                messages=[
                    {"role": "system", "content": "You are an English tutor. Answer clearly and helpfully."},
                    {"role": "user", "content": user_input}
                ]
            )
            answer = response.choices[0].message.content
        st.write(f"🤖 Tutor: {answer}")
    else:
        st.warning("Please enter a question or topic.")
