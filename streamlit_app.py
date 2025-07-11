# streamlit_app.py
import os
import streamlit as st
from openai import OpenAI
from streamlit_openai import Chat

# Securely load API key from Streamlit secrets
API_KEY = st.secrets["OPENAI"]["API_KEY"]

@st.cache_resource
def get_client():
    return OpenAI(api_key=API_KEY)

client = get_client()

st.set_page_config(page_title="AI English Tutor (GPT‑4.1‑nano)")
st.title("📝 English Tutor – GPT‑4.1‑nano")

if "chat" not in st.session_state:
    st.session_state.chat = Chat(
        client=client,
        model="gpt-4.1-nano",
        placeholder="Ask your English question…",
        show_clear_button=True
    )

st.session_state.chat.run()

# Display token usage metrics
chat = st.session_state.chat
if hasattr(chat, "history") and chat.history:
    last = chat.history[-1]
    if hasattr(last, "usage_tokens"):
        ut = last.usage_tokens
        st.sidebar.markdown(
            f"**Last session tokens:** {ut['prompt_tokens']} in, "
            f"{ut['completion_tokens']} out, **{ut['total_tokens']} total**"
        )
        # Running total
        total = st.session_state.get("total_tokens", 0) + ut["total_tokens"]
        st.session_state["total_tokens"] = total
        cost = total * (0.10 + 0.40) / 1_000_000  # $0.10/M input + $0.40/M output :contentReference[oaicite:1]{index=1}
        st.sidebar.markdown(f"**Session total tokens:** {total}")
        st.sidebar.markdown(f"**Estimated cost:** ${cost:.4f}")
