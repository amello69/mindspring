import streamlit as st
from openai import OpenAI

# Load OpenAI key from secrets
client = OpenAI(api_key=st.secrets["OPENAI"]["API_KEY"])

# --- Auth check ---
if "logged_in_user" not in st.session_state:
    st.warning("Please log in from the main page.")
    st.stop()

# --- Init states ---
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
if "input_key_counter" not in st.session_state:
    st.session_state["input_key_counter"] = 0

st.title("🗣️ AI English Tutor")

username = st.session_state.get("logged_in_user", "")
name = st.session_state.get("logged_in_name", "")
tokens_remaining = st.session_state.get("tokens_remaining", 0)

st.sidebar.markdown(f"**Tokens remaining:** {tokens_remaining}")

if tokens_remaining <= 0:
    st.error("You have exhausted your monthly tokens. Please purchase more.")
    st.stop()

# --- Clear chat button ---
if st.button("🗑️ Clear Chat"):
    st.session_state["chat_history"] = []
    st.success
