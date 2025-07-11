import streamlit as st
from openai import OpenAI
from streamlit_openai import Chat
from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage

# Securely load Lambda credentials from secrets
LAMBDA_KEY = st.secrets["LAMBDA"]["API_KEY"]
BASE_URL = st.secrets["LAMBDA"]["BASE_URL"]

# Cache the OpenAI-compatible client to avoid reinitialization
@st.cache_resource
def get_client():
    return OpenAI(api_key=LAMBDA_KEY, base_url=BASE_URL)

client = get_client()

st.title("📝 English Tutor (Phase 1)")

# Initialize chat UI using streamlit_openai for ease
if "chat" not in st.session_state:
    st.session_state.chat = Chat(
        client=client,
        model="llama-3.1-8b-instruct",
        placeholder="Ask your English question…",
        show_clear_button=True
    )

# Display chat interface
st.session_state.chat.run()

# Track and display token usage for each session
if hasattr(st.session_state.chat, "history"):
    last = st.session_state.chat.history[-1]
    if hasattr(last, "usage_tokens"):
        ut = last.usage_tokens
        st.sidebar.markdown(f"**Last session tokens:** {ut['prompt_tokens']} in, {ut['completion_tokens']} out, **{ut['total_tokens']} total**")
